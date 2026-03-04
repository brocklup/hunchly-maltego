#!/usr/bin/env bash
#
# Build the hunchly-maltego standalone binary using PyInstaller.
#
# Usage:
#   ./build.sh
#
# Output:
#   dist/hunchly-maltego          (macOS/Linux)
#   dist/hunchly-maltego.exe      (Windows via CI)
#

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "─── Installing build dependencies ───"
pip install pyinstaller --quiet
pip install -e . --quiet

echo ""
echo "─── Building standalone binary ───"
pyinstaller hunchly-maltego.spec --clean --noconfirm

echo ""
echo "─── Verifying binary ───"
BINARY="dist/hunchly-maltego"
if [ -f "$BINARY" ]; then
    echo "  ✓ Built: $BINARY ($(du -h "$BINARY" | cut -f1))"
    echo ""
    echo "  Testing..."
    "$BINARY" check 2>/dev/null || true
    echo ""
    "$BINARY" configure -o dist/hunchly-local.mtz 2>/dev/null
    echo ""
    echo "─── Done ───"
    echo "  Binary:  $BINARY"
    echo "  Config:  dist/hunchly-local.mtz"
    echo ""
    echo "  To distribute: zip up the binary and README,"
    echo "  or use the GitHub Actions workflow for cross-platform builds."
else
    echo "  ✗ Build failed — binary not found at $BINARY"
    exit 1
fi
