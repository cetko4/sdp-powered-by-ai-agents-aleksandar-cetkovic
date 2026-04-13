# 8. Cross-cutting Concepts

## 8.1 Configuration and Secrets

Email credentials (host, port, username, password) are read from environment variables at startup. No secrets are stored in source code or the SQLite file.

| Variable | Purpose |
|----------|---------|
| `EMAIL_HOST` | SMTP host or API endpoint |
| `EMAIL_PORT` | SMTP port (e.g., 587) |
| `EMAIL_USER` | Sender account username |
| `EMAIL_PASSWORD` | Sender account password or API key |
| `EMAIL_SENDER` | From-address used in outgoing emails |

## 8.2 Error Handling

| Situation | Behaviour |
|-----------|-----------|
| Database file missing or unreadable | Log error, exit with code 1 |
| No contacts found | Log info message, exit with code 0 |
| Email delivery failure | Log error with contact details, exit with code 1 |

Errors propagate up to `main.py`, which is the single place responsible for catching, logging, and setting the exit code. No silent failures.

## 8.3 Logging

Python's built-in `logging` module is used. Log output goes to stdout so the OS scheduler (cron) can capture and redirect it.

| Level | Usage |
|-------|-------|
| INFO | Application start, number of contacts found, each email sent |
| WARNING | Unexpected but non-fatal conditions |
| ERROR | Failures that prevent normal completion |

## 8.4 Date Handling

Birthday matching compares only month and day, ignoring year. Leap-year birthdays (Feb 29) are sent on Feb 28 in non-leap years.

## 8.5 Testability

I/O dependencies (`ContactRepository`, `EmailSender`) are injected into `main` as parameters, allowing tests to substitute fakes without patching globals or the filesystem.
