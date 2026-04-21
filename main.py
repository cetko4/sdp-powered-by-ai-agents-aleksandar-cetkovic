import logging
import os
import sys
from datetime import date

from app.contact_repository import ContactRepository
from app.email_sender import EmailSender
from app.greeting_service import GreetingService

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format="%(levelname)s %(message)s")
logger = logging.getLogger(__name__)

DB_PATH = os.environ.get("DB_PATH", "contacts.db")


def run(repo, sender=None, today=None):
    if today is None:
        today = date.today()
    try:
        contacts = repo.get_birthday_contacts(today)
    except Exception as e:
        logger.error("Failed to load contacts: %s", e)
        sys.exit(1)

    if sender is None:
        sender = EmailSender()

    service = GreetingService()
    for contact in contacts:
        try:
            message = service.compose(contact)
            sender.send(message)
            logger.info("Sent greeting to %s", contact.email)
        except Exception as e:
            logger.error("Failed to send greeting to %s: %s", contact.email, e)
            sys.exit(1)


if __name__ == "__main__":
    run(ContactRepository(DB_PATH))
