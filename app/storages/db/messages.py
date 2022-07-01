# -*- coding: utf-8 -*-
from app.models.db.common import try_cast_participant_id
from app.models.db.messages import MessageDb
from app.models.domain.message import MessageInsertModel, MessageReadModel
from app.storages.base.messages import (AsyncMessagesStorage,
                                        MessageNotFoundError)
from sqlalchemy import and_, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import Select


def _prepare_select_query_for_dialog(
  sender_pk: int, recipient_pk: int, skip: int, limit: int
) -> Select:
  return (
    select(MessageDb)
    .where(
      and_(MessageDb.sender_pk == sender_pk,
           MessageDb.recipient_pk == recipient_pk))
    .order_by(desc(MessageDb.created_at))
    .limit(limit)
    .offset(skip)
  )


def _prepare_select_query_for_room(
  room_pk: int, skip: int, limit: int
) -> Select:
  return (
    select(MessageDb)
    .where(MessageDb.room_pk == room_pk)
    .order_by(desc(MessageDb.created_at))
    .limit(limit)
    .offset(skip)
  )


async def _select_query_on_messages(
  session: AsyncSession, select_query: Select
) -> list[MessageReadModel]:
  query_result = await session.execute(select_query)
  messages_dbs: list[MessageDb] = query_result.scalars().all()

  if not messages_dbs:
    raise MessageNotFoundError

  return [message_db.to_entity() for message_db in messages_dbs]


class AsyncDBMessagesStorage(AsyncMessagesStorage):
  def __init__(self, session: AsyncSession):
    self.__session = session

  async def create(self, message: MessageInsertModel) -> None:
    message_db = MessageDb.from_entity(message)
    self.__session.add(message_db)
    await self.__session.flush()

  async def fetch_dialog_recent(
    self, sender_id: str, recipient_id: str, skip: int, limit: int
  ) -> list[MessageReadModel]:
    select_query = _prepare_select_query_for_dialog(
      sender_pk=try_cast_participant_id(sender_id),
      recipient_pk=try_cast_participant_id(recipient_id),
      skip=skip,
      limit=limit
    )
    return await _select_query_on_messages(
      session=self.__session,
      select_query=select_query
    )

  async def fetch_room_recent(
    self, room_id: str, skip: int, limit: int
  ) -> list[MessageReadModel]:
    select_query = _prepare_select_query_for_room(
      room_pk=try_cast_participant_id(room_id),
      skip=skip,
      limit=limit
    )
    return await _select_query_on_messages(
      session=self.__session,
      select_query=select_query
    )
