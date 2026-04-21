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
**AS A** developer
**I WANT** email credentials to be passed to the container via environment variables
**SO THAT** no secrets are stored in source code or the Docker image

**Architecture Reference:** Chapter 8 Cross-cutting Concepts — Configuration and Secrets; Chapter 7 Deployment View — Deployment Steps

#### SCENARIO 1: All required variables are present at container startup
**Scenario ID**: DELIVERY-INFRA-001.1-S1
**Architecture Reference**: Chapter 8 Cross-cutting Concepts — Configuration and Secrets

**GIVEN**
- `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_USER`, `EMAIL_PASSWORD`, and `EMAIL_SENDER` are passed via `docker run -e`

**WHEN**
- the container starts and `main.py` runs

**THEN**
- `EmailSender` is configured with the values from the environment
- no credentials appear in logs or the image filesystem

#### SCENARIO 2: A required variable is missing
**Scenario ID**: DELIVERY-INFRA-001.1-S2
**Architecture Reference**: Chapter 8 Cross-cutting Concepts — Configuration and Secrets; Chapter 8 Cross-cutting Concepts — Error Handling

**GIVEN**
- one or more required email environment variables are not set in the container

**WHEN**
- the container starts

**THEN**
- the application raises a configuration error
- an ERROR log entry identifies the missing variable
- the container exits with code 1 before attempting any delivery

---

### DELIVERY-INFRA-001.2
**AS A** developer
**I WANT** the pytest suite to verify `EmailSender` behaviour inside the Docker container using a fake sender
**SO THAT** delivery logic is tested without a real network connection

**Architecture Reference:** ADR-004 (Chapter 9 Architecture Decisions); Chapter 8 Cross-cutting Concepts — Testability; Chapter 10 Quality Requirements — QS-3

#### SCENARIO 1: Fake sender tests run inside the container
**Scenario ID**: DELIVERY-INFRA-001.2-S1
**Architecture Reference**: ADR-004 (Chapter 9 Architecture Decisions); Chapter 10 Quality Requirements — QS-3

**GIVEN**
- the Docker image has been built
- delivery tests use a fake `EmailSender` injected as a parameter

**WHEN**
- `docker run <image> pytest` is executed

**THEN**
- pytest discovers and runs the delivery tests
- the fake sender receives exactly the expected messages
- no real network call is made
- the container exits with code 0

---

### DELIVERY-INFRA-001.3
**AS A** developer
**I WANT** log output from the container to go to stdout
**SO THAT** the operator can capture delivery confirmations and errors from `docker run` output

**Architecture Reference:** Chapter 8 Cross-cutting Concepts — Logging; Chapter 7 Deployment View — Deployment Steps

#### SCENARIO 1: Successful send is logged at INFO to stdout
**Scenario ID**: DELIVERY-INFRA-001.3-S1
**Architecture Reference**: Chapter 8 Cross-cutting Concepts — Logging

**GIVEN**
- the Docker image has been built
- all required email environment variables are passed via `docker run -e`
- a contact with a birthday today exists in the database

**WHEN**
- `docker run -e EMAIL_HOST=... <image> python main.py` is executed and `EmailSender.send(message)` returns without error

**THEN**
- an INFO log entry is written to stdout identifying the recipient
- the log is visible in the `docker run` terminal output
- the container exits with code 0

#### SCENARIO 2: Failed send is logged at ERROR to stdout
**Scenario ID**: DELIVERY-INFRA-001.3-S2
**Architecture Reference**: Chapter 8 Cross-cutting Concepts — Logging; Chapter 8 Cross-cutting Concepts — Error Handling

**GIVEN**
- the Docker image has been built
- all required email environment variables are passed via `docker run -e`
- the external email service is unreachable

**WHEN**
- `docker run -e EMAIL_HOST=... <image> python main.py` is executed and `EmailSender.send(message)` raises an exception

**THEN**
- an ERROR log entry including contact details and failure reason is written to stdout
- the container exits with code 1

---

## Traceability Summary

| Field | Value |
|-------|-------|
| Parent Story | `DELIVERY-STORY-001` |
| Backend Sub-Stories | `DELIVERY-BE-001.1`, `DELIVERY-BE-001.2` |
| Infrastructure Sub-Stories | `DELIVERY-INFRA-001.1`, `DELIVERY-INFRA-001.2`, `DELIVERY-INFRA-001.3` |
| Architecture References | Chapter 1 FR-3, Chapter 5 Building Block View — Email Sender / Main Runner, Chapter 6 Runtime View — Successful Birthday Greeting / Email Delivery Failure, Chapter 7 Deployment View — Deployment Steps / OS Scheduler, Chapter 8 Cross-cutting Concepts — Configuration and Secrets / Error Handling / Logging / Testability, Chapter 9 ADR-001 / ADR-003 / ADR-004, Chapter 10 QS-3 |
| Testable Outcomes | message transmitted to external service; exception raised and propagated on failure; exit code 1 on delivery error; N contacts → N send calls; credentials from container env vars only; missing env var → container exits with code 1; fake sender tests run inside Docker with no network; INFO log to stdout on success; ERROR log to stdout with contact details on failure |
