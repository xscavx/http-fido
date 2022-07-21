# -*- coding: utf-8 -*-
from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    func,
)

from app.models.db.base import BaseDBModel
from app.models.db.common import try_cast_participant_id
from app.models.db.rooms import RoomDb
from app.models.db.users import UserDb
from app.models.domain.message import MessageInsertModel, MessageReadModel


class MessageDb(BaseDBModel):
    __tablename__ = "messages"

    pk = Column(Integer, primary_key=True, autoincrement=True, index=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    text = Column(String, nullable=False)
    sender_pk = Column(Integer, ForeignKey(UserDb.pk), nullable=False, index=True)
    recipient_pk = Column(Integer, ForeignKey(UserDb.pk), index=True)
    room_pk = Column(Integer, ForeignKey(RoomDb.pk), index=True)

    __table_args__ = (
        CheckConstraint(
            "(recipient_pk IS NOT NULL AND room_pk IS NULL)"
            "OR"
            "(recipient_pk IS NULL AND room_pk IS NULL)"
        ),
    )

    def to_entity(self) -> MessageReadModel:
        return MessageReadModel(
            id=str(self.pk),
            text=str(self.text),
            sender_id=str(self.sender_pk),
            recipient_id=str(self.recipient_pk),
            room_id=str(self.room_pk),
        )

    @staticmethod
    def from_entity(entity: MessageInsertModel) -> "MessageDb":
        return MessageDb(
            text=entity.text,
            sender_pk=try_cast_participant_id(entity.sender_id),
            recipient_pk=try_cast_participant_id(entity.recipient_id),
            room_pk=try_cast_participant_id(entity.room_id),
        )
