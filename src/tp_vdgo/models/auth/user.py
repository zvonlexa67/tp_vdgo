from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

class User(BaseModel):
    """Модель пользователя"""
    # model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(..., ge=1)
    username: str = Field(..., min_length=3, max_length=50, pattern=r'^[a-zA-Z0-9_]+$')
    email: EmailStr = Field(..., description="Email пользователя")
    full_name: Optional[str] = Field(None, max_length=100)
    role_id: int = Field(..., ge=1, description="ID роли")
    is_active: bool = Field(default=True)
    last_login: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.now)