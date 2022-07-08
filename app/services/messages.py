# -*- coding: utf-8 -*-
from app.models.domain.message import (MessageContentModel, MessageInsertModel,
                                       MessageReadModel)
from app.storages.base.messages import AsyncMessagesStorage
from app.storages.base.rooms import AsyncRoomsStorage
from app.storages.base.users import AsyncUsersStorage


class AsyncMessagesService:
  def __init__(
    self,
    messages_storage: AsyncMessagesStorage,
    users_storage: AsyncUsersStorage,
    rooms_storage: AsyncRoomsStorage = None
  ):
    self.__storage: AsyncMessagesStorage = messages_storage
    self.__users: AsyncUsersStorage = users_storage
    self.__rooms: AsyncRoomsStorage = rooms_storage

  async def create_dialog_message(
    self, sender_id: str, recipient_id: str, message: MessageContentModel
  ) -> None:
    await self.__users.try_find_by_id(sender_id)
    await self.__users.try_find_by_id(recipient_id)

    return await self.__storage.create(
      message=MessageInsertModel(
        **message.dict(), sender_id=sender_id, recipient_id=recipient_id
      )
    )

  async def create_room_message(
    self, sender_id: str, room_id: str, message: MessageContentModel
  ) -> None:
    await self.__users.try_find_by_id(sender_id)
    # await self.__rooms.try_find_by_id(room_id)

    return await self.__storage.create(
      message=MessageInsertModel(
        **message.dict(), sender_id=sender_id, room_id=room_id
      )
    )

  async def fetch_dialog_recent(
    self, sender_id: str, recipient_id: str, skip: int, limit: int
  ) -> list[MessageReadModel]:
    await self.__users.try_find_by_id(sender_id)
    await self.__users.try_find_by_id(recipient_id)
    return await self.__storage.fetch_dialog_recent(
      sender_id, recipient_id, skip, limit
    )

  async def fetch_room_recent(
    self, room_id: str, skip: int, limit: int
  ) -> list[MessageReadModel]:
    # await self.__rooms.try_find_by_id(room_id)
    return await self.__storage.fetch_room_recent(room_id, skip, limit)


__all__ = ['AsyncMessagesService']
