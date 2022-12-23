from fastapi import APIRouter

from controllers.clickup import clickup_controller


router = APIRouter(
    prefix="/clickup/list",
    tags=["clickup", "team"]
)

@router.get(
    "/{id}/custom_fields/",
    summary="Returns all lists for a space",
    description="This api call simulates fetching all spaces for a team",
    response_description="The list of available spaces",
)
def get_spaces_by_team_id(id: int):
    return clickup_controller.get_custom_fields()
