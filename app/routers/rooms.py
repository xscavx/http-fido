# -*- coding: utf-8 -*-
from app.dependencides import verify_authorization_header
from fastapi import APIRouter, Depends


router = APIRouter(
  dependencies=[Depends(verify_authorization_header)],
  tags=['rooms']
)


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
