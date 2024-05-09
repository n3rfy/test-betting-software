import pytest
import testing.postgresql
from httpx import ASGITransport
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import clear_mappers

from src.api.application import create_application
from src.api.di import DependencyProvider
from src.bets.infrastructure.database import Base
from src.bets.infrastructure.database import DatabaseConfiguration
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
async def create_trigger_table(di_provider: DependencyProvider):
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


@pytest.fixture(scope='function')
async def test_client(di_provider: DependencyProvider):
    application = create_application(dependency_provider=di_provider)
    async with AsyncClient(
            base_url='http://test',
            transport=ASGITransport(app=application),
    ) as client:
        yield client
