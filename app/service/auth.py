from dataclasses import dataclass
import datetime as dt
from datetime import timedelta

from jose import jwt, JWTError

from app.client import GoogleClient, YandexClient
from app.settings import Settings
from app.exception import UserNotFoundException, UserNotCorrectPasswordException, TokenNotCorrect, TokenExpired
from app.models import UserProfile
from app.repository import UserRepository
from app.shema import UserLoginShema, UserCreateShema


@dataclass
class AuthService:
    user_repository: UserRepository
    settings: Settings
    google_client: GoogleClient
    yandex_client: YandexClient

    async def google_auth(self, code: str):
        user_data = await self.google_client.get_user_info(code)

        if user := await self.user_repository.get_user_by_email(user_data.email):
            access_token = self.generate_access_token(user_id=user.id)
            print('user_login_google')
            return UserLoginShema(user_id=user.id, access_token=access_token)

        create_user_data = UserCreateShema(
            google_access_token=user_data.access_token,
            email=user_data.email,
            name=user_data.name
        )
        created_user = await self.user_repository.create_user(create_user_data)
        access_token = self.generate_access_token(user_id=created_user.id)
        print('user_create_google')
        return UserLoginShema(user_id=created_user.id, access_token=access_token)

    async def yandex_auth(self, code: str):
        user_data = await self.yandex_client.get_user_info(code)

        if user := await self.user_repository.get_user_by_email(user_data.default_email):
            access_token = self.generate_access_token(user_id=user.id)
            print('user_login_yandex')
            return UserLoginShema(user_id=user.id, access_token=access_token)

        create_user_data = UserCreateShema(
            yandex_access_token=user_data.access_token,
            email=user_data.default_email,
            name=user_data.name
        )
        created_user = await self.user_repository.create_user(create_user_data)
        access_token = self.generate_access_token(user_id=created_user.id)
        print('user_create_yandex')
        return UserLoginShema(user_id=created_user.id, access_token=access_token)


    def get_google_redirect_url(self):
        return self.settings.google_redirect_url

    def get_yandex_redirect_url(self):
        return self.settings.yandex_redirect_url

    async def login(self, username: str, password: str) -> UserLoginShema:
        user = await self.user_repository.get_user_by_username(username)
        self._validate_auth_user(user, password)
        access_token = self.generate_access_token(user_id=user.id)
        return UserLoginShema(user_id=user.id, access_token=access_token)

    @staticmethod
    def _validate_auth_user(user: UserProfile, password:str):
        if not user:
            raise UserNotFoundException

        if user.password != password:
            raise UserNotCorrectPasswordException

    def generate_access_token(self, user_id: int) -> str:
        expires_date_unix = (dt.datetime.now() + timedelta(days=7)).timestamp()
        token = jwt.encode({'user_id': user_id,
                            'expire': expires_date_unix },
                           self.settings.JWT_SECRET_KEY,
                           algorithm=self.settings.JWT_ENCODE_ALGORITHM)
        return token

    def get_user_id_from_access_token(self, token: str) -> int:
        try:
            payload = jwt.decode(token, self.settings.JWT_SECRET_KEY, algorithms=[self.settings.JWT_ENCODE_ALGORITHM])
        except JWTError:
            raise TokenNotCorrect
        if payload["expire"] < dt.datetime.now().timestamp():
            raise TokenExpired
        print(payload)
        return payload["user_id"]

