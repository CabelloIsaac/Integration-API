from fastapi import APIRouter

from . import controller
from .schemas import ClientBase, TaskUpdatedElement

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


@router.get(
    "/task/sync-all",
    summary="Fix tasks",
    description="Fixes tasks in ClickUp updating the projects with the client data",
    response_description="Count of tasks fixed",
)
def fix_tasks():
    return controller.sync_all_tasks()


@router.post(
    "/task/sync",
    summary="Fix tasks",
    description="Fixes tasks in ClickUp updating the projects with the client data",
    response_description="Count of tasks fixed",
)
def fix_tasks(request: TaskUpdatedElement):
    return controller.sync_task(request=request)