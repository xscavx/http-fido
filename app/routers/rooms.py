# -*- coding: utf-8 -*-
from fastapi import APIRouter


router = APIRouter()


@router.post('/rooms')
async def create_room():
  raise NotImplementedError


@router.get('/rooms')
async def list_all_rooms():
  raise NotImplementedError


@router.get('/rooms/{room_id}')
async def get_room(room_id: str):
  raise NotImplementedError


@router.get('/rooms/{room_id}/users')
async def list_room_users(room_id: str):
  raise NotImplementedError
