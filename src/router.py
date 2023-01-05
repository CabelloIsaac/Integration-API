from fastapi import APIRouter
from . import controller

router = APIRouter(
    prefix="/sync",
    tags=["Hubspot", "ClickUp"]
)

@router.get(
    "/clients",
    summary="Syncs clients from Hubspot to ClickUp",
    description="Syncs clients and projects between Hubspot and ClickUp",
    response_description="Synced clients from Hubspot to ClickUp",
)
def sync_clients():
    return controller.sync_clients()