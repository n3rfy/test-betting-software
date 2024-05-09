import httpx
from httpx import AsyncClient


async def test_correct_create_event(
        test_client: AsyncClient,
        create_tables,
):
    response = await test_client.post(
        url='events/',
        json={'event_id': '3fa85f64-5717-4562-b3fc-2c963f66afa6'},
    )
    assert response.status_code == httpx.codes.CREATED
