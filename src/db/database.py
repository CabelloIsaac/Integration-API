from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from src.slack import controller as slack_controller
from src.logging.service import LoggingService
from dotenv import load_dotenv

load_dotenv()

database = os.getenv("DB_NAME")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")

SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{database}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

logging_service = LoggingService(module=__name__)

def create_tables(tables):
    try:
        Base.metadata.create_all(engine, tables=tables)
    except Exception as e:
        message = f"Database connection error: {e}"
        slack_controller.send_error_alert(message=message)
        logging_service.error(message=message)
        

def get_db():
    db = SessionLocal()
    try:
        print("db")
        yield db
    finally:
        print("db.close()")
        db.close()
