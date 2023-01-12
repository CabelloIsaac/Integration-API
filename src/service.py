import logging
from datetime import datetime

from sqlalchemy.orm.session import Session

from src.db.models import APICall

from .slack import controller as slack_controller


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


    def update_record(db: Session, id, result):
        """
        Set the execution result of an APICall
        """
        has_error = False
        if "status" in result:
            has_error = result["status"] == "error"
                
        apicall_data: APICall = db.query(APICall).filter(APICall.id == id).first()
        result = str(result)
        apicall_data.result = result
        db.add(apicall_data)
        
        logging.info(result)
        id_length = len(str(id))
        closing_brackets = ''.join(['#' for i in range(id_length)])
        logging.info(f"{'########################'+closing_brackets}\n")
        
        if has_error:
            apicall_id = f"apicall_id: {apicall_data.id}"
            apicall_endpoint = f"endpoint: {apicall_data.endpoint}"
            apicall_request_body = f"request_body: {apicall_data.request_body}"
            apicall_result = f"result: {apicall_data.result}"

            message_body = f"{apicall_id}\n{apicall_endpoint}\n{apicall_request_body}\n{apicall_result}"
            
            slack_controller.send_alert(message=f"❌ ERROR DETECTED at {datetime.now()}:\n{message_body}")
        
        db.commit()
        
    
class LoggingService:
    
    def __init__(self, module: str):
        self.module: str = module
    
    def info(self, message: str, to_file: bool = True):
        """
        Log an info message to console and/or file
        
        Args:
            message (str): Message to log
            to_file (bool): Log to file if True
        """
        
        # Log to console
        print (f"{self.module} - INFO: {message}")
        
        # Log to file
        if to_file:
            logging.info(f"{self.module}: {message}")
            
            
    def error(self, message: str, to_file: bool = True):
        """
        Log an error message to console and/or file
        
        Args:
            message (str): Message to log
            to_file (bool): Log to file if True
        """
        
        # Log to console
        print (f"{self.module.upper()} - ERROR: {message}")
        
        # Log to file
        if to_file:
            logging.error(f"{self.module}: {message}")
            
            
    def debug(self, message: str, to_file: bool = True):
        """
        Log an debug message to console and/or file
        
        Args:
            message (str): Message to log
            to_file (bool): Log to file if True
        """
        
        # Log to console
        print (f"{self.module.upper()} - DEBUG: {message}")
        
        # Log to file
        if to_file:
            logging.debug(f"{self.module}: {message}")