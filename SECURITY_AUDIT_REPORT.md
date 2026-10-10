# Security Audit Report  
**Project:** CodeAlpha_SecureCodingReview  
**Date:** 2026-10-10  
**Author:** Educational static-analysis exercise  
**Classification:** Training material only – not a professional penetration test

---

## 1. Scope and Methodology

### Scope
- Source files under `app/`
- Focus on four intentionally introduced educational vulnerabilities:
  1. Unsafe subprocess usage
  2. Hardcoded credentials
  3. Weak temporary-file handling
  4. Unsafe deserialization

### Methodology
1. Manual code review of `app/vulnerable_examples.py` and `app/secure_app.py`.
2. Static analysis with **Bandit** (PyCQA) using the command:
   ```
   bandit -r app/ -f txt
   ```
3. Comparison of vulnerable vs. secure implementations.
4. Verification that the secure functions pass unit tests (see `tests/`).

**Important disclaimer**  
This is a controlled educational exercise. Bandit (and static analysis in general) cannot detect every possible vulnerability. The findings below are limited to the patterns deliberately placed in the sample code. No dynamic testing, network scanning, or exploitation of real systems was performed.

---

## 2. Tools Used

| Tool          | Version / Notes                     | Purpose                          |
|---------------|-------------------------------------|----------------------------------|
| Bandit        | Latest available via pip            | Python static security analysis  |
| pytest        | Latest available via pip            | Unit tests for secure functions  |
| Python 3      | Standard library only for the app   | Runtime                          |
| Manual review | —                                   | Context and remediation design   |

---

## 3. Findings Table

| ID       | Vulnerability                        | Severity | Affected File / Line                          | Evidence (Bandit / Manual)                          | Impact                                                                 | Remediation                                      |
|----------|--------------------------------------|----------|-----------------------------------------------|-----------------------------------------------------|------------------------------------------------------------------------|--------------------------------------------------|
| VULN-001 | Command injection via shell=True     | High     | `app/vulnerable_examples.py` – `vulnerable_run_command` | Bandit B602: subprocess_popen_with_shell_equals_true | Attacker-controlled input can execute arbitrary OS commands            | Use `subprocess.run([...], shell=False)`         |
| VULN-002 | Hardcoded credentials                | Medium   | `app/vulnerable_examples.py` – `vulnerable_get_db_connection` | Bandit B105: hardcoded_password_string             | Secrets visible in source / version control                            | Load from environment variables or secret store  |
| VULN-003 | Insecure temporary file              | Medium   | `app/vulnerable_examples.py` – `vulnerable_write_temp_data` | Manual + related Bandit tempfile rules (predictable path) | Race condition / data leakage on multi-user systems                    | Use `tempfile.NamedTemporaryFile`                |
| VULN-004 | Unsafe deserialization (pickle)      | High     | `app/vulnerable_examples.py` – `vulnerable_load_data` | Bandit B301: pickle                                 | Arbitrary code execution if untrusted data is unpickled                | Use JSON (or another data-only format)           |

> **Note:** Exact line numbers and Bandit confidence scores will appear when you run the scanner yourself. The table above maps each intentional pattern to the corresponding Bandit rule ID.

---

## 4. Before-and-After Code Examples

### VULN-001 – Subprocess

**Before (vulnerable)**
```python
result = subprocess.Popen(
    f"echo {user_input}",
    shell=True,
    ...
)
```

**After (secure)**
```python
result = subprocess.run(
    ["echo", user_input],
    capture_output=True,
    text=True,
    check=True,
    timeout=5,
)
```

### VULN-002 – Credentials

**Before**
```python
username = "admin"
password = "SuperSecret123!"
```

**After**
```python
username = os.environ.get("APP_DB_USER")
password = os.environ.get("APP_DB_PASSWORD")
if not username or not password:
    raise ValueError("...")
```

### VULN-003 – Temporary files

**Before**
```python
temp_path = "/tmp/myapp_secret_data.txt"
with open(temp_path, "w") as f:
    f.write(data)
```

**After**
```python
with tempfile.NamedTemporaryFile(mode="w", prefix="myapp_", suffix=".txt", delete=False) as tmp:
    tmp.write(data)
    temp_path = tmp.name
os.chmod(temp_path, 0o600)  # best-effort restrictive permissions
```

### VULN-004 – Deserialization

**Before**
```python
return pickle.loads(serialized)
```

**After**
```python
return json.loads(serialized)
```

---

## 5. How to Reproduce Findings Safely

1. Open a terminal in the project root.
2. Install Bandit (see README).
3. Run:
   ```powershell
   bandit -r app/ -f txt
   ```
4. Observe the issues reported against `vulnerable_examples.py`.
5. Confirm that `secure_app.py` produces far fewer (or zero) high/medium findings for the same patterns.

**Never** call the functions inside `vulnerable_examples.py` with untrusted input or against real systems.

---

## 6. Limitations

- Static analysis only – no runtime or network testing.
- Only the four educational patterns were examined.
- Bandit may produce false positives or miss context-specific issues.
- The secure examples demonstrate good practices but are not a complete application security program.
- This report does **not** constitute a professional penetration test or formal security certification.

---

## 7. Conclusion

The sample application successfully demonstrates four common Python security pitfalls and their corresponding fixes. By keeping the vulnerable code isolated, clearly labelled, and never executed automatically, the project remains safe for educational use while still producing real, reproducible Bandit findings.

Students should:

1. Run Bandit themselves and match the output to the table above.
2. Read the secure counterparts side-by-side.
3. Study the Learning Guide for deeper explanations.
4. Apply the same review process to their own future code.
