from datetime import date

from app.contact import Contact


class ContactRepository:
    def __init__(self, conn):
        self._conn = conn

    def get_birthday_contacts(self, today):
        month_day = today.strftime("%m-%d")
        rows = self._conn.execute(
            "SELECT name, email, dob FROM contacts WHERE strftime('%m-%d', dob) = ?",
            (month_day,),
        ).fetchall()
        return [
            Contact(name=r[0], email=r[1], dob=date.fromisoformat(r[2])) for r in rows
        ]
