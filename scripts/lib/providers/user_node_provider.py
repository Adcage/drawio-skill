from __future__ import annotations

import shutil
import subprocess
import os
from pathlib import Path


class UserNodeProvider:
    name = "user-node"
    is_remote = False

    def __init__(self, npm_prefix: str | None = None):
        explicit = os.environ.get("DRAWIO_USER_NODE_CMD")
        if explicit:
            self.npx = explicit
            self.available = True
        else:
            self.npx = shutil.which("npx")
            self.available = False
        self.npm_prefix = npm_prefix

    def export(self, request):
        if not self.available:
            raise RuntimeError("npx is not available")

        input_path = Path(request.input_path)
        output_dir = Path(request.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        base_name = input_path.stem

        outputs = []
        for fmt in request.formats:
            output_path = output_dir / f"{base_name}.{fmt}"

            command = [
                self.npx,
                "--yes"
                if self.npx.endswith("npx") or self.npx.endswith("npx.cmd")
                else "",
                os.environ.get("DRAWIO_USER_NODE_PACKAGE", "@shongcheng/drawio-export"),
                str(input_path),
                "--format",
                fmt,
                "--output",
                str(output_path),
            ]
            command = [arg for arg in command if arg]
            if fmt == "png" and request.png_scale:
                command.extend(["--scale", str(request.png_scale)])
            if request.page is not None:
                command.extend(["--page-index", str(request.page)])

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
                    or "user-node export failed"
                )

            outputs.append(str(output_path))

        return outputs
