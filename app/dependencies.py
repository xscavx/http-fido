# -*- coding: utf-8 -*-
from fastapi import Depends, Header, HTTPException, Query, status

from app.database import AsyncDBSession
from app.models.domain.user import User
from app.services.messages import AsyncMessagesService
from app.storages.base.users import AsyncUsersStorage, UserNotFoundError
from app.storages.db.messages import AsyncDBMessagesStorage
from app.storages.db.users import AsyncDBUsersStorage


async def prepare_messages_service() -> AsyncMessagesService:
    async with AsyncDBSession.begin() as session:
        yield AsyncMessagesService(
            messages_storage=AsyncDBMessagesStorage(session=session),
            users_storage=AsyncDBUsersStorage(session=session),
            rooms_storage=None,
        )


async def prepare_users_storage() -> AsyncUsersStorage:
    async with AsyncDBSession.begin() as session:
        yield AsyncDBUsersStorage(session=session)


async def get_authorized_user(
    access_token: str = Header(),
    users_storage: AsyncUsersStorage = Depends(prepare_users_storage),
) -> User:
    try:
        # assess token is just email string
        return await users_storage.try_find_by_email(access_token)
    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


class QueryPagination:
    def __init__(
        self,
        skip: int = Query(default=0, ge=0),
        limit: int = Query(default=100, ge=10, le=10000),
    ):
        self.skip = skip
        self.limit = limit
