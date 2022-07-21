# -*- coding: utf-8 -*-
from typing import AsyncGenerator

import pytest

from app.storages.base.messages import AsyncMessagesStorage
from app.storages.db.messages import AsyncDBMessagesStorage


@pytest.fixture(scope="session")
async def f_setup_database(f_prepare_tables, f_db_session_maker):
    async with f_db_session_maker.begin() as session:
        # session.add(MessageDb(**msg))
        await session.flush()


@pytest.fixture
async def f_users_db_storage(
    f_db_session_maker,
) -> AsyncGenerator[AsyncMessagesStorage, None]:
    async with f_db_session_maker.begin() as session:
        yield AsyncDBMessagesStorage(session=session)


async def test_fetch_dialog_recent(f_setup_database, f_users_db_storage):
    assert True
