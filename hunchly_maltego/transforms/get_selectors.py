"""
Transform: Hunchly Case / Page → Selectors

Retrieves OSINT selectors (emails, usernames, phone numbers, etc.)
identified by Hunchly during capture.
"""

from maltego_trx.transform import DiscoverableTransform

from hunchly_maltego import api, entities


class GetSelectors(DiscoverableTransform):
    """
    Input:  hunchly.HunchlyCase or hunchly.HunchlyPage
    Output: hunchly.HunchlySelector (one per selector)
    """

    @classmethod
    def create_entities(cls, request, response):
        page_id = request.getProperty("page_id")
        case_name = request.getProperty("properties.hunchlycase") or request.Value

        try:
            selectors = api.get_selectors(
                page_id=page_id if page_id else None,
                case_name=case_name if not page_id else None,
            )
        except api.HunchlyAPIError as exc:
            response.addUIMessage(f"HunchlyAPI error: {exc}")
            return

        for sel in selectors:
            value = sel.get("selector", str(sel))
            response.addEntity(entities.HUNCHLY_SELECTOR, value)
