"""
Secure reference implementation.
Each function corresponds to a vulnerability shown in vulnerable_examples.py
and demonstrates the recommended remediation.
"""

import tempfile
import json
import os
from pathlib import Path

# ---------------------------------------------------------------------------
# SECURE-001: Safe subprocess usage
# ---------------------------------------------------------------------------
def secure_run_command(user_input: str) -> str:
    """Return user-provided text without executing a system command."""
    return user_input.strip()


# ---------------------------------------------------------------------------
# SECURE-002: No hardcoded credentials
# ---------------------------------------------------------------------------
def secure_get_db_connection():
    """
    Credentials are read from environment variables.
    Never store secrets in source code.
    """
    username = os.environ.get("APP_DB_USER")
    password = os.environ.get("APP_DB_PASSWORD")

    if not username or not password:
        raise ValueError(
            "Database credentials must be provided via "
            "APP_DB_USER and APP_DB_PASSWORD environment variables."
        )

    # In a real application you would return a connection object.
    # Here we simply confirm the values were loaded securely.
    return {"user": username, "credential_available": True}


# ---------------------------------------------------------------------------
# SECURE-003: Secure temporary-file handling
# ---------------------------------------------------------------------------
def secure_write_temp_data(data: str) -> str:
    """
    Uses the tempfile module with secure defaults:
    - Unique, unpredictable name
    - File created with restrictive permissions (0600 on Unix)
    - Automatically cleaned up when the context exits (or caller can manage)
    """
    # NamedTemporaryFile with delete=False so the path can be returned;
    # the caller is responsible for unlinking when finished.
    with tempfile.NamedTemporaryFile(
        mode="w",
        prefix="myapp_",
        suffix=".txt",
        delete=False,
    ) as tmp:
        tmp.write(data)
        temp_path = tmp.name

    # Explicitly set restrictive permissions (best effort on all platforms)
    try:
        os.chmod(temp_path, 0o600)
    except OSError:
        pass  # Windows may not support the same mode bits

    return temp_path


# ---------------------------------------------------------------------------
# SECURE-004: Safe data exchange (JSON instead of pickle)
# ---------------------------------------------------------------------------
def safe_deserialize(serialized: bytes):
    """Safely parse JSON data instead of untrusted pickle data."""
    text = serialized.decode("utf-8")
    return json.loads(text)

def secure_load_data(serialized: str):
    """
    Use a safe, data-only format such as JSON.
    Never unpickle untrusted data.
    """
    return json.loads(serialized)


def secure_dump_data(obj) -> str:
    """Companion serializer using JSON."""
    return json.dumps(obj)


# ---------------------------------------------------------------------------
# Small helper used by tests
# ---------------------------------------------------------------------------
def process_message(message: str) -> str:
    """Example of a normal, safe application function."""
    if not isinstance(message, str):
        raise TypeError("message must be a string")
    return f"Processed: {message.strip()}"
