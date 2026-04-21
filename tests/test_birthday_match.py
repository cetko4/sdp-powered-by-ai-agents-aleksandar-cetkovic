import sqlite3
import sys
from datetime import date
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.birthday_match import is_birthday_today
from app.contact import Contact
from app.contact_repository import ContactRepository
from app.greeting_service import GreetingService


# Story: GREETING-STORY-001 / Sub-story: GREETING-BE-001.1
# Scenario: GREETING-BE-001.1-S1
def test_greeting_be_001_1_s1_month_and_day_match_contact_is_selected():
    # GIVEN a contact whose birth month and day match today
    dob = date(1990, 6, 15)
    today = date(2026, 6, 15)

    # WHEN the birthday check is evaluated
    result = is_birthday_today(dob, today)

    # THEN the result is a positive match (year is not considered)
    assert result is True  # nosec B101


# Story: GREETING-STORY-001 / Sub-story: GREETING-BE-001.1
# Scenario: GREETING-BE-001.1-S2
def test_greeting_be_001_1_s2_month_and_day_do_not_match_contact_is_excluded():
    # GIVEN a contact whose birth month and day do not match today
    dob = date(1990, 6, 15)
    today = date(2026, 7, 15)

    # WHEN the birthday check is evaluated
    result = is_birthday_today(dob, today)

    # THEN the result is a negative match
    assert result is False  # nosec B101


# Story: GREETING-STORY-002 / Sub-story: GREETING-BE-002.1
# Scenario: GREETING-BE-002.1-S1
def test_greeting_be_002_1_s1_feb29_contact_matches_feb28_in_non_leap_year():
    # GIVEN a contact born on Feb 29 and today is Feb 28 in a non-leap year
    dob = date(1992, 2, 29)
    today = date(2026, 2, 28)  # 2026 is not a leap year

    # WHEN the birthday check is evaluated
    result = is_birthday_today(dob, today)

    # THEN the contact is treated as a match (Feb 28 substitution applied)
    assert result is True  # nosec B101


# Story: GREETING-STORY-002
# Scenario: GREETING-STORY-002-S1
def test_greeting_story_002_s1_feb29_contact_greeted_on_feb28_non_leap_year():
    # GIVEN a contact born on Feb 29 stored in the database
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE contacts (name TEXT, email TEXT, dob TEXT)")
    conn.execute("INSERT INTO contacts VALUES (?, ?, ?)", ("Bob", "bob@example.com", "1992-02-29"))
    conn.commit()
    today = date(2026, 2, 28)  # non-leap year

    # WHEN the pipeline fetches contacts and composes a greeting
    contacts = ContactRepository(conn).get_birthday_contacts(today)
    messages = [GreetingService().compose(c) for c in contacts]

    # THEN the Feb 29 contact is selected and a greeting is produced
    assert len(messages) == 1  # nosec B101
    assert "Bob" in messages[0].body  # nosec B101


# Story: GREETING-STORY-002
# Scenario: GREETING-STORY-002-S2
def test_greeting_story_002_s2_feb29_contact_greeted_on_feb29_in_leap_year():
    # GIVEN a contact born on Feb 29 and today is Feb 29 in a leap year
    contact = Contact(name="Carol", email="carol@example.com", dob=date(1992, 2, 29))
    today = date(2028, 2, 29)  # 2028 is a leap year

    # WHEN the birthday check is evaluated and a greeting is composed
    matched = is_birthday_today(contact.dob, today)
    message = GreetingService().compose(contact) if matched else None

    # THEN the contact is matched on their actual birthday and a greeting is produced
    assert matched is True  # nosec B101
    assert message is not None  # nosec B101
    assert "Carol" in message.body  # nosec B101


# Story: GREETING-STORY-002
# Scenario: GREETING-STORY-002-S3
def test_greeting_story_002_s3_feb29_contact_not_matched_on_feb28_in_leap_year():
    # GIVEN a contact born on Feb 29 and today is Feb 28 in a leap year
    contact = Contact(name="Dave", email="dave@example.com", dob=date(1992, 2, 29))
    today = date(2028, 2, 28)  # 2028 is a leap year

    # WHEN the birthday check is evaluated
    matched = is_birthday_today(contact.dob, today)

    # THEN the contact is not matched (no substitution in a leap year)
    assert matched is False  # nosec B101
