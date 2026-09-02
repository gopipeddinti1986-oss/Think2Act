from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker
)

from sqlalchemy.orm import declarative_base
from sqlalchemy.engine import make_url

from app.core.config import settings


# Get database URL from environment
database_url = settings.DATABASE_URL

# Extra connection settings
connect_args = {}

# Configure PostgreSQL + asyncpg
if database_url.startswith("postgresql+asyncpg://"):

    url = make_url(database_url)

    # Remove parameters that asyncpg does not accept
    url = url.difference_update_query(
        ["sslmode", "channel_binding"]
    )

    database_url = url

    # Neon requires SSL
    connect_args = {
        "ssl": "require"
    }


# Create database engine
engine = create_async_engine(
    database_url,
    echo=False,
    future=True,
    connect_args=connect_args
)


# Create database sessions
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


# Base class for database models
Base = declarative_base()


# Database dependency
async def get_db():

    async with AsyncSessionLocal() as session:

        try:
            yield session

        finally:
            await session.close()