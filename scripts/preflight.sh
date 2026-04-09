#!/usr/bin/env bash
if command -v python.exe >/dev/null 2>&1; then
  python.exe scripts/drawio_preflight.py
elif command -v python >/dev/null 2>&1; then
  python scripts/drawio_preflight.py
elif command -v python3 >/dev/null 2>&1; then
  python3 scripts/drawio_preflight.py
elif command -v py >/dev/null 2>&1; then
  py -3 scripts/drawio_preflight.py
else
  echo "Python interpreter not found" >&2
  exit 1
fi
