from sqlalchemy import (
    Column,
    Integer,
    Text,
    DateTime,
    Index
)

from .meta import Base


class RequestLog(Base):
    __tablename__ = 'request_log'
    id = Column(Integer, primary_key=True)
    session_id = Column(Text)
    request = Column(Text)
    timestamp = Column(DateTime)

Index('session_index', RequestLog.session_id)
