#!/usr/bin/env bash
# Simple environment setup helper
set -euo pipefail
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
echo "Environment ready"
