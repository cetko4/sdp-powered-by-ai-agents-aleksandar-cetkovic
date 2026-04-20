from datetime import date

from app.contact import Contact


class ContactRepository:
    def __init__(self, conn):
        self._conn = conn

    def get_birthday_contacts(self, today):
        malformed = self._conn.execute(
            "SELECT COUNT(*) FROM contacts"
            " WHERE name IS NULL OR email IS NULL OR dob IS NULL"
        ).fetchone()[0]
        if malformed:
            raise ValueError(
                "contacts table contains rows with missing required fields"
            )
        month_day = today.strftime("%m-%d")
        rows = self._conn.execute(
            "SELECT name, email, dob FROM contacts WHERE strftime('%m-%d', dob) = ?",
            (month_day,),
        ).fetchall()
        return [
            Contact(name=r[0], email=r[1], dob=date.fromisoformat(r[2])) for r in rows
        ]
