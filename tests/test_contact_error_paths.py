import sqlite3
import sys
from datetime import date
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.contact_repository import ContactRepository


# CONTACT-INFRA-002.1 / CONTACT-BE-002.1-S1
def test_contact_be_002_1_s1_missing_db_raises_exception():
    # GIVEN the path configured for the SQLite file does not exist
    repo = ContactRepository("/nonexistent/path/contacts.db")

    # WHEN get_birthday_contacts is called
    # THEN an exception is raised and propagates (not swallowed)
    with pytest.raises((OSError, Exception)):
        repo.get_birthday_contacts(date(2026, 4, 20))


# CONTACT-INFRA-002.1 / CONTACT-BE-002.2-S2
def test_contact_be_002_2_s2_malformed_row_raises_exception():
    # GIVEN a SQLite connection with a row missing the dob field (NULL)
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE contacts (name TEXT, email TEXT, dob TEXT)")
    conn.execute(
        "INSERT INTO contacts VALUES (?, ?, ?)", ("Alice", "alice@example.com", None)
    )
    conn.commit()

    # WHEN get_birthday_contacts processes the result set
    repo = ContactRepository(conn)

    # THEN an exception is raised for the malformed row
    with pytest.raises(ValueError):
        repo.get_birthday_contacts(date(2026, 4, 20))
