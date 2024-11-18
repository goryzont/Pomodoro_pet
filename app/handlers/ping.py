from fastapi import APIRouter
from app.settings import Settings

router = APIRouter(
    prefix='/ping',
    tags=['ping']
)

@router.get('/')
async def ping_app():
    settings = Settings()

    return {'message': settings.GOOGLE_TOKEN_ID}
