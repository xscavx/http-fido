# -*- coding: utf-8 -*-
from app.dependencides import check_authorization_header, prepare_users_storage
from app.models.domain.user import User
from app.storages.base.users import (AsyncUsersStorage, UserAlreadyExistError,
                                     UserNotFoundError)
from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from pydantic import EmailStr


router = APIRouter(
  dependencies=[Depends(check_authorization_header)]
)


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


@router.get(
  '/users',
  response_model=list[User]
)
async def list_all_users(
  page_size: int = Query(default=1000, ge=10, le=10000),
  skip: int = Query(default=0, ge=0),
  users_storage: AsyncUsersStorage = Depends(prepare_users_storage)
):
  try:
    return await users_storage.fetch_page(page_size=page_size, skip=skip)
  except UserNotFoundError as ex:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=ex.message
    )


@router.get('/users/me')
async def get_me(
  users_storage: AsyncUsersStorage = Depends(prepare_users_storage)
):
  raise NotImplementedError


@router.get(
  '/users/{user_id}',
  response_model=User
)
async def get_user(
  user_id: str,
  users_storage: AsyncUsersStorage = Depends(prepare_users_storage)
):
  try:
    return await users_storage.find_by_id(user_id)
  except UserNotFoundError as ex:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=ex.message
    )
