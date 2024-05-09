from sqlalchemy.orm import relationship

from src.bets.domain.bet import Bet
from src.bets.domain.event import Event
from src.bets.infrastructure.database.base import Base
from src.bets.infrastructure.database.tables import bet_table


def start_mapper() -> None:
    Base.registry.map_imperatively(
        class_=Bet,
        local_table=bet_table,
        properties=dict(
            id=bet_table.c.id,
            amount=bet_table.c.amount,
            created_at=bet_table.c.created_at,
            event=relationship(Event, lazy='selectin'),
        ),
        always_refresh=True
    )
