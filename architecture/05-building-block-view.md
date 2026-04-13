# 5. Building Block View

## 5.1 Level 1 — Containers

The system is a single Python process. There are no separate deployable units beyond the application itself and its external dependencies.

See [`diagrams/c4-container.puml`](diagrams/c4-container.puml).

| Container | Technology | Responsibility |
|-----------|------------|----------------|
| Birthday Greetings App | Python script | Orchestrates the full pipeline: fetch, compose, send |
| SQLite Database | SQLite file | Persists contact records |
| External Email Service | SMTP / API | Delivers greeting emails to recipients |

## 5.2 Level 2 — Components of the Birthday Greetings App

The application is composed of four modules:

See [`diagrams/c4-component.puml`](diagrams/c4-component.puml).

| Component | Module | Responsibility |
|-----------|--------|----------------|
| Main / Runner | `main.py` | Entry point; wires components together and runs the pipeline |
| Contact Repository | `contact_repository.py` | Queries SQLite for contacts whose birthday matches today |
| Greeting Service | `greeting_service.py` | Composes the greeting message for a given contact |
| Email Sender | `email_sender.py` | Sends the composed message via the external email service |
