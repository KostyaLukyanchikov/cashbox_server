from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class TaskStatus(str, Enum):
    IN_PROGRESS = "in_progress"
    ERROR = "error"
    SUCCESS = "success"


class TaskResponseModel(BaseModel):
    number: str
    clientId: str
    createDate: datetime
    status: TaskStatus
    statusMessage: Optional[str]

    class Config:
        orm_mode = True
        fields = {
            "clientId": "id",
            "createDate": "create_date",
            "statusMessage": "status_message",
        }
