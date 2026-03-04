"""
Transform: Hunchly Photo → EXIF Metadata

Retrieves EXIF data for a photo (identified by SHA-256 hash)
and outputs each key:value pair as a Phrase entity.
"""

from maltego_trx.entities import Phrase
from maltego_trx.transform import DiscoverableTransform

from hunchly_maltego import api


class GetPhotoExif(DiscoverableTransform):
    """
    Input:  hunchly.HunchlyPhoto
    Output: maltego.Phrase (one per EXIF key:value pair)
    """

    @classmethod
    def create_entities(cls, request, response):
        sha256 = request.getProperty("hash") or request.Value

        try:
            photos = api.get_photo_by_hash(sha256=sha256)
        except api.HunchlyAPIError as exc:
            response.addUIMessage(f"HunchlyAPI error: {exc}")
            return

        for photo in photos:
            exif = photo.get("exif_data")
            if not exif:
                continue

            for key, value in exif.items():
                label = f"{key}:{value}"
                ent = response.addEntity(Phrase, label)
                ent.addProperty("text", "Text", "loose", label)
