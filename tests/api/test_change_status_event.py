import httpx
from httpx import AsyncClient


async def test_correct_change_status_event(
        test_client: AsyncClient,
        create_tables,
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


async def test_change_status_event_with_final_status(
        test_client: AsyncClient,
        create_tables,
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

    response = await test_client.put(
        url='events/3fa85f64-5717-4562-b3fc-2c963f66afa6',
        json={'status': 'WIN'},
    )
    assert response.status_code == httpx.codes.BAD_REQUEST
    assert response.json()['code'] == 'EVENT_STATUS_ALREADY_IS_FINAL'
