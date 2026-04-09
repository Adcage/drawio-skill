#!/usr/bin/env bash
set -e

if command -v python.exe >/dev/null 2>&1; then
  PYTHON_CMD=(python.exe)
elif command -v python >/dev/null 2>&1; then
  PYTHON_CMD=(python)
elif command -v python3 >/dev/null 2>&1; then
  PYTHON_CMD=(python3)
elif command -v py >/dev/null 2>&1; then
  PYTHON_CMD=(py -3)
else
  echo "Python interpreter not found" >&2
  exit 1
fi

PREFLIGHT_FILE=.drawio-preflight.json
"${PYTHON_CMD[@]}" scripts/drawio_preflight.py > "$PREFLIGHT_FILE"

if ! "${PYTHON_CMD[@]}" - <<'PY'
import json
from pathlib import Path
data = json.loads(Path('.drawio-preflight.json').read_text(encoding='utf-8'))
raise SystemExit(0 if data.get('ok') else 1)
PY
then
  "${PYTHON_CMD[@]}" scripts/drawio_bootstrap.py --non-admin
fi

"${PYTHON_CMD[@]}" scripts/drawio_export.py --input examples/minimal.drawio --output-dir outputs --formats png,svg --png-scale 4
rm -f "$PREFLIGHT_FILE"
