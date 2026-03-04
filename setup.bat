@echo off
REM ═══════════════════════════════════════════════════════════
REM   Hunchly Maltego Transforms — Installer (Windows)
REM
REM   This script:
REM     1. Checks for Python 3.10+
REM     2. Creates a virtual environment
REM     3. Installs the Hunchly transforms
REM     4. Generates the Maltego configuration file (.mtz)
REM     5. Tells you what to do next
REM
REM   Usage: Double-click setup.bat or run it from Command Prompt
REM ═══════════════════════════════════════════════════════════

setlocal enabledelayedexpansion

echo.
echo  ══════════════════════════════════════════════════
echo       Hunchly Maltego Transforms — Installer
echo  ══════════════════════════════════════════════════
echo.

REM ── Step 1: Find Python 3.10+ ─────────────────────────────

echo [*] Checking for Python 3.10+...

set "PYTHON="

REM Try common Python commands
for %%P in (python3 python py) do (
    where %%P >nul 2>&1
    if !errorlevel! equ 0 (
        for /f "tokens=*" %%V in ('%%P -c "import sys; v=sys.version_info; print(f'{v.major}.{v.minor}') if v.major>=3 and v.minor>=10 else print('old')" 2^>nul') do (
            if not "%%V"=="old" (
                if "!PYTHON!"=="" (
                    set "PYTHON=%%P"
                    echo [+] Found %%P ^(Python %%V^)
                )
            )
        )
    )
)

if "!PYTHON!"=="" (
    echo.
    echo [X] ERROR: Python 3.10 or newer is required but was not found.
    echo.
    echo     Download Python from: https://www.python.org/downloads/
    echo.
    echo     IMPORTANT: During installation, check the box that says
    echo     "Add Python to PATH"
    echo.
    echo     Then run this script again.
    echo.
    pause
    exit /b 1
)

REM ── Step 2: Create virtual environment ─────────────────────

set "SCRIPT_DIR=%~dp0"
set "VENV_DIR=%SCRIPT_DIR%.venv"

echo [*] Creating virtual environment...

if exist "%VENV_DIR%\Scripts\activate.bat" (
    echo [!] Virtual environment already exists — reusing it
) else (
    %PYTHON% -m venv "%VENV_DIR%"
    if !errorlevel! neq 0 (
        echo [X] ERROR: Failed to create virtual environment.
        pause
        exit /b 1
    )
    echo [+] Created virtual environment at .venv
)

REM Activate
call "%VENV_DIR%\Scripts\activate.bat"

REM ── Step 3: Install ────────────────────────────────────────

echo [*] Installing Hunchly Maltego transforms...

pip install --upgrade pip --quiet
pip install -e "%SCRIPT_DIR%" --quiet

if !errorlevel! neq 0 (
    echo [X] ERROR: Installation failed.
    pause
    exit /b 1
)

echo [+] Installed successfully

REM ── Step 4: Check for HunchlyAPI ───────────────────────────

echo [*] Looking for HunchlyAPI...
hunchly-maltego check 2>nul
echo.

REM ── Step 5: Generate .mtz ─────────────────────────────────

set "MTZ_PATH=%SCRIPT_DIR%hunchly-local.mtz"

echo [*] Generating Maltego configuration file...
hunchly-maltego configure -o "%MTZ_PATH%"

echo.
echo  ══════════════════════════════════════════════════
echo                  Setup Complete!
echo  ══════════════════════════════════════════════════
echo.
echo   One last step:
echo.
echo   1. Open Maltego
echo   2. Go to Import → Configuration
echo   3. Select: %MTZ_PATH%
echo.
echo   That's it! Drag a Hunchly Case entity onto your
echo   graph, name it after a case, and run transforms.
echo.

pause
