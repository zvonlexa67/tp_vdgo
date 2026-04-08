from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional, List
from datetime import datetime
from enum import Enum

class PostRole(str, Enum):
    SUPER = "super_vdgo"
    ADMIN = "admin_vdgo"
    USER = "user_vdgo"
    GUEST = "guest_vdgo"
    OTHER = "other_vdgo"

class Role(BaseModel):
    """Модель роли"""
    # model_config = ConfigDict(
    #     from_attributes=True,  # Для работы с SQLAlchemy/ORM
    #     populate_by_name=True,  # Работа с разными именами полей
    #     json_schema_extra={
    #         "example": {
    #             "id": 1,
    #             "name": "admin",
    #             "description": "Administrator role"
    #         }
    #     }
    # )
    
    id: int = Field(..., description="ID роли", ge=1)
    name: str = Field(..., min_length=2, max_length=50, description="Название роли")
    description: Optional[str] = Field(None, max_length=200, description="Описание")
    postuser: PostRole = Field(default=PostRole.OTHER)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
