"""
Transform: Phrase → Hunchly Pages (keyword search)

Runs a full-text keyword search across all Hunchly cases
and returns matching pages.
"""

from html import escape

from maltego_trx.transform import DiscoverableTransform

from hunchly_maltego import api, entities


class KeywordSearch(DiscoverableTransform):
    """
    Input:  maltego.Phrase (search term)
    Output: hunchly.HunchlyPage (matching pages)
    """

    @classmethod
    def create_entities(cls, request, response):
        query = request.getProperty("text") or request.Value

        try:
            results = api.keyword_search(query=query)
        except api.HunchlyAPIError as exc:
            response.addUIMessage(f"HunchlyAPI error: {exc}")
            return

        for result in results:
            url = result.get("url", "")
            if not url:
                continue

            ent = response.addEntity(entities.HUNCHLY_PAGE, url)
            ent.addProperty("url", "URL", "loose", url)
            ent.addProperty("page_id", "Page ID", "loose", str(result.get("page_id", "")))
            ent.addProperty("title", "Title", "loose", escape(result.get("title", "")))
            ent.addProperty("short-title", "Short Title", "loose", escape(result.get("title", "")))
