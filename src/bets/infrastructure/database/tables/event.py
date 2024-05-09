from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import Table
from sqlalchemy import UUID

from src.bets.domain.event import EventStatus
from src.bets.infrastructure.database.base import Base


event_table = Table(
    'event',
    Base.metadata,
    Column('id', UUID, primary_key=True),
    Column('status', Enum(EventStatus), nullable=False),
    Column('created_at', DateTime, nullable=False),
)
