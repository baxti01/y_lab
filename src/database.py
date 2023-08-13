from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from src.settings import settings

DATABASE_URL = f'postgresql+asyncpg://' \
               f'{settings.postgres_user}:{settings.postgres_password}@' \
               f'{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}'

engine = create_async_engine(
    url=DATABASE_URL
)

async_session = async_sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False
)

Base = declarative_base()


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
