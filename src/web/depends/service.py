from fastapi.params import Depends
from typing import Annotated

from src.integrations.users import UsersClient
from src.repositories.device import DeviceRepository
from src.repositories.mail import MailRepository
from src.repositories.notification import NotificationRepository
from src.services.device import DeviceService
from src.services.mail import MailService
from src.services.notification import NotificationService
from src.web.depends.integrations import get_users_client
from src.web.depends.repository import get_device_repository, get_notification_repository, get_mail_repository


async def get_device_service(
    device_repository: Annotated[DeviceRepository, Depends(get_device_repository)]
) -> DeviceService:
    return DeviceService(device_repository)


async def get_notification_service(
    notification_repository: Annotated[NotificationRepository, Depends(get_notification_repository)],
    device_repository: Annotated[DeviceRepository, Depends(get_device_repository)],
) -> NotificationService:
    return NotificationService(notification_repository, device_repository)


async def get_mail_service(
    mail_repository: Annotated[MailRepository, Depends(get_mail_repository)],
    users_client: Annotated[UsersClient, Depends(get_users_client)],
) -> MailService:
    return MailService(mail_repository, users_client)
