from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from pathlib import Path

from scripts.lib.config_store import load_config


def find_drawio_cli() -> str | None:
    env_path = os.environ.get("DRAWIO_CLI_PATH")
    if env_path and Path(env_path).exists():
        return env_path

    config = load_config()
    config_path = config.get("drawio_cli_path")
    if isinstance(config_path, str) and Path(config_path).exists():
        return config_path

    candidates = [
        "drawio",
        "draw.io",
        r"C:\Program Files\draw.io\draw.io.exe",
        r"C:\Program Files\draw.io\drawio.exe",
    ]

    for item in candidates:
        resolved = shutil.which(item)
        if resolved and Path(resolved).exists():
            return resolved
        if Path(item).exists():
            return item

    return None


class LocalCliProvider:
    name = "local-cli"
    is_remote = False

    def __init__(self):
        self.executable = find_drawio_cli()
        self.available = self.executable is not None and _probe_cli_export(
            self.executable
        )

    def export(self, request):
        if not self.available:
            raise RuntimeError("draw.io CLI is not available")

        input_path = Path(request.input_path).resolve()
        output_dir = Path(request.output_dir).resolve()
        output_dir.mkdir(parents=True, exist_ok=True)
        base_name = input_path.stem

        outputs = []
        for fmt in request.formats:
            output_path = output_dir / f"{base_name}.{fmt}"
            command = [
                self.executable,
                "-x",
                "-f",
                fmt,
                "-o",
                str(output_path),
            ]
            if request.page is not None:
                command.extend(["-p", str(request.page)])
            if fmt == "png" and request.png_scale:
                command.extend(["--scale", str(request.png_scale)])
            command.append(str(input_path))

            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode != 0:
                raise RuntimeError(
                    result.stderr.strip()
                    or result.stdout.strip()
                    or "draw.io export failed"
                )

            if not output_path.exists() or output_path.stat().st_size == 0:
                raise RuntimeError("draw.io export produced no output file")

            outputs.append(str(output_path))

        return outputs


def _probe_cli_export(executable: str) -> bool:
    sample = """<mxfile host=\"app.diagrams.net\"><diagram id=\"d1\" name=\"Page-1\"><mxGraphModel pageWidth=\"200\" pageHeight=\"120\"><root><mxCell id=\"0\"/><mxCell id=\"1\" parent=\"0\"/><mxCell id=\"n1\" value=\"A\" parent=\"1\" vertex=\"1\"><mxGeometry x=\"10\" y=\"10\" width=\"80\" height=\"40\" as=\"geometry\"/></mxCell></root></mxGraphModel></diagram></mxfile>"""

    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            input_file = temp_path / "probe.drawio"
            output_file = temp_path / "probe.svg"
            input_file.write_text(sample, encoding="utf-8")

            result = subprocess.run(
                [
                    executable,
                    "-x",
                    "-f",
                    "svg",
                    "-o",
                    str(output_file),
                    str(input_file),
                ],
                capture_output=True,
                text=True,
                check=False,
                timeout=45,
            )
            return (
                result.returncode == 0
                and output_file.exists()
                and output_file.stat().st_size > 0
            )
    except (OSError, subprocess.TimeoutExpired):
        return False
