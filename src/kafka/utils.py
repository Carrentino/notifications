from functools import lru_cache

from src.repositories.device import DeviceRepository
from src.repositories.notification import NotificationRepository
from src.services.notification import NotificationService


@lru_cache
def get_notifications_repository(pushes_listener):
    return NotificationService(
        NotificationRepository(pushes_listener.db_client.get_session()),
        DeviceRepository(pushes_listener.db_client.get_session()),
    )
