from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.config_loader import config


def database_configuration() -> str:
    return "{drivername}://{user}:{password}@{host}:{port}/{database}".format(
        drivername="postgresql+asyncpg",
        user=config.DB_LOGIN,
        password=config.DB_PASSWORD,
        host=config.DB_HOST,
        port=config.DB_PORT,
        database=config.DB_DATABASE,
    )


engine = create_async_engine(
    database_configuration(),
    pool_pre_ping=True,
    pool_recycle=3600,
    pool_size=5,
    max_overflow=5,
    connect_args={
        "command_timeout": 60,
    },
)

async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)
