import os
import smtplib
from email.mime.text import MIMEText


class EmailSender:
    def __init__(self):
        self._host = os.environ["EMAIL_HOST"]
        self._port = int(os.environ["EMAIL_PORT"])
        self._user = os.environ["EMAIL_USER"]
        self._password = os.environ["EMAIL_PASSWORD"]
        self._sender = os.environ["EMAIL_SENDER"]

    def send(self, message):
        msg = MIMEText(message.body)
        msg["Subject"] = message.subject
        msg["From"] = self._sender
        msg["To"] = message.recipient
        with smtplib.SMTP(self._host, self._port) as smtp:
            smtp.login(self._user, self._password)
            smtp.sendmail(self._sender, message.recipient, msg.as_string())
