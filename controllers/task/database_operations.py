from datetime import datetime
from typing import Optional

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.task import TaskStatusEnum, Task


async def create_task_in_db(db: AsyncSession, task_data: dict):
    now = datetime.now()
    query = insert(Task).values(
        {
            Task.number: task_data["number"],
            Task.create_date: now,
            Task.data: task_data["data"],
            Task.client_id: task_data["clientId"],
            Task.status: TaskStatusEnum.IN_PROGRESS.value,
        }
    )
    result = await db.execute(query)
    await db.commit()
    return result


async def get_task_by_number_from_db(db: AsyncSession, task_number: str):
    query = select(Task).filter(Task.number == task_number)
    result = (await db.execute(query)).unique().scalars().first()
    return result


async def change_task_status_in_db(
    db: AsyncSession, task_number: str, status: TaskStatusEnum, status_message: Optional[str] = None
):
    query = (
        update(Task)
        .where(Task.number == task_number)
        .values({Task.status: status, Task.status_message: status_message})
    )
    result = await db.execute(query)
    await db.commit()
    return result
