from dataclasses import dataclass

from repository import UserRepository
from service.auth import AuthService
from shema import UserLoginShema, UserCreateShema


@dataclass
class UserService:
    user_repository: UserRepository
    auth_service: AuthService


    async def create_user(self, username: str, password: str) -> UserLoginShema:
        user_data_create = UserCreateShema(username=username, password=password)
        user = await self.user_repository.create_user(user_data_create)
        access_token = self.auth_service.generate_access_token(user_id=user.id)
        return UserLoginShema(user_id=user.id, access_token=access_token)


