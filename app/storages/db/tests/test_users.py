# -*- coding: utf-8 -*-
from typing import AsyncGenerator

import pytest
from pydantic import EmailStr
from sqlalchemy.future import select

from app.models.db.users import UserDb
from app.models.domain.user import User
from app.storages.base.users import AsyncUsersStorage, UserNotFoundError
from app.storages.db.users import AsyncDBUsersStorage

DB_SIZE_RECORDS = 1000 + 213


@pytest.fixture(scope="session")
async def f_setup_database(f_prepare_tables, f_db_session_maker):
    users_gen = (
        {"email": f"user{idx}@domain{idx}.org"} for idx in range(DB_SIZE_RECORDS)
    )
    async with f_db_session_maker.begin() as session:
        for user in users_gen:
            session.add(UserDb(**user))
        await session.flush()


@pytest.fixture
async def f_users_db_storage(
    f_db_session_maker,
) -> AsyncGenerator[AsyncUsersStorage, None]:
    async with f_db_session_maker.begin() as session:
        yield AsyncDBUsersStorage(session=session)


@pytest.mark.parametrize(
    ["page_size", "actual_size"],
    [
        (1, min(1, DB_SIZE_RECORDS)),
        (5, min(5, DB_SIZE_RECORDS)),
        (10, min(10, DB_SIZE_RECORDS)),
        (15, min(15, DB_SIZE_RECORDS)),
        (2000, min(2000, DB_SIZE_RECORDS)),
    ],
)
async def test_fetch_page(
    f_setup_database,
    f_users_db_storage: AsyncUsersStorage,
    page_size: int,
    actual_size: int,
):
    users: list[User] = await f_users_db_storage.fetch_all(limit=page_size, skip=0)
    assert len(users) == actual_size


@pytest.mark.parametrize(["page_size"], [(100,), (2000,)])
async def test_fetch_all(
    f_setup_database, f_users_db_storage: AsyncUsersStorage, page_size: int
):
    users_count = 0
    while True:
        try:
            users: list[User] = await f_users_db_storage.fetch_all(
                limit=page_size, skip=users_count
            )
            users_count += len(users)
        except UserNotFoundError:
            break

    assert users_count == DB_SIZE_RECORDS


@pytest.mark.parametrize(
    ["user_id"],
    [
        ("1",),
        ("356",),
        pytest.param(
            "invalid_ids_then", marks=pytest.mark.xfail(reason="User not found")
        ),
        pytest.param("100532", marks=pytest.mark.xfail(reason="User not found")),
    ],
)
async def test_try_find_by_id(
    f_setup_database, f_users_db_storage: AsyncUsersStorage, user_id: str
):
    found: User = await f_users_db_storage.try_find_by_id(user_id)
    assert found.id == user_id
    assert found.email


@pytest.mark.parametrize(
    ["email"],
    [
        ("user5@domain5.org",),
        ("user99@domain99.org",),
        pytest.param(
            "invalid@mail.then", marks=pytest.mark.xfail(reason="User not found")
        ),
        pytest.param("not a mail", marks=pytest.mark.xfail(reason="User not found")),
    ],
)
async def test_try_find_by_email(
    f_setup_database, f_users_db_storage: AsyncUsersStorage, email: str
):
    found: User = await f_users_db_storage.try_find_by_email(email)
    assert found.id
    assert found.email == email


@pytest.mark.parametrize(
    ["email"], [("new2142342@email.com",), ("another234234@email.org",)]
)
async def test_create_user(f_setup_database, f_db_session_maker, email: str):
    async with f_db_session_maker.begin() as create_session:
        users_storage = AsyncDBUsersStorage(session=create_session)
        await users_storage.create(User(email=EmailStr(email)))

    async with f_db_session_maker.begin() as read_session:
        query_result = await read_session.execute(
            select(UserDb).where(UserDb.email == email)
        )
        user_db: UserDb = query_result.scalars().one()

    assert user_db.email == email
