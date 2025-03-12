from uuid import UUID

from pydantic import BaseModel


class SendPushMsg(BaseModel):
    to_user: UUID
    title: str
    body: str
