#!/bin/bash

# Deployment helper for the OpenFrame project
# Usage: ./deploy.sh [major|minor|patch] (default: patch)

set -euo pipefail

BUMP_TYPE=${1:-patch}
if [[ ! "$BUMP_TYPE" =~ ^(major|minor|patch)$ ]]; then
  echo "Invalid bump type: $BUMP_TYPE (use major/minor/patch)"
  exit 1
fi

python3 --version >/dev/null

python3 - <<'PY'
import importlib
import subprocess
import sys

missing = []
for module in ("build", "twine"):
    try:
        importlib.import_module(module)
    except ImportError:
        missing.append(module)

if missing:
    subprocess.run([sys.executable, "-m", "pip", "install", *missing], check=True)
PY

NEW_VERSION=$(python3 - "$BUMP_TYPE" <<'PY'
import re
import sys
from pathlib import Path

BUMP_TYPE = sys.argv[1]
path = Path("pyproject.toml")
text = path.read_text()
match = re.search(r'^version = "([^"]+)"', text, re.MULTILINE)

if not match:
    raise SystemExit("version field not found in pyproject.toml")

major, minor, patch = map(int, match.group(1).split("."))

if BUMP_TYPE == "major":
    major += 1
    minor = 0
    patch = 0
elif BUMP_TYPE == "minor":
    minor += 1
    patch = 0
else:
    patch += 1

new_version = f"{major}.{minor}.{patch}"
path.write_text(text.replace(match.group(0), f'version = "{new_version}"', 1))
print(new_version)
PY
)

echo "Version set to $NEW_VERSION"

rm -rf dist build *.egg-info

python3 -m build

python3 -m twine check dist/*

echo "Uploading OpenFrame $NEW_VERSION to PyPI (ensure ~/.pypirc token is configured)"
python3 -m twine upload dist/*

rm -rf dist build *.egg-info

echo "Deployment finished. Version $NEW_VERSION published."


