from typing import Optional
from pydantic import BaseModel

class ClientBase(BaseModel):
    name: str
    nif_cif: str
    cs_owner: str
    products: Optional[list[dict]]
    custom_fields: Optional[list[dict]]


class TaskUpdatedElement(BaseModel):
    task_id: Optional[str] = None
    custom_task_ids: Optional[bool] = False
