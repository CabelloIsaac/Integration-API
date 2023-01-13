import logging

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