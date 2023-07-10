from enum import Enum

from sqlalchemy import Column, Integer, BigInteger, String, DateTime, Text

from db.models.base import Base


class TaskStatusEnum(Enum):
    IN_PROGRESS = "in_progress"
    ERROR = "error"
    SUCCESS = "success"


class Task(Base):
    __tablename__ = "task"

    id = Column(BigInteger, primary_key=True, autoincrement=True)  # noqa A003
    number = Column(String, unique=True)
    client_id = Column(Integer)
    data = Column(Text)
    create_date = Column(DateTime(timezone=False))
    status = Column(String)
    status_message = Column(Text)
