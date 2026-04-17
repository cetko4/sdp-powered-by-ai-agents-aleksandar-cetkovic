from dataclasses import dataclass
from datetime import date


@dataclass
class Contact:
    name: str
    email: str
    dob: date
