"""
Тесты для операций с БД: создание/удаление пользователей, БД, таблиц auth.
Используют моки для изоляции от реальной БД.
"""

import pytest
from unittest.mock import MagicMock, patch, call

from tp_vdgo.core.db.createuser import createusers
from tp_vdgo.core.db.dropusers import dropusers
from tp_vdgo.core.db.createdb import createdb
from tp_vdgo.core.db.dropdb import dropdb
from tp_vdgo.core.auth.auth import Auth
from tp_vdgo.models.auth.role import Role
from tp_vdgo.models.auth.user import User


class TestCreateUsers:
    """Тесты для функции createusers."""

    @patch("tp_vdgo.core.db.createuser.testdb")
    @patch("tp_vdgo.core.db.createuser.db")
    def test_createusers_creates_all_roles(self, mock_db_cls, mock_testdb):
        """Проверка, что createusers создает все 5 ролей."""
        mock_testdb.return_value = True

        mock_db = MagicMock()
        mock_db_cls.return_value = mock_db
        mock_db.settings.users = [
            MagicMock(puser="super_vdgo", passwd="pass1"),
            MagicMock(puser="admin_vdgo", passwd="pass2"),
            MagicMock(puser="user_vdgo", passwd="pass3"),
            MagicMock(puser="guest_vdgo", passwd="pass4"),
            MagicMock(puser="other_vdgo", passwd="pass5"),
        ]

        mock_cursor = MagicMock()
        mock_db.cursor.return_value.__enter__.return_value = mock_cursor

        createusers()

        assert mock_cursor.execute.call_count == 5
        mock_testdb.assert_called_with("template1")
        assert mock_db.dbname == "template1"

    @patch("tp_vdgo.core.db.createuser.testdb")
    def test_createusers_skips_if_testdb_false(self, mock_testdb):
        """Проверка, что createusers не выполняется, если testdb возвращает False."""
        mock_testdb.return_value = False

        createusers()

        mock_testdb.assert_called_with("template1")


class TestDropUsers:
    """Тесты для функции dropusers."""

    @patch("tp_vdgo.core.db.dropusers.testdb")
    @patch("tp_vdgo.core.db.dropusers.db")
    def test_dropusers_drops_all_roles(self, mock_db_cls, mock_testdb):
        """Проверка, что dropusers удаляет все 5 ролей."""
        mock_testdb.return_value = True

        mock_db = MagicMock()
        mock_db_cls.return_value = mock_db
        mock_db.settings.users = [
            MagicMock(puser="super_vdgo", passwd="pass1"),
            MagicMock(puser="admin_vdgo", passwd="pass2"),
        ]

        mock_cursor = MagicMock()
        mock_db.cursor.return_value.__enter__.return_value = mock_cursor

        dropusers()

        assert mock_cursor.execute.call_count == 2
        assert "DROP USER IF EXISTS super_vdgo" in mock_cursor.execute.call_args_list[0][0][0]
        assert "DROP USER IF EXISTS admin_vdgo" in mock_cursor.execute.call_args_list[1][0][0]

    @patch("tp_vdgo.core.db.dropusers.testdb")
    def test_dropusers_skips_if_testdb_false(self, mock_testdb):
        """Проверка, что dropusers не выполняется, если testdb возвращает False."""
        mock_testdb.return_value = False

        dropusers()

        mock_testdb.assert_called_with("template1")


class TestCreateDB:
    """Тесты для функции createdb."""

    @patch("tp_vdgo.core.db.createdb.testdb")
    @patch("tp_vdgo.core.db.createdb.db")
    def test_createdb_creates_database(self, mock_db_cls, mock_testdb):
        """Проверка, что createdb создает БД."""
        mock_testdb.side_effect = lambda dbname=None, exp=True: dbname == "template1"

        mock_db = MagicMock()
        mock_db_cls.return_value = mock_db
        mock_db.settings.db_name = "tp_vdgo_test"
        mock_db.settings.super_vdgo = MagicMock(puser="super_vdgo", passwd="pass")

        mock_cursor = MagicMock()
        mock_db.cursor.return_value.__enter__.return_value = mock_cursor

        createdb()

        mock_db.cursor.assert_called_once_with(autocommit=True)
        mock_cursor.execute.assert_called_once_with("CREATE DATABASE tp_vdgo_test;")

    @patch("tp_vdgo.core.db.createdb.testdb")
    def test_createdb_skips_if_db_exists(self, mock_testdb):
        """Проверка, что createdb не выполняется, если БД уже существует."""
        mock_testdb.return_value = True  # БД уже существует

        createdb()

        # Функция должна выйти на первой проверке: not testdb(exp=False) == False
        assert mock_testdb.call_count >= 1


class TestDropDB:
    """Тесты для функции dropdb."""

    @patch("tp_vdgo.core.db.dropdb.testdb")
    @patch("tp_vdgo.core.db.dropdb.db")
    def test_dropdb_drops_database(self, mock_db_cls, mock_testdb):
        """Проверка, что dropdb удаляет БД."""
        mock_testdb.return_value = True

        mock_db = MagicMock()
        mock_db_cls.return_value = mock_db
        mock_db.settings.db_name = "tp_vdgo_test"

        mock_cursor = MagicMock()
        mock_db.cursor.return_value.__enter__.return_value = mock_cursor

        dropdb()

        mock_cursor.execute.assert_called_once_with("DROP DATABASE tp_vdgo_test;")

    @patch("tp_vdgo.core.db.dropdb.testdb")
    def test_dropdb_skips_if_testdb_false(self, mock_testdb):
        """Проверка, что dropdb не выполняется, если testdb возвращает False."""
        mock_testdb.return_value = False

        dropdb()

        mock_testdb.assert_called_with("template1")


class TestAuthCreate:
    """Тесты для класса Auth (create)."""

    @patch("tp_vdgo.core.auth.auth.db")
    def test_auth_create_executes_ddl(self, mock_db_cls):
        """Проверка, что Auth.create() выполняет DDL для Role и User."""
        mock_db = MagicMock()
        mock_db_cls.return_value = mock_db
        mock_db.settings = MagicMock()
        mock_db.settings.super_vdgo = MagicMock(puser="super_vdgo", passwd="pass")

        mock_cursor = MagicMock()
        mock_db.cursor.return_value.__enter__.return_value = mock_cursor

        auth = Auth()
        auth.create()

        assert mock_cursor.execute.call_count == 2

        # Проверяем порядок: сначала Role (т.к. User ссылается на Role через FK)
        first_call = mock_cursor.execute.call_args_list[0][0][0]
        second_call = mock_cursor.execute.call_args_list[1][0][0]

        assert "CREATE TABLE IF NOT EXISTS roles" in first_call
        assert "CREATE TABLE IF NOT EXISTS users" in second_call


class TestAuthDrop:
    """Тесты для класса Auth (drop)."""

    @patch("tp_vdgo.core.auth.auth.db")
    def test_auth_drop_executes_ddl(self, mock_db_cls):
        """Проверка, что Auth.drop() выполняет DROP для User и Role."""
        mock_db = MagicMock()
        mock_db_cls.return_value = mock_db
        mock_db.settings = MagicMock()
        mock_db.settings.super_vdgo = MagicMock(puser="super_vdgo", passwd="pass")

        mock_cursor = MagicMock()
        mock_db.cursor.return_value.__enter__.return_value = mock_cursor

        auth = Auth()
        auth.drop()

        assert mock_cursor.execute.call_count == 2

        # Проверяем порядок: сначала User (т.к. ссылается на Role через FK)
        first_call = mock_cursor.execute.call_args_list[0][0][0]
        second_call = mock_cursor.execute.call_args_list[1][0][0]

        assert "DROP TABLE IF EXISTS users" in first_call
        assert "DROP TABLE IF EXISTS roles" in second_call


class TestDbClass:
    """Тесты для класса db."""

    @patch("tp_vdgo.core.db.db.Settings")
    def test_db_initializes_with_default_settings(self, mock_settings_cls):
        """Проверка инициализации db с настройками по умолчанию."""
        from tp_vdgo.core.db.db import db

        mock_settings = MagicMock()
        mock_settings.db_host = "localhost"
        mock_settings.db_port = "5432"
        mock_settings.db_name = "tp_vdgo"
        mock_settings.db_user = "admin"
        mock_settings.db_pass = "password"
        mock_settings_cls.return_value = mock_settings

        # При создании экземпляра вызывается conn_params, который использует __db_host и т.д.
        db_instance = db()

        assert db_instance.host == "localhost"
        assert db_instance.port == "5432"
        assert db_instance.dbname == "tp_vdgo"
        assert db_instance.user == "admin"
        assert db_instance.passwd == "password"

    @patch("tp_vdgo.core.db.db.Settings")
    def test_db_host_setter_updates_conn_params(self, mock_settings_cls):
        """Проверка, что сеттер host обновляет conn_params."""
        from tp_vdgo.core.db.db import db

        mock_settings = MagicMock()
        mock_settings.db_host = "localhost"
        mock_settings.db_port = "5432"
        mock_settings.db_name = "tp_vdgo"
        mock_settings.db_user = "admin"
        mock_settings.db_pass = "password"
        mock_settings_cls.return_value = mock_settings

        db_instance = db()
        db_instance.host = "newhost"

        assert db_instance.host == "newhost"

    @patch("tp_vdgo.core.db.db.Settings")
    def test_db_params_returns_string(self, mock_settings_cls):
        """Проверка, что params возвращает строку подключения."""
        from tp_vdgo.core.db.db import db

        mock_settings = MagicMock()
        mock_settings.db_host = "localhost"
        mock_settings.db_port = "5432"
        mock_settings.db_name = "tp_vdgo"
        mock_settings.db_user = "admin"
        mock_settings.db_pass = "password"
        mock_settings_cls.return_value = mock_settings

        db_instance = db()
        params = db_instance.params

        assert isinstance(params, str)
        assert "host=localhost" in params
        assert "port=5432" in params
        assert "dbname=tp_vdgo" in params
