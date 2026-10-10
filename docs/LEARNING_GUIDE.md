# Learning Guide – Secure Coding Review

This guide explains every major concept used in the project in beginner-friendly language.

---

## 1. What is a Security Audit (Static Analysis)?

A **static security analysis** looks at source code *without running it*.  
Tools such as Bandit read Python files and look for known dangerous patterns (hardcoded passwords, `shell=True`, `pickle.loads`, etc.).

It is **not** a penetration test. It cannot prove that an application is safe; it only highlights places that *might* be risky.

---

## 2. Bandit

Bandit is an open-source tool maintained by the Python Code Quality Authority (PyCQA).  
It walks through every `.py` file and applies a set of rules (called “plugins”).

Common Bandit issue IDs you will see in this project:

| ID   | Meaning                                      | Severity |
|------|----------------------------------------------|----------|
| B602 | `subprocess` with `shell=True`               | High     |
| B105 | Hardcoded password string                    | Low/Med  |
| B301 | Use of `pickle`                              | Medium   |
| B306 | Use of `tempfile.mktemp` (or similar patterns)| Medium   |

You run it with:

```powershell
bandit -r app/
```

---

## 3. The Four Vulnerabilities Explained

### VULN-001 – Command Injection via `subprocess` + `shell=True`

**What happens**  
When you write:

```python
subprocess.Popen(f"echo {user_input}", shell=True)
```

the operating system’s shell interprets the whole string.  
If `user_input` contains `; rm -rf /` (or any other shell metacharacters), those commands also run.

**Why it matters**  
An attacker who can control the input can execute arbitrary commands on the server.

**Safe alternative**  
Pass arguments as a *list* and never set `shell=True`:

```python
subprocess.run(["echo", user_input], ...)
```

---

### VULN-002 – Hardcoded Credentials

**What happens**  
A password or API key is written directly in the source code:

```python
password = "SuperSecret123!"
```

Anyone who can read the repository (or a leaked backup) now knows the secret.

**Why it matters**  
Secrets should live in environment variables, a secrets manager, or an encrypted vault—not in Git.

**Safe alternative**  
Read from the environment:

```python
password = os.environ["APP_DB_PASSWORD"]
```

---

### VULN-003 – Insecure Temporary Files

**What happens**  
Creating a file with a fixed, predictable name:

```python
temp_path = "/tmp/myapp_secret_data.txt"
```

Another process on the same machine can create a symlink with that name *before* your program runs (a race condition).  
The file may also be world-readable.

**Why it matters**  
Sensitive data can be stolen or overwritten by another user on a multi-user system.

**Safe alternative**  
Use the `tempfile` module, which creates files with random names and restrictive permissions:

```python
with tempfile.NamedTemporaryFile(...) as tmp:
    ...
```

---

### VULN-004 – Unsafe Deserialization (`pickle`)

**What happens**  
`pickle.loads(data)` can execute arbitrary Python code while it reconstructs an object.  
If an attacker supplies the bytes, they can run any code they want.

**Why it matters**  
This is a classic remote-code-execution (RCE) vector.

**Safe alternative**  
Use a data-only format such as JSON, MessagePack, or Protocol Buffers:

```python
json.loads(data)
```

---

## 4. Severity Ratings (Quick Reference)

| Rating | Meaning                                      |
|--------|----------------------------------------------|
| High   | Can lead to remote code execution or full compromise |
| Medium | Significant impact under realistic conditions |
| Low    | Limited impact or requires unusual conditions |
| Info   | Best-practice recommendation, not a direct vuln |

---

## 5. How to Read a Finding

Every finding in the security report has:

- **ID** – unique identifier (e.g. VULN-001)
- **Vulnerability** – short name
- **Severity** – High / Medium / Low
- **Affected file / line** – exact location
- **Evidence** – the code snippet or Bandit message
- **Impact** – what an attacker could achieve
- **Remediation** – how to fix it

---

## 6. Ethical Use

- These examples exist **only** for learning.
- Never run the vulnerable functions against real systems or networks.
- Never commit real secrets into source control.
- When you find a real vulnerability in someone else’s code, follow responsible disclosure.

---

## 7. Next Steps After This Project

1. Run Bandit on any Python project you write.
2. Learn about additional tools: `safety` (dependency checking), `semgrep`, `pip-audit`.
3. Read the OWASP Top 10 and the Python-specific guidance on the OWASP site.
4. Practice fixing findings one by one and re-running the scanner.
