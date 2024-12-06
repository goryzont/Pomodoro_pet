import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.settings import Settings
from app.infrastructure.database.database import Base


@pytest.fixture
def settings():
    return Settings()

engine = create_async_engine(url="postgresql+asyncpg://postgres:postgres@0.0.0.0:5432/pomidoro-test",
                             future=True,
                             echo=True,
                             )

AsyncSessionFactory = async_sessionmaker(
    engine,
    expire_on_commit=False
)

@pytest_asyncio.fixture(autouse=True, scope="function")
async def init_models(event_loop):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture(scope='function')
async def get_db_session() -> AsyncSession:
    return AsyncSessionFactory()