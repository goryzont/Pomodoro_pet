from typing import Annotated

from fastapi import APIRouter, Depends

from app.dependency import get_user_service
from app.service import UserService
from app.shema import UserLoginShema, UserCreateShema

router = APIRouter(prefix='/user', tags=['user'])


@router.post('/create_user', response_model=UserLoginShema)
async def create_user(body: UserCreateShema, user_service: Annotated[UserService, Depends(get_user_service)]):
    return await user_service.create_user(body.username, body.password)

