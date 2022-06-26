# -*- coding: utf-8 -*-
from app.models.rooms import Rooms
from app.models.users import Users
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class RoomsUsers(Base):
  __tablename__ = 'rooms_users'

  room = Column(
    Integer,
    ForeignKey(Rooms.pk),
    primary_key=True,
    index=True
  )
  user = Column(
    Integer,
    ForeignKey(Users.pk),
    primary_key=True
  )
