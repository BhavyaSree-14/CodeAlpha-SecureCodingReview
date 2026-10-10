"""
Tests for the secure reference implementation only.
We never execute the intentionally vulnerable functions.
"""

import os
import json
import pytest
from pathlib import Path

from app.secure_app import (
    secure_run_command,
    secure_get_db_connection,
    secure_write_temp_data,
    secure_load_data,
    secure_dump_data,
    process_message,
)
def test_secure_run_command():
    result = secure_run_command("hello world")
    assert "hello world" in result


def test_secure_get_db_connection_missing_env(monkeypatch):
    monkeypatch.delenv("APP_DB_USER", raising=False)
    monkeypatch.delenv("APP_DB_PASSWORD", raising=False)
    with pytest.raises(ValueError, match="credentials must be provided"):
        secure_get_db_connection()


def test_secure_get_db_connection_with_env(monkeypatch):
    monkeypatch.setenv("APP_DB_USER", "testuser")
    monkeypatch.setenv("APP_DB_PASSWORD", "testpass")

    conn = secure_get_db_connection()

    assert conn["user"] == "testuser"
    assert conn["credential_available"] is True
    assert "pass" not in conn
    assert "password" not in conn


def test_secure_write_temp_data():
    path_str = secure_write_temp_data("secret educational data")
    path = Path(path_str)
    assert path.exists()
    assert path.read_text() == "secret educational data"
    # Clean up
    path.unlink()


def test_secure_json_roundtrip():
    original = {"msg": "safe data", "count": 42}
    serialized = secure_dump_data(original)
    restored = secure_load_data(serialized)
    assert restored == original


def test_process_message():
    assert process_message("  hi  ") == "Processed: hi"


def test_process_message_type_error():
    with pytest.raises(TypeError):
        process_message(123)  # type: ignore
