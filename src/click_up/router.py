from fastapi import APIRouter

from . import controller
from .schemas import ClientBase

router = APIRouter(
    prefix="/clickup",
    tags=["clickup"]
)

@router.post(
    "/client/",
    summary="Create a client",
    description="Creates a client in ClickUp",
    response_description="The client created",
)
def create_client(request: ClientBase):
    return controller.create_client(request=request)

