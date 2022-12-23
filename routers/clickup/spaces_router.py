from typing import Optional
from fastapi import APIRouter, status, Response
from .teams_router import router as teams_router

from controllers.clickup import spaces_controller


router = teams_router
router.tags.append("space")


@router.get(
    "/{id}/space/",
    summary="Returns all spaces for a team",
    description="This api call simulates fetching all spaces for a team",
    response_description="The list of available spaces",
)
def get_spaces_by_team_id(id: int):
    return spaces_controller.get_by_team(id)
