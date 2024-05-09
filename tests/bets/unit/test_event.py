from datetime import datetime
from uuid import UUID

import pytest

from src.bets.domain.event import Event
from src.bets.domain.event import EventStatus
from src.bets.domain.event import StatusAlreadyIsFinal


def test_correct_change_status_to_win():
    event = Event(
        id=UUID('3fa85f64-5717-4562-b3fc-2c963f66afa6'),
        status=EventStatus.PENDING,
        created_at=datetime(2020, 1, 1),
    )

    event.win()

    assert event.status == EventStatus.WIN


def test_correct_change_status_to_lose():
    event = Event(
        id=UUID('3fa85f64-5717-4562-b3fc-2c963f66afa6'),
        status=EventStatus.PENDING,
        created_at=datetime(2020, 1, 1),
    )

    event.lose()

    assert event.status == EventStatus.LOSE


def test_change_status_if_status_already_is_final():
    event = Event(
        id=UUID('3fa85f64-5717-4562-b3fc-2c963f66afa6'),
        status=EventStatus.WIN,
        created_at=datetime(2020, 1, 1),
    )

    assert event.has_final_status() is True

    with pytest.raises(StatusAlreadyIsFinal):
        event.lose()
