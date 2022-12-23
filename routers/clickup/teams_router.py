from fastapi import APIRouter
from controllers.clickup import teams_controller


router = APIRouter(
    prefix="/clickup/team",
    tags=["clickup", "team"]
)


@router.get(
    "/",
    summary="Returns all teams",
    description="This api call simulates fetching all teams",
    response_description="The list of available teams",
)
async def get_all_teams():
    teams = teams_controller.get_all()
    return teams
