"""
Entry point for the Hunchly Maltego transform server.

Usage:
  # Development server (auto-reload)
  python project.py runserver

  # List registered transforms
  python project.py list

  # Production (via gunicorn)
  gunicorn --bind=0.0.0.0:8080 --threads=25 --workers=2 project:application
"""

# ── Path fix for Maltego local transforms ────────────────────────────────────
# Maltego runs this script with the working directory set to the package
# directory (hunchly_maltego/). Python adds that dir to sys.path, but we
# need the *parent* (project root) so `from hunchly_maltego import ...` works.
import os
import sys

_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)
# ─────────────────────────────────────────────────────────────────────────────

from maltego_trx.server import app
from maltego_trx.handler import handle_run

# Import the registry — this triggers transform auto-registration
from hunchly_maltego.extensions import registry  # noqa: F401

# Import all transform classes so they get discovered
from hunchly_maltego.transforms.get_pages import GetPages  # noqa: F401
from hunchly_maltego.transforms.get_data import GetData  # noqa: F401
from hunchly_maltego.transforms.get_selectors import GetSelectors  # noqa: F401
from hunchly_maltego.transforms.get_photos import GetPhotos  # noqa: F401
from hunchly_maltego.transforms.get_photo_exif import GetPhotoExif  # noqa: F401
from hunchly_maltego.transforms.keyword_search import KeywordSearch  # noqa: F401

# maltego-trx's auto-discovery expects filename == classname (e.g. GetPages.py).
# Since we use snake_case filenames, register transforms manually.
from maltego_trx.registry import transform_classes, update_mapping

for cls in [GetPages, GetData, GetSelectors, GetPhotos, GetPhotoExif, KeywordSearch]:
    if cls not in transform_classes:
        transform_classes.append(cls)
update_mapping()

# WSGI application for gunicorn
application = app


if __name__ == "__main__":
    handle_run(__name__, sys.argv, app, port=8080)
