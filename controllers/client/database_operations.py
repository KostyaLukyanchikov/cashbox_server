from datetime import datetime

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.client import Client


async def create_client_in_db(db: AsyncSession, client_data: dict):
    now = datetime.now()
    query = insert(Client).values(
        {
            Client.external_id: client_data["external_id"],
            Client.name: client_data["name"],
            Client.is_active: True,
            Client.create_date: now,
            Client.activate_date: now,
            Client.deactivate_date: None,
            Client.cashbox_connection_key: client_data["cashbox_connection_key"],
        }
    )
    await db.execute(query)
    await db.commit()
    return await get_client_by_external_id_from_db(db, client_data["external_id"])


async def get_clients_from_db(db: AsyncSession, offset=0, limit=100):
    query = select(Client).offset(offset).limit(limit)
    result = (await db.execute(query)).unique().scalars().all()
    return result


async def get_client_by_external_id_from_db(db: AsyncSession, client_external_id):
    query = select(Client).filter(Client.external_id == client_external_id)
    result = (await db.execute(query)).unique().scalars().first()
    return result


async def get_client_by_cashbox_connection_key_from_db(db: AsyncSession, cashbox_conenction_key):
    query = select(Client).filter(Client.cashbox_connection_key == cashbox_conenction_key)
    result = (await db.execute(query)).unique().scalars().first()
    return result


async def change_client_activation_in_db(db: AsyncSession, client_external_id: str, is_active: bool):
    query = update(Client).where(Client.external_id == client_external_id).values({Client.is_active: is_active})
    result = await db.execute(query)
    await db.commit()
    return result
