from dataclasses import dataclass
import httpx

from shema import GoogleUserData
from database.settings import Settings

@dataclass
class GoogleClient:
    settings: Settings
    async_client: httpx.AsyncClient

    async def get_user_info(self, code: str) -> GoogleUserData:
        access_token = await self._get_user_access_token(code=code)
        # Не используем повторно `async with`, просто отправляем запрос
        user_info = await self.async_client.get(
            "https://www.googleapis.com/oauth2/v1/userinfo",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        return GoogleUserData(**user_info.json(), access_token=access_token)

    async def _get_user_access_token(self, code: str) -> str:
        data = {
            "code": code,
            "client_id": self.settings.GOOGLE_CLIENT_ID,
            "client_secret": self.settings.GOOGLE_SECRET_KEY,
            "redirect_uri": self.settings.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code"
        }
        # То же самое здесь — отправляем запрос без повторного открытия клиента
        response = await self.async_client.post(self.settings.GOOGLE_TOKEN_URL, data=data)
        return response.json()["access_token"]