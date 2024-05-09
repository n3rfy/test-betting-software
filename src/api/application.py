import traceback

import fastapi
import structlog
from fastapi.requests import Request

from src.api.di import ChangeEventStatusCommandHandlerStub
from src.api.di import CreateBetCommandHandlerStub
from src.api.di import CreateEventCommandHandlerStub
from src.api.di import DependencyProvider
from src.api.di import GetBetsCommandHandlerStub
from src.api.di import database_engine_stub
from src.api.di import database_session_stub
from src.api.error_message import InternalServerErrorMessage
from src.api.handlers import bet
from src.api.handlers import event
from src.bets.domain.bet import BetRegistry
from src.bets.domain.event import EventRegistry
from src.bets.infrastructure import struct_logging
from src.bets.infrastructure.database.orm.bet import start_mapper as start_bet_mapper
from src.bets.infrastructure.database.orm.event import start_mapper as start_event_mapper


logger: structlog.stdlib.BoundLogger = structlog.get_logger()


async def startup():
    struct_logging.setup_logging()
    start_bet_mapper()
    start_event_mapper()
    logger.info('APPLICATION_STARTED')


async def shutdown():
    logger.info('APPLICATION_STOPPED')


def exception_handler(_: Request, exception: Exception):
    exception_name = type(exception).__name__
    logger.error(
        'UNHANDLED_EXCEPTION',
        message=f'Необработанное исключение {exception_name}',
        exception=exception_name,
        traceback=traceback.format_tb(exception.__traceback__),
    )
    return InternalServerErrorMessage.to_response()


def create_application(dependency_provider: DependencyProvider) -> fastapi.FastAPI:
    application = fastapi.FastAPI(
        title='Bet Maker',
        version='0.0.1',
    )

    application.on_event('startup')(startup)
    application.on_event('shutdown')(shutdown)

    application.exception_handler(Exception)(exception_handler)

    application.include_router(bet.router)
    application.include_router(event.router)

    application.dependency_overrides = {
        database_engine_stub: dependency_provider.get_database_engine,
        database_session_stub: dependency_provider.get_database_session,
        EventRegistry: dependency_provider.get_event_registry,
        BetRegistry: dependency_provider.get_bet_registry,
        CreateEventCommandHandlerStub: dependency_provider.get_create_event_command_handler,
        ChangeEventStatusCommandHandlerStub: dependency_provider.get_change_event_status_command_handler,
        CreateBetCommandHandlerStub: dependency_provider.get_create_bet_command_handler,
        GetBetsCommandHandlerStub: dependency_provider.get_get_bets_command_handler,
    }
    return application
