from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.settings import settings

DATABASE_URL = f'postgresql+psycopg2://' \
               f'{settings.postgres_user}:{settings.postgres_password}@' \
               f'{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}'

engine = create_engine(
    url=DATABASE_URL
)

Session = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

Base = declarative_base()


def get_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()
