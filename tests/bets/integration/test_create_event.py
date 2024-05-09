from uuid import UUID

from sqlalchemy import text

from src.bets.application.create_event import CreateEventCommand
from src.bets.application.create_event import CreateEventCommandHandler
from src.bets.domain.event import EventStatus
from src.bets.infrastructure.database import DatabaseSession
from src.bets.infrastructure.event_registry import PostgreSQLEventRegistry


async def test_correct_create_event(
        database_session: DatabaseSession,
        create_tables,
):
    create_event_command_handler = CreateEventCommandHandler(
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


async def test_idempotence_create_event(
        database_session: DatabaseSession,
        create_tables,
):
    create_event_command_handler = CreateEventCommandHandler(
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

    await create_event_command_handler.handle(
        command=CreateEventCommand(event_id=UUID('3fa85f64-5717-4562-b3fc-2c963f66afa6')),
    )
    async with database_session.begin():
        event_data = (await database_session.execute(
            statement=text('select id, status from event'),
        )).mappings().one()
    assert event_data['id'] == UUID('3fa85f64-5717-4562-b3fc-2c963f66afa6')
    assert event_data['status'] == EventStatus.PENDING.value
