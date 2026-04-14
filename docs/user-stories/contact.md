# CONTACT Story Bundle

## Original Story

### CONTACT-STORY-001
**AS A** system
**I WANT** to retrieve all contacts from the SQLite database whose birthday matches today's month and day
**SO THAT** the greeting pipeline has the correct set of recipients for the current run

**Architecture Reference:** Chapter 5 Building Block View — Contact Repository; Chapter 6 Runtime View — Successful Birthday Greeting; FR-1, FR-2 (Chapter 1 Introduction and Goals)

---

### SCENARIO 1: Contacts with today's birthday are returned
**Scenario ID**: CONTACT-STORY-001-S1
**Architecture Reference**: Chapter 6 Runtime View — Successful Birthday Greeting

**GIVEN**
- the SQLite database file is accessible
- one or more contact records have a date of birth whose month and day match today's date

**WHEN**
- `ContactRepository.get_birthday_contacts(today)` is called

**THEN**
- the repository returns a non-empty list containing only the matching contacts
- each returned contact includes name, email, and date of birth

---

### SCENARIO 2: No contacts have a birthday today
**Scenario ID**: CONTACT-STORY-001-S2
**Architecture Reference**: Chapter 6 Runtime View — No Birthdays Today

**GIVEN**
- the SQLite database file is accessible
- no contact records have a date of birth whose month and day match today's date

**WHEN**
- `ContactRepository.get_birthday_contacts(today)` is called

**THEN**
- the repository returns an empty list
- no error is raised
- the calling pipeline performs no further processing

---

### SCENARIO 3: Database file is missing or unreadable
**Scenario ID**: CONTACT-STORY-001-S3
**Architecture Reference**: Chapter 8 Cross-cutting Concepts — Error Handling

**GIVEN**
- the SQLite database file does not exist or cannot be opened

**WHEN**
- `ContactRepository.get_birthday_contacts(today)` is called

**THEN**
- the repository raises an exception
- `main.py` catches the exception, logs an error, and exits with code 1

---

## Frontend Sub-Stories

The Birthday Greetings system has no user-facing interface (Chapter 3 Context and Scope). No frontend sub-stories are applicable.

---

## Backend Sub-Stories

### CONTACT-BE-001.1
**AS A** system
**I WANT** to query the SQLite database for contacts matching today's month and day
**SO THAT** only relevant contacts are returned to the pipeline

**Architecture Reference:** Chapter 5 Building Block View — Contact Repository; ADR-002 (Chapter 9 Architecture Decisions)

#### SCENARIO 1: Query returns matching rows
**Scenario ID**: CONTACT-BE-001.1-S1
**Architecture Reference**: Chapter 5 Building Block View — Contact Repository

**GIVEN**
- a SQLite connection is available (real or injected fake)
- the contacts table contains rows where `strftime('%m-%d', dob)` equals today's month-day

**WHEN**
- the SELECT query is executed

**THEN**
- only rows matching today's month and day are returned
- year is not considered in the comparison

#### SCENARIO 2: Query returns no rows
**Scenario ID**: CONTACT-BE-001.1-S2
**Architecture Reference**: Chapter 6 Runtime View — No Birthdays Today

**GIVEN**
- a SQLite connection is available
- no rows match today's month and day

**WHEN**
- the SELECT query is executed

**THEN**
- an empty result set is returned
- no exception is raised

---

### CONTACT-BE-001.2
**AS A** system
**I WANT** to map each database row to a Contact object
**SO THAT** downstream components work with a typed domain object rather than raw tuples

**Architecture Reference:** Chapter 5 Building Block View — Contact Repository; Chapter 12 Glossary — Contact

#### SCENARIO 1: Row is mapped to a Contact
**Scenario ID**: CONTACT-BE-001.2-S1
**Architecture Reference**: Chapter 5 Building Block View — Contact Repository

**GIVEN**
- a database row contains name, email, and date of birth fields

**WHEN**
- the repository maps the row to a domain object

**THEN**
- a Contact object is returned with the correct name, email, and date of birth values

---

## Infrastructure Sub-Stories

### CONTACT-INFRA-001.1
**AS A** system
**I WANT** the SQLite database file to be initialized with the contacts schema
**SO THAT** the application has a valid data source on first run

**Architecture Reference:** Chapter 7 Deployment View — Deployment Steps; ADR-002 (Chapter 9 Architecture Decisions)

#### SCENARIO 1: Database is initialized successfully
**Scenario ID**: CONTACT-INFRA-001.1-S1
**Architecture Reference**: Chapter 7 Deployment View — Deployment Steps

**GIVEN**
- Python 3.x is installed on the operator machine
- `init_db.py` is executed

**WHEN**
- the initialization script runs

**THEN**
- the SQLite file is created at the configured path
- the contacts table exists with the required columns (name, email, date of birth)

---

### CONTACT-INFRA-001.2
**AS A** system
**I WANT** the `ContactRepository` to receive its database connection via dependency injection
**SO THAT** unit tests can substitute a fake connection without touching the filesystem

**Architecture Reference:** ADR-004 (Chapter 9 Architecture Decisions); Chapter 10 Quality Requirements — QS-2

#### SCENARIO 1: Fake connection is accepted in tests
**Scenario ID**: CONTACT-INFRA-001.2-S1
**Architecture Reference**: ADR-004 (Chapter 9 Architecture Decisions)

**GIVEN**
- a fake in-memory SQLite connection is created for testing
- the connection is passed to `ContactRepository` as a parameter

**WHEN**
- `get_birthday_contacts(today)` is called

**THEN**
- the repository uses the injected connection
- no real database file is accessed
- the correct contacts are returned based on the fake data

---

## Traceability Summary

| Field | Value |
|-------|-------|
| Parent Story | `CONTACT-STORY-001` |
| Backend Sub-Stories | `CONTACT-BE-001.1`, `CONTACT-BE-001.2` |
| Infrastructure Sub-Stories | `CONTACT-INFRA-001.1`, `CONTACT-INFRA-001.2` |
| Architecture References | Chapter 1 FR-1/FR-2, Chapter 5 Building Block View — Contact Repository, Chapter 6 Runtime View — Successful Birthday Greeting / No Birthdays Today, Chapter 7 Deployment View — Deployment Steps, Chapter 8 Cross-cutting Concepts — Error Handling, Chapter 9 ADR-002 / ADR-004, Chapter 10 QS-2, Chapter 12 Glossary — Contact |
| Testable Outcomes | birthday-matched query returns correct contacts; empty list on no match; exception + exit code 1 on DB failure; row-to-Contact mapping; DI allows fake connection in unit tests; DB initialized by `init_db.py` |
