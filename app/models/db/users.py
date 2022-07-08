# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String

from app.models.db.base import BaseDBModel
from app.models.domain.user import User


class UserDb(BaseDBModel):
    __tablename__ = "users"

    pk = Column(Integer, primary_key=True, autoincrement=True, index=True)
    email = Column(String, nullable=False, index=True, unique=True)

    def to_entity(self) -> User:
        return User(id=str(self.pk), email=self.email)

    @staticmethod
    def from_entity(entity: User) -> "UserDb":
        return UserDb(email=entity.email)
