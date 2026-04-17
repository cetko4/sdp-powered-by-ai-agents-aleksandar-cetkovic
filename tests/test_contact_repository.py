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


# Story: CONTACT-STORY-001 / Sub-story: CONTACT-BE-001.1 / Scenario: CONTACT-BE-001.1-S2
def test_contact_be_001_1_s2_query_returns_empty_list_when_no_match():
    # GIVEN a SQLite connection with contacts whose dob does NOT match today
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE contacts (name TEXT, email TEXT, dob TEXT)")
    today = date(2026, 4, 17)
    conn.execute(
        "INSERT INTO contacts VALUES (?, ?, ?)",
        ("Bob", "bob@example.com", "1985-06-01"),  # does NOT match
    )
    conn.commit()

    # WHEN the SELECT query is executed via ContactRepository
    repo = ContactRepository(conn)
    results = repo.get_birthday_contacts(today)

    # THEN an empty list is returned and no exception is raised
    assert results == []  # nosec B101


# Story: CONTACT-STORY-001 / Sub-story: CONTACT-BE-001.2 / Scenario: CONTACT-BE-001.2-S1
def test_contact_be_001_2_s1_row_is_mapped_to_contact_with_typed_dob():
    # GIVEN a contacts table row with name, email, and dob
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE contacts (name TEXT, email TEXT, dob TEXT)")
    conn.execute(
        "INSERT INTO contacts VALUES (?, ?, ?)",
        ("Alice", "alice@example.com", "1990-04-17"),
    )
    conn.commit()

    # WHEN the repository maps the row to a Contact
    repo = ContactRepository(conn)
    results = repo.get_birthday_contacts(date(2026, 4, 17))

    # THEN the Contact has correct name, email, and dob as a date object
    assert len(results) == 1  # nosec B101
    contact = results[0]
    assert contact.name == "Alice"  # nosec B101
    assert contact.email == "alice@example.com"  # nosec B101
    assert contact.dob == date(1990, 4, 17)  # nosec B101
    assert isinstance(contact.dob, date)  # nosec B101
