$preflight = python "scripts/drawio_preflight.py" | Out-String
$preflightObj = $preflight | ConvertFrom-Json

if (-not $preflightObj.ok) {
  python "scripts/drawio_bootstrap.py" --non-admin
}

python "scripts/drawio_export.py" --input "examples/minimal.drawio" --output-dir "outputs" --formats "png,svg" --png-scale 4
