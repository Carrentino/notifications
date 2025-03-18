from datetime import datetime

from helpers.sqlalchemy.base_model import Base
from sqlalchemy import Index, Enum
from sqlalchemy.orm import Mapped, mapped_column

from src.db.models.consts import MailAndPushSentStatus


class Mail(Base):
    __tablename__ = 'mails'

    title: Mapped[str]
    body: Mapped[str]
    to_email: Mapped[str]
    status: Mapped[str] = mapped_column(Enum(MailAndPushSentStatus))
    sent_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now())

    __table_args__ = (Index('ix_mails_to_email', 'to_email', postgresql_using='btree'),)
