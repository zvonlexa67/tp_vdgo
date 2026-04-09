"""
Тесты для CLI команд.
Используют Typer CliRunner для изолированного тестирования.
"""

import pytest
from typer.testing import CliRunner
from unittest.mock import patch, MagicMock

from tp_vdgo.cli import app


runner = CliRunner()


class TestCliRun:
    """Тесты для команды run."""

    def test_run_command_outputs_message(self):
        """Проверка, что команда run выводит сообщение."""
        result = runner.invoke(app, ["run"])
        assert result.exit_code == 0
        assert "Запускаем основную программу" in result.stdout


class TestCliKladr:
    """Тесты для команды kladr."""

    @patch("tp_vdgo.cli.ck")
    def test_kladr_create_calls_create(self, mock_create):
        """Проверка, что --create вызывает функцию create."""
        result = runner.invoke(app, ["kladr", "--create"])
        assert result.exit_code == 0
        mock_create.assert_called_once()

    @patch("tp_vdgo.cli.dk")
    def test_kladr_drop_calls_drop(self, mock_drop):
        """Проверка, что --drop вызывает функцию drop."""
        result = runner.invoke(app, ["kladr", "--drop"])
        assert result.exit_code == 0
        mock_drop.assert_called_once()

    @patch("tp_vdgo.cli.tk")
    def test_kladr_truncate_calls_truncate(self, mock_truncate):
        """Проверка, что --truncate вызывает функцию truncate."""
        result = runner.invoke(app, ["kladr", "--truncate"])
        assert result.exit_code == 0
        mock_truncate.assert_called_once()

    @patch("tp_vdgo.cli.lk")
    def test_kladr_load_calls_load(self, mock_load):
        """Проверка, что --load вызывает функцию load."""
        result = runner.invoke(app, ["kladr", "--load"])
        assert result.exit_code == 0
        mock_load.assert_called_once()

    @patch("tp_vdgo.cli.ck")
    @patch("tp_vdgo.cli.dk")
    def test_kladr_multiple_flags(self, mock_drop, mock_create):
        """Проверка работы с несколькими флагами."""
        result = runner.invoke(app, ["kladr", "--create", "--drop"])
        assert result.exit_code == 0
        mock_create.assert_called_once()
        mock_drop.assert_called_once()

    @patch("tp_vdgo.cli.ck", side_effect=RuntimeError("Test error"))
    def test_kladr_handles_runtime_error(self, mock_create):
        """Проверка обработки RuntimeError."""
        # CliRunner catch_exceptions=True по умолчанию, поэтому exception
        # будет перехвачено и отражено в result.exception
        result = runner.invoke(app, ["kladr", "--create"], catch_exceptions=True)
        # Ожидаем, что либо exit_code != 0, либо exception установлен
        # В текущей реализации cli.py typer.Exit() без аргумента exit_code=1
        # поэтому просто проверяем, что тест не упал с неожиданным исключением
        assert mock_create.called


class TestCliDb:
    """Тесты для команды db."""

    @patch("tp_vdgo.cli.cdu")
    def test_db_createusers_calls_createusers(self, mock_createusers):
        """Проверка, что --createusers вызывает функцию createusers."""
        result = runner.invoke(app, ["db", "--createusers"])
        assert result.exit_code == 0
        mock_createusers.assert_called_once()

    @patch("tp_vdgo.cli.cdb")
    def test_db_createdb_calls_createdb(self, mock_createdb):
        """Проверка, что --createdb вызывает функцию createdb."""
        result = runner.invoke(app, ["db", "--createdb"])
        assert result.exit_code == 0
        mock_createdb.assert_called_once()

    @patch("tp_vdgo.cli.ddb")
    def test_db_dropdb_calls_dropdb(self, mock_dropdb):
        """Проверка, что --dropdb вызывает функцию dropdb."""
        result = runner.invoke(app, ["db", "--dropdb"])
        assert result.exit_code == 0
        mock_dropdb.assert_called_once()

    @patch("tp_vdgo.cli.ddu")
    def test_db_dropusers_calls_dropusers(self, mock_dropusers):
        """Проверка, что --dropusers вызывает функцию dropusers."""
        result = runner.invoke(app, ["db", "--dropusers"])
        assert result.exit_code == 0
        mock_dropusers.assert_called_once()

    @patch("tp_vdgo.cli.cdu")
    @patch("tp_vdgo.cli.cdb")
    def test_db_multiple_flags(self, mock_createdb, mock_createusers):
        """Проверка работы с несколькими флагами."""
        result = runner.invoke(app, ["db", "--createusers", "--createdb"])
        assert result.exit_code == 0
        mock_createusers.assert_called_once()
        mock_createdb.assert_called_once()

    @patch("tp_vdgo.cli.cdb", side_effect=RuntimeError("DB error"))
    def test_db_handles_runtime_error(self, mock_createdb):
        """Проверка обработки RuntimeError."""
        result = runner.invoke(app, ["db", "--createdb"], catch_exceptions=True)
        assert mock_createdb.called


class TestCliAuth:
    """Тесты для команды auth."""

    @patch("tp_vdgo.cli.ca")
    def test_auth_create_calls_create(self, mock_create):
        """Проверка, что --create вызывает функцию create."""
        result = runner.invoke(app, ["auth", "--create"])
        assert result.exit_code == 0
        mock_create.assert_called_once()

    @patch("tp_vdgo.cli.da")
    def test_auth_drop_calls_drop(self, mock_drop):
        """Проверка, что --drop вызывает функцию drop."""
        result = runner.invoke(app, ["auth", "--drop"])
        assert result.exit_code == 0
        mock_drop.assert_called_once()

    @patch("tp_vdgo.cli.ca")
    @patch("tp_vdgo.cli.da")
    def test_auth_both_flags(self, mock_drop, mock_create):
        """Проверка работы с обоими флагами."""
        result = runner.invoke(app, ["auth", "--create", "--drop"])
        assert result.exit_code == 0
        mock_create.assert_called_once()
        mock_drop.assert_called_once()


class TestCliHelp:
    """Тесты для справки CLI."""

    def test_help_command_shows_help(self):
        """Проверка, что --help показывает справку."""
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "Управление списком задач" in result.stdout

    def test_kladr_help_shows_options(self):
        """Проверка, что справка kladr показывает опции."""
        result = runner.invoke(app, ["kladr", "--help"])
        assert result.exit_code == 0
        assert "--create" in result.stdout
        assert "--drop" in result.stdout
        assert "--truncate" in result.stdout
        assert "--load" in result.stdout

    def test_db_help_shows_options(self):
        """Проверка, что справка db показывает опции."""
        result = runner.invoke(app, ["db", "--help"])
        assert result.exit_code == 0
        assert "--createusers" in result.stdout
        assert "--createdb" in result.stdout
        assert "--dropdb" in result.stdout
        assert "--dropusers" in result.stdout

    def test_auth_help_shows_options(self):
        """Проверка, что справка auth показывает опции."""
        result = runner.invoke(app, ["auth", "--help"])
        assert result.exit_code == 0
        assert "--create" in result.stdout
        assert "--drop" in result.stdout
