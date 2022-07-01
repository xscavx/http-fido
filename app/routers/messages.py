# -*- coding: utf-8 -*-
from app.dependencies import (QueryPagination, get_authorized_user,
                              prepare_messages_service)
from app.models.domain.message import MessageContentModel, MessageReadModel
from app.models.domain.user import User
from app.services.messages import AsyncMessagesService
from app.storages.base.messages import MessageNotFoundError
from app.storages.base.rooms import RoomNotFoundError
from app.storages.base.users import UserNotFoundError
from fastapi import APIRouter, Depends, HTTPException, Response, status


router = APIRouter(
  dependencies=[Depends(get_authorized_user)],
  tags=['messages']
)


@router.post('/users/{user_id}/messages', response_class=Response)
async def create_user_message(
  user_id: str,
  message: MessageContentModel,
  current_user: User = Depends(get_authorized_user),
  messages_service: AsyncMessagesService = Depends(prepare_messages_service)
):
  try:
    await messages_service.create_dialog_message(
      sender_id=current_user.id,
      recipient_id=user_id,
      message=message
    )
  except UserNotFoundError as ex:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=ex.message
    )


@router.get('/users/{user_id}/messages', response_model=list[MessageReadModel])
async def fetch_user_recent_messages(
  user_id: str,
  pagination: QueryPagination = Depends(),
  current_user: User = Depends(get_authorized_user),
  messages_service: AsyncMessagesService = Depends(prepare_messages_service)
):
  try:
    return await messages_service.fetch_dialog_recent(
      sender_id=user_id,
      recipient_id=current_user.id,
      skip=pagination.skip,
      limit=pagination.limit
    )
  except (MessageNotFoundError, UserNotFoundError) as ex:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=ex.message
    )


@router.post('/rooms/{room_id}/messages', response_class=Response)
async def create_room_message(
  room_id: str,
  message: MessageContentModel,
  current_user: User = Depends(get_authorized_user),
  messages_service: AsyncMessagesService = Depends(prepare_messages_service)
):
  try:
    await messages_service.create_room_message(
      sender_id=current_user.id,
      room_id=room_id,
      message=message
    )
  except (RoomNotFoundError, UserNotFoundError) as ex:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=ex.message
    )


@router.get('/rooms/{room_id}/messages', response_model=list[MessageReadModel])
async def fetch_room_recent(
  room_id: str,
  pagination: QueryPagination = Depends(),
  messages_service: AsyncMessagesService = Depends(prepare_messages_service)
):
  try:
    return await messages_service.fetch_room_recent(
      room_id=room_id,
      skip=pagination.skip,
      limit=pagination.limit
    )
  except (MessageNotFoundError, RoomNotFoundError) as ex:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=ex.message
    )
