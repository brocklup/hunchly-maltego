# Hunchly Maltego Transforms

Pull your Hunchly case data — pages, selectors, photos, EXIF metadata — directly into Maltego graphs.

![Maltego + Hunchly]

## What You Need

Before you start, make sure you have:

- **Hunchly 2** installed and running
- **Maltego** installed (any edition — CE, Classic, or XL)

## Installation

### Option A: Standalone Binary (Recommended)

No Python required. Download the binary for your platform from the [Releases page](https://github.com/brocklup/hunchly-maltego/releases):

| Platform | Download |
|----------|----------|
| macOS | `hunchly-maltego-macos.zip` |
| Windows | `hunchly-maltego-windows.zip` |
| Linux | `hunchly-maltego-linux.tar.gz` |

**macOS / Linux:**

```
unzip hunchly-maltego-macos.zip
chmod +x hunchly-maltego
./hunchly-maltego configure
```

**Windows:**

1. Extract `hunchly-maltego-windows.zip`
2. Open Command Prompt in that folder
3. Run: `hunchly-maltego.exe configure`

This generates a `hunchly-local.mtz` file. Import it into Maltego (see below).

> **macOS users:** If macOS blocks the binary with "unidentified developer", right-click → Open, or go to System Settings → Privacy & Security and click "Allow Anyway".

### Option B: Install from Source

Requires **Python 3.10+** — [download here](https://www.python.org/downloads/) if you don't have it.

> **Windows users:** When installing Python, make sure to check **"Add Python to PATH"** on the first screen of the installer.

**macOS / Linux:**

```
chmod +x setup.sh
./setup.sh
```

**Windows:**

Double-click **`setup.bat`**, or run it from Command Prompt.

### Import into Maltego

After either option, you'll have a `hunchly-local.mtz` file. Import it:

1. Open **Maltego**
2. Go to **Import → Configuration**
3. Browse to and select **`hunchly-local.mtz`**
4. Click through the import wizard — accept all defaults

You should now see **Hunchly** entities in your entity palette and **Hunchly** transforms available in the transform menu.

## Using the Transforms

### Basic usage

1. Drag a **Hunchly Case** entity from the palette onto your graph
2. Double-click it and type the exact name of one of your Hunchly cases
3. Right-click the entity → **Run Transform** → choose a Hunchly transform

### Available transforms

| Transform | What it does |
|-----------|-------------|
| **Get Pages** | Pulls all captured web pages from a case |
| **Get Data** | Extracts structured data (form fields, metadata) from a case or page |
| **Get Selectors** | Finds emails, usernames, phone numbers, and other identifiers |
| **Get Photos** | Retrieves all captured images (with thumbnail previews) |
| **Get Photo EXIF** | Extracts camera metadata (GPS, device info, timestamps) from a photo |
| **Keyword Search** | Searches across all your cases for pages matching a keyword |

### Running everything at once

Instead of running transforms one at a time, use the **Hunchly Full Case Extraction** machine:

1. Right-click your Hunchly Case entity
2. Select **Run Machine → Hunchly Full Case Extraction**

This automatically runs all transforms in sequence and populates your graph with pages, selectors, data, photos, and EXIF metadata.

## Troubleshooting

### "Error running local transform" / exit code 1

This usually means one of:

- **Hunchly isn't running.** Open the Hunchly application before running transforms.
- **The case name doesn't match.** The entity value must exactly match a case name in Hunchly (case-sensitive).
- **Python can't be found.** Re-run the setup script to regenerate the `.mtz` with the correct paths.

To see the actual error, open a terminal and run:

```
# macOS / Linux
cd /path/to/hunchly-maltego-v2/hunchly_maltego
../.venv/bin/python3 project.py local getpages "YourCaseName" "properties.hunchlycase=YourCaseName"

# Windows
cd C:\path\to\hunchly-maltego-v2\hunchly_maltego
..\.venv\Scripts\python.exe project.py local getpages "YourCaseName" "properties.hunchlycase=YourCaseName"
```

This will print the actual error message instead of the generic Maltego dialog.

### "Could not locate the HunchlyAPI binary"

The transforms need to find Hunchly's API tool on your computer. It checks the standard install locations automatically. If Hunchly is installed somewhere unusual, set this before running the setup script:

```
# macOS / Linux
export HUNCHLY_API_PATH=/your/path/to/HunchlyAPI
./setup.sh

# Windows (Command Prompt)
set HUNCHLY_API_PATH=C:\your\path\to\HunchlyAPI.exe
setup.bat
```

### Entities don't appear in Maltego

Make sure you imported the `hunchly-local.mtz` file (not just the transforms). The `.mtz` file contains the Hunchly entity definitions, icons, and category. Go to **Import → Configuration** and re-import if needed.

### Port conflict on macOS (AirPlay Receiver)

If you use `hunchly-maltego serve` and get a port 5000 error, macOS AirPlay Receiver is using that port. Either:

- Disable it: **System Settings → General → AirDrop & Handoff → AirPlay Receiver → Off**
- Or use a different port: `hunchly-maltego serve --port 8080`

## Updating

To update to a newer version, extract the new release and run the setup script again. It will reuse your existing virtual environment and update everything in place. Then re-import the new `hunchly-local.mtz` in Maltego.

## For Developers

<details>
<summary>Click to expand developer documentation</summary>

### Manual install

```bash
python3.12 -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

### CLI reference

```
hunchly-maltego configure [-o OUTPUT]   Generate local .mtz (default: ./hunchly-local.mtz)
hunchly-maltego serve [--port PORT]     Start remote transform server
hunchly-maltego check                   Verify HunchlyAPI is reachable
```

### Remote / team deployment

Run transforms as a shared server instead of local installs:

```bash
pip install -e ".[remote]"

# Development
hunchly-maltego serve --port 8080

# Production
gunicorn --bind=0.0.0.0:8080 --threads=25 --workers=2 hunchly_maltego.project:application
```

Then configure a TDS seed in Maltego pointing at `http://your-server:8080`.

### Project structure

```
hunchly_maltego/
├── __init__.py
├── api.py              # HunchlyAPI subprocess wrapper
├── cli.py              # CLI entry point (configure / serve / check)
├── config.py           # Platform-aware API path auto-detection
├── entities.py         # Custom Hunchly entity type definitions
├── extensions.py       # Transform registry (display names, metadata)
├── project.py          # maltego-trx server entry point
├── resources/          # Entity definitions, icons, machines (bundled into .mtz)
└── transforms/
    ├── get_data.py
    ├── get_pages.py
    ├── get_photo_exif.py
    ├── get_photos.py
    ├── get_selectors.py
    └── keyword_search.py
```

### Running tests

```bash
pytest
ruff check .
```

</details>

## License

Apache 2.0 — see [LICENSE](LICENSE).
