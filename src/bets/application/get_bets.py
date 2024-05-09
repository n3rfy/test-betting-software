from dataclasses import dataclass

from src.bets.domain.bet import Bet
from src.bets.domain.bet import BetRegistry
from src.bets.infrastructure.database import DatabaseSession


@dataclass
class GetBetsCommand:
    pass


class GetBetsCommandHandler:
    def __init__(
            self,
            bet_registry: BetRegistry,
            database_session: DatabaseSession,
    ):
        self._bet_registry = bet_registry
        self._database_session = database_session

    async def handle(self, _: GetBetsCommand) -> list[Bet]:
        async with self._database_session.begin():
            bets = await self._bet_registry.get()
            await self._database_session.commit()
        return bets
