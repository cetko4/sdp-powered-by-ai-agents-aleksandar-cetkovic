# GREETING Story Bundle

## Original Story

### GREETING-STORY-001
**AS A** system
**I WANT** to detect when a contact has a birthday today and compose a personalized greeting message
**SO THAT** the contact receives a birthday message on the correct day

**Architecture Reference:** Chapter 5 Building Block View — Greeting Service; Chapter 6 Runtime View — Successful Birthday Greeting; FR-2, FR-3 (Chapter 1 Introduction and Goals)

---

### SCENARIO 1: Contact with today's birthday receives a greeting
**Scenario ID**: GREETING-STORY-001-S1
**Architecture Reference**: Chapter 6 Runtime View — Successful Birthday Greeting

**GIVEN**
- a contact exists whose date of birth month and day match today's date
- the contact's name and email address are available

**WHEN**
- the birthday greeting pipeline is executed

**THEN**
- the system identifies the contact as today's birthday recipient
- a personalized greeting message is composed for that contact
- the message is passed to `EmailSender` for delivery

---

### SCENARIO 2: No contacts have a birthday today
**Scenario ID**: GREETING-STORY-001-S2
**Architecture Reference**: Chapter 6 Runtime View — No Birthdays Today

**GIVEN**
- contact records exist in the data source
- none of the contacts have a date of birth matching today's month and day

**WHEN**
- the birthday greeting pipeline is executed

**THEN**
- no greeting message is composed
- no delivery request is made
- the process exits normally with code 0

---

## Frontend Sub-Stories

The Birthday Greetings system has no user-facing interface (Chapter 3 Context and Scope). No frontend sub-stories are applicable.

---

## Backend Sub-Stories

### GREETING-BE-001.1
**AS A** system
**I WANT** to determine whether today matches a contact's birthday by comparing month and day
**SO THAT** only contacts with a birthday today are selected for greeting

**Architecture Reference:** Chapter 5 Building Block View — Greeting Service; Chapter 8 Cross-cutting Concepts — Date Handling; Chapter 10 Quality Requirements — QS-1

#### SCENARIO 1: Month and day match — contact is selected
**Scenario ID**: GREETING-BE-001.1-S1
**Architecture Reference**: Chapter 5 Building Block View — Greeting Service; Chapter 8 Cross-cutting Concepts — Date Handling

**GIVEN**
- a contact record contains a valid date of birth
- today's month and day are equal to the contact's birth month and day

**WHEN**
- the birthday check is evaluated

**THEN**
- the result is a positive match
- the contact is included in the greeting pipeline
- the birth year is not considered in the comparison

#### SCENARIO 2: Month and day do not match — contact is excluded
**Scenario ID**: GREETING-BE-001.1-S2
**Architecture Reference**: Chapter 5 Building Block View — Greeting Service; Chapter 6 Runtime View — No Birthdays Today

**GIVEN**
- a contact record contains a valid date of birth
- today's month and day do not equal the contact's birth month and day

**WHEN**
- the birthday check is evaluated

**THEN**
- the result is a negative match
- the contact is excluded from the greeting pipeline

---

### GREETING-BE-001.2
**AS A** system
**I WANT** to compose a personalized greeting message for each contact identified as having a birthday today
**SO THAT** the delivery component receives a complete, ready-to-send message

**Architecture Reference:** Chapter 5 Building Block View — Greeting Service; Chapter 6 Runtime View — Successful Birthday Greeting; Chapter 10 Quality Requirements — QS-1

#### SCENARIO 1: Greeting message is composed for a matching contact
**Scenario ID**: GREETING-BE-001.2-S1
**Architecture Reference**: Chapter 5 Building Block View — Greeting Service; Chapter 10 Quality Requirements — QS-1

**GIVEN**
- a contact has been identified as having a birthday today
- the contact's name is available

**WHEN**
- `GreetingService.compose(contact)` is called

**THEN**
- a Message object is returned containing the contact's name and a greeting body
- the message is ready to be passed to `EmailSender`
- no database or network access occurs during composition

---

## Infrastructure Sub-Stories

### GREETING-INFRA-001.1
**AS A** system
**I WANT** the full greeting pipeline to be wired and executed by `main.py` in a single run
**SO THAT** contact loading, birthday detection, message composition, and delivery happen in the correct sequence

**Architecture Reference:** Chapter 5 Building Block View — Main / Runner; Chapter 6 Runtime View — Successful Birthday Greeting; ADR-001 (Chapter 9 Architecture Decisions)

#### SCENARIO 1: Pipeline executes all steps in order
**Scenario ID**: GREETING-INFRA-001.1-S1
**Architecture Reference**: Chapter 6 Runtime View — Successful Birthday Greeting; ADR-001 (Chapter 9 Architecture Decisions)

**GIVEN**
- the application is triggered by the OS scheduler or manually
- `ContactRepository` and `EmailSender` are wired into `main.py`

**WHEN**
- `main.py` runs

**THEN**
- contacts are fetched first
- birthday detection and message composition follow for each matching contact
- delivery is invoked last for each composed message
- the process exits with code 0 on success

---

### GREETING-INFRA-001.2
**AS A** system
**I WANT** `GreetingService` to be a pure function with no I/O dependencies
**SO THAT** it can be unit-tested without a database or network

**Architecture Reference:** Chapter 4 Solution Strategy — Dependency Direction; ADR-004 (Chapter 9 Architecture Decisions); Chapter 10 Quality Requirements — QS-1, QS-3

#### SCENARIO 1: GreetingService is testable in isolation
**Scenario ID**: GREETING-INFRA-001.2-S1
**Architecture Reference**: Chapter 4 Solution Strategy — Dependency Direction; Chapter 10 Quality Requirements — QS-1

**GIVEN**
- a Contact object is constructed in-memory for a test
- no database connection or network is available

**WHEN**
- `GreetingService.compose(contact)` is called directly

**THEN**
- a Message object is returned with the expected content
- no I/O side effects occur

---

### GREETING-INFRA-001.3
**AS A** system
**I WANT** the pipeline to be triggered daily by the OS scheduler (cron)
**SO THAT** greetings are sent automatically without manual intervention

**Architecture Reference:** Chapter 7 Deployment View — OS Scheduler (cron); ADR-005 (Chapter 9 Architecture Decisions); FR-4 (Chapter 1 Introduction and Goals)

#### SCENARIO 1: Cron triggers the pipeline at the configured time
**Scenario ID**: GREETING-INFRA-001.3-S1
**Architecture Reference**: Chapter 7 Deployment View — OS Scheduler (cron); ADR-005 (Chapter 9 Architecture Decisions)

**GIVEN**
- a cron entry is configured to run `main.py` once per day
- the operator machine is running at the scheduled time

**WHEN**
- the scheduled time is reached

**THEN**
- cron executes `main.py`
- the full greeting pipeline runs
- stdout output (logs) is captured by cron for operator review

---

## Traceability Summary

| Field | Value |
|-------|-------|
| Parent Story | `GREETING-STORY-001` |
| Backend Sub-Stories | `GREETING-BE-001.1`, `GREETING-BE-001.2` |
| Infrastructure Sub-Stories | `GREETING-INFRA-001.1`, `GREETING-INFRA-001.2`, `GREETING-INFRA-001.3` |
| Architecture References | Chapter 1 FR-2/FR-3/FR-4, Chapter 4 Solution Strategy — Dependency Direction, Chapter 5 Building Block View — Greeting Service / Main Runner, Chapter 6 Runtime View — Successful Birthday Greeting / No Birthdays Today, Chapter 7 Deployment View — OS Scheduler, Chapter 8 Cross-cutting Concepts — Date Handling, Chapter 9 ADR-001 / ADR-004 / ADR-005, Chapter 10 QS-1 / QS-3 |
| Testable Outcomes | birthday match on month/day only (year ignored); no match → no message composed; `GreetingService.compose()` returns correct Message with no I/O; pipeline steps execute in correct order; exit code 0 on success; `GreetingService` unit-testable in isolation; cron triggers daily run |
