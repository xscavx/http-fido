# -*- coding: utf-8 -*-
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.models.db.base import BaseDBModel

""" 
  imports below are only for one reason - force sqlalchemy to create all models
  not a production code
"""
from os import environ as env

from app.models.db.messages import MessageDb
from app.models.db.rooms import RoomDb
from app.models.db.users import UserDb


def create_db_engine(
    db_user: str, db_password: str, db_host: str, db_name: str, echo: bool = False
):
    return create_async_engine(
        f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}/{db_name}", echo=echo
    )


engine = create_db_engine(
    db_user=env.get("FIDO_DB_USER"),
    db_password=env.get("FIDO_DB_PASSWORD"),
    db_host=env.get("FIDO_DB_HOST"),
    db_name=env.get("FIDO_DB_NAME"),
)
AsyncDBSession = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def create_tables(engine):
    """definitely not a production code!"""
    async with engine.begin() as conn:
        await conn.run_sync(BaseDBModel.metadata.create_all)


async def drop_tables(engine):
    """definitely not a production code!"""
    async with engine.begin() as conn:
        await conn.run_sync(BaseDBModel.metadata.drop_all)


async def recreate_tables(engine):
    """definitely not a production code!"""
    async with engine.begin() as conn:
        await conn.run_sync(BaseDBModel.metadata.drop_all)
        await conn.run_sync(BaseDBModel.metadata.create_all)
