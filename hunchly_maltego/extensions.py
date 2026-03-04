"""
Transform Registry — metadata used for .mtz generation and TDS configuration.

This file configures how transforms appear in Maltego's UI:
display names, descriptions, input/output entity types, and
the transform set seed.
"""

from maltego_trx.decorator_registry import TransformRegistry

registry = TransformRegistry(
    owner="Hunchly",
    author="Hunchly <support@hunch.ly>",
    host_url="https://localhost:8080",
    seed_ids=["hunchly"],
)

registry.version = "2.0"

# ── Transform display metadata ──────────────────────────────────────────────
# These decorators are picked up when the transforms auto-register.
# We import and decorate here to keep the transform files clean.

# ── Import transforms so they're discoverable by maltego-trx ─────────────────
# The @registry.register_transform decorator below both registers metadata
# AND wraps the class, so these imports must come after registry is created.

from hunchly_maltego.transforms.get_pages import GetPages  # noqa: E402
from hunchly_maltego.transforms.get_data import GetData  # noqa: E402
from hunchly_maltego.transforms.get_selectors import GetSelectors  # noqa: E402
from hunchly_maltego.transforms.get_photos import GetPhotos  # noqa: E402
from hunchly_maltego.transforms.get_photo_exif import GetPhotoExif  # noqa: E402
from hunchly_maltego.transforms.keyword_search import KeywordSearch  # noqa: E402

# register_transform() is a decorator — it returns a wrapper that takes the class.
# Signature: register_transform(display_name, input_entity, description, ...)(TransformClass)

registry.register_transform(
    "Hunchly: Get Pages [Case → Pages]",
    "hunchly.HunchlyCase",
    "Retrieve all pages captured under a Hunchly case.",
)(GetPages)

registry.register_transform(
    "Hunchly: Get Data [Case/Page → Data]",
    "hunchly.HunchlyCase",
    "Retrieve structured data records from a Hunchly case or page.",
)(GetData)

registry.register_transform(
    "Hunchly: Get Selectors [Case/Page → Selectors]",
    "hunchly.HunchlyCase",
    "Retrieve OSINT selectors (emails, usernames, etc.) from a case or page.",
)(GetSelectors)

registry.register_transform(
    "Hunchly: Get Photos [Case/Page → Photos]",
    "hunchly.HunchlyCase",
    "Retrieve captured photos from a Hunchly case or page.",
)(GetPhotos)

registry.register_transform(
    "Hunchly: Get Photo EXIF [Photo → EXIF Data]",
    "hunchly.HunchlyPhoto",
    "Extract EXIF metadata from a Hunchly photo.",
)(GetPhotoExif)

registry.register_transform(
    "Hunchly: Keyword Search [Phrase → Pages]",
    "maltego.Phrase",
    "Full-text search across all Hunchly cases.",
)(KeywordSearch)
