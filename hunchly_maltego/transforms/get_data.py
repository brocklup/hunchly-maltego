"""
Transform: Hunchly Case / Page → Data Records

Retrieves structured data records captured by Hunchly
(form fields, metadata, etc.) for a case or specific page.
"""

from maltego_trx.transform import DiscoverableTransform

from hunchly_maltego import api, entities


class GetData(DiscoverableTransform):
    """
    Input:  hunchly.HunchlyCase or hunchly.HunchlyPage
    Output: hunchly.HunchlyData (one per data record)
    """

    @classmethod
    def create_entities(cls, request, response):
        page_id = request.getProperty("page_id")
        case_name = request.getProperty("properties.hunchlycase") or request.Value

        try:
            records = api.get_case_data(
                page_id=page_id if page_id else None,
                case_name=case_name if not page_id else None,
            )
        except api.HunchlyAPIError as exc:
            response.addUIMessage(f"HunchlyAPI error: {exc}")
            return

        for record in records:
            value = record.get("data_record", str(record))
            response.addEntity(entities.HUNCHLY_DATA, value)
