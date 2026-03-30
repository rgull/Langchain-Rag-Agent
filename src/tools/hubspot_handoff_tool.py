from langchain.tools import tool
from hubspot import HubSpot
from hubspot.crm.contacts import PublicObjectSearchRequest

from config.settings import settings


@tool
def handoff_to_hubspot_tool(reason: str, user_email: str):
    """
    Submit escalation details to HubSpot when the agent cannot fully answer.

    Args:
        reason: Short reason why escalation is needed.
        user_email: Required user email taken from user for support follow-up.
    """
    safe_reason = reason.strip() if reason else "Additional support is required."
    safe_email = user_email.strip()
    if not safe_email:
        return "Escalation requires user_email so the HubSpot team can contact the user."

    access_token = (settings.HUBSPOT_ACCESS_TOKEN or "").strip()
    if not access_token:
        return "HubSpot handoff is not configured. Missing HUBSPOT_ACCESS_TOKEN."

    try:
        client = HubSpot(access_token=access_token)
        search_request = PublicObjectSearchRequest(
            filter_groups=[
                {
                    "filters": [
                        {
                            "propertyName": "email",
                            "operator": "EQ",
                            "value": safe_email,
                        }
                    ]
                }
            ],
            properties=["email", "firstname", "lastname"],
            limit=1,
        )
        search_result = client.crm.contacts.search_api.do_search(
            public_object_search_request=search_request
        )

        if search_result.results:
            contact_id = search_result.results[0].id
            return (
                "Escalation sent to HubSpot successfully. "
                f"Existing contact found (id={contact_id}, email={safe_email}). "
                f"Reason: {safe_reason}."
            )

        create_payload = {"properties": {"email": safe_email}}
        created = client.crm.contacts.basic_api.create(
            simple_public_object_input_for_create=create_payload
        )
        return (
            "Escalation sent to HubSpot successfully. "
            f"New contact created (id={created.id}, email={safe_email}). "
            f"Reason: {safe_reason}."
        )
    except Exception as exc:
        return f"Error while sending escalation to HubSpot. details={str(exc)}"