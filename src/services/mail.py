import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from src.db.models.consts import MailAndPushSentStatus
from src.db.models.mail import Mail
from src.errors.service import UserServiceIsUnavailableError
from src.integrations.users import UsersClient
from src.kafka.emails.schems import SendMail
from src.repositories.mail import MailRepository
from src.settings import get_settings


class MailService:
    def __init__(self, mail_repository: MailRepository, users_client: UsersClient):
        self.mail_repository = mail_repository
        self.users_client = users_client

    async def send_mail(self, mail_data: SendMail) -> MailAndPushSentStatus:
        if mail_data.to_user_email is None and mail_data.to_user_id is None:
            return MailAndPushSentStatus.FAILED
        if mail_data.to_user_email:
            to_email = mail_data.to_user_email
        else:
            try:
                response = await self.users_client.get_user_info(str(mail_data.to_user_id))
                to_email = response.json()[0]['email']
            except UserServiceIsUnavailableError:
                return MailAndPushSentStatus.FAILED
        try:
            msg = MIMEMultipart()
            msg['From'] = get_settings().smtp.username
            msg['To'] = to_email
            msg['Subject'] = mail_data.title

            msg.attach(MIMEText(mail_data.body, 'html'))

            with smtplib.SMTP(get_settings().smtp.server, get_settings().smtp.port) as server:
                server.starttls()
                server.login(get_settings().smtp.username, get_settings().smtp.password)
                server.sendmail(get_settings().smtp.username, to_email, msg.as_string())

            await self.mail_repository.create(
                Mail(to_email=to_email, status=MailAndPushSentStatus.SENT, title=mail_data.title, body=mail_data.body)
            )
            return MailAndPushSentStatus.SENT  # noqa
        except Exception as e:  # noqa
            await self.mail_repository.create(
                Mail(to_email=to_email, status=MailAndPushSentStatus.FAILED, title=mail_data.title, body=mail_data.body)
            )
            return MailAndPushSentStatus.FAILED
