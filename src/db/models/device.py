from uuid import UUID

from helpers.sqlalchemy.base_model import Base
from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column

from src.db.models.consts import DeviceType


class Device(Base):
    __tablename__ = "devices"

    user_id: Mapped[UUID]
    fcm_token: Mapped[str]
    device_type: Mapped[DeviceType] = mapped_column(Enum(DeviceType), nullable=True)
