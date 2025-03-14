from unittest.mock import patch, Mock

import pytest

from src.db.models.consts import MailAndPushSentStatus
from src.kafka.pushes.schems import SendPushMsg
from src.services.notification import NotificationService
from tests.factories.device import DeviceFactory


@pytest.mark.parametrize('firebase_success_count', [1, 0])
@patch('firebase_admin.messaging.Message')
@patch('firebase_admin.messaging.send_each')
async def test_send_push(
    fcm_send: Mock, fcm_msg: Mock, firebase_success_count, notifications_service: NotificationService
):
    device = await DeviceFactory.create()

    class BimBimBamBam:
        pass

    obj = BimBimBamBam()
    obj.success_count = firebase_success_count
    fcm_send.return_value = obj

    fcm_msg.return_value = ['bbb']
    push_msg = SendPushMsg(to_user=device.user_id, title='bb', body='sss')
    await notifications_service.send_push(push_msg)
    notification = await notifications_service.notification_repository.get_one_by(user_id=push_msg.to_user)
    assert (
        notification.status == MailAndPushSentStatus.SENT
        if firebase_success_count == 1
        else MailAndPushSentStatus.FAILED
    )
