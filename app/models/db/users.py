# -*- coding: utf-8 -*-
from app.models.db.base import BaseDBModel
from app.models.domain.user import User
from sqlalchemy import Column, Integer, String


class UserDb(BaseDBModel):
  __tablename__ = 'users'

  pk = Column(
    Integer,
    primary_key=True,
    autoincrement=True,
    index=True
  )
  email = Column(
    String,
    nullable=False,
    index=True,
    unique=True
  )

  @property
  def id(self):
    return None if self.pk is None else str(self.pk)

  def to_entity(self) -> User:
    return User(
      id=self.id,
      email=self.email
    )

  @staticmethod
  def from_entity(entity: User) -> "UserDb":
    return UserDb(
      email=entity.email
    )
