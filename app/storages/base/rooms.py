# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

from app.models.domain.room import Room


class AsyncRoomsStorage(ABC):
  pass


class RoomNotFoundError(Exception):
  message = "The room you spcecified does not exist."

  def __str__(self):
    return RoomNotFoundError.message


class RoomAlreadyExistError(Exception):
  message = "The room you spcecified already exist."

  def __str__(self):
    return RoomAlreadyExistError.message
