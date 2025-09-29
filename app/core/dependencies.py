from fastapi import Header, HTTPException, status
from app.core.config import settings


async def get_api_key(x_api_key: str = Header(...)):
    """
    Проверка API Key.
    Если ключ неверный — возвращает 401 Unauthorized.
    """
    if x_api_key != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key"
        )
