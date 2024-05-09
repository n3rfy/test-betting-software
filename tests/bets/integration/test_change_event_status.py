from uuid import UUID

import pytest
from sqlalchemy import text

from src.bets.application.change_event_status import ChangeEventStatusCommand
from src.bets.application.change_event_status import ChangeEventStatusCommandHandler
from src.bets.application.change_event_status import EventNotFoundError
from src.bets.application.change_event_status import EventStatusAlreadyIsFinalError
from src.bets.application.change_event_status import EventStatusIsNotPendingError
from src.bets.application.create_event import CreateEventCommand
from src.bets.application.create_event import CreateEventCommandHandler
from src.bets.domain.event import EventStatus
from src.bets.infrastructure.database import DatabaseSession
from src.bets.infrastructure.event_registry import PostgreSQLEventRegistry


async def test_correct_change_event_status(
        database_session: DatabaseSession,
        create_tables,
):
    create_event_command_handler = CreateEventCommandHandler(
        event_registry=PostgreSQLEventRegistry(
            database_session=database_session,
        ),
        database_session=database_session,
    )
    change_event_status_command_handler = ChangeEventStatusCommandHandler(
        event_registry=PostgreSQLEventRegistry(
            database_session=database_session,
        ),
        database_session=database_session,
    )

    await create_event_command_handler.handle(
        command=CreateEventCommand(event_id=UUID('3fa85f64-5717-4562-b3fc-2c963f66afa6')),
    )

    async with database_session.begin():
        event_data = (await database_session.execute(
            statement=text('select id, status from event'),
        )).mappings().one()
    assert event_data['id'] == UUID('3fa85f64-5717-4562-b3fc-2c963f66afa6')
    assert event_data['status'] == EventStatus.PENDING.value

    await change_event_status_command_handler.handle(
        command=ChangeEventStatusCommand(
            event_id=UUID('3fa85f64-5717-4562-b3fc-2c963f66afa6'),
            event_status=EventStatus.WIN,
        ),
    )
    async with database_session.begin():
        event_data = (await database_session.execute(
            statement=text('select id, status from event'),
        )).mappings().one()
    assert event_data['id'] == UUID('3fa85f64-5717-4562-b3fc-2c963f66afa6')
    assert event_data['status'] == EventStatus.WIN.value


async def test_change_event_status_if_status_is_final(
        database_session: DatabaseSession,
        create_tables,
):
    create_event_command_handler = CreateEventCommandHandler(
        event_registry=PostgreSQLEventRegistry(
            database_session=database_session,
        ),
        database_session=database_session,
    )
    change_event_status_command_handler = ChangeEventStatusCommandHandler(
        event_registry=PostgreSQLEventRegistry(
            database_session=database_session,
        ),
        database_session=database_session,
    )

    await create_event_command_handler.handle(
        command=CreateEventCommand(event_id=UUID('3fa85f64-5717-4562-b3fc-2c963f66afa6')),
    )

    async with database_session.begin():
        event_data = (await database_session.execute(
            statement=text('select id, status from event'),
        )).mappings().one()
    assert event_data['id'] == UUID('3fa85f64-5717-4562-b3fc-2c963f66afa6')
    assert event_data['status'] == EventStatus.PENDING.value

    await change_event_status_command_handler.handle(
        command=ChangeEventStatusCommand(
            event_id=UUID('3fa85f64-5717-4562-b3fc-2c963f66afa6'),
            event_status=EventStatus.WIN,
        ),
    )
    async with database_session.begin():
        event_data = (await database_session.execute(
            statement=text('select id, status from event'),
        )).mappings().one()
    assert event_data['id'] == UUID('3fa85f64-5717-4562-b3fc-2c963f66afa6')
    assert event_data['status'] == EventStatus.WIN.value

    with pytest.raises(EventStatusAlreadyIsFinalError):
        await change_event_status_command_handler.handle(
            command=ChangeEventStatusCommand(
                event_id=UUID('3fa85f64-5717-4562-b3fc-2c963f66afa6'),
                event_status=EventStatus.WIN,
            ),
        )


async def test_change_event_status_if_event_not_found(
        database_session: DatabaseSession,
        create_tables,
):
    change_event_status_command_handler = ChangeEventStatusCommandHandler(
        event_registry=PostgreSQLEventRegistry(
            database_session=database_session,
        ),
        database_session=database_session,
    )

    with pytest.raises(EventNotFoundError):
        await change_event_status_command_handler.handle(
            command=ChangeEventStatusCommand(
                event_id=UUID('3fa85f64-5717-4562-b3fc-2c963f66afa6'),
                event_status=EventStatus.WIN,
            ),
        )


async def test_change_event_status_if_event_not_not_pending(
        database_session: DatabaseSession,
        create_tables,
):
    create_event_command_handler = CreateEventCommandHandler(
        event_registry=PostgreSQLEventRegistry(
            database_session=database_session,
        ),
        database_session=database_session,
    )
    change_event_status_command_handler = ChangeEventStatusCommandHandler(
        event_registry=PostgreSQLEventRegistry(
            database_session=database_session,
        ),
        database_session=database_session,
    )

    await create_event_command_handler.handle(
        command=CreateEventCommand(event_id=UUID('3fa85f64-5717-4562-b3fc-2c963f66afa6')),
    )

    async with database_session.begin():
        event_data = (await database_session.execute(
            statement=text('select id, status from event'),
        )).mappings().one()
    assert event_data['id'] == UUID('3fa85f64-5717-4562-b3fc-2c963f66afa6')
    assert event_data['status'] == EventStatus.PENDING.value

    with pytest.raises(EventStatusIsNotPendingError):
        await change_event_status_command_handler.handle(
            command=ChangeEventStatusCommand(
                event_id=UUID('3fa85f64-5717-4562-b3fc-2c963f66afa6'),
                event_status=EventStatus.PENDING,
            ),
        )
