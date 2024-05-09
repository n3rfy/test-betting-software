__all__ = ['DatabaseSession']


from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker


# noinspection PyTypeChecker
DatabaseSession: type[AsyncSession] = async_sessionmaker(
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)
