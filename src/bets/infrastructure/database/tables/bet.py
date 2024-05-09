from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Numeric
from sqlalchemy import Table
from sqlalchemy import UUID

from src.bets.infrastructure.database.base import Base


bet_table = Table(
    'bet',
    Base.metadata,
    Column('id', UUID, primary_key=True),
    Column('event_id', UUID, ForeignKey('event.id'), nullable=False),
    Column('amount', Numeric(precision=10, scale=2), nullable=False),
    Column('created_at', DateTime, nullable=False),
)
