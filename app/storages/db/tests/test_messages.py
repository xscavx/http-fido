# -*- coding: utf-8 -*-
import pytest
from sqlalchemy.future import select

from app.models.db.messages import MessageDb
from app.models.domain.message import MessageInsertModel, MessageReadModel
from app.storages.base.messages import AsyncMessagesStorage, MessageNotFoundError
from app.storages.db.messages import AsyncDBMessagesStorage


@pytest.fixture(scope="session")
async def f_setup_database(f_prepare_tables, f_db_session_maker):
    async with f_db_session_maker.begin() as session:
        # session.add(MessageDb(**msg))
        await session.flush()


@pytest.fixture
async def f_users_db_storage(f_db_session_maker) -> AsyncMessagesStorage:
    async with f_db_session_maker.begin() as session:
        yield AsyncDBMessagesStorage(session=session)


async def test_fetch_dialog_recent(f_setup_database, f_users_db_storage):
    assert True
