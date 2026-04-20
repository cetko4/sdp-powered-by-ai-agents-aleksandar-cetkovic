import logging
import sys
from datetime import date
from pathlib import Path
from unittest.mock import MagicMock

import pytest

sys.path.append(str(Path(__file__).resolve().parent.parent))

import main  # noqa: E402


# Story: CONTACT-BE-002.2 / Scenario: CONTACT-BE-002.2-S1
def test_contact_be_002_2_s1_repository_exception_is_caught_and_logged(caplog):
    # GIVEN ContactRepository.get_birthday_contacts raises an exception
    repo = MagicMock()
    repo.get_birthday_contacts.side_effect = FileNotFoundError("contacts.db not found")

    # WHEN main.run(repo) executes the pipeline
    # THEN sys.exit(1) is called
    with pytest.raises(SystemExit) as exc_info:
        with caplog.at_level(logging.ERROR):
            main.run(repo)

    assert exc_info.value.code == 1  # nosec B101
    assert any("ERROR" in r.levelname for r in caplog.records)  # nosec B101
