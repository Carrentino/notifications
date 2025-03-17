from datetime import datetime
from uuid import UUID

from helpers.sqlalchemy.base_model import Base
from sqlalchemy import Text, String, Enum, Index
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from src.db.models.consts import MailAndPushSentStatus


class Notification(Base):
    __tablename__ = 'notifications'

    user_id: Mapped[UUID]
    title: Mapped[str] = mapped_column(String(100))
    body: Mapped[str] = mapped_column(Text())
    status: Mapped[str] = mapped_column(Enum(MailAndPushSentStatus))
    sent_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now())

    __table_args__ = (Index('ix_notifications_user_id', 'user_id', postgresql_using='btree'),)
