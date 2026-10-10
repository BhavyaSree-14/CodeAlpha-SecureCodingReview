# CodeAlpha_SecureCodingReview

Educational project for the CodeAlpha Cyber Security Internship – Task 3: Secure Coding Review.

A small, self-contained Python sample that demonstrates common insecure patterns, shows how Bandit detects them, and provides clean secure alternatives.

> **This is a learning exercise only.**  
> It is **not** a professional penetration test and does **not** claim to find every possible vulnerability.

---

## Project Structure

```
CodeAlpha_SecureCodingReview/
├── app/
│   ├── __init__.py
│   ├── vulnerable_examples.py   # Intentionally vulnerable (never auto-executed)
│   └── secure_app.py            # Fixed versions of the same patterns
├── examples/
│   └── README.md
├── tests/
│   └── test_secure.py           # Tests for the secure functions only
├── docs/
│   └── LEARNING_GUIDE.md        # Beginner-friendly explanations
├── README.md                    # This file
├── SECURITY_AUDIT_REPORT.md     # Full audit report
├── requirements.txt
└── .gitignore
```

---

## Quick Setup (Windows + VS Code + PowerShell)

### 1. Open the project
- Open VS Code.
- File → Open Folder → select the `CodeAlpha_SecureCodingReview` folder.

### 2. Create a virtual environment
Open the integrated PowerShell terminal (`Ctrl+`` `) and run:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If you see an execution-policy error, run once:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 3. Install dependencies
```powershell
pip install -r requirements.txt
```

### 4. Run Bandit (the security scanner)
```powershell
bandit -r app/ -f txt
```

You should see findings against `vulnerable_examples.py` (B602, B105, B301, etc.).

### 5. Run the unit tests (secure code only)
```powershell
pytest tests/ -v
```

---

## Ethical Use Notes

- The file `app/vulnerable_examples.py` contains **intentionally insecure** code for learning.
- Those functions are **never** called by the application or by the tests.
- Do not run them against real systems, networks, or with untrusted input.
- Never commit real passwords or API keys into source control.

---

## Next Steps for Learning

1. Read `docs/LEARNING_GUIDE.md` – every concept is explained in plain language.
2. Open `app/vulnerable_examples.py` and `app/secure_app.py` side-by-side.
3. Re-run Bandit after you understand each finding.
4. Study the findings table in `SECURITY_AUDIT_REPORT.md`.

When you are ready, share the Bandit output with your mentor and we will walk through each finding together.
