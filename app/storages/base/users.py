# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

from app.models.domain.user import User


class AsyncUsersStorage(ABC):
    @abstractmethod
    async def try_find_by_email(self, email: str) -> User:
        raise NotImplementedError

    @abstractmethod
    async def try_find_by_id(self, id: str) -> User:
        raise NotImplementedError

    @abstractmethod
    async def create(self, user: User) -> User:
        raise NotImplementedError

    @abstractmethod
    async def fetch_all(self, skip: int, limit: int) -> list[User]:
        raise NotImplementedError


class UserNotFoundError(Exception):
    message = "The user you spcecified does not exist."

    def __str__(self):
        return UserNotFoundError.message


class UserAlreadyExistError(Exception):
    message = "The user you spcecified already exist."

    def __str__(self):
        return UserAlreadyExistError.message
