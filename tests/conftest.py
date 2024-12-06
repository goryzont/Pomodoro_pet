import asyncio

import pytest

pytest_plugins = [
     "tests.fixtures.auth.auth_service",
     "tests.fixtures.auth.clients",
     'tests.fixtures.users.user_repository',
     'tests.fixtures.infrastructure',

]

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()