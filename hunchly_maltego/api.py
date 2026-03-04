"""
Thin wrapper around the HunchlyAPI CLI binary.

Every transform calls one of these functions instead of
doing raw subprocess.Popen inline. This makes it trivial
to mock the API in tests and keeps the transforms focused
on Maltego entity logic.
"""

from __future__ import annotations

import json
import logging
from subprocess import PIPE, Popen
from typing import Any

from hunchly_maltego.config import get_api_path

log = logging.getLogger(__name__)


class HunchlyAPIError(RuntimeError):
    """Raised when the HunchlyAPI binary returns non-JSON or a non-zero exit."""


def _run(args: list[str]) -> dict[str, Any]:
    """Execute HunchlyAPI with *args* and return parsed JSON."""
    api = get_api_path()
    cmd = [api, *args]
    log.debug("Running: %s", " ".join(cmd))

    proc = Popen(cmd, stdout=PIPE, stderr=PIPE, errors="replace")
    stdout, stderr = proc.communicate()

    if proc.returncode != 0:
        raise HunchlyAPIError(f"HunchlyAPI exited {proc.returncode}: {stderr.strip()}")

    try:
        return json.loads(stdout)
    except json.JSONDecodeError as exc:
        raise HunchlyAPIError(f"HunchlyAPI returned invalid JSON: {exc}") from exc


# ── Public helpers (one per API verb) ────────────────────────────────────────


def list_pages(*, case_name: str) -> list[dict]:
    """Return pages for *case_name*."""
    result = _run(["page", "list", "-n", case_name])
    return result.get("pages", [])


def get_case_data(*, case_name: str | None = None, page_id: str | None = None) -> list[dict]:
    """Return case data records, filtered by case name or page ID."""
    if page_id:
        result = _run(["caseData", "-p", page_id])
    elif case_name:
        result = _run(["caseData", "-n", case_name])
    else:
        raise ValueError("Either case_name or page_id is required")

    if result.get("number_of_results", 0) == 0:
        return []
    return result.get("data", [])


def get_selectors(*, case_name: str | None = None, page_id: str | None = None) -> list[dict]:
    """Return selectors for a case or page."""
    if page_id:
        result = _run(["selector", "get", "-p", page_id])
    elif case_name:
        result = _run(["selector", "get", "-n", case_name])
    else:
        raise ValueError("Either case_name or page_id is required")

    if result.get("number_of_results", 0) == 0:
        return []
    return result.get("selectors", [])


def get_photos(*, case_name: str | None = None, page_id: str | None = None) -> list[dict]:
    """Return photos for a case or page."""
    if page_id:
        result = _run(["photo", "get", "-p", page_id])
    elif case_name:
        result = _run(["photo", "get", "-n", case_name])
    else:
        raise ValueError("Either case_name or page_id is required")

    if result.get("number_of_results", 0) == 0:
        return []
    return result.get("photos", [])


def get_photo_by_hash(*, sha256: str) -> list[dict]:
    """Return photo(s) matching a SHA-256 hash."""
    result = _run(["photo", "get", "-s", sha256])
    if result.get("number_of_results", 0) == 0:
        return []
    return result.get("photos", [])


def keyword_search(*, query: str) -> list[dict]:
    """Full-text search across all cases (no case filter)."""
    result = _run(["search", "-q", f'+"{query}"', "--nc"])
    return result.get("results", [])
