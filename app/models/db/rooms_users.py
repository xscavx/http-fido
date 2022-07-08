# -*- coding: utf-8 -*-
from sqlalchemy import Column, ForeignKey, Integer, Table

from app.models.db.base import BaseDBModel

rooms_users_table = Table(
    "rooms_users",
    BaseDBModel.metadata,
    Column("room_pk", Integer, ForeignKey("rooms.pk"), primary_key=True, index=True),
    Column("user_pk", Integer, ForeignKey("users.pk"), primary_key=True, index=True),
)
