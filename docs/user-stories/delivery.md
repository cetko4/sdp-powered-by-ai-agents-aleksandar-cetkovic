# DELIVERY Story Bundle

## Original Story

### DELIVERY-STORY-001
**AS A** system
**I WANT** to send each composed greeting message to its recipient via the external email service
**SO THAT** the birthday person receives their greeting on the correct day

**Architecture Reference:** Chapter 5 Building Block View — Email Sender; Chapter 6 Runtime View — Successful Birthday Greeting; FR-3 (Chapter 1 Introduction and Goals)

---

### SCENARIO 1: Message is delivered successfully
**Scenario ID**: DELIVERY-STORY-001-S1
**Architecture Reference**: Chapter 6 Runtime View — Successful Birthday Greeting

**GIVEN**
- a greeting message has been composed for a contact
- the external email service is reachable
- email credentials are available via environment variables

**WHEN**
- `EmailSender.send(message)` is called

**THEN**
- the message is transmitted to the external email service
- the service accepts the request and delivers the email to the recipient
- an INFO log entry records the successful send
- the pipeline continues to the next contact

---

### SCENARIO 2: Email delivery fails
**Scenario ID**: DELIVERY-STORY-001-S2
**Architecture Reference**: Chapter 6 Runtime View — Email Delivery Failure; Chapter 8 Cross-cutting Concepts — Error Handling

**GIVEN**
- a greeting message has been composed for a contact
- the external email service is unreachable or returns an error

**WHEN**
- `EmailSender.send(message)` is called

**THEN**
- `EmailSender` raises an exception
- `main.py` catches the exception and logs an ERROR entry including the contact details
- the process exits with code 1
- the OS scheduler can detect the failure via the non-zero exit code

---

### SCENARIO 3: Multiple contacts are processed in sequence
**Scenario ID**: DELIVERY-STORY-001-S3
**Architecture Reference**: Chapter 6 Runtime View — Successful Birthday Greeting; ADR-001 (Chapter 9 Architecture Decisions)

**GIVEN**
- two or more contacts have a birthday today
- a composed message exists for each contact

**WHEN**
- the pipeline iterates over all contacts and calls `EmailSender.send(message)` for each

**THEN**
- each message is sent in sequence
- one INFO log entry is written per successful send
- all recipients receive their greeting

---

## Frontend Sub-Stories

The Birthday Greetings system has no user-facing interface (Chapter 3 Context and Scope). No frontend sub-stories are applicable.

---

## Backend Sub-Stories

### DELIVERY-BE-001.1
**AS A** system
**I WANT** to transmit a greeting message to the external email service using the configured protocol
**SO THAT** the recipient's inbox receives the email

**Architecture Reference:** Chapter 5 Building Block View — Email Sender; ADR-003 (Chapter 9 Architecture Decisions)

#### SCENARIO 1: Message is sent via SMTP or API
**Scenario ID**: DELIVERY-BE-001.1-S1
**Architecture Reference**: Chapter 5 Building Block View — Email Sender; ADR-003 (Chapter 9 Architecture Decisions)

**GIVEN**
- a Message object with recipient address and body is available
- `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_USER`, `EMAIL_PASSWORD`, and `EMAIL_SENDER` are set

**WHEN**
- `EmailSender.send(message)` is called

**THEN**
- the message is submitted to the external service using the configured host and credentials
- no credentials appear in log output or source code

#### SCENARIO 2: Exception propagates on delivery failure
**Scenario ID**: DELIVERY-BE-001.1-S2
**Architecture Reference**: Chapter 6 Runtime View — Email Delivery Failure; Chapter 8 Cross-cutting Concepts — Error Handling

**GIVEN**
- the external email service returns an error or is unreachable

**WHEN**
- `EmailSender.send(message)` is called

**THEN**
- an exception is raised by `EmailSender`
- the exception is not swallowed inside `email_sender.py`
- it propagates to `main.py` for centralized handling

---

### DELIVERY-BE-001.2
**AS A** system
**I WANT** `main.py` to orchestrate sending for every contact returned by the repository
**SO THAT** no birthday contact is skipped

**Architecture Reference:** Chapter 5 Building Block View — Main / Runner; Chapter 6 Runtime View — Successful Birthday Greeting

#### SCENARIO 1: All contacts receive a send call
**Scenario ID**: DELIVERY-BE-001.2-S1
**Architecture Reference**: Chapter 6 Runtime View — Successful Birthday Greeting

**GIVEN**
- `ContactRepository` returns a list of N contacts
- a message has been composed for each contact by `GreetingService`

**WHEN**
- `main.py` iterates over the contact list

**THEN**
- `EmailSender.send(message)` is called exactly N times
- each call uses the message composed for the corresponding contact

---

## Infrastructure Sub-Stories

### DELIVERY-INFRA-001.1
**AS A** system
**I WANT** email credentials to be read from environment variables at startup
**SO THAT** no secrets are stored in source code or the database

**Architecture Reference:** Chapter 8 Cross-cutting Concepts — Configuration and Secrets; Chapter 7 Deployment View — Deployment Steps

#### SCENARIO 1: All required variables are present
**Scenario ID**: DELIVERY-INFRA-001.1-S1
**Architecture Reference**: Chapter 8 Cross-cutting Concepts — Configuration and Secrets

**GIVEN**
- `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_USER`, `EMAIL_PASSWORD`, and `EMAIL_SENDER` are set in the environment

**WHEN**
- the application starts

**THEN**
- `EmailSender` is configured with the values from the environment
- no credentials are written to logs or source files

#### SCENARIO 2: A required variable is missing
**Scenario ID**: DELIVERY-INFRA-001.1-S2
**Architecture Reference**: Chapter 8 Cross-cutting Concepts — Configuration and Secrets; Chapter 8 Cross-cutting Concepts — Error Handling

**GIVEN**
- one or more required email environment variables are not set

**WHEN**
- the application starts

**THEN**
- the application raises a configuration error
- an ERROR log entry identifies the missing variable
- the process exits with code 1 before attempting any delivery

---

### DELIVERY-INFRA-001.2
**AS A** system
**I WANT** `EmailSender` to be injected into the pipeline rather than instantiated inside `main.py`
**SO THAT** unit tests can substitute a fake sender without network access

**Architecture Reference:** ADR-004 (Chapter 9 Architecture Decisions); Chapter 10 Quality Requirements — QS-3; Chapter 8 Cross-cutting Concepts — Testability

#### SCENARIO 1: Fake sender is accepted in tests
**Scenario ID**: DELIVERY-INFRA-001.2-S1
**Architecture Reference**: ADR-004 (Chapter 9 Architecture Decisions); Chapter 10 Quality Requirements — QS-3

**GIVEN**
- a fake `EmailSender` implementation is created for testing
- the fake is passed to the main pipeline function as a parameter

**WHEN**
- the pipeline runs with birthday contacts present

**THEN**
- the fake sender receives exactly the expected messages
- no real network call is made
- the test can assert on the messages received by the fake

---

### DELIVERY-INFRA-001.3
**AS A** system
**I WANT** each send attempt to produce a log entry at the appropriate level
**SO THAT** the operator can confirm delivery or diagnose failures from cron output

**Architecture Reference:** Chapter 8 Cross-cutting Concepts — Logging; Chapter 7 Deployment View — OS Scheduler (cron)

#### SCENARIO 1: Successful send is logged at INFO
**Scenario ID**: DELIVERY-INFRA-001.3-S1
**Architecture Reference**: Chapter 8 Cross-cutting Concepts — Logging

**GIVEN**
- a greeting message is sent successfully

**WHEN**
- `EmailSender.send(message)` returns without error

**THEN**
- an INFO log entry is written identifying the recipient and confirming the send

#### SCENARIO 2: Failed send is logged at ERROR
**Scenario ID**: DELIVERY-INFRA-001.3-S2
**Architecture Reference**: Chapter 8 Cross-cutting Concepts — Logging; Chapter 8 Cross-cutting Concepts — Error Handling

**GIVEN**
- `EmailSender.send(message)` raises an exception

**WHEN**
- `main.py` catches the exception

**THEN**
- an ERROR log entry is written including the contact details and failure reason
- log output goes to stdout so cron can capture it

---

## Traceability Summary

| Field | Value |
|-------|-------|
| Parent Story | `DELIVERY-STORY-001` |
| Backend Sub-Stories | `DELIVERY-BE-001.1`, `DELIVERY-BE-001.2` |
| Infrastructure Sub-Stories | `DELIVERY-INFRA-001.1`, `DELIVERY-INFRA-001.2`, `DELIVERY-INFRA-001.3` |
| Architecture References | Chapter 1 FR-3, Chapter 5 Building Block View — Email Sender / Main Runner, Chapter 6 Runtime View — Successful Birthday Greeting / Email Delivery Failure, Chapter 7 Deployment View — Deployment Steps / OS Scheduler, Chapter 8 Cross-cutting Concepts — Configuration and Secrets / Error Handling / Logging / Testability, Chapter 9 ADR-001 / ADR-003 / ADR-004, Chapter 10 QS-3 |
| Testable Outcomes | message transmitted to external service; exception raised and propagated on failure; exit code 1 on delivery error; N contacts → N send calls; credentials from env vars only; missing env var → exit code 1; fake sender usable in unit tests; INFO log on success; ERROR log with contact details on failure |
