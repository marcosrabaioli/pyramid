from sqlalchemy import (
    Column,
    Integer,
    Text,
)

from .meta import Base


class Quote(Base):
    __tablename__ = 'quote'
    id = Column(Integer, primary_key=True)
    quote = Column(Text)


