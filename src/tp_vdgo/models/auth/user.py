from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

class User(BaseModel):
    """Модель пользователя"""
    
    id: int = Field(..., ge=1)
    username: str = Field(..., min_length=3, max_length=50, pattern=r'^[a-zA-Z0-9_]+$')
    #email: EmailStr = Field(..., description="Email пользователя")
    full_name: Optional[str] = Field(None, max_length=100)
    role_id: int = Field(..., ge=1, description="ID роли")
    is_active: bool = Field(default=True)
    last_login: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.now)

    @classmethod
    def get_pg_table_definition(cls):
        table = "users"
        return f"""
            -- Таблица пользователей
            CREATE TABLE IF NOT EXISTS {table} (
                -- Первичный ключ
                id SERIAL PRIMARY KEY,
            
                -- Имя пользователя (уникальное, 3-50 символов, только буквы/цифры/_)
                username VARCHAR(50) NOT NULL,
            
                -- Email (уникальный, валидный формат)
                -- email VARCHAR(255) NOT NULL,
            
                -- Полное имя (опционально)
                full_name VARCHAR(100),
            
                -- Внешний ключ к таблице role
                role_id INTEGER NOT NULL,
            
                -- Статус активности
                is_active BOOLEAN NOT NULL DEFAULT TRUE,
            
                -- Дата последнего входа
                last_login TIMESTAMP,
            
                -- Дата создания записи
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            
                -- Ограничения
                CONSTRAINT chk_username_length CHECK (char_length(username) >= 7),
                CONSTRAINT chk_username_pattern CHECK (username ~ '^[a-zA-Z0-9_]+$'),
                -- CONSTRAINT chk_email_format CHECK (email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
                CONSTRAINT fk_user_role FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE RESTRICT
            );

            -- Комментарии к таблице и колонкам
            COMMENT ON TABLE {table} IS 'Таблица пользователей системы';
            COMMENT ON COLUMN {table}.id IS 'Уникальный идентификатор пользователя';
            COMMENT ON COLUMN {table}.username IS 'Имя пользователя для входа (только буквы, цифры, _)';
            -- COMMENT ON COLUMN {table}.email IS 'Email пользователя (уникальный)';
            COMMENT ON COLUMN {table}.full_name IS 'Полное имя пользователя (опционально)';
            COMMENT ON COLUMN {table}.role_id IS 'ID роли (ссылка на таблицу role)';
            COMMENT ON COLUMN {table}.is_active IS 'Флаг активности пользователя';
            COMMENT ON COLUMN {table}.last_login IS 'Дата и время последнего входа';
            COMMENT ON COLUMN {table}.created_at IS 'Дата и время создания учетной записи';

            -- Уникальные индексы
            CREATE UNIQUE INDEX IF NOT EXISTS idx_users_username ON {table}(username);
            -- CREATE UNIQUE INDEX IF NOT EXISTS idx_users_email ON users(email);

            -- Обычные индексы
            CREATE INDEX IF NOT EXISTS idx_users_role_id ON {table}(role_id);
            -- CREATE INDEX IF NOT EXISTS idx_users_is_active ON users(is_active);
            -- CREATE INDEX IF NOT EXISTS idx_users_last_login ON users(last_login);
            -- CREATE INDEX IF NOT EXISTS idx_users_created_at ON users(created_at);

            -- Составные индексы для частых запросов
            -- CREATE INDEX IF NOT EXISTS idx_users_active_role ON users(is_active, role_id);
            -- CREATE INDEX IF NOT EXISTS idx_users_username_active ON users(username, is_active);
        """
    
    @classmethod
    def get_pg_pg_table_drop(cls):
        table = "users"
        return f"DROP TABLE IF EXISTS {table}"