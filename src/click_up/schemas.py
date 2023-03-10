from typing import Optional
from pydantic import BaseModel

class ClientBase(BaseModel):
    name: str
    cif_nif: str
    cs_owner: str
    send_slack_notification: bool
    send_email_notification: bool
    products: Optional[list[str]]
    custom_fields: Optional[list[dict]]