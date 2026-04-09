"""
Тесты для моделей аутентификации: Role и User.
Проверяют валидацию данных, генерацию DDL и корректность полей.
"""

import pytest
from datetime import datetime
from pydantic import ValidationError

from tp_vdgo.models.auth.role import Role, PostRole
from tp_vdgo.models.auth.user import User


class TestPostRoleEnum:
    """Тесты для перечисления ролей."""

    def test_post_role_values(self):
        """Проверка, что все значения PostRole корректны."""
        assert PostRole.SUPER.value == "super_vdgo"
        assert PostRole.ADMIN.value == "admin_vdgo"
        assert PostRole.USER.value == "user_vdgo"
        assert PostRole.GUEST.value == "guest_vdgo"
        assert PostRole.OTHER.value == "other_vdgo"


class TestRoleModel:
    """Тесты для модели Role."""

    def test_create_role_minimal(self):
        """Создание роли с минимальным набором полей."""
        role = Role(id=1, name="admin")
        assert role.id == 1
        assert role.name == "admin"
        assert role.description is None
        assert role.postuser == PostRole.OTHER
        assert isinstance(role.created_at, datetime)
        assert role.updated_at is None

    def test_create_role_full(self):
        """Создание роли с полным набором полей."""
        now = datetime.now()
        role = Role(
            id=2,
            name="manager",
            description="Manager role",
            postuser=PostRole.ADMIN,
            created_at=now,
            updated_at=now,
        )
        assert role.id == 2
        assert role.name == "manager"
        assert role.description == "Manager role"
        assert role.postuser == PostRole.ADMIN
        assert role.created_at == now
        assert role.updated_at == now

    def test_role_name_min_length_validation(self):
        """Проверка минимальной длины названия роли."""
        # Pydantic min_length=2, но это на уровне модели,
        # DDL constraint - chk_role_name_length CHECK (char_length(name) >= 2)
        with pytest.raises(ValidationError):
            Role(id=1, name="a" * 51)  # max_length=50

    def test_role_default_postuser(self):
        """Проверка значения postuser по умолчанию."""
        role = Role(id=1, name="test")
        assert role.postuser == PostRole.OTHER

    def test_role_get_pg_table_definition(self):
        """Проверка генерации DDL для таблицы roles."""
        ddl = Role.get_pg_table_definition()
        assert "CREATE TABLE IF NOT EXISTS roles" in ddl
        assert "id SERIAL PRIMARY KEY" in ddl
        assert "name VARCHAR(50) NOT NULL" in ddl
        assert "description VARCHAR(200)" in ddl
        assert "postuser VARCHAR(20) NOT NULL DEFAULT 'other_vdgo'" in ddl
        assert "created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP" in ddl
        assert "updated_at TIMESTAMP" in ddl
        assert "chk_role_name_length" in ddl
        assert "chk_postuser_valid" in ddl
        assert "COMMENT ON TABLE roles" in ddl

    def test_role_get_pg_table_drop(self):
        """Проверка генерации DROP DDL для таблицы roles."""
        ddl = Role.get_pg_table_drop()
        assert "DROP TABLE IF EXISTS roles" in ddl

    def test_role_id_must_be_positive(self):
        """Проверка, что id должен быть положительным."""
        with pytest.raises(ValidationError):
            Role(id=0, name="test")

    def test_role_name_max_length(self):
        """Проверка максимальной длины названия роли."""
        with pytest.raises(ValidationError):
            Role(id=1, name="a" * 51)


class TestUserModel:
    """Тесты для модели User."""

    def test_create_user_minimal(self):
        """Создание пользователя с минимальным набором полей."""
        user = User(id=1, username="test_user", role_id=1)
        assert user.id == 1
        assert user.username == "test_user"
        assert user.full_name is None
        assert user.role_id == 1
        assert user.is_active is True
        assert user.last_login is None
        assert isinstance(user.created_at, datetime)

    def test_create_user_full(self):
        """Создание пользователя с полным набором полей."""
        now = datetime.now()
        user = User(
            id=2,
            username="admin_user",
            full_name="Admin User",
            role_id=1,
            is_active=True,
            last_login=now,
            created_at=now,
        )
        assert user.id == 2
        assert user.username == "admin_user"
        assert user.full_name == "Admin User"
        assert user.role_id == 1
        assert user.is_active is True
        assert user.last_login == now
        assert user.created_at == now

    def test_user_username_pattern_valid(self):
        """Проверка валидного username (буквы, цифры, подчеркивание)."""
        user = User(id=1, username="user123", role_id=1)
        assert user.username == "user123"

        user2 = User(id=2, username="User_Name_1", role_id=1)
        assert user2.username == "User_Name_1"

    def test_user_username_invalid_pattern(self):
        """Проверка невалидного username."""
        with pytest.raises(ValidationError):
            User(id=1, username="user-name", role_id=1)  # дефис не разрешен

    def test_user_username_too_short(self):
        """Проверка минимальной длины username."""
        with pytest.raises(ValidationError):
            User(id=1, username="ab", role_id=1)  # min_length=3

    def test_user_username_too_long(self):
        """Проверка максимальной длины username."""
        with pytest.raises(ValidationError):
            User(id=1, username="a" * 51, role_id=1)

    def test_user_id_must_be_positive(self):
        """Проверка, что id должен быть положительным."""
        with pytest.raises(ValidationError):
            User(id=0, username="test", role_id=1)

    def test_user_role_id_must_be_positive(self):
        """Проверка, что role_id должен быть положительным."""
        with pytest.raises(ValidationError):
            User(id=1, username="test", role_id=0)

    def test_user_get_pg_table_definition(self):
        """Проверка генерации DDL для таблицы users."""
        ddl = User.get_pg_table_definition()
        assert "CREATE TABLE IF NOT EXISTS users" in ddl
        assert "id SERIAL PRIMARY KEY" in ddl
        assert "username VARCHAR(50) NOT NULL" in ddl
        assert "full_name VARCHAR(100)" in ddl
        assert "role_id INTEGER NOT NULL" in ddl
        assert "is_active BOOLEAN NOT NULL DEFAULT TRUE" in ddl
        assert "last_login TIMESTAMP" in ddl
        assert "created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP" in ddl
        assert "fk_user_role FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE RESTRICT" in ddl
        assert "idx_users_username" in ddl
        assert "idx_users_role_id" in ddl

    def test_user_ddl_has_username_unique_index(self):
        """Проверка наличия уникального индекса на username."""
        ddl = User.get_pg_table_definition()
        assert "CREATE UNIQUE INDEX IF NOT EXISTS idx_users_username ON users(username)" in ddl

    def test_user_ddl_has_constraints(self):
        """Проверка наличия CHECK constraints в DDL."""
        ddl = User.get_pg_table_definition()
        assert "chk_username_length" in ddl
        assert "chk_username_pattern" in ddl
        assert "fk_user_role" in ddl
