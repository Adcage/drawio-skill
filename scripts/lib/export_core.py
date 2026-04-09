from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, List


SUPPORTED_FORMATS = {"png", "svg", "pdf"}
SUPPORTED_PROVIDER_MODES = {"auto", "local-cli", "user-node"}
AUTO_PROVIDER_ORDER = ("local-cli", "user-node")


class ExportError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


@dataclass
class ExportRequest:
    input_path: str
    output_dir: str
    formats: List[str] = field(default_factory=lambda: ["png", "svg"])
    png_scale: float = 4.0
    provider_mode: str = "auto"
    page: int | None = None


def _normalize_formats(formats: Iterable[str]) -> List[str]:
    normalized = [item.strip().lower() for item in formats if item.strip()]
    if not normalized:
        raise ValueError("At least one export format is required")

    for fmt in normalized:
        if fmt not in SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported format: {fmt}")

    return normalized


def select_provider(providers: Iterable[object], request: ExportRequest):
    if request.provider_mode not in SUPPORTED_PROVIDER_MODES:
        raise ExportError(
            "E_UNSUPPORTED_PROVIDER",
            f"Provider mode '{request.provider_mode}' is not supported",
        )

    indexed = {
        provider.name: provider
        for provider in providers
        if getattr(provider, "available", False)
        and not getattr(provider, "is_remote", False)
    }

    if request.provider_mode != "auto":
        provider = indexed.get(request.provider_mode)
        if provider is None:
            raise ExportError(
                "E_NO_PROVIDER",
                f"Provider '{request.provider_mode}' is unavailable",
            )
        return provider

    for provider_name in AUTO_PROVIDER_ORDER:
        if provider_name in indexed:
            return indexed[provider_name]

    raise ExportError(
        "E_NO_PROVIDER",
        "No local export provider is available. Remote export is disabled by policy.",
    )


def run_export(request: ExportRequest, providers: Iterable[object]):
    input_path = Path(request.input_path)
    if not input_path.exists():
        raise ExportError(
            "E_INPUT_NOT_FOUND", f"Input file does not exist: {input_path}"
        )

    request.formats = _normalize_formats(request.formats)

    output_dir = Path(request.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    provider = select_provider(providers, request)

    try:
        output_paths = provider.export(request)
    except ExportError:
        raise
    except Exception as exc:  # noqa: BLE001
        raise ExportError("E_EXPORT_FAILED", str(exc)) from exc

    outputs = []
    for output_path in output_paths:
        suffix = Path(output_path).suffix.lower().lstrip(".")
        item = {
            "format": suffix,
            "path": str(Path(output_path)),
        }
        if suffix == "png":
            item["scale"] = request.png_scale
        outputs.append(item)

    return {
        "provider": provider.name,
        "input": str(input_path),
        "outputs": outputs,
        "policy": {
            "allow_remote": False,
            "require_admin": False,
        },
    }
