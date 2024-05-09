import httpx
from httpx import AsyncClient


async def test_correct_create_bet(
        test_client: AsyncClient,
        create_trigger_table,
):
    response = await test_client.post(
        url='events/',
        json={'event_id': '3fa85f64-5717-4562-b3fc-2c963f66afa6'},
    )
    assert response.status_code == httpx.codes.CREATED

    response = await test_client.post(
        url='bets/',
        json={
            'id': '3fa85f64-5717-4562-b3fc-2c963f66afa6',
            'amount': 1,
            'event_id': '3fa85f64-5717-4562-b3fc-2c963f66afa6',
        },
    )
    assert response.status_code == httpx.codes.CREATED

    response = await test_client.get(url='bets/')
    assert response.status_code == httpx.codes.OK
    assert len(response.json()['bets']) == 1


async def test_create_bet_without_event(
        test_client: AsyncClient,
        create_trigger_table,
):
    response = await test_client.post(
        url='bets/',
        json={
            'id': '3fa85f64-5717-4562-b3fc-2c963f66afa6',
            'amount': 1,
            'event_id': '3fa85f64-5717-4562-b3fc-2c963f66afa6',
        },
    )
    assert response.status_code == httpx.codes.BAD_REQUEST
    assert response.json()['code'] == 'EVENT_NOT_FOUND'


async def test_create_bet_on_event_with_final_status(
        test_client: AsyncClient,
        create_trigger_table,
):
    response = await test_client.post(
        url='events/',
        json={'event_id': '3fa85f64-5717-4562-b3fc-2c963f66afa6'},
    )
    assert response.status_code == httpx.codes.CREATED

    response = await test_client.put(
        url='events/3fa85f64-5717-4562-b3fc-2c963f66afa6',
        json={'status': 'WIN'},
    )
    assert response.status_code == httpx.codes.OK

    response = await test_client.post(
        url='bets/',
        json={
            'id': '3fa85f64-5717-4562-b3fc-2c963f66afa6',
            'amount': 1,
            'event_id': '3fa85f64-5717-4562-b3fc-2c963f66afa6',
        },
    )
    assert response.status_code == httpx.codes.BAD_REQUEST
    assert response.json()['code'] == 'EVENT_STATUS_ALREADY_IS_FINAL'
