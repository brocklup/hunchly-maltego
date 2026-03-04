"""
Custom Hunchly entity definitions for Maltego.

Only the Hunchly-specific entities are defined here.
Stock Maltego entities (Phrase, URL, Domain, etc.) are
already available via the maltego-trx library.
"""

from maltego_trx.entities import Phrase  # noqa: F401 — re-export for convenience


# ── Hunchly entity type strings ─────────────────────────────────────────────

HUNCHLY_CASE = "hunchly.HunchlyCase"
HUNCHLY_PAGE = "hunchly.HunchlyPage"
HUNCHLY_PHOTO = "hunchly.HunchlyPhoto"
HUNCHLY_SELECTOR = "hunchly.HunchlySelector"
HUNCHLY_DATA = "hunchly.HunchlyData"
