# -*- coding: utf-8 -*-
from pydantic import BaseModel


class BaseMessage(BaseModel):
  id: str | None = None
  text: str
  sender_id: str


class DialogMessage(BaseMessage):
  receiver_id: str


class RoomMessage(BaseMessage):
  room_id: str
