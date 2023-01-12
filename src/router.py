from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from . import controller
from .db.database import get_db
from .service import APICallService

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
def sync_clients(db: Session = Depends(get_db)):
    api_call_id = APICallService.create_record(
        db=db,
        request_url=router.url_path_for("sync_clients"),
        request_body=""
    ).id
        
    result = controller.sync_clients()
    
    APICallService.update_record(db=db, id=api_call_id, result=result)
    
    return result
