from dataclasses import dataclass

import pytest

from app.shema import UserCreateShema
from tests.fixtures.users.user_model import UserProfileFactory


@dataclass
class FakeUserRepository:

    async def get_user_by_email(self, email):
        return None

    async def create_user(self, user_data: UserCreateShema):
        return UserProfileFactory()


@pytest.fixture
def user_repository():
    return FakeUserRepository()
