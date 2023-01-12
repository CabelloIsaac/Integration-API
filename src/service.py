import logging
from datetime import datetime

from sqlalchemy.orm.session import Session

from src.db.models import APICall

class APICallService:

    def create_record(db: Session, request_url, request_body = None):
        """
        Create a new APICall in database
        
        Args:
            db (Session): Database session
            request_url (str): Request URL
            request_body (str): Request body
            
        Returns:
            APICall: APICall object
        """
        data = APICall(
            created_at = datetime.now(),
            endpoint = request_url,
            request_body = request_body,
        )
        db.add(data)
        db.commit()
        db.refresh(data)
        
        logging.info(datetime.now())
        logging.info(f"########## API_CALL_ID: {data.id}")
        logging.info(f"endpoint: {data.endpoint}")
            
        return data


    def update_record(db: Session, id, result: str):
        """
        Set the execution result of an APICall
        """
        apicall_data: APICall = db.query(APICall).filter(APICall.id == id).first()
        result = str(result)
        apicall_data.result = result
        db.add(apicall_data)
        
        logging.info(result)
        id_length = len(str(id))
        closing_brackets = ''.join(['#' for i in range(id_length)])
        logging.info(f"{'########################'+closing_brackets}\n")
        
        db.commit()