from helpers.sqlalchemy.base_repo import ISqlAlchemyRepository
from sqlalchemy import select, and_

from src.db.models.device import Device


class DeviceRepository(ISqlAlchemyRepository[Device]):
    _model = Device

    async def create_or_update(self, device: Device):
        existing_device = await self.session.execute(
            select(Device).where(and_(Device.user_id == device.user_id, Device.device_type == device.device_type))
        )
        existing_device = existing_device.scalar_one_or_none()
        if existing_device:
            await self.update(existing_device.id, fcm_token=existing_device.fcm_token)
        else:
            await self.create(device)
