from firebase_admin import messaging
from firebase_admin.exceptions import FirebaseError

from src.db.models.consts import MailAndPushSentStatus
from src.db.models.notification import Notification
from src.kafka.pushes.schems import SendPushMsg
from src.repositories.device import DeviceRepository
from src.repositories.notification import NotificationRepository


class NotificationService:
    def __init__(self, notification_repository: NotificationRepository, device_repository: DeviceRepository):
        self.notification_repository = notification_repository
        self.device_repository = device_repository

    async def send_push(self, push_data: SendPushMsg) -> MailAndPushSentStatus:
        devices = await self.device_repository.get_list(user_id=push_data.to_user)
        try:
            messages = [
                messaging.Message(
                    notification=messaging.Notification(
                        title=push_data.title,
                        body=push_data.body,
                    ),
                    token=device.fcm_token,
                )
                for device in devices
            ]
            resp = messaging.send_each(messages)
            if resp.success_count != len(devices):
                status = MailAndPushSentStatus.FAILED
            else:
                status = MailAndPushSentStatus.SENT
                push = Notification(
                    user_id=push_data.to_user, status=status, title=push_data.title, body=push_data.body
                )
                await self.notification_repository.create(push)
        except FirebaseError:
            status = MailAndPushSentStatus.FAILED
        return status
