import sys
from datetime import date
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.contact import Contact
from app.greeting_service import GreetingService
from app.message import Message


def test_compose_returns_personalized_message_for_matching_contact():
    # GIVEN
    contact = Contact(
        name="Alice",
        email="alice@example.com",
        dob=date(1990, 4, 17),
    )
    service = GreetingService()

    # WHEN
    message = service.compose(contact)

    # THEN
    assert isinstance(message, Message)  # nosec B101
    assert message is not None  # nosec B101
    assert "Alice" in message.body  # nosec B101
