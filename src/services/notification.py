from firebase_admin import messaging
from firebase_admin.exceptions import FirebaseError

from src.kafka.pushes.schems import SendPushMsg
from src.repositories.device import DeviceRepository
from src.repositories.notification import NotificationRepository


class NotificationService:
    def __init__(self, notification_repository: NotificationRepository, device_repository: DeviceRepository):
        self.notification_repository = (notification_repository,)
        self.device_repository = device_repository

    async def send_push(self, push_data: SendPushMsg) -> bool:
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
            messaging.send_each(messages)
            return True  # noqa
        except FirebaseError:
            return False
