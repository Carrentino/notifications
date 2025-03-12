import uuid

import factory

from src.db.models.consts import DeviceType
from src.db.models.device import Device
from tests.factories.base import BaseSqlAlchemyFactory


class DeviceFactory(BaseSqlAlchemyFactory):
    user_id = factory.LazyFunction(uuid.uuid4)
    fcm_token = factory.Faker('word')
    device_type = DeviceType.IOS

    class Meta:
        model = Device
