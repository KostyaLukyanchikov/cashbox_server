import uuid
from fastapi import Response

from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import NotFoundError
from controllers.client.database_operations import (
    create_client_in_db,
    get_clients_from_db,
    get_client_by_external_id_from_db,
    change_client_activation_in_db,
    get_client_by_cashbox_connection_key_from_db,
)
from serializers.request.create_client import CreateClientRequestModel
from serializers.response.create_client import ClientResponseModel


class CreateClient:
    def __init__(self, request_model: CreateClientRequestModel, db: AsyncSession):
        self.request_model = request_model
        self.db = db

    def generate_cashbox_key(self) -> str:
        return str(uuid.uuid4())

    async def process(self):
        client_data = {
            "external_id": self.request_model.externalId,
            "name": self.request_model.name,
            "cashbox_connection_key": self.generate_cashbox_key(),
        }
        a = await create_client_in_db(self.db, client_data)
        return a


class GetClient:
    def __init__(self, db: AsyncSession, client_external_id=None, offset: int = 0, limit: int = 100):
        self.db = db
        self.client_external_id = client_external_id
        self.offset = offset
        self.limit = limit

    async def process(self):
        if self.client_external_id:
            return await self.__get_one()
        else:
            return await self.__get_many()

    async def __get_one(self):
        client = await get_client_by_external_id_from_db(self.db, self.client_external_id)
        if not client:
            raise NotFoundError(message="Client was not found")
        return client

    async def __get_many(self):
        clients: list = await get_clients_from_db(self.db, offset=self.offset, limit=self.limit)
        result = {"clients": []}
        for client in clients:
            rec = ClientResponseModel.from_orm(client)
            result["clients"].append(rec)

        return result


class ChangeActivationClient:
    def __init__(self, is_active: bool, client_external_id: str, db: AsyncSession):
        self.client_external_id = client_external_id
        self.is_active: bool = is_active
        self.db = db

    async def process(self):
        if not await get_client_by_external_id_from_db(self.db, self.client_external_id):
            return Response(status_code=404)
        await change_client_activation_in_db(self.db, self.client_external_id, self.is_active)


class GetClientByCashboxKey:
    def __init__(self, cashbox_connection_key: str, db: AsyncSession):
        self.cashbox_connection_key = cashbox_connection_key
        self.db = db

    async def process(self):
        client = await get_client_by_cashbox_connection_key_from_db(self.db, self.cashbox_connection_key)
        if not client:
            return None
        return client
