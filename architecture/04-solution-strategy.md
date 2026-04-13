# 4. Solution Strategy

## 4.1 Core Approach

The system is structured as a small pipeline of three clearly separated responsibilities:

1. **Fetch** — load today's date and retrieve matching contacts from SQLite
2. **Compose** — build a greeting message for each contact
3. **Send** — hand the message off to an external email service

Each step is implemented as a distinct module, keeping I/O at the edges and business logic in the centre.

## 4.2 Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Architecture style | Single-process pipeline | Proportional to the problem; no concurrency or distribution needed. |
| Dependency direction | Business logic has no dependency on I/O modules | Enables unit testing without a database or network. |
| Storage | SQLite via Python's built-in `sqlite3` | Zero infrastructure; fits a single-machine kata. |
| Email delivery | Abstracted behind a sender interface | Allows swapping SMTP for an API-based service without touching business logic. |
| Scheduling | External (cron / OS scheduler) | Keeps the application stateless and simple; no internal timer needed. |

## 4.3 How Quality Goals Are Addressed

| Quality Goal | Strategy |
|--------------|----------|
| Testability | Birthday detection and message composition are pure functions with no I/O side effects. |
| Simplicity | Three modules, no frameworks, no background processes. |
| Maintainability | Storage and email sending are isolated behind narrow interfaces; replacing either requires changing one module only. |
