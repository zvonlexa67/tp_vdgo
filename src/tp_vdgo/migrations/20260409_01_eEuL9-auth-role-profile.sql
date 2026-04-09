-- Auth Role Profile
-- depends: 20260406_01_LAooh-inital-schema-kladr

-- Таблица ролей
CREATE TABLE IF NOT EXISTS roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description VARCHAR(200),
    postuser VARCHAR(20) NOT NULL DEFAULT 'other_vdgo',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    CONSTRAINT chk_role_name_length CHECK (char_length(name) >= 2),
    CONSTRAINT chk_postuser_valid CHECK (postuser IN ('super_vdgo', 'admin_vdgo', 'user_vdgo', 'guest_vdgo', 'other_vdgo'))
);

COMMENT ON TABLE roles IS 'Таблица ролей пользователей';
COMMENT ON COLUMN roles.id IS 'ID роли (автоинкремент)';
COMMENT ON COLUMN roles.name IS 'Название роли (2-50 символов)';
COMMENT ON COLUMN roles.description IS 'Описание роли (опционально)';
COMMENT ON COLUMN roles.postuser IS 'Тип пользователя: super_vdgo, admin_vdgo, user_vdgo, guest_vdgo, other_vdgo';
COMMENT ON COLUMN roles.created_at IS 'Дата и время создания записи';
COMMENT ON COLUMN roles.updated_at IS 'Дата и время последнего обновления';

-- Таблица пользователей
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    full_name VARCHAR(100),
    role_id INTEGER NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    last_login TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_username_length CHECK (char_length(username) >= 3),
    CONSTRAINT chk_username_pattern CHECK (username ~ '^[a-zA-Z0-9_]+$'),
    CONSTRAINT fk_user_role FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE RESTRICT
);

COMMENT ON TABLE users IS 'Таблица пользователей системы';
COMMENT ON COLUMN users.id IS 'Уникальный идентификатор пользователя';
COMMENT ON COLUMN users.username IS 'Имя пользователя для входа (только буквы, цифры, _)';
COMMENT ON COLUMN users.full_name IS 'Полное имя пользователя (опционально)';
COMMENT ON COLUMN users.role_id IS 'ID роли (ссылка на таблицу roles)';
COMMENT ON COLUMN users.is_active IS 'Флаг активности пользователя';
COMMENT ON COLUMN users.last_login IS 'Дата и время последнего входа';
COMMENT ON COLUMN users.created_at IS 'Дата и время создания учетной записи';

-- Уникальные индексы
CREATE UNIQUE INDEX IF NOT EXISTS idx_users_username ON users(username);

-- Обычные индексы
CREATE INDEX IF NOT EXISTS idx_users_role_id ON users(role_id);
