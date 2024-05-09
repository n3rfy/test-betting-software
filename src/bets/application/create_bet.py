from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from src.bets.domain.bet import Bet
from src.bets.domain.bet import BetAlreadyExists
from src.bets.domain.bet import BetRegistry
from src.bets.domain.bet import IncorrectBetAmount
from src.bets.domain.event import EventNotFound
from src.bets.domain.event import EventRegistry
from src.bets.infrastructure.database import DatabaseSession


class EventNotFoundError(Exception):
    pass


class EventStatusAlreadyIsFinalError(Exception):
    pass


class IncorrectBetAmountError(Exception):
    pass


@dataclass
class CreateBetCommand:
    bet_id: UUID
    event_id: UUID
    bet_amount: Decimal


class CreateBetCommandHandler:
    def __init__(
            self,
            bet_registry: BetRegistry,
            event_registry: EventRegistry,
            database_session: DatabaseSession,
    ):
        self._event_registry = event_registry
        self._bet_registry = bet_registry
        self._database_session = database_session

    async def handle(self, command: CreateBetCommand) -> None:
        async with self._database_session.begin():
            try:
                event = await self._event_registry.get(id=command.event_id)
            except EventNotFound as exc:
                raise EventNotFoundError from exc
            if event.has_final_status():
                raise EventStatusAlreadyIsFinalError

            try:
                bet = Bet(
                    id=command.bet_id,
                    amount=command.bet_amount,
                    created_at=datetime.utcnow(),
                    event=event,
                )
            except IncorrectBetAmount as exc:
                raise IncorrectBetAmountError from exc

            try:
                await self._bet_registry.add(bet)
            except BetAlreadyExists:
                await self._database_session.rollback()
            else:
                await self._database_session.commit()
