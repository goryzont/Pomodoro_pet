
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession


engine = create_async_engine(url="postgresql+asyncpg://postgres:postgres@0.0.0.0:5432/pomidoro",
                             future=True,
                             echo=True,
                             )

AsyncSessionFactory = async_sessionmaker(
    engine,
    expire_on_commit=False
)

async def get_db() -> AsyncSession:
    async with AsyncSessionFactory() as session:
        yield session

Base = declarative_base()

