# 9. Architecture Decisions

## ADR-001: Single-Process Pipeline Architecture

### Status
Accepted

### Context
The system has a simple, linear flow: read contacts, compose messages, send emails. No concurrency, no shared state, and no user interaction are required.

### Decision
Implement the system as a single Python process with a sequential pipeline.

### Rationale
A pipeline matches the problem shape exactly. Introducing a web server, message queue, or background worker would add complexity with no benefit at this scale.

### Consequences
- Simple to understand, run, and debug.
- Not suitable if the contact list grows to a size where sequential sending becomes too slow (not a concern for this kata).

---

## ADR-002: SQLite for Contact Storage

### Status
Accepted

### Context
Contact data must be persisted between runs. The system operates on a single machine with a single operator.

### Decision
Use SQLite via Python's built-in `sqlite3` module.

### Rationale
SQLite requires no server setup, no credentials, and no network access. It is sufficient for the expected data volume and is available in the Python standard library.

### Consequences
- Zero infrastructure overhead.
- Not suitable for multi-process or multi-machine deployments, which are out of scope.

---

## ADR-003: External Email Service for Delivery

### Status
Accepted

### Context
The system must send emails but should not implement mail server functionality.

### Decision
Delegate email delivery to an external SMTP server or API-based service (e.g., SendGrid). The sender is abstracted behind an `EmailSender` interface.

### Rationale
Building or hosting a mail server is out of scope. Abstracting the sender keeps the provider swappable without touching business logic.

### Consequences
- Email delivery depends on a third-party service and network availability.
- Switching providers requires changing only `email_sender.py`.

---

## ADR-004: Dependency Injection for I/O Components

### Status
Accepted

### Context
`ContactRepository` and `EmailSender` both perform I/O. Testing them inline makes unit tests dependent on a real database and network.

### Decision
Pass `ContactRepository` and `EmailSender` as parameters to the main pipeline function.

### Rationale
Constructor/parameter injection is the simplest form of dependency inversion. It allows tests to substitute fakes without monkey-patching or mocking frameworks.

### Consequences
- Core logic is fully unit-testable in isolation.
- Slightly more explicit wiring in `main.py`, which is acceptable at this scale.

---

## ADR-005: External Scheduling via Cron

### Status
Accepted

### Context
The system must run once per day at a fixed time. An internal timer or daemon would keep a process alive continuously.

### Decision
Rely on the OS scheduler (cron) to trigger the script daily.

### Rationale
Cron is universally available, requires no application code, and keeps the application stateless. The application does not need to know about time between runs.

### Consequences
- Deployment requires a cron entry to be configured manually.
- Missed runs (e.g., machine off) are not automatically retried — acceptable for an educational kata.
