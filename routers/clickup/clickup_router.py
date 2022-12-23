from fastapi import APIRouter

from controllers.clickup import clickup_controller
from schemas.clickup_schemas import ClientBase


router = APIRouter(
    prefix="/clickup",
    tags=["clickup"]
)

@router.post(
    "/client/",
    summary="Create a client",
    description="This api call simulates creating a client",
    response_description="The client created",
)
def create_client(request: ClientBase):
    return clickup_controller.create_client(request=request)

