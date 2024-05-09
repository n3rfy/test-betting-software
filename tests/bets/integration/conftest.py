import pytest
import testing.postgresql
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import clear_mappers

from src.api.di import DependencyProvider
from src.bets.infrastructure.database import Base
from src.bets.infrastructure.database import DatabaseConfiguration
from src.bets.infrastructure.database import DatabaseSession
from src.bets.infrastructure.database.orm.bet import start_mapper as start_bet_mapper
from src.bets.infrastructure.database.orm.event import start_mapper as start_event_mapper


@pytest.fixture(scope='package')
def postgresql():
    postgresql = testing.postgresql.Postgresql()
    yield postgresql
    postgresql.stop()


@pytest.fixture(scope='function')
async def di_provider(postgresql: testing.postgresql.Postgresql):
    dsn = postgresql.dsn()
    database_config = DatabaseConfiguration(
        dsn=f'postgresql+asyncpg://{dsn["user"]}@{dsn["host"]}:{dsn["port"]}/{dsn["database"]}',
    )
    return DependencyProvider(
        database_configuration=database_config,
    )


@pytest.fixture(scope='function')
async def database_session(di_provider: DependencyProvider):
    engine = di_provider.get_database_engine()
    async with DatabaseSession(bind=engine) as db_session:
        yield db_session


@pytest.fixture(scope='function')
async def create_tables(di_provider: DependencyProvider):
    engine: AsyncEngine = di_provider.get_database_engine()
    async with engine.connect() as connection:
        await connection.run_sync(Base.metadata.create_all)
        await connection.commit()
    start_event_mapper()
    start_bet_mapper()
    yield
    async with engine.connect() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.commit()
    clear_mappers()
