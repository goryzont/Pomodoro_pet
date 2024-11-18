import httpx
from fastapi import Depends,  security, Security, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.client import GoogleClient, YandexClient
from database.settings import Settings
from exception import TokenExpired, TokenNotCorrect
from app.repository import TaskRepository, TaskCache, UserRepository
from database import get_db
from cache import get_redis_connection
from app.service import TaskService, UserService
from app.service.auth import AuthService


async def get_tasks_repository(db_session: AsyncSession = Depends(get_db)) -> TaskRepository:
    return TaskRepository(db_session)

async def get_tasks_cache_repository() -> TaskCache:
    redis_session = get_redis_connection()
    return TaskCache(redis_session)

async def get_tasks_service(
        task_repository: TaskRepository = Depends(get_tasks_repository),
        task_cache: TaskCache = Depends(get_tasks_cache_repository)
) -> TaskService:
    return TaskService(
        task_repository=task_repository,
        task_cache=task_cache
    )


async def get_user_repository(db_session: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(db_session=db_session)

async def get_async_client() -> httpx.AsyncClient:
    return httpx.AsyncClient()

async def get_google_client(async_client: httpx.AsyncClient() = Depends(get_async_client)) -> GoogleClient:
    return GoogleClient(
        settings=Settings(),
        async_client=async_client
    )

async def get_yandex_client(async_client: httpx.AsyncClient() = Depends(get_async_client)) -> YandexClient:
    return YandexClient(
        settings=Settings(),
        async_client=async_client
    )

async def get_auth_service(
    user_repository: UserRepository = Depends(get_user_repository),
    google_client: GoogleClient = Depends(get_google_client),
    yandex_client: YandexClient = Depends(get_yandex_client)

) -> AuthService:
    return AuthService(
        user_repository=user_repository,
        settings=Settings(),
        google_client=google_client,
        yandex_client=yandex_client
    )

async def get_user_service(
        user_repository: UserRepository = Depends(get_user_repository),
        auth_service: AuthService = Depends(get_auth_service)
)-> UserService:
    return UserService(
        user_repository=user_repository,
        auth_service=auth_service
    )


reusable_oauth2 = security.HTTPBearer()


async def get_request_user_id(
        auth_service: AuthService = Depends(get_auth_service),
        token: security.http.HTTPAuthorizationCredentials = Security(reusable_oauth2)) -> int:
    try:
        user_id = auth_service.get_user_id_from_access_token(token.credentials)

    except TokenExpired as e:
        raise HTTPException(status_code=401, detail=e.detail)
    except TokenNotCorrect as e:
        raise HTTPException(status_code=401, detail=e.detail)
    return user_id
