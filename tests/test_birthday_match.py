import sys
from datetime import date
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.birthday_match import is_birthday_today
from app.contact import Contact
from app.greeting_service import GreetingService


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
    # GIVEN a contact born on Feb 29 and today is Feb 28 in a non-leap year
    contact = Contact(name="Bob", email="bob@example.com", dob=date(1992, 2, 29))
    today = date(2026, 2, 28)  # 2026 is not a leap year

    # WHEN the birthday check is evaluated and a greeting is composed
    matched = is_birthday_today(contact.dob, today)
    message = GreetingService().compose(contact) if matched else None

    # THEN the contact is matched and a greeting message is produced
    assert matched is True  # nosec B101
    assert message is not None  # nosec B101
    assert "Bob" in message.body  # nosec B101
