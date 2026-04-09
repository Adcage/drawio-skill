from __future__ import annotations

import os
import platform
from pathlib import Path


def user_data_dir(app_name: str = "drawio-skill") -> Path:
    system = platform.system().lower()
    home = Path.home()

    if system == "windows":
        base = Path(os.environ.get("LOCALAPPDATA", home / "AppData" / "Local"))
    elif system == "darwin":
        base = home / "Library" / "Application Support"
    else:
        base = Path(os.environ.get("XDG_DATA_HOME", home / ".local" / "share"))

    target = base / app_name
    target.mkdir(parents=True, exist_ok=True)
    return target


def user_bin_dir(app_name: str = "drawio-skill") -> Path:
    target = user_data_dir(app_name) / "bin"
    target.mkdir(parents=True, exist_ok=True)
    return target
