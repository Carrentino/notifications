from enum import StrEnum


class DeviceType(StrEnum):
    IOS = 'ios'
    WEB = 'web'
    ANDROID = 'android'


class MailAndPushSentStatus(StrEnum):
    SENT = 'sent'
    FAILED = 'failed'
