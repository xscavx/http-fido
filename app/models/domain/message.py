# -*- coding: utf-8 -*-
from app.models.domain.room import Room
from app.models.domain.user import User

from pydantic import BaseModel


class Message(BaseModel):
  id: str
  text: str
  sender_id: User
  receiver_id: User | Room
