from pydantic import BaseModel

from src.db.models.consts import DeviceType


class CreateDeviceReq(BaseModel):
    fcm_token: str
    device_type: DeviceType

    class Config:
        from_attributes = True
        use_enum_values = True


class MessageResponse(BaseModel):
    message: str
