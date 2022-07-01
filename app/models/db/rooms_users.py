# -*- coding: utf-8 -*-
from app.models.db.base import BaseDBModel
from app.models.db.rooms import RoomDb
from app.models.db.users import UserDb
from sqlalchemy import Column, ForeignKey, Integer


class RoomUserDb(BaseDBModel):
  __tablename__ = 'rooms_users'

  room_pk = Column(
    Integer,
    ForeignKey(RoomDb.pk),
    primary_key=True,
    index=True
  )
  user_pk = Column(
    Integer,
    ForeignKey(UserDb.pk),
    primary_key=True,
    index=True
  )
