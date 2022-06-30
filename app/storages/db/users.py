# -*- coding: utf-8 -*-
from app.models.db.users import UserDb
from app.models.domain.user import User
from app.storages.base.users import (AsyncUsersStorage, UserAlreadyExistError,
                                     UserNotFoundError)
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class AsyncDBUsersStorage(AsyncUsersStorage):
  def __init__(self, session: AsyncSession):
    self.__session: AsyncSession = session

  async def find_by_email(self, email: str) -> User:
    query_result = await self.__session.execute(
      select(UserDb)
      .where(UserDb.email == email)
    )
    try:
      user_db = query_result.scalars().one()
    except NoResultFound:
      raise UserNotFoundError

    return user_db.to_entity()

  async def find_by_id(self, id: str) -> User:
    """ Details of bad implementation of DB storage
        id - string, but User.pk is integer primary key.
        So mimic like we cannot find user with id == 'Jason'
    """
    try:
      pk=int(id)
    except ValueError:
      raise UserNotFoundError

    query_result = await self.__session.execute(
      select(UserDb)
      .where(UserDb.pk == pk)
    )
    try:
      user_db = query_result.scalars().one()
    except NoResultFound:
      raise UserNotFoundError
    
    return user_db.to_entity()

  async def create(self, user: User) -> User:
    user_db = UserDb.from_entity(user)
    self.__session.add(user_db)
    try:
      await self.__session.flush()
    except IntegrityError:
      raise UserAlreadyExistError

    return await self.find_by_email(user.email)

  async def fetch_page(self, skip: int, limit: int) -> list[User]:
    query_result = await self.__session.execute(
      select(UserDb)
      .order_by(UserDb.pk)
      .limit(limit)
      .offset(skip)
    )
    user_dbs = query_result.scalars().all()
    if not user_dbs:
      raise UserNotFoundError

    # maybe a little heavy for async? 
    return [user_db.to_entity() for user_db in user_dbs]
