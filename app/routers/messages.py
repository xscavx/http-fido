# -*- coding: utf-8 -*-
from app.dependencides import verify_authorization_header
from fastapi import APIRouter, Depends


router = APIRouter(
  dependencies=[Depends(verify_authorization_header)],
  tags=['messages']
)


@router.post('/users/{user_id}/messages')
async def create_user_message(message: str):
  raise NotImplementedError


@router.get('/users/{user_id}/messages')
async def list_user_messages(user_id: str):
  raise NotImplementedError


@router.post('/rooms/{room_id}/messages')
async def create_room_message(message: str):
  raise NotImplementedError


@router.get('/rooms/{room_id}/messages')
async def list_room_messages(room_id: str):
  raise NotImplementedError
