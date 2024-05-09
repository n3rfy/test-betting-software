
from sqlalchemy import select
from sqlalchemy.exc import DBAPIError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import InterfaceError

from src.bets.domain.bet import Bet
from src.bets.domain.bet import BetAlreadyExists
from src.bets.domain.bet import BetRegistry
from src.bets.domain.bet import BetRegistryIsUnavailable
from src.bets.infrastructure.database import DatabaseSession


class PostgreSQLBetRegistry(BetRegistry):
    def __init__(self, database_session: DatabaseSession) -> None:
        self._database_session = database_session

    async def add(self, bet: Bet) -> None:
        try:
            self._database_session.add(bet)
            await self._database_session.flush()
        except IntegrityError as exc:
            raise BetAlreadyExists from exc

    async def get(self) -> list[Bet]:
        try:
            orders = (
                await self._database_session.execute(statement=select(Bet))
            ).scalars().all()
        except (InterfaceError, DBAPIError) as exc:
            raise BetRegistryIsUnavailable from exc
        return list(orders)
