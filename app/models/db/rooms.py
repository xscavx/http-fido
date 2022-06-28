# -*- coding: utf-8 -*-
from app.models.db.base import BaseDBModel
from sqlalchemy import Column, Integer


class RoomDb(BaseDBModel):
  __tablename__ = 'rooms'

  pk = Column(
    Integer,
    primary_key=True,
    autoincrement=True,
    index=True,
  )
