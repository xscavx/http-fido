# -*- coding: utf-8 -*-
from pydantic import BaseModel

from app.models.domain.user import User


class Room(BaseModel):
    id: str
    participants: list[User]
