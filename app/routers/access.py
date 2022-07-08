# -*- coding: utf-8 -*-
from app.dependencies import prepare_users_storage
from app.models.domain.user import User
from app.storages.base.users import (AsyncUsersStorage, UserAlreadyExistError,
                                     UserNotFoundError)
from fastapi import APIRouter, Body, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr


router = APIRouter(
  tags=['access']
)


@router.post(
  '/register',
  response_model=User
)
async def register_user(
  email: EmailStr = Body(),
  users_storage: AsyncUsersStorage = Depends(prepare_users_storage)
):
  try:
    return await users_storage.create(
      User(email=email)
    )
  except UserAlreadyExistError as ex:
    raise HTTPException(
      status_code=status.HTTP_409_CONFLICT,
      detail=ex.message
    )


class AuthResponse(BaseModel):
  access_token: str


@router.post(
  '/auth',
  response_model=AuthResponse
)
async def authorize_user(
  email: EmailStr = Body(),
  users_storage: AsyncUsersStorage = Depends(prepare_users_storage)
):
  try:
    await users_storage.try_find_by_email(email)
  except UserNotFoundError as ex:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail=ex.message
    )
  # assess token is just an email string
  return {'access_token': email}


__all__ = ['router']
