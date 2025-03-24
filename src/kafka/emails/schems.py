from uuid import UUID

from pydantic import BaseModel


class SendMail(BaseModel):
    to_user_id: UUID | None = None
    to_user_email: str | None = None
    title: str
    body: str
