# -*- coding: utf-8 -*-
from fastapi import APIRouter


router = APIRouter()

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
