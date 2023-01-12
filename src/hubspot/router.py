from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.service import APICallService

from . import controller

router = APIRouter(
    prefix="/hubspot",
    tags=["hubspot"]
)

@router.get(
    "/deals/",
    summary="Get deals",
    description="Get deals from Hubspot",
    response_description="Deals",
)
def get_deals(db: Session = Depends(get_db)):
    api_call_id = APICallService.create_record(
        db=db,
        request_url=router.url_path_for("get_deals"),
    ).id
        
    result = controller.get_deals()
    
    APICallService.update_record(db=db, id=api_call_id, result=result)
    
    return result


@router.get(
    "/deals/process",
    summary="Process deals",
    description="Process deals from Hubspot",
    response_description="Deals",
)
def process_deals(db: Session = Depends(get_db)):
    api_call_id = APICallService.create_record(
        db=db,
        request_url=router.url_path_for("process_deals"),
    ).id
    result = controller.process_deals()
    
    APICallService.update_record(db=db, id=api_call_id, result=result)
    
    return result