from fastapi import HTTPException

from controllers.client import get_client


def general_validation(notification, client_id):
    # Verify that it is a valid type
    if "SMS" not in notification and "Email" not in notification:
        raise HTTPException(status_code=404, detail="Invalid notification type")

    # Verify the client and fund exist
    try:
        client = get_client(client_id)[0]
    except:
        client = None

    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    return client
