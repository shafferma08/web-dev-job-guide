#!/bin/sh
# Rebuilds the PDF and the web page from build/build.py. Run from the repo root.
set -e
pip install --quiet --break-system-packages reportlab 2>/dev/null || pip install --quiet reportlab
python3 build/build.py
SITE_DIR=. python3 build/html_build.py
mv build/PTC-Web-Developer-Job-Search-Guide.pdf ./PTC-Web-Developer-Job-Search-Guide.pdf
