from sqlalchemy import Column, Integer, String, Boolean, DateTime

from db.models.base import Base


class Client(Base):
    __tablename__ = "client"

    id = Column(Integer, primary_key=True, autoincrement=True)  # noqa A003
    external_id = Column(String, unique=True)
    name = Column(String)
    is_active = Column(Boolean)
    create_date = Column(DateTime(timezone=False))
    activate_date = Column(DateTime(timezone=False))
    deactivate_date = Column(DateTime(timezone=False), nullable=True)
    cashbox_connection_key = Column(String, unique=True)
