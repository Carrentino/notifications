from helpers.depends.db_session import get_db_session_context
from helpers.kafka.consumer import KafkaConsumerTopicsListeners

from src.kafka.db_client import make_db_client
from src.kafka.pushes.schems import SendPushMsg
from src.repositories.device import DeviceRepository
from src.repositories.notification import NotificationRepository
from src.web.depends.service import get_notification_service

pushes_listener = KafkaConsumerTopicsListeners()


@pushes_listener.add('notifications_pushes', SendPushMsg)
async def send_push(message: SendPushMsg) -> None:
    async with get_db_session_context(make_db_client()) as session:
        notifications_service = await get_notification_service(
            NotificationRepository(session=session), DeviceRepository(session=session)
        )
        await notifications_service.send_push(message)
