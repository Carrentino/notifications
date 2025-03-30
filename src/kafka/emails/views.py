from helpers.depends.db_session import get_db_session_context
from helpers.kafka.consumer import KafkaConsumerTopicsListeners

from src.integrations.users import UsersClient
from src.kafka.db_client import make_db_client
from src.kafka.emails.schems import SendMail
from src.repositories.mail import MailRepository
from src.settings import get_settings
from src.web.depends.service import get_mail_service

mail_listener = KafkaConsumerTopicsListeners()


@mail_listener.add(get_settings().kafka.topic_notifications_mails, SendMail)
async def send_push(message: SendMail) -> None:
    print('Получено сообщение на отправку письма')  # noqa
    async with get_db_session_context(make_db_client()) as session:
        mail_service = await get_mail_service(MailRepository(session=session), UsersClient())
        await mail_service.send_mail(message)
