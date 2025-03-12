from fastapi.params import Depends
from typing import Annotated

from src.repositories.device import DeviceRepository
from src.repositories.notification import NotificationRepository
from src.services.device import DeviceService
from src.services.notification import NotificationService
from src.web.depends.repository import get_device_repository, get_notification_repository


async def get_device_service(
    device_repository: Annotated[DeviceRepository, Depends(get_device_repository)]
) -> DeviceService:
    return DeviceService(device_repository)


async def get_notification_service(
    notification_repository: Annotated[NotificationRepository, Depends(get_notification_repository)],
    device_repository: Annotated[DeviceRepository, Depends(get_device_repository)],
) -> NotificationService:
    return NotificationService(notification_repository, device_repository)
