# -*- coding: utf-8 -*-
from fastapi import Depends, Header, HTTPException, status

from app.database import AsyncDBSession
from app.storages.base.users import AsyncUsersStorage, UserNotFoundError
from app.storages.db.users import AsyncDBUsersStorage


async def prepare_users_storage() -> AsyncUsersStorage:
  async with AsyncDBSession.begin() as session:
    yield AsyncDBUsersStorage(session=session)


async def verify_authorization_header(
  access_token: str = Header(),
  users_storage: AsyncUsersStorage = Depends(prepare_users_storage)
) -> None:
  try:
    # assess token is just email string
    await users_storage.find_by_email(access_token)
  except UserNotFoundError as ex:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
    )
