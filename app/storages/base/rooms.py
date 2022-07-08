# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

from app.models.domain.room import Room


class AsyncRoomsStorage(ABC):
    @abstractmethod
    async def try_find_by_id(self, id: str) -> Room:
        raise NotImplementedError

    @abstractmethod
    async def create(self, user: Room) -> Room:
        raise NotImplementedError

    @abstractmethod
    async def fetch_all(self, skip: int, limit: int) -> list[Room]:
        raise NotImplementedError


class RoomNotFoundError(Exception):
    message = "The room you spcecified does not exist."

    def __str__(self):
        return RoomNotFoundError.message


class RoomAlreadyExistError(Exception):
    message = "The room you spcecified already exist."

    def __str__(self):
        return RoomAlreadyExistError.message
