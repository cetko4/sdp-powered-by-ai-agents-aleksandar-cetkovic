from dataclasses import dataclass


@dataclass
class Message:
    subject: str
    body: str
    recipient: str
