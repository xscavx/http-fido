# -*- coding: utf-8 -*-
from app.models.domain.user import User

from pydantic import BaseModel


class Room(BaseModel):
  id: str
  participants: list[User]


__all__ = ['Room']
