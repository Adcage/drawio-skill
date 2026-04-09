from __future__ import annotations

import argparse
import tempfile
import json
import platform
import stat
import subprocess
import urllib.request
from pathlib import Path

import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from scripts.lib.config_store import load_config, save_config
from scripts.lib.path_resolver import user_bin_dir, user_data_dir
from scripts.lib.providers.local_cli_provider import LocalCliProvider


RELEASE_API = "https://api.github.com/repos/jgraph/drawio-desktop/releases/latest"
RELEASES_API = "https://api.github.com/repos/jgraph/drawio-desktop/releases?per_page=30"


def _download_json(url: str):
    with urllib.request.urlopen(url) as response:  # noqa: S310
        return json.loads(response.read().decode("utf-8"))


def _pick_assets(assets: list[dict]) -> list[dict]:
    system = platform.system().lower()
    machine = platform.machine().lower()
    names = [(item.get("name", "").lower(), item) for item in assets]
    ordered: list[dict] = []

    def add_matches(predicate):
        for name, item in names:
            if predicate(name) and item not in ordered:
                ordered.append(item)

    if system == "windows":
        is_arm = "arm" in machine
        if is_arm:
            add_matches(
                lambda n: n.endswith(".exe") and "arm64" in n and "no-installer" in n
            )
            add_matches(
                lambda n: n.endswith(".exe") and "arm64" in n and "portable" in n
            )
        else:
            add_matches(
                lambda n: n.endswith(".exe") and "x64" in n and "no-installer" in n
            )
            add_matches(
                lambda n: n.endswith(".exe")
                and "windows" in n
                and "no-installer" in n
                and "arm64" not in n
            )
            add_matches(
                lambda n: n.endswith(".exe")
                and "no-installer" in n
                and "arm64" not in n
            )
        if is_arm:
            add_matches(lambda n: n.endswith(".exe") and "no-installer" in n)
        add_matches(lambda n: n.endswith(".zip") and "windows" in n and "portable" in n)
    elif system == "linux":
        add_matches(lambda n: "appimage" in n)
        add_matches(lambda n: "linux" in n)
    else:
        if "arm" in machine:
            preferred = ["arm64", "darwin", "mac"]
        else:
            preferred = ["universal", "darwin", "mac"]

        for token in preferred:
            add_matches(
                lambda n, t=token: t in n and (n.endswith(".dmg") or n.endswith(".zip"))
            )

    return ordered


def _validate_cli(path: Path) -> bool:
    sample = """<mxfile host=\"app.diagrams.net\"><diagram id=\"d1\" name=\"Page-1\"><mxGraphModel pageWidth=\"300\" pageHeight=\"200\"><root><mxCell id=\"0\"/><mxCell id=\"1\" parent=\"0\"/><mxCell id=\"n1\" value=\"A\" parent=\"1\" vertex=\"1\"><mxGeometry x=\"10\" y=\"10\" width=\"80\" height=\"40\" as=\"geometry\"/></mxCell></root></mxGraphModel></diagram></mxfile>"""

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        input_file = temp_path / "probe.drawio"
        output_file = temp_path / "probe.svg"
        input_file.write_text(sample, encoding="utf-8")

        try:
            result = subprocess.run(
                [str(path), "-x", "-f", "svg", "-o", str(output_file), str(input_file)],
                capture_output=True,
                text=True,
                check=False,
                timeout=45,
            )
        except (OSError, subprocess.TimeoutExpired):
            return False

        return result.returncode == 0 and output_file.exists()


def _download_asset(asset: dict, target_dir: Path) -> Path:
    target_dir.mkdir(parents=True, exist_ok=True)
    file_name = asset["name"]
    url = asset["browser_download_url"]
    target = target_dir / file_name
    urllib.request.urlretrieve(url, target)  # noqa: S310

    if platform.system().lower() != "windows":
        mode = target.stat().st_mode
        target.chmod(mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    return target


def _bootstrap_drawio_cli(dry_run: bool = False):
    release = _download_json(RELEASE_API)
    assets = release.get("assets", [])
    ordered_assets = _pick_assets(assets)

    if not ordered_assets:
        releases = _download_json(RELEASES_API)
        historical_assets = []
        for item in releases:
            historical_assets.extend(item.get("assets", []))
        ordered_assets = _pick_assets(historical_assets)

    if not ordered_assets:
        raise RuntimeError("No suitable release asset found for current platform")

    if dry_run:
        asset = ordered_assets[0]
        return {
            "asset_name": asset["name"],
            "asset_url": asset["browser_download_url"],
        }

    install_dir = user_bin_dir() / "drawio"
    errors = []
    cli_path = None
    for asset in ordered_assets:
        candidate = _download_asset(asset, install_dir)
        if _validate_cli(candidate):
            cli_path = candidate
            break
        errors.append(f"{asset['name']}: validation failed")

    if cli_path is None:
        raise RuntimeError(
            "Unable to find a runnable draw.io binary. " + "; ".join(errors)
        )

    config = load_config()
    config["drawio_cli_path"] = str(cli_path)
    save_config(config)

    return cli_path


def main():
    parser = argparse.ArgumentParser(
        description="No-admin bootstrap for local drawio export"
    )
    parser.add_argument(
        "--non-admin", action="store_true", help="Must be set for this tool"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only resolve download asset without downloading",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force re-download even if local provider is currently available",
    )
    args = parser.parse_args()

    if not args.non_admin:
        payload = {
            "ok": False,
            "error": "This bootstrap only supports non-admin mode",
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 1

    try:
        local_provider = LocalCliProvider()
        source = "existing"
        cli_path = local_provider.executable
        download_plan = None

        if (not local_provider.available) or args.force:
            if args.dry_run:
                download_plan = _bootstrap_drawio_cli(dry_run=True)
                source = "planned"
            else:
                cli_path = _bootstrap_drawio_cli(dry_run=False)
                source = "downloaded"
    except Exception as exc:  # noqa: BLE001
        payload = {
            "ok": False,
            "mode": "non-admin",
            "error": str(exc),
            "policy": {
                "allow_remote": False,
                "require_admin": False,
            },
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 1

    payload = {
        "ok": True,
        "mode": "non-admin",
        "runtime_source": source,
        "drawio_cli_path": str(cli_path) if cli_path else None,
        "download_plan": download_plan,
        "user_data": str(user_data_dir()),
        "user_bin": str(user_bin_dir()),
        "policy": {
            "allow_remote": False,
            "require_admin": False,
        },
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
