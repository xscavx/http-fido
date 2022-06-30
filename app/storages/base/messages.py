# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

from app.models.domain.message import MessageUnsentModel, MessageReadModel


class AsyncMessagesStorage(ABC):
  @abstractmethod
  async def create_dialog_message(
    self,
    recipient_id: str,
    message: MessageUnsentModel
  ) -> MessageReadModel:
    raise NotImplementedError

  @abstractmethod
  async def create_room_message(
    self,
    room_id: str,
    message: MessageUnsentModel
  ) -> MessageReadModel:
    raise NotImplementedError

  @abstractmethod
  async def fetch_dialog_recent_messages(
    self,
    sender_id: str,
    recipient_id: str,
    skip: int,
    limit: int
  ) -> list[MessageReadModel]:
    raise NotImplementedError

  @abstractmethod
  async def fetch_room_recent_messages(
    self,
    room_id: str,
    skip: int,
    limit: int
  ) -> list[MessageReadModel]:
    raise NotImplementedError
