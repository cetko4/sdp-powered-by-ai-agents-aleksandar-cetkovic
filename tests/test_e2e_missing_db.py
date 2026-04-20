import subprocess  # nosec B404
import sys
from pathlib import Path

# Story: CONTACT-E2E-002.1 / Scenario: CONTACT-E2E-002.1-S1


def test_contact_e2e_002_1_s1_missing_db_exits_1_with_error_log():
    # GIVEN the Docker image has been built (simulated: run main.py directly)
    # AND all required email environment variables are passed
    # AND no SQLite database file is mounted or pre-seeded
    project_root = Path(__file__).resolve().parent.parent
    env_vars = {
        "DB_PATH": "/nonexistent/contacts.db",
        "EMAIL_HOST": "smtp.example.com",
        "EMAIL_PORT": "587",
        "EMAIL_USER": "user@example.com",
        "EMAIL_PASSWORD": "secret",
        "EMAIL_SENDER": "sender@example.com",
    }

    # WHEN python main.py is executed with email env vars but no DB
    result = subprocess.run(  # nosec B404 B603
        [sys.executable, str(project_root / "main.py")],
        capture_output=True,
        text=True,
        cwd=str(project_root),
        env={**_base_env(), **env_vars},
    )

    # THEN ERROR log identifying the missing database is written to stdout
    assert result.returncode == 1  # nosec B101
    assert "ERROR" in result.stdout  # nosec B101
    # AND no email delivery is attempted (stdout contains no INFO send entry)
    assert "Sent" not in result.stdout  # nosec B101


def _base_env():
    """Minimal env so Python itself can run (PATH, HOME, etc.)."""
    import os
    return {k: v for k, v in os.environ.items() if k in ("PATH", "HOME", "PYTHONPATH", "LANG")}
