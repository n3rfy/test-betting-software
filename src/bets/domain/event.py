import abc
import enum
from datetime import datetime
from uuid import UUID


class EventStatus(enum.Enum):
    PENDING = 'PENDING'
    WIN = 'WIN'
    LOSE = 'LOSE'


class StatusAlreadyIsFinal(Exception):
    pass


class Event:
    def __init__(
            self,
            id: UUID,
            status: EventStatus,
            created_at: datetime,
    ) -> None:
        self._id = id
        self._created_at = created_at
        self._status = status

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def status(self) -> EventStatus:
        return self._status

    @property
    def created_at(self) -> datetime:
        return self._created_at

    def has_final_status(self) -> bool:
        if self._status in (EventStatus.WIN, EventStatus.LOSE):
            return True
        return False

    def win(self):
        if self.has_final_status():
            raise StatusAlreadyIsFinal
        self._status = EventStatus.WIN

    def lose(self):
        if self.has_final_status():
            raise StatusAlreadyIsFinal
        self._status = EventStatus.LOSE


class EventRegistryIsUnavailable(Exception):
    pass


class EventNotFound(Exception):
    pass


class EventAlreadyExists(Exception):
    pass


class EventRegistry(abc.ABC):
    @abc.abstractmethod
    async def get(self, id: UUID) -> Event:
        raise NotImplementedError

    @abc.abstractmethod
    async def add(self, event: Event) -> None:
        raise NotImplementedError
