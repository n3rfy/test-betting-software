from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine

from src.bets.application.change_event_status import ChangeEventStatusCommandHandler
from src.bets.application.create_bet import CreateBetCommandHandler
from src.bets.application.create_event import CreateEventCommandHandler
from src.bets.application.get_bets import GetBetsCommandHandler
from src.bets.domain.bet import BetRegistry
from src.bets.domain.event import EventRegistry
from src.bets.infrastructure.bet_registry import PostgreSQLBetRegistry
from src.bets.infrastructure.database import DatabaseConfiguration
from src.bets.infrastructure.database import DatabaseSession
from src.bets.infrastructure.event_registry import PostgreSQLEventRegistry


def stub():
    def void():
        ...

    return void


database_engine_stub = stub()
database_session_stub = stub()
CreateBetCommandHandlerStub = stub()
GetBetsCommandHandlerStub = stub()
CreateEventCommandHandlerStub = stub()
ChangeEventStatusCommandHandlerStub = stub()


class DependencyProvider:
    def __init__(
            self,
            database_configuration: DatabaseConfiguration,
    ) -> None:
        self._database_engine = create_async_engine(
            url=database_configuration.dsn,
            future=True
        )

    def get_database_engine(self):
        return self._database_engine

    @staticmethod
    async def get_database_session(
            db_engine: database_engine_stub = Depends()
    ):
        async with DatabaseSession(bind=db_engine) as session:
            yield session

    @staticmethod
    def get_event_registry(
            database_session: database_session_stub = Depends(),
    ) -> EventRegistry:
        return PostgreSQLEventRegistry(
            database_session=database_session
        )

    @staticmethod
    def get_bet_registry(
            database_session: database_session_stub = Depends(),
    ) -> BetRegistry:
        return PostgreSQLBetRegistry(
            database_session=database_session
        )

    @staticmethod
    def get_create_event_command_handler(
            event_registry: EventRegistry = Depends(),
            database_session: database_session_stub = Depends(),
    ) -> CreateEventCommandHandler:
        return CreateEventCommandHandler(
            event_registry=event_registry,
            database_session=database_session,
        )

    @staticmethod
    def get_change_event_status_command_handler(
            event_registry: EventRegistry = Depends(),
            database_session: database_session_stub = Depends(),
    ) -> ChangeEventStatusCommandHandler:
        return ChangeEventStatusCommandHandler(
            event_registry=event_registry,
            database_session=database_session,
        )

    @staticmethod
    def get_create_bet_command_handler(
            event_registry: EventRegistry = Depends(),
            bet_registry: BetRegistry = Depends(),
            database_session: database_session_stub = Depends(),
    ) -> CreateBetCommandHandler:
        return CreateBetCommandHandler(
            event_registry=event_registry,
            bet_registry=bet_registry,
            database_session=database_session,
        )

    @staticmethod
    def get_get_bets_command_handler(
            bet_registry: BetRegistry = Depends(),
            database_session: database_session_stub = Depends(),
    ) -> GetBetsCommandHandler:
        return GetBetsCommandHandler(
            bet_registry=bet_registry,
            database_session=database_session,
        )
