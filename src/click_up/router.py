from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.service import APICallService
from src.db.database import get_db

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
def create_client(request: ClientBase, db: Session = Depends(get_db)):
    api_call_id = APICallService.create_record(
        db=db,
        request_url=router.url_path_for("create_client"),
        request_body=request.json()
    ).id
    
    result = controller.sync_client(request=request)
    
    APICallService.update_record(db=db, id=api_call_id, result=result)
    
    return result


@router.post(
    "/client/fix-status",
    summary="Apply its lowest project status to client",
    description="",
    response_description="The client updated",
)
def apply_its_lowest_status_to_client(request: TaskUpdatedElement, db: Session = Depends(get_db)):
    api_call_id = APICallService.create_record(
        db=db,
        request_url=router.url_path_for("apply_its_lowest_status_to_client"),
        request_body=request.json()
    ).id
    
    result = controller.apply_its_lowest_status_to_client(request=request)
    
    APICallService.update_record(db=db, id=api_call_id, result=result)
    
    return result


@router.get(
    "/task/sync-all",
    summary="Fix tasks",
    description="Fixes tasks in ClickUp updating the projects with the client data",
    response_description="Count of tasks fixed",
)
def sync_all_tasks(db: Session = Depends(get_db)):
    api_call_id = APICallService.create_record(
        db=db,
        request_url=router.url_path_for("sync_all_tasks"),
    ).id
    
    result = controller.sync_all_tasks()
    
    APICallService.update_record(db=db, id=api_call_id, result=result)
    
    return result


@router.post(
    "/task/sync",
    summary="Fix tasks",
    description="Fixes tasks in ClickUp updating the projects with the client data",
    response_description="Count of tasks fixed",
)
def sync_task(request: TaskUpdatedElement, db: Session = Depends(get_db)):
    api_call_id = APICallService.create_record(
        db=db,
        request_url=router.url_path_for("sync_task"),
        request_body=request.json()
    ).id
    
    result = controller.sync_task(request=request)
    
    APICallService.update_record(db=db, id=api_call_id, result=result)
    
    return result