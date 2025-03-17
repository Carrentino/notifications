from uuid import UUID

from src.db.models.device import Device
from src.repositories.device import DeviceRepository
from src.web.api.devices.schemas import CreateDeviceReq


class DeviceService:
    def __init__(self, device_repository: DeviceRepository):
        self.device_repository = device_repository

    async def create_device(self, device_data: CreateDeviceReq, user_id: UUID):
        device = Device(**device_data.model_dump(), user_id=user_id)
        await self.device_repository.create_or_update(device)
