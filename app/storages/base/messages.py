# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

from app.models.domain.message import MessageInsertModel, MessageReadModel


class AsyncMessagesStorage(ABC):
  @abstractmethod
  async def create(self, message: MessageInsertModel) -> None:
    raise NotImplementedError

  @abstractmethod
  async def fetch_dialog_recent(
    self, sender_id: str, recipient_id: str, skip: int, limit: int
  ) -> list[MessageReadModel]:
    raise NotImplementedError

  @abstractmethod
  async def fetch_room_recent(
    self, room_id: str, skip: int, limit: int
  ) -> list[MessageReadModel]:
    raise NotImplementedError


class MessageNotFoundError(Exception):
  message = "Messages not found."

  def __str__(self):
    return MessageNotFoundError.message


__all__ = ['AsyncMessagesStorage', 'MessageNotFoundError']
