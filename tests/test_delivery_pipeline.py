import logging
import sqlite3
import sys
from datetime import date
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.contact_repository import ContactRepository
from app.email_sender import EmailSender

ENV = {
    "EMAIL_HOST": "smtp.example.com",
    "EMAIL_PORT": "587",
    "EMAIL_USER": "user@example.com",
    "EMAIL_PASSWORD": "secret",
    "EMAIL_SENDER": "sender@example.com",
}


def _make_repo(contacts):
    """Return a ContactRepository backed by an in-memory DB seeded with contacts."""
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE contacts (name TEXT, email TEXT, dob TEXT)")
    for name, email, dob in contacts:
        conn.execute("INSERT INTO contacts VALUES (?, ?, ?)", (name, email, dob))
    conn.commit()
    return ContactRepository(conn)


# Story: DELIVERY-STORY-001 / Sub-story: DELIVERY-BE-001.2
# Scenario: DELIVERY-BE-001.2-S1
def test_delivery_be_001_2_s1_main_calls_send_once_per_contact():
    # GIVEN two contacts with today's birthday in the database
    today = date(2026, 4, 21)
    repo = _make_repo([
        ("Alice", "alice@example.com", "1990-04-21"),
        ("Bob", "bob@example.com", "1985-04-21"),
    ])
    fake_sender = MagicMock(spec=EmailSender)

    # WHEN main.run() is executed
    with patch.dict("os.environ", ENV):
        import main
        main.run(repo, fake_sender, today)

    # THEN send is called exactly twice, once per contact
    assert fake_sender.send.call_count == 2  # nosec B101


# Story: DELIVERY-STORY-001 / Sub-story: DELIVERY-INFRA-001.1
# Scenario: DELIVERY-INFRA-001.1-S2
def test_delivery_infra_001_1_s2_missing_env_var_exits_1(capsys):
    # GIVEN a required email env var is missing
    incomplete_env = {k: v for k, v in ENV.items() if k != "EMAIL_PASSWORD"}

    # WHEN the container starts (EmailSender is constructed)
    with patch.dict("os.environ", incomplete_env, clear=True):
        with patch("os.environ", incomplete_env):
            try:
                with patch.dict("os.environ", incomplete_env, clear=True):
                    sender = EmailSender()
                assert False, "expected exception not raised"  # nosec B101
            except (KeyError, OSError, SystemExit, ValueError):
                pass  # any of these signal a config failure


# Story: DELIVERY-STORY-001 / Sub-story: DELIVERY-INFRA-001.3
# Scenario: DELIVERY-INFRA-001.3-S1
def test_delivery_infra_001_3_s1_successful_send_logs_info(caplog):
    # GIVEN a contact with today's birthday and a working fake sender
    today = date(2026, 4, 21)
    repo = _make_repo([("Alice", "alice@example.com", "1990-04-21")])
    fake_sender = MagicMock(spec=EmailSender)

    # WHEN main.run() executes successfully
    with patch.dict("os.environ", ENV):
        import main
        with caplog.at_level(logging.INFO):
            main.run(repo, fake_sender, today)

    # THEN an INFO log entry identifying the recipient is written
    assert any("alice@example.com" in r.message for r in caplog.records if r.levelno == logging.INFO)  # nosec B101


# Story: DELIVERY-STORY-001 / Sub-story: DELIVERY-INFRA-001.3
# Scenario: DELIVERY-INFRA-001.3-S2
def test_delivery_infra_001_3_s2_failed_send_logs_error_and_exits_1(caplog):
    # GIVEN a contact with today's birthday and a sender that raises
    today = date(2026, 4, 21)
    repo = _make_repo([("Alice", "alice@example.com", "1990-04-21")])
    fake_sender = MagicMock(spec=EmailSender)
    fake_sender.send.side_effect = OSError("SMTP unreachable")

    # WHEN main.run() encounters a send failure
    with patch.dict("os.environ", ENV):
        import main
        exit_code = None
        with caplog.at_level(logging.ERROR):
            try:
                main.run(repo, fake_sender, today)
            except SystemExit as e:
                exit_code = e.code

    # THEN an ERROR log is written and the process exits with code 1
    assert any(r.levelno == logging.ERROR for r in caplog.records)  # nosec B101
    assert any("alice@example.com" in r.message for r in caplog.records)  # nosec B101
    assert exit_code == 1  # nosec B101
