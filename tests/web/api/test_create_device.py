from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.db.models.device import Device


async def test_create_device(auth_client: AsyncClient, session: AsyncSession):
    data = {'device_type': 'ios', 'fcm_token': 'bimbimbambam'}
    response = await auth_client.post('api/v1/devices/', json=data)
    assert response.status_code == status.HTTP_201_CREATED
    device = await session.execute(select(Device).where(Device.fcm_token == data['fcm_token']))
    device = device.scalars().first()
    assert device.fcm_token == data['fcm_token']
