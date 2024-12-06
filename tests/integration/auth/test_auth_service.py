import pytest
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import UserProfile
from tests.fixtures.users.user_model import EXISTS_GOOGLE_USER_ID, EXISTS_GOOGLE_USER_EMAIL

pytestmark = pytest.mark.asyncio


async def test_google_auth__login_not_exists_user(auth_service, get_db_session):
    session: AsyncSession = get_db_session
    code = 'fake_code'

    async with session as session:
        users = (await session.execute(select(UserProfile))).scalars().all()
        session.expire_all()

    user = await auth_service.google_auth(code)

    async with session as session:
        login_user = (await session.execute(select(UserProfile).where(UserProfile.id == user.user_id))).scalars().all()
        session.expire_all()


    assert len(users) == 0
    assert user is not None
    assert login_user is not None


async def test_google_auth__login_exists_user(auth_service, get_db_session):
    session: AsyncSession = get_db_session
    code = 'fake_code'
    query = insert(UserProfile).values(
        id=EXISTS_GOOGLE_USER_ID,
        email=EXISTS_GOOGLE_USER_EMAIL
    )

    async with session as session:
        await  session.execute(query)
        await session.commit()

    async with session as session:
        user_data = await auth_service.google_auth(code)
        login_user = (await session.execute(select(UserProfile).where(UserProfile.id == user_data.user_id))).scalar_one_or_none()

        assert login_user.email == EXISTS_GOOGLE_USER_EMAIL
        assert user_data.user_id == EXISTS_GOOGLE_USER_ID

async def test_base_login__success(auth_service, get_db_session):
    session: AsyncSession = get_db_session
    username = "test_username"
    password = "test_password"

    query = insert(UserProfile).values(
        username=username,
        password=password
    )
    async with session as session:
        await session.execute(query)
        await session.commit()

    async with session as session:
        login_user = (await session.execute(select(UserProfile).where(UserProfile.username == username))).scalar_one_or_none()

    user_data = await auth_service.login(username=username, password=password)

    assert login_user is not None
    assert user_data.user_id == login_user.id
