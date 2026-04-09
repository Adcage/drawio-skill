from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from scripts.lib.export_core import ExportError, ExportRequest, run_export
from scripts.lib.layout_tools import auto_fix_layout
from scripts.lib.providers import LocalCliProvider, UserNodeProvider


def parse_args():
    parser = argparse.ArgumentParser(description="DrawIO local-only export tool")
    parser.add_argument("--input", required=True, help="Input .drawio file path")
    parser.add_argument("--output-dir", default="outputs", help="Output directory")
    parser.add_argument(
        "--formats", default="png,svg", help="Export formats, e.g. png,svg,pdf"
    )
    parser.add_argument("--png-scale", type=float, default=4.0, help="PNG scale")
    parser.add_argument(
        "--provider",
        default="auto",
        choices=["auto", "local-cli", "user-node"],
        help="Export provider",
    )
    parser.add_argument("--page", type=int, default=None, help="Page index to export")
    parser.add_argument(
        "--auto-fix", action="store_true", help="Enable layout auto-fix"
    )
    parser.add_argument(
        "--max-iterations", type=int, default=2, help="Max auto-fix iterations"
    )
    parser.add_argument(
        "--min-spacing", type=float, default=20.0, help="Minimum spacing"
    )
    return parser.parse_args()


def maybe_fix_layout(request: ExportRequest, min_spacing: float, max_iterations: int):
    input_path = Path(request.input_path)
    xml_text = input_path.read_text(encoding="utf-8")
    fixed_xml, report = auto_fix_layout(
        xml_text,
        min_spacing=min_spacing,
        max_iterations=max_iterations,
    )

    fixed_path = Path(request.output_dir) / f"{input_path.stem}.autofix.drawio"
    fixed_path.parent.mkdir(parents=True, exist_ok=True)
    fixed_path.write_text(fixed_xml, encoding="utf-8")

    request.input_path = str(fixed_path)
    return report


def main() -> int:
    args = parse_args()
    formats = [item.strip() for item in args.formats.split(",") if item.strip()]

    request = ExportRequest(
        input_path=args.input,
        output_dir=args.output_dir,
        formats=formats,
        png_scale=args.png_scale,
        provider_mode=args.provider,
        page=args.page,
    )

    providers = [LocalCliProvider(), UserNodeProvider()]

    auto_fix_report = None
    if args.auto_fix:
        auto_fix_report = maybe_fix_layout(
            request,
            min_spacing=args.min_spacing,
            max_iterations=args.max_iterations,
        )

    try:
        manifest = run_export(request, providers)
    except ExportError as exc:
        error_payload = {
            "ok": False,
            "error": {
                "code": exc.code,
                "message": str(exc),
            },
        }
        print(json.dumps(error_payload, indent=2, ensure_ascii=False))
        return 1

    payload = {
        "ok": True,
        "manifest": manifest,
        "auto_fix": auto_fix_report,
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
