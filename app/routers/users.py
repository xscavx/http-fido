# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.dependencies import QueryPagination, get_authorized_user, prepare_users_storage
from app.models.domain.user import User
from app.storages.base.users import AsyncUsersStorage, UserNotFoundError

router = APIRouter(dependencies=[Depends(get_authorized_user)], tags=["users"])


@router.get("/users", response_model=list[User])
async def list_all_users(
    pagination: QueryPagination = Depends(),
    users_storage: AsyncUsersStorage = Depends(prepare_users_storage),
):
    try:
        return await users_storage.fetch_all(
            skip=pagination.skip, limit=pagination.limit
        )
    except UserNotFoundError as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ex.message)


@router.get("/users/me")
async def get_me(current_user: User = Depends(get_authorized_user)):
    return current_user


@router.get("/users/{user_id}", response_model=User)
async def get_user(
    user_id: str, users_storage: AsyncUsersStorage = Depends(prepare_users_storage)
):
    try:
        return await users_storage.try_find_by_id(user_id)
    except UserNotFoundError as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ex.message)
