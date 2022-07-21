# -*- coding: utf-8 -*-
import asyncio
from os import environ as env

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from app.database import create_db_engine, create_tables, drop_tables


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def f_db_engine():
    return create_db_engine(
        db_user=env["FIDO_TEST_DB_USER"],
        db_password=env["FIDO_TEST_DB_PASSWORD"],
        db_host=env["FIDO_TEST_DB_HOST"],
        db_name=env["FIDO_TEST_DB_NAME"],
    )


@pytest.fixture(scope="session")
def f_db_session_maker(f_db_engine):
    return sessionmaker(f_db_engine, expire_on_commit=False, class_=AsyncSession)


@pytest.fixture(scope="session")
async def f_prepare_tables(f_db_engine, f_db_session_maker):
    await drop_tables(f_db_engine)
    await create_tables(f_db_engine)
    yield
    await drop_tables(f_db_engine)
