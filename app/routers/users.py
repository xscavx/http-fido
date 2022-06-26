# -*- coding: utf-8 -*-
from fastapi import APIRouter, Body
from pydantic import EmailStr


router = APIRouter(
  prefix='/users'
)

@router.post('/')
async def create_user(email: EmailStr = Body()):
  return []


@router.get('/')
async def list_all_users():
  return []


@router.get('/me')
async def get_me():
  return ''


@router.get('/{user_id}')
async def get_user(user_id: int):
  return {}
