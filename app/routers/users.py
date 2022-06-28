# -*- coding: utf-8 -*-
from app.database import AsyncDBSession
from app.models.domain.user import User
from app.storages.base.users import (AsyncUsersStorage, UserAlreadyExistError,
                                     UserNotFoundError)
from app.storages.db.users import AsyncDBUsersStorage
from fastapi import APIRouter, Body, Depends, HTTPException, status
from pydantic import EmailStr


async def prepare_users_storage() -> AsyncUsersStorage:
  async with AsyncDBSession.begin() as session:
    yield AsyncDBUsersStorage(session=session)


router = APIRouter()


@router.post(
  '/users',
  response_model=User
)
async def create_user(
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
  except Exception:
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )


@router.get(
  '/users',
  response_model=list[User]
)
async def list_all_users(
  users_storage: AsyncUsersStorage = Depends(prepare_users_storage)
):
  try:
    return await users_storage.fetch_all()
  except Exception:
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )


@router.get('/users/me')
async def get_me():
  raise NotImplementedError


@router.get(
  '/users/{user_id}',
  response_model=User
)
async def get_user(
  user_id: int,
  users_storage: AsyncUsersStorage = Depends(prepare_users_storage)
):
  try:
    return await users_storage.find_by_id(user_id)
  except UserNotFoundError as ex:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=ex.message,
    )
  except Exception:
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
