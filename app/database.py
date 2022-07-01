# -*- coding: utf-8 -*-
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.models.db.base import BaseDBModel
""" 
  imports below are only for one reason - force sqlalchemy to create all models
  not a production code
"""
from app.models.db.messages import MessageDb
from app.models.db.rooms import RoomDb
from app.models.db.rooms_users import RoomUserDb
from app.models.db.users import UserDb


# so bad
CONNECTION_URL = 'postgresql+asyncpg://fido:fido@localhost/fido'

engine = create_async_engine(
  CONNECTION_URL,
  echo=True
)

AsyncDBSession = sessionmaker(
  engine,
  expire_on_commit=False,
  class_=AsyncSession
)


async def create_tables():
  """ definitely not a production code! """
  async with engine.begin() as conn:
    await conn.run_sync(BaseDBModel.metadata.drop_all)
    await conn.run_sync(BaseDBModel.metadata.create_all)
