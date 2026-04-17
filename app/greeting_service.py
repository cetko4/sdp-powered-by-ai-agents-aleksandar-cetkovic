from app.message import Message


class GreetingService:
    def compose(self, contact):
        return Message(
            subject="Happy Birthday!",
            body=f"Happy Birthday, {contact.name}!",
            recipient=contact.email,
        )
