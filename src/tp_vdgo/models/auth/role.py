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

    @classmethod
    def get_pg_table_definition(cls):
        table = "roles"
        return f"""
            -- Таблица ролей
            CREATE TABLE IF NOT EXISTS {table} (
            -- Первичный ключ (автоинкремент)
            id SERIAL PRIMARY KEY,
            
            -- Название роли (обязательное, от 2 до 50 символов)
            name VARCHAR(50) NOT NULL,
            
            -- Описание роли (опциональное, до 200 символов)
            description VARCHAR(200),
            
            -- Тип пользователя (обязательное, значение по умолчанию 'other_vdgo')
            postuser VARCHAR(20) NOT NULL DEFAULT 'other_vdgo',
            
            -- Дата создания (автоматически устанавливается при вставке)
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            
            -- Дата обновления (обновляется вручную или триггером)
            updated_at TIMESTAMP,
            
            -- Ограничения (constraints)
            CONSTRAINT chk_role_name_length CHECK (char_length(name) >= 2),
            CONSTRAINT chk_postuser_valid CHECK (postuser IN ('super_vdgo', 'admin_vdgo', 'user_vdgo', 'guest_vdgo', 'other_vdgo'))
        );

        -- Комментарии к столбцам (документация)
        COMMENT ON TABLE {table} IS 'Таблица ролей пользователей';
        COMMENT ON COLUMN {table}.id IS 'ID роли (автоинкремент)';
        COMMENT ON COLUMN {table}.name IS 'Название роли (2-50 символов)';
        COMMENT ON COLUMN {table}.description IS 'Описание роли (опционально)';
        COMMENT ON COLUMN {table}.postuser IS 'Тип пользователя: super_vdgo, admin_vdgo, user_vdgo, guest_vdgo, other_vdgo';
        COMMENT ON COLUMN {table}.created_at IS 'Дата и время создания записи';
        COMMENT ON COLUMN {table}.updated_at IS 'Дата и время последнего обновления';
        """
    
    @classmethod
    def get_pg_table_drop(cls):
        table = "roles"
        return f"DROP TABLE IF EXISTS {table};"