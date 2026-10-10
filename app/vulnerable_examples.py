"""
INTENTIONALLY VULNERABLE CODE - EDUCATIONAL USE ONLY
=====================================================
This file contains deliberately insecure patterns for learning purposes.
These functions are NEVER called automatically by the application.
Do not import or execute these functions in production or against real systems.
All examples use harmless, local, controlled inputs only.
"""

import subprocess
import tempfile
import pickle
import os


# ---------------------------------------------------------------------------
# VULN-001: Unsafe subprocess usage (command injection risk)
# ---------------------------------------------------------------------------
def vulnerable_run_command(user_input: str) -> str:
    """
    INTENTIONALLY VULNERABLE: Passes unsanitized user input to shell=True.
    Bandit finding: B602 (subprocess_popen_with_shell_equals_true)
    Safe demonstration only – do not pass real shell metacharacters.
    """
    # DANGEROUS: shell=True + untrusted input
    result = subprocess.Popen(
        f"echo {user_input}",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    stdout, _ = result.communicate()
    return stdout.strip()
 


# ---------------------------------------------------------------------------
# VULN-002: Hardcoded credentials
# ---------------------------------------------------------------------------
def vulnerable_get_db_connection():
    """
    INTENTIONALLY VULNERABLE: Hardcoded username and password in source.
    Bandit finding: B105 (hardcoded_password_string)
    These credentials are fake and point nowhere.
    """
    # DANGEROUS: secrets in source code
    username = "admin"
    password = "SuperSecret123!"  # noqa: S105 – intentional for demo
    # In a real app this would connect; here we just return the values
    return {"user": username, "pass": password}


# ---------------------------------------------------------------------------
# VULN-003: Weak temporary-file handling
# ---------------------------------------------------------------------------
def vulnerable_write_temp_data(data: str) -> str:
    """
    INTENTIONALLY VULNERABLE: Predictable temp file name + insecure permissions.
    Bandit finding: B306 (mktemp_q) / related insecure tempfile patterns
    Uses a fixed name in /tmp which is race-condition prone.
    """
    # DANGEROUS: predictable path, no secure creation
    temp_path = "/tmp/myapp_secret_data.txt"
    with open(temp_path, "w") as f:
        f.write(data)
    # Permissions left world-readable on many systems
    return temp_path


# ---------------------------------------------------------------------------
# VULN-004: Unsafe deserialization
# ---------------------------------------------------------------------------
def vulnerable_load_data(serialized: bytes):
    """
    INTENTIONALLY VULNERABLE: Untrusted pickle.loads().
    Bandit finding: B301 (pickle)
    Only ever call with data you yourself just pickled in the same process.
    Never unpickle data from the network or untrusted sources.
    """
    # DANGEROUS: pickle can execute arbitrary code during load
    return pickle.loads(serialized)


# ---------------------------------------------------------------------------
# Helper used only for safe local demonstration of the pickle issue
# ---------------------------------------------------------------------------
def _safe_demo_pickle_roundtrip():
    """Creates a harmless pickle payload and immediately loads it.
    This is the ONLY safe way to illustrate the call site.
    """
    harmless = {"message": "hello from educational demo"}
    payload = pickle.dumps(harmless)
    return vulnerable_load_data(payload)


if __name__ == "__main__":
    print("=" * 60)
    print("This module is for static analysis and education only.")
    print("It does NOT execute any vulnerable functions by default.")
    print("Run Bandit against this file to see the findings.")
    print("=" * 60)
