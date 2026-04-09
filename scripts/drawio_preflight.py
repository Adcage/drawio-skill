from __future__ import annotations

import json
import os
import platform
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from scripts.lib.path_resolver import user_data_dir
from scripts.lib.providers import LocalCliProvider, UserNodeProvider


def main() -> int:
    providers = [LocalCliProvider(), UserNodeProvider()]
    provider_report = {
        provider.name: {
            "available": provider.available,
            "is_remote": provider.is_remote,
        }
        for provider in providers
    }

    output_dir = Path("outputs")
    writable = True
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        probe = output_dir / ".write-test"
        probe.write_text("ok", encoding="utf-8")
        probe.unlink()
    except OSError:
        writable = False

    user_dir = user_data_dir()
    python_ok = sys.version_info >= (3, 10)
    has_local_provider = provider_report["local-cli"]["available"]
    has_user_node_provider = provider_report["user-node"]["available"]

    next_actions = []
    if not has_local_provider and not has_user_node_provider:
        next_actions.append(
            "run bootstrap to download local draw.io CLI into user directory"
        )
    if not writable:
        next_actions.append("ensure outputs directory is writable")
    if not python_ok:
        next_actions.append("install Python 3.10+")

    payload = {
        "ok": (has_local_provider or has_user_node_provider) and writable and python_ok,
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
        },
        "python": {
            "version": platform.python_version(),
            "ok": python_ok,
        },
        "paths": {
            "cwd": str(Path.cwd()),
            "user_data": str(user_dir),
        },
        "providers": provider_report,
        "policy": {
            "allow_remote": False,
            "require_admin": False,
        },
        "next_actions": next_actions,
    }

    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
