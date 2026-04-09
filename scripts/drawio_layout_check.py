from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from scripts.lib.layout_tools import analyze_layout


def main() -> int:
    parser = argparse.ArgumentParser(description="Check drawio layout issues")
    parser.add_argument("--input", required=True, help="Input .drawio file path")
    parser.add_argument("--min-spacing", type=float, default=20.0)
    args = parser.parse_args()

    input_path = Path(args.input)
    xml_text = input_path.read_text(encoding="utf-8")
    report = analyze_layout(xml_text, min_spacing=args.min_spacing)

    total = (
        len(report["overlaps"])
        + len(report["out_of_bounds"])
        + len(report["spacing_violations"])
    )
    payload = {
        "ok": total == 0,
        "issues_total": total,
        "report": report,
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if total == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
