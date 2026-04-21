import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.email_sender import EmailSender
from app.message import Message

ENV = {
    "EMAIL_HOST": "smtp.example.com",
    "EMAIL_PORT": "587",
    "EMAIL_USER": "user@example.com",
    "EMAIL_PASSWORD": "secret",
    "EMAIL_SENDER": "sender@example.com",
}


# Story: DELIVERY-STORY-001 / Sub-story: DELIVERY-BE-001.1
# Scenario: DELIVERY-BE-001.1-S1
def test_delivery_be_001_1_s1_send_submits_message_via_smtp():
    # GIVEN a configured EmailSender and a Message
    message = Message(subject="Happy Birthday!", body="Happy Birthday, Alice!", recipient="alice@example.com")

    with patch("smtplib.SMTP") as mock_smtp_class:
        mock_smtp = MagicMock()
        mock_smtp_class.return_value.__enter__ = MagicMock(return_value=mock_smtp)
        mock_smtp_class.return_value.__exit__ = MagicMock(return_value=False)

        with patch.dict("os.environ", ENV):
            sender = EmailSender()

            # WHEN send is called
            sender.send(message)

    # THEN the message was submitted to the SMTP server
    mock_smtp.sendmail.assert_called_once()  # nosec B101


# Story: DELIVERY-STORY-001 / Sub-story: DELIVERY-BE-001.1
# Scenario: DELIVERY-BE-001.1-S2
def test_delivery_be_001_1_s2_smtp_exception_propagates():
    # GIVEN an EmailSender whose SMTP connection raises
    message = Message(subject="Happy Birthday!", body="Happy Birthday, Alice!", recipient="alice@example.com")

    with patch("smtplib.SMTP") as mock_smtp_class:
        mock_smtp_class.side_effect = OSError("connection refused")

        with patch.dict("os.environ", ENV):
            sender = EmailSender()

            # WHEN send is called and SMTP raises
            # THEN the exception propagates out of EmailSender
            try:
                sender.send(message)
                assert False, "expected exception was not raised"  # nosec B101
            except OSError:
                pass
