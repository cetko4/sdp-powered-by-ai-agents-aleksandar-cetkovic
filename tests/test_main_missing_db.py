import subprocess  # nosec B404
import sys
from pathlib import Path

# Story: CONTACT-INFRA-002.1 / Scenario: CONTACT-INFRA-002.1-S2


def test_contact_infra_002_1_s2_missing_db_exits_nonzero_with_error_log():
    # GIVEN no SQLite database file is present (no DB_PATH env var, no pre-seeded file)
    project_root = Path(__file__).resolve().parent.parent
    main_py = project_root / "main.py"

    # WHEN python main.py is executed
    result = subprocess.run(  # nosec B404 B603
        [sys.executable, str(main_py)],
        capture_output=True,
        text=True,
        cwd=str(project_root),
    )

    # THEN an ERROR log entry is written to stdout and exit code is 1
    assert result.returncode == 1  # nosec B101
    assert "ERROR" in result.stdout  # nosec B101
