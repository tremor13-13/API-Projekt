from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class UserResponse(BaseModel):
    """
    Модель для валидации ответа
    """
    email: str
    name: str
    nickname: str
    avatar_url: Optional[str] = None
    uuid: UUID