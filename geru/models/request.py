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
    sessionId = Column(Text)
    request = Column(Text)
    timestamp = Column(DateTime)

Index('session_index', RequestLog.sessionId)
