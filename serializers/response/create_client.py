from typing import Optional, List
from datetime import datetime

from pydantic import BaseModel


class ClientResponseModel(BaseModel):
    clientId: str
    externalId: str
    name: str
    isActive: bool
    createDate: datetime
    activateDate: datetime
    deactivateDate: Optional[datetime]
    cashBoxConnectionKey: str

    class Config:
        orm_mode = True
        fields = {
            "clientId": "id",
            "externalId": "external_id",
            "isActive": "is_active",
            "createDate": "create_date",
            "activateDate": "activate_date",
            "deactivateDate": "deactivate_date",
            "cashBoxConnectionKey": "cashbox_connection_key",
        }


class ClientsResponseModel(BaseModel):
    clients: Optional[List[ClientResponseModel]]
