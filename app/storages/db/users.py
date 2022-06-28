# -*- coding: utf-8 -*-
from app.models.db.users import UserDb
from app.models.domain.user import User
from app.storages.base.users import (AsyncUsersStorage, UserAlreadyExistError,
                                     UserNotFoundError)
from sqlalchemy.future import select
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session


class AsyncDBUsersStorage(AsyncUsersStorage):
  def __init__(self, session: Session):
    self.__session: Session = session

  async def find_by_email(self, email: str) -> User:
    try:
      user_dto = await self.__session.execute(
        select(UserDb)
        .where(UserDb.email == email)
        .one()
      )
    except NoResultFound:
      raise UserNotFoundError

    return user_dto.to_entity()

  async def find_by_id(self, id: str) -> User:
    try:
      pk=int(id)
    except ValueError:
      raise UserNotFoundError

    try:
      user_dto = await self.__session.execute(
        select(UserDb)
        .where(UserDb.pk == pk)
        .one()
      )
    except NoResultFound:
      raise UserNotFoundError

    return user_dto.to_entity()

  async def create(self, user: User) -> User:
    user_dto = UserDb.from_entity(user)
    await self.__session.add(user_dto)
    return user_dto.to_entity()

  async def fetch_all(self) -> list[User]:
    user_dtos = await self.__session.execute(
      select(UserDb)
      .order_by(UserDb.pk)
      .limit(1000)
      .all()
    )

    if not user_dtos:
      return []

    return list(map(lambda user_dto: user_dto.to_entity(), user_dtos))
