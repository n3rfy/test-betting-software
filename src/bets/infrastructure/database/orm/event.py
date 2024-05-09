from src.bets.domain.event import Event
from src.bets.infrastructure.database.base import Base
from src.bets.infrastructure.database.tables import event_table


def start_mapper() -> None:
    Base.registry.map_imperatively(
        class_=Event,
        local_table=event_table,
        properties={
            '_id': event_table.c.id,
            '_created_at': event_table.c.created_at,
            '_status': event_table.c.status,
        },
        always_refresh=True,
    )
