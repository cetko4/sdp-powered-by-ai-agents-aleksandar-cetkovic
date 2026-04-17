import sqlite3
import sys
from datetime import date
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.contact_repository import ContactRepository


# Story: CONTACT-STORY-001 / Sub-story: CONTACT-BE-001.1 / Scenario: CONTACT-BE-001.1-S1
def test_contact_be_001_1_s1_query_returns_matching_rows():
    # GIVEN a SQLite connection with a contacts table
    # and a row whose dob month-day matches today
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE contacts (name TEXT, email TEXT, dob TEXT)")
    today = date(2026, 4, 17)
    conn.execute(
        "INSERT INTO contacts VALUES (?, ?, ?)",
        ("Alice", "alice@example.com", "1990-04-17"),  # matches today's month-day
    )
    conn.execute(
        "INSERT INTO contacts VALUES (?, ?, ?)",
        ("Bob", "bob@example.com", "1985-06-01"),  # does NOT match
    )
    conn.commit()

    # WHEN the SELECT query is executed via ContactRepository
    repo = ContactRepository(conn)
    results = repo.get_birthday_contacts(today)

    # THEN only the matching row is returned; year is not considered
    assert len(results) == 1  # nosec B101
    assert results[0].name == "Alice"  # nosec B101
