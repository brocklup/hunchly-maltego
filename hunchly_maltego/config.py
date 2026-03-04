"""
Auto-detect the HunchlyAPI binary path across platforms.

Resolution order:
  1. HUNCHLY_API_PATH environment variable (always wins)
  2. Platform-specific default install locations
  3. Raise a clear error with remediation instructions
"""

import os
import sys
import shutil
from pathlib import Path

# Known default install paths per platform
_KNOWN_PATHS: dict[str, list[str]] = {
    "win32": [
        r"C:\Program Files (x86)\Hunchly 2\Dashboard\HunchlyAPI.exe",
        r"C:\Program Files\Hunchly 2\Dashboard\HunchlyAPI.exe",
    ],
    "darwin": [
        "/Applications/Hunchly2.app/Contents/MacOS/HunchlyAPI",
        str(Path.home() / "Applications" / "Hunchly2.app" / "Contents" / "MacOS" / "HunchlyAPI"),
    ],
    "linux": [
        "/usr/lib/hunchly/HunchlyAPI",
        "/opt/hunchly/HunchlyAPI",
        str(Path.home() / ".local" / "bin" / "HunchlyAPI"),
    ],
}


class HunchlyAPINotFoundError(FileNotFoundError):
    """Raised when the HunchlyAPI binary can't be located."""

    def __init__(self) -> None:
        platform = sys.platform
        candidates = _KNOWN_PATHS.get(platform, [])
        msg_lines = [
            "Could not locate the HunchlyAPI binary.",
            "",
            "Checked:",
        ]
        for p in candidates:
            msg_lines.append(f"  • {p}")
        msg_lines += [
            "",
            "Fix: set the HUNCHLY_API_PATH environment variable to the full path of HunchlyAPI.",
            "  export HUNCHLY_API_PATH=/path/to/HunchlyAPI",
        ]
        super().__init__("\n".join(msg_lines))


def detect_api_path() -> str:
    """Return the resolved path to the HunchlyAPI binary, or raise."""

    # 1. Env var override
    env_path = os.environ.get("HUNCHLY_API_PATH")
    if env_path:
        resolved = Path(env_path).expanduser().resolve()
        if resolved.is_file():
            return str(resolved)
        # Also check PATH
        on_path = shutil.which(env_path)
        if on_path:
            return on_path
        raise HunchlyAPINotFoundError()

    # 2. Platform defaults
    platform = sys.platform
    for candidate in _KNOWN_PATHS.get(platform, []):
        if Path(candidate).is_file():
            return candidate

    # 3. Last resort: check PATH
    on_path = shutil.which("HunchlyAPI")
    if on_path:
        return on_path

    raise HunchlyAPINotFoundError()


def get_api_path() -> str:
    """Convenience wrapper — returns the path or raises with a helpful message."""
    return detect_api_path()
