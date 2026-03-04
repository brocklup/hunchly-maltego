"""
Transform: Hunchly Case / Page → Photos

Retrieves photos captured by Hunchly, with local file paths
resolved as file:// URIs for Maltego icon rendering.
"""

from pathlib import Path

from maltego_trx.transform import DiscoverableTransform

from hunchly_maltego import api, entities


class GetPhotos(DiscoverableTransform):
    """
    Input:  hunchly.HunchlyCase or hunchly.HunchlyPage
    Output: hunchly.HunchlyPhoto (one per image, with thumbnail icon)
    """

    @classmethod
    def create_entities(cls, request, response):
        page_id = request.getProperty("page_id")
        case_name = request.getProperty("properties.hunchlycase") or request.Value

        try:
            photos = api.get_photos(
                page_id=page_id if page_id else None,
                case_name=case_name if not page_id else None,
            )
        except api.HunchlyAPIError as exc:
            response.addUIMessage(f"HunchlyAPI error: {exc}")
            return

        for photo in photos:
            photo_hash = photo.get("photo_hash", "")
            if not photo_hash:
                continue

            ent = response.addEntity(entities.HUNCHLY_PHOTO, photo_hash)
            ent.addProperty("url", "URL", "loose", photo.get("photo_url", ""))
            ent.addProperty("hash", "SHA-256", "loose", photo_hash)

            # Resolve local file path to a clickable file:// URI
            raw_path = photo.get("photo_local_file_path")
            if raw_path:
                try:
                    local_uri = Path(raw_path).as_uri()
                    ent.addProperty("local_file", "Local File", "loose", local_uri)
                    ent.setIconURL(local_uri)
                except Exception:
                    # Non-fatal — just skip the icon
                    ent.addProperty("local_file", "Local File", "loose", raw_path)
