"""
Конфигурация pytest для проекта tp_vdgo.
Содержит общие фикстуры и утилиты для тестирования.
"""

import os
import pytest
from unittest.mock import MagicMock, patch


@pytest.fixture
def mock_settings():
    """Фикстура для мока настроек."""
    settings = MagicMock()
    settings.db_host = "localhost"
    settings.db_port = "5432"
    settings.db_name = "tp_vdgo_test"
    settings.db_user = "admin"
    settings.db_pass = "testpassword"
    settings.debug = False
    return settings


@pytest.fixture
def mock_db_connection():
    """Фикстура для мока подключения к БД."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    return mock_conn, mock_cursor
