from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.service import APICallService

from . import controller

router = APIRouter(
    prefix="/slack",
    tags=["slack"]
)

@router.get(
    "/test/",
    summary="Test Slack connection",
    response_description="Test Slack connection",
)
def test_connection(db: Session = Depends(get_db)):
    api_call_id = APICallService.create_record(
        db=db,
        request_url=router.url_path_for("test_connection"),
    ).id
        
    result = controller.test_connection()
    
    APICallService.update_record(db=db, id=api_call_id, result=result)
    
    return result
