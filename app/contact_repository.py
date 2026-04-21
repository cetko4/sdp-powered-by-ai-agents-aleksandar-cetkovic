import calendar
import sqlite3
from datetime import date
from pathlib import Path

from app.contact import Contact


class ContactRepository:
    def __init__(self, conn):
        self._conn = conn

    def _connection(self):
        if isinstance(self._conn, str | Path):
            if not Path(self._conn).exists():
                raise FileNotFoundError(f"Database file not found: {self._conn}")
            return sqlite3.connect(self._conn)
        return self._conn

    def get_birthday_contacts(self, today):
        conn = self._connection()
        malformed = conn.execute(
            "SELECT COUNT(*) FROM contacts"
            " WHERE name IS NULL OR email IS NULL OR dob IS NULL"
        ).fetchone()[0]
        if malformed:
            raise ValueError(
                "contacts table contains rows with missing required fields"
            )
        month_day = today.strftime("%m-%d")
        params = [month_day]
        if month_day == "02-28" and not calendar.isleap(today.year):
            params.append("02-29")
        placeholders = ",".join("?" * len(params))
        rows = conn.execute(
            f"SELECT name, email, dob FROM contacts WHERE strftime('%m-%d', dob) IN ({placeholders})",  # noqa: S608
            params,
        ).fetchall()
        return [
            Contact(name=r[0], email=r[1], dob=date.fromisoformat(r[2])) for r in rows
        ]
