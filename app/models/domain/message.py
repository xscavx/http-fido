# -*- coding: utf-8 -*-
from pydantic import BaseModel


class MessageUnsentModel(BaseModel):
  text: str
  sender_id: str


class MessageReadModel(MessageUnsentModel):
  id: str
  recipient_id: str | None
  room_id: str | None

  class Config:
    orm_mode = True
