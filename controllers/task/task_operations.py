import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import NotFoundError
from controllers.task.database_operations import (
    create_task_in_db,
    get_task_by_number_from_db,
    change_task_status_in_db,
)
from db.models.task import TaskStatusEnum
from serializers.request.task import TaskRequestModel


class CreateTask:
    def __init__(self, task: TaskRequestModel, client_id: int, db: AsyncSession):
        self.task: TaskRequestModel = task
        self.db = db
        self.client_id = client_id

    async def process(self):
        number = self.generate_task_number()
        task_data = {
            "data": self.task.json(),
            "clientId": self.client_id,
            "number": number,
        }
        await create_task_in_db(self.db, task_data)
        return number

    def generate_task_number(self):
        return f"TASK-{self.client_id}-{uuid.uuid4()}"


class GetTask:
    def __init__(self, task_number: str, db: AsyncSession):
        self.db = db
        self.task_number = task_number

    async def process(self):
        task = await get_task_by_number_from_db(self.db, self.task_number)
        if not task:
            raise NotFoundError(detail=f"Task was not found with number {self.task_number}")
        return task


class SuccessTask:
    def __init__(self, task_number: str, message: str, db: AsyncSession):
        self.task_number: str = task_number
        self.message: str = message
        self.db = db

    async def process(self):
        if not await get_task_by_number_from_db(self.db, self.task_number):
            raise NotFoundError(detail=f"Task was not found by number {self.task_number}")
        await change_task_status_in_db(self.db, self.task_number, TaskStatusEnum.SUCCESS.value, self.message)


class ErrorTask:
    def __init__(self, task_number: str, error_detail: str, db: AsyncSession):
        self.task_number: str = task_number
        self.error_detail = error_detail
        self.db = db

    async def process(self):
        if not await get_task_by_number_from_db(self.db, self.task_number):
            raise NotFoundError(detail=f"Task was not found by number {self.task_number}")
        await change_task_status_in_db(self.db, self.task_number, TaskStatusEnum.ERROR.value, self.error_detail)
