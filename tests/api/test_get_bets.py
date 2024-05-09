import httpx
from httpx import AsyncClient


async def test_correct_get_bets(
        test_client: AsyncClient,
        create_trigger_table,
):
    response = await test_client.get(url='bets/')
    assert response.status_code == httpx.codes.OK
    assert len(response.json()['bets']) == 0

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
