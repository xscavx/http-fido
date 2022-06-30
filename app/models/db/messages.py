# -*- coding: utf-8 -*-
from app.models.db.base import BaseDBModel
from app.models.db.rooms import RoomDb
from app.models.db.users import UserDb
from app.models.domain.message import MessageReadModel, MessageUnsentModel
from sqlalchemy import (CheckConstraint, Column, DateTime, ForeignKey, Integer,
                        String, func)


class MessageDb(BaseDBModel):
  __tablename__ = 'messages'

  pk = Column(
    Integer,
    primary_key=True,
    autoincrement=True,
    index=True
  )
  created_at = Column(
    DateTime(timezone=True),
    server_default=func.now(),
    nullable=False
  )
  text = Column(
    String,
    nullable=False
  )
  sender_id = Column(
    Integer,
    ForeignKey(UserDb.pk),
    nullable=False,
    index=True
  )
  recipient_id = Column(
    Integer,
    ForeignKey(UserDb.pk),
    index=True
  )
  room_id = Column(
    Integer,
    ForeignKey(RoomDb.pk),
    index=True
  )

  __table_args__ = (
    CheckConstraint(
      'recipient_id IS NOT NULL XOR room_id IS NOT NULL'
    ),
  )

  @property
  def id(self):
    return None if self.pk is None else str(self.pk)

  def to_entity(self) -> MessageReadModel:
    return MessageReadModel(self)

  @staticmethod
  def from_entity(entity: MessageUnsentModel) -> "MessageDb":
    return MessageDb(
      text=entity.text,
      sender_user=entity.sender_id
    )
