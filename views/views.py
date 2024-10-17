import json

from fastapi import APIRouter, Depends, WebSocketException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.websockets import WebSocket, WebSocketDisconnect

from app import logger
from app.dependencies import get_db
from app.exceptions import ForbiddenError, WebsocketError, TaskError
from controllers.client.client_operations import (
    CreateClient,
    GetClient,
    ChangeActivationClient,
    GetClientByCashboxKey,
)
from controllers.task.task_operations import CreateTask, SuccessTask, ErrorTask, GetTask
from db.models.client import Client
from serializers.request.create_client import CreateClientRequestModel
from serializers.request.task import TaskRequestModel
from serializers.response.create_client import ClientResponseModel, ClientsResponseModel
from serializers.response.task import TaskResponseModel

routes = APIRouter()
websocket_routes = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[dict] = []

    def get_connection_by_client_id(self, client_id: str):
        for con in self.active_connections:
            if con["client_id"] == client_id:
                return con["websocket"]
        return None

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()

        for conn in self.active_connections:
            if conn["client_id"] == client_id:
                raise WebSocketException(403, reason="Client with same conn_key already connected")

        self.active_connections.append({"websocket": websocket, "client_id": client_id})
        logger.info("WS_CONNECTED: " + client_id)

    async def disconnect(self, websocket: WebSocket, client_id: str, reason: str):
        try:
            await websocket.close(reason=reason)
        except (WebSocketDisconnect, WebSocketException, RuntimeError):
            pass

        try:
            self.active_connections.remove({"websocket": websocket, "client_id": client_id})
        except ValueError:
            pass

        logger.info("WS_DISCONNECTED: " + client_id)

    async def send_personal_message(self, message: str, client_id: str):
        websocket = self.get_connection_by_client_id(client_id)
        if not websocket:
            raise WebsocketError(message="Client is not connected")
        await websocket.send_text(message)
        logger.info("WS_SENT: " + client_id + ": " + message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


# MAINTAINCE ROUTES
@routes.post("/client", response_model=ClientResponseModel)
async def create_client(request_model: CreateClientRequestModel, db: AsyncSession = Depends(get_db)):
    return await CreateClient(request_model, db).process()


@routes.post("/client/{client_external_id}/deactivate")
async def deactivate_client(client_external_id: str, db: AsyncSession = Depends(get_db)):
    return await ChangeActivationClient(False, client_external_id, db).process()


@routes.post("/client/{client_external_id}/activate")
async def activate_client(client_external_id: str, db: AsyncSession = Depends(get_db)):
    return await ChangeActivationClient(True, client_external_id, db).process()


@routes.get("/client", response_model=ClientsResponseModel)
async def get_clients(db: AsyncSession = Depends(get_db), offset: int = 0, limit: int = 100):
    return await GetClient(db, offset=offset, limit=limit).process()


@routes.get("/client/{client_external_id}", response_model=ClientResponseModel)
async def get_client(client_external_id: str, db: AsyncSession = Depends(get_db)):
    return await GetClient(db, client_external_id=client_external_id).process()


@routes.get("/clients/{client_external_id}/connection_key")
async def get_client_key(client_external_id: str, db: AsyncSession = Depends(get_db)):
    client: Client = await GetClient(db, client_external_id=client_external_id).process()
    return client.cashbox_connection_key


@routes.post("/clients/{client_external_id}/task")
async def send_task(client_external_id: str, task: TaskRequestModel, db: AsyncSession = Depends(get_db)):
    client: Client = await GetClient(db, client_external_id=client_external_id).process()
    if not client.is_active:
        raise ForbiddenError(message="Client is not active")
    task_number = await CreateTask(task, client.id, db).process()
    task_msg = task.dict()
    task_msg.update({"number": task_number})
    try:
        await manager.send_personal_message(json.dumps(task_msg), client.cashbox_connection_key)
    except Exception as exp:
        await ErrorTask(task_number, str(exp), db).process()
        raise exp
    return task_msg


@routes.get("/task/{number}", response_model=TaskResponseModel)
async def get_task(number: str, db: AsyncSession = Depends(get_db)):
    return await GetTask(number, db).process()


# CLIENT ROUTES
@websocket_routes.websocket("/task/{cashbox_connection_key}")
async def websocket_endpoint(websocket: WebSocket, cashbox_connection_key: str, db: AsyncSession = Depends(get_db)):
    try:
        await manager.connect(websocket, cashbox_connection_key)

        client: Client = await GetClientByCashboxKey(cashbox_connection_key, db).process()
        if not client:
            raise WebSocketException(403, reason="Client not found")

        while True:
            data = await websocket.receive_text()
            logger.info("WS_RECEIVED: " + cashbox_connection_key + ": " + data)
            try:
                data_dict = json.loads(data)
                if "number" and "status" in data_dict:
                    if data_dict["status"] == "success":
                        await SuccessTask(data_dict["number"], data_dict["data"], db).process()
                    elif data_dict["status"] == "error":
                        error = TaskError(message=data_dict["data"])
                        await ErrorTask(data_dict["number"], str(error), db).process()
            except Exception as exp:
                logger.error(exp)

    except (WebSocketException, WebSocketDisconnect) as e:
        logger.error(e)
        await manager.disconnect(websocket, cashbox_connection_key, reason=e.reason)
