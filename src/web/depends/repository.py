from typing import Annotated

from fastapi import Depends
from helpers.depends.db_session import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.device import DeviceRepository
from src.repositories.notification import NotificationRepository


async def get_device_repository(session: Annotated[AsyncSession, Depends(get_db_session)]) -> DeviceRepository:
    return DeviceRepository(session=session)


async def get_notification_repository(
    session: Annotated[AsyncSession, Depends(get_db_session)]
) -> NotificationRepository:
    return NotificationRepository(session=session)
