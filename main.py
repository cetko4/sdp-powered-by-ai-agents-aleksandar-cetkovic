import logging
import os
import sys
from datetime import date

from app.contact_repository import ContactRepository

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format="%(levelname)s %(message)s")
logger = logging.getLogger(__name__)

DB_PATH = os.environ.get("DB_PATH", "contacts.db")


def run(repo):
    try:
        repo.get_birthday_contacts(date.today())
    except Exception as e:
        logger.error("Failed to load contacts: %s", e)
        sys.exit(1)


if __name__ == "__main__":
    run(ContactRepository(DB_PATH))
