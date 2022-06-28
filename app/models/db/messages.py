# -*- coding: utf-8 -*-
from app.models.db.base import BaseDBModel
from app.models.db.rooms import RoomDb
from app.models.db.users import UserDb
from sqlalchemy import CheckConstraint, Column, ForeignKey, Integer, String


class MessageDb(BaseDBModel):
  __tablename__ = 'messages'

  pk = Column(
    Integer,
    primary_key=True,
    autoincrement=True,
    index=True,
  )
  text = Column(
    String,
    nullable=False
  )
  sender_user = Column(
    Integer,
    ForeignKey(UserDb.pk),
    nullable=False,
    index=True
  )
  recipient_user = Column(
    Integer,
    ForeignKey(UserDb.pk),
    index=True
  )
  recipient_room = Column(
    Integer,
    ForeignKey(RoomDb.pk),
    index=True
  )

  __table_args__ = (
    CheckConstraint(
      'recipient_user IS NOT NULL OR recipient_room IS NOT NULL'
    ),
  )
