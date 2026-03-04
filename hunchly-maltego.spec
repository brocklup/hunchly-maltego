# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec for hunchly-maltego standalone binary.

Produces a single-file executable that:
  - Runs `hunchly-maltego configure` to generate the .mtz
  - Runs `hunchly-maltego local <transform> ...` when invoked by Maltego
  - Runs `hunchly-maltego check` to verify HunchlyAPI
  - Runs `hunchly-maltego serve` for remote transform server

Build:
  pyinstaller hunchly-maltego.spec
"""

import os
import sys
from pathlib import Path

block_cipher = None

# Locate the package
pkg_dir = Path("hunchly_maltego")
resources_dir = pkg_dir / "resources"

# Collect all resource files (entities, icons, machines, etc.)
resource_datas = []
for root, dirs, files in os.walk(resources_dir):
    for f in files:
        src = os.path.join(root, f)
        # Destination preserves the path relative to project root
        dst = os.path.dirname(src)
        resource_datas.append((src, dst))

a = Analysis(
    ["hunchly_maltego/cli.py"],
    pathex=["."],
    binaries=[],
    datas=resource_datas,
    hiddenimports=[
        "hunchly_maltego",
        "hunchly_maltego.api",
        "hunchly_maltego.cli",
        "hunchly_maltego.config",
        "hunchly_maltego.entities",
        "hunchly_maltego.extensions",
        "hunchly_maltego.project",
        "hunchly_maltego.transforms",
        "hunchly_maltego.transforms.get_pages",
        "hunchly_maltego.transforms.get_data",
        "hunchly_maltego.transforms.get_selectors",
        "hunchly_maltego.transforms.get_photos",
        "hunchly_maltego.transforms.get_photo_exif",
        "hunchly_maltego.transforms.keyword_search",
        "maltego_trx",
        "maltego_trx.server",
        "maltego_trx.handler",
        "maltego_trx.registry",
        "maltego_trx.transform",
        "maltego_trx.entities",
        "maltego_trx.maltego",
        "maltego_trx.decorator_registry",
        "maltego_trx.mtz",
        "flask",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="hunchly-maltego",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
