#!/usr/bin/env bash

set -euo pipefail

PROJECT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$(dirname -- "$PROJECT_DIR")/env"

if [[ ! -f "$VENV_DIR/bin/activate" ]]; then
    echo "No se encontro el entorno virtual en: $VENV_DIR" >&2
    echo "Creelo con: cd \"$(dirname -- "$PROJECT_DIR")\" && python3 -m venv env" >&2
    exit 1
fi

cd "$PROJECT_DIR"
# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"
exec python main.py
