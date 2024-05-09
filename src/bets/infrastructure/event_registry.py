from typing import cast
from uuid import UUID

from sqlalchemy.exc import DBAPIError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import InterfaceError

from src.bets.domain.event import Event
from src.bets.domain.event import EventAlreadyExists
from src.bets.domain.event import EventNotFound
from src.bets.domain.event import EventRegistry
from src.bets.domain.event import EventRegistryIsUnavailable
from src.bets.infrastructure.database import DatabaseSession


class PostgreSQLEventRegistry(EventRegistry):
    def __init__(self, database_session: DatabaseSession) -> None:
        self._database_session = database_session

    async def get(self, id: UUID) -> Event:
        try:
            event = await self._database_session.get(Event, id)
        except (InterfaceError, DBAPIError) as exc:
            raise EventRegistryIsUnavailable from exc
        if event is None:
            raise EventNotFound
        return cast(Event, event)

    async def add(self, event: Event) -> None:
        try:
            self._database_session.add(event)
            await self._database_session.flush()
        except IntegrityError as exc:
            raise EventAlreadyExists from exc
