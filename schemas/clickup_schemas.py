from typing import Optional
from pydantic import BaseModel

# make custom fields opcional
class ClientBase(BaseModel):
    name: str
    description: str
    status: str
    assignees: list[int]
    custom_fields: Optional[list[dict]]