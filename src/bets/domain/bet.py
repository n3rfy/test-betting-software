import abc
import uuid
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import List

from src.bets.domain.event import Event


class IncorrectBetAmount(Exception):
    pass


@dataclass
class Bet:
    id: uuid.UUID
    amount: Decimal
    created_at: datetime
    event: Event

    def __post_init__(self):
        if self.amount <= 0:
            raise IncorrectBetAmount


class BetRegistryIsUnavailable(Exception):
    pass


class BetAlreadyExists(Exception):
    pass


class BetRegistry(abc.ABC):
    @abc.abstractmethod
    async def add(self, bet: Bet) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def get(self) -> List[Bet]:
        raise NotImplementedError
