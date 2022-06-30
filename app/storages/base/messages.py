# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

from app.models.domain.message import DialogMessage, RoomMessage


class AsyncMessagesStorage(ABC):
  @abstractmethod
  async def create_dialog_message(self,
                                  messages: DialogMessage) -> DialogMessage:
    raise NotImplementedError

  @abstractmethod
  async def create_room_message(self,
                                message: RoomMessage) -> RoomMessage:
    raise NotImplementedError

  @abstractmethod
  async def fetch_dialog_recent_messages(
    self,
    sender_id: str,
    recipient_id: str,
    skip: int,
    limit: int
  ) -> list[DialogMessage]:
    raise NotImplementedError

  @abstractmethod
  async def fetch_room_recent_messages(
    self,
    room_id: str,
    skip: int,
    limit: int
  ) -> list[RoomMessage]:
    raise NotImplementedError
