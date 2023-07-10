from pydantic import BaseModel


class CreateClientRequestModel(BaseModel):
    externalId: str
    name: str
