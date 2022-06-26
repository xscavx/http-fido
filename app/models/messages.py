# -*- coding: utf-8 -*-
from app.models.users import Users
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Messages(Base):
  __tablename__ = 'messages'

  pk = Column(
    Integer,
    primary_key=True,
    index=True
  )
  text = Column(
    String,
    nullable=False
  )
  sender_user = Column(
    Integer,
    ForeignKey(Users.pk),
    nullable=False,
    index=True
  )
  recipient_user = Column(
    Integer,
    ForeignKey(Users.pk),
    index=True
  )
  recipient_room = Column(
    Integer,
    ForeignKey(Users.pk),
    index=True
  )
