from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status
from helpers.depends.auth import get_current_user
from helpers.models.user import UserContext

from src.services.device import DeviceService
from src.web.api.devices.schemas import CreateDeviceReq, MessageResponse
from src.web.depends.service import get_device_service

devices_router = APIRouter()


@devices_router.post('/', status_code=status.HTTP_201_CREATED, response_model=MessageResponse)
async def create_device(
    device_service: Annotated[DeviceService, Depends(get_device_service)],
    current_user: Annotated[UserContext, Depends(get_current_user)],
    req_data: CreateDeviceReq,
) -> MessageResponse:
    await device_service.create_device(req_data, current_user.user_id)
    return MessageResponse(message='OK')
