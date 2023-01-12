from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from .database import Base, create_tables

class APICall(Base):
    __tablename__ = 'apicalls'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    created_at = Column(DateTime, default=datetime.now)
    endpoint = Column(String, nullable=True)
    request_body = Column(String, nullable=True)
    result = Column(String, nullable=True)

create_tables([APICall.__table__])