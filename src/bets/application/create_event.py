from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from src.bets.domain.event import Event
from src.bets.domain.event import EventAlreadyExists
from src.bets.domain.event import EventRegistry
from src.bets.domain.event import EventStatus
from src.bets.infrastructure.database import DatabaseSession


@dataclass
class CreateEventCommand:
    event_id: UUID


class CreateEventCommandHandler:
    def __init__(
            self,
            event_registry: EventRegistry,
            database_session: DatabaseSession
    ):
        self._event_registry = event_registry
        self._database_session = database_session

    async def handle(self, command: CreateEventCommand) -> None:
        async with self._database_session.begin():
            event = Event(
                id=command.event_id,
                status=EventStatus.PENDING,
                created_at=datetime.utcnow()
            )
            try:
                await self._event_registry.add(event)
            except EventAlreadyExists:
                await self._database_session.rollback()
            else:
                await self._database_session.commit()
