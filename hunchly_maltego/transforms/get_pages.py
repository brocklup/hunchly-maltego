"""
Transform: Hunchly Case → Pages

Retrieves all pages captured under a Hunchly case and adds
them to the Maltego graph as HunchlyPage entities.
"""

from html import escape

from maltego_trx.transform import DiscoverableTransform

from hunchly_maltego import api, entities


class GetPages(DiscoverableTransform):
    """
    Input:  hunchly.HunchlyCase
    Output: hunchly.HunchlyPage (one per captured page)
    """

    @classmethod
    def create_entities(cls, request, response):
        case_name = request.getProperty("properties.hunchlycase") or request.Value

        try:
            pages = api.list_pages(case_name=case_name)
        except api.HunchlyAPIError as exc:
            response.addUIMessage(f"HunchlyAPI error: {exc}")
            return

        for page in pages:
            ent = response.addEntity(entities.HUNCHLY_PAGE, page["url"])
            ent.addProperty("url", "URL", "loose", page["url"])
            ent.addProperty("page_id", "Page ID", "loose", str(page["id"]))
            ent.addProperty("title", "Title", "loose", escape(page.get("title", "")))
            ent.addProperty("short-title", "Short Title", "loose", escape(page.get("title", "")))
