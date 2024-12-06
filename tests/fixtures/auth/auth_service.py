import pytest
import pytest_asyncio

from app.repository import UserRepository
from app.service import AuthService
from app.settings import Settings


@pytest.fixture
def mock_auth_service(yandex_client, google_client, fake_user_repository):
    return AuthService(
        user_repository=fake_user_repository,
        settings=Settings(),
        google_client=google_client,
        yandex_client=yandex_client
    )

@pytest_asyncio.fixture
def auth_service(yandex_client, google_client, mock_auth_service, get_db_session):
    return AuthService(
        user_repository=UserRepository(db_session=get_db_session),
        settings=Settings(),
        google_client=google_client,
        yandex_client=yandex_client
    )