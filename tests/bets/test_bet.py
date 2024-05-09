from datetime import datetime
from decimal import Decimal
from uuid import UUID

import pytest

from src.bets.domain.bet import Bet
from src.bets.domain.bet import IncorrectBetAmount
from src.bets.domain.event import Event
from src.bets.domain.event import EventStatus


def test_correct_bet():
    bet = Bet(
        id=UUID('3fa85f64-5717-4562-b3fc-2c963f66afa6'),
        amount=Decimal('1'),
        created_at=datetime(2020, 1, 2),
        event=Event(
            id=UUID('3fa85f64-5717-4562-b3fc-2c963f66afa5'),
            status=EventStatus.PENDING,
            created_at=datetime(2020, 1, 1),
        )
    )

    assert bet.id == UUID('3fa85f64-5717-4562-b3fc-2c963f66afa6')


def test_incorrect_bet_amount():
    with pytest.raises(IncorrectBetAmount):
        Bet(
            id=UUID('3fa85f64-5717-4562-b3fc-2c963f66afa6'),
            amount=Decimal('0'),
            created_at=datetime(2020, 1, 2),
            event=Event(
                id=UUID('3fa85f64-5717-4562-b3fc-2c963f66afa5'),
                status=EventStatus.PENDING,
                created_at=datetime(2020, 1, 1),
            )
        )
