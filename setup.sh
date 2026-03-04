#!/usr/bin/env bash
#
# Hunchly Maltego Transforms — Installer (macOS / Linux)
#
# This script:
#   1. Checks for Python 3.10+
#   2. Creates a virtual environment
#   3. Installs the Hunchly transforms
#   4. Generates the Maltego configuration file (.mtz)
#   5. Tells you what to do next
#
# Usage:
#   chmod +x setup.sh
#   ./setup.sh
#

set -e

# ── Colors ───────────────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
NC='\033[0m' # No Color

info()    { echo -e "${BOLD}▸ $1${NC}"; }
success() { echo -e "${GREEN}✓ $1${NC}"; }
warn()    { echo -e "${YELLOW}⚠ $1${NC}"; }
fail()    { echo -e "${RED}✗ $1${NC}"; exit 1; }

echo ""
echo -e "${BOLD}╔══════════════════════════════════════════════════╗${NC}"
echo -e "${BOLD}║     Hunchly Maltego Transforms — Installer      ║${NC}"
echo -e "${BOLD}╚══════════════════════════════════════════════════╝${NC}"
echo ""

# ── Step 1: Find Python 3.10+ ────────────────────────────────────────────────
info "Checking for Python 3.10+..."

PYTHON=""
for cmd in python3.13 python3.12 python3.11 python3.10 python3; do
    if command -v "$cmd" &>/dev/null; then
        version=$("$cmd" -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>/dev/null || echo "0.0")
        major=$(echo "$version" | cut -d. -f1)
        minor=$(echo "$version" | cut -d. -f2)
        if [ "$major" -ge 3 ] && [ "$minor" -ge 10 ]; then
            PYTHON="$cmd"
            break
        fi
    fi
done

if [ -z "$PYTHON" ]; then
    echo ""
    fail "Python 3.10 or newer is required but was not found.

    To install Python:
      macOS:   brew install python@3.12
      Ubuntu:  sudo apt install python3.12 python3.12-venv
      Other:   https://www.python.org/downloads/

    Then run this script again."
fi

success "Found $PYTHON ($($PYTHON --version 2>&1))"

# ── Step 2: Create virtual environment ────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"

info "Creating virtual environment..."

if [ -d "$VENV_DIR" ]; then
    warn "Virtual environment already exists at .venv — reusing it"
else
    "$PYTHON" -m venv "$VENV_DIR" || fail "Failed to create virtual environment. On Ubuntu, try: sudo apt install python3.12-venv"
    success "Created virtual environment at .venv"
fi

# Activate
source "$VENV_DIR/bin/activate"

# ── Step 3: Install ──────────────────────────────────────────────────────────
info "Installing Hunchly Maltego transforms..."

pip install --upgrade pip --quiet
pip install -e "$SCRIPT_DIR" --quiet

success "Installed successfully"

# ── Step 4: Check for HunchlyAPI ─────────────────────────────────────────────
info "Looking for HunchlyAPI..."

hunchly-maltego check 2>/dev/null && true
echo ""

# ── Step 5: Generate .mtz ───────────────────────────────────────────────────
MTZ_PATH="$SCRIPT_DIR/hunchly-local.mtz"

info "Generating Maltego configuration file..."
hunchly-maltego configure -o "$MTZ_PATH"

echo ""
echo -e "${BOLD}╔══════════════════════════════════════════════════╗${NC}"
echo -e "${BOLD}║                 Setup Complete!                  ║${NC}"
echo -e "${BOLD}╚══════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "  ${BOLD}One last step:${NC}"
echo ""
echo -e "  1. Open ${BOLD}Maltego${NC}"
echo -e "  2. Go to ${BOLD}Import → Configuration${NC}"
echo -e "  3. Select: ${BOLD}${MTZ_PATH}${NC}"
echo ""
echo -e "  That's it! Drag a ${BOLD}Hunchly Case${NC} entity onto your"
echo -e "  graph, name it after a case, and run transforms."
echo ""
