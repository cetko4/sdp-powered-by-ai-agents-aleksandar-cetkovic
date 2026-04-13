# 6. Runtime View

## 6.1 Scenario: Successful Birthday Greeting

The primary runtime scenario — one or more contacts have a birthday today.

See [`diagrams/seq-happy-path.puml`](diagrams/seq-happy-path.puml).

1. The scheduler triggers `main.py`.
2. `main` asks `ContactRepository` for today's birthday contacts.
3. `ContactRepository` queries SQLite and returns a list of matching contacts.
4. For each contact, `main` asks `GreetingService` to compose a message.
5. `main` passes each message to `EmailSender`.
6. `EmailSender` delivers it via the external email service.

## 6.2 Scenario: No Birthdays Today

`ContactRepository` returns an empty list. The loop in `main` does not execute. No emails are sent. The process exits normally.

## 6.3 Scenario: Email Delivery Failure

`EmailSender` raises an exception. The error is logged and the process exits with a non-zero code, allowing the scheduler to detect and report the failure.
