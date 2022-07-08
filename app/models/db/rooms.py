# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

from app.models.db.base import BaseDBModel
from app.models.db.rooms_users import rooms_users_table
from app.models.db.users import UserDb


class RoomDb(BaseDBModel):
    __tablename__ = "rooms"

    pk = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True,
    )

    participants = relationship(UserDb, secondary=rooms_users_table)
