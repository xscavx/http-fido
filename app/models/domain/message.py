# -*- coding: utf-8 -*-
from pydantic import BaseModel


class MessageContentModel(BaseModel):
    text: str


class MessageInsertModel(MessageContentModel):
    text: str
    sender_id: str
    recipient_id: str | None
    room_id: str | None


class MessageReadModel(MessageInsertModel):
    id: str

    class Config:
        orm_mode = True
