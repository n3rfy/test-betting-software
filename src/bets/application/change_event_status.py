from dataclasses import dataclass
from uuid import UUID

from src.bets.domain.event import EventNotFound
from src.bets.domain.event import EventRegistry
from src.bets.domain.event import EventStatus
from src.bets.domain.event import StatusAlreadyIsFinal
from src.bets.infrastructure.database import DatabaseSession


class EventNotFoundError(Exception):
    pass


class EventStatusAlreadyIsFinalError(Exception):
    pass


class EventStatusIsNotPendingError(Exception):
    pass


@dataclass
class ChangeEventStatusCommand:
    event_id: UUID
    event_status: EventStatus


class ChangeEventStatusCommandHandler:
    def __init__(
            self,
            event_registry: EventRegistry,
            database_session: DatabaseSession
    ):
        self._event_registry = event_registry
        self._database_session = database_session

    async def handle(self, command: ChangeEventStatusCommand) -> None:
        async with self._database_session.begin():
            try:
                event = await self._event_registry.get(command.event_id)
            except EventNotFound:
                raise EventNotFoundError
            try:
                if command.event_status is EventStatus.WIN:
                    event.win()
                elif command.event_status is EventStatus.LOSE:
                    event.lose()
                else:
                    raise EventStatusIsNotPendingError
            except StatusAlreadyIsFinal:
                raise EventStatusAlreadyIsFinalError
            await self._database_session.commit()
