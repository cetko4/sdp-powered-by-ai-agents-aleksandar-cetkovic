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
**AS A** developer
**I WANT** the Docker image to build successfully with all Python dependencies installed
**SO THAT** the application is ready to run in a container without manual setup

**Architecture Reference:** Chapter 7 Deployment View — Deployment Steps; Chapter 2 Constraints — TC-1, TC-2

#### SCENARIO 1: Docker image builds with dependencies
**Scenario ID**: CONTACT-INFRA-001.1-S1
**Architecture Reference**: Chapter 7 Deployment View — Deployment Steps

**GIVEN**
- a `Dockerfile` exists at the project root
- `requirements.txt` lists all runtime dependencies

**WHEN**
- `docker build` is executed

**THEN**
- the image builds without error
- all packages from `requirements.txt` are installed inside the image
- the SQLite module is available (Python standard library)

---

### CONTACT-INFRA-001.2
**AS A** developer
**I WANT** the pytest suite to run inside the Docker container
**SO THAT** test results are reproducible in any environment without local Python setup

**Architecture Reference:** Chapter 8 Cross-cutting Concepts — Testability; ADR-004 (Chapter 9 Architecture Decisions)

#### SCENARIO 1: Tests execute successfully inside the container
**Scenario ID**: CONTACT-INFRA-001.2-S1
**Architecture Reference**: Chapter 8 Cross-cutting Concepts — Testability; ADR-004 (Chapter 9 Architecture Decisions)

**GIVEN**
- the Docker image has been built
- the project structure places tests where pytest can discover them (e.g., `tests/` directory with `test_*.py` files)

**WHEN**
- `docker run <image> pytest` is executed

**THEN**
- pytest discovers and runs all test files
- `ContactRepository` tests pass using an in-memory SQLite connection
- the container exits with code 0 on success

#### SCENARIO 2: Missing dependency causes test failure at import
**Scenario ID**: CONTACT-INFRA-001.2-S2
**Architecture Reference**: Chapter 7 Deployment View — Deployment Steps

**GIVEN**
- a required package is absent from `requirements.txt`

**WHEN**
- `docker run <image> pytest` is executed

**THEN**
- pytest reports an import error identifying the missing package
- the container exits with a non-zero code

---

### CONTACT-INFRA-001.3
**AS A** developer
**I WANT** the SQLite database file to be initialised via a script that can be run inside the container
**SO THAT** the application has a valid data source when the container starts

**Architecture Reference:** Chapter 7 Deployment View — Deployment Steps; ADR-002 (Chapter 9 Architecture Decisions)

#### SCENARIO 1: Database is initialised inside the container
**Scenario ID**: CONTACT-INFRA-001.3-S1
**Architecture Reference**: Chapter 7 Deployment View — Deployment Steps; ADR-002 (Chapter 9 Architecture Decisions)

**GIVEN**
- the Docker image has been built
- `init_db.py` is present in the image

**WHEN**
- `docker run <image> python init_db.py` is executed

**THEN**
- the SQLite file is created at the path configured via environment variable or default
- the contacts table exists with the required columns (name, email, date of birth)
- the script exits with code 0

---

## Traceability Summary

| Field | Value |
|-------|-------|
| Parent Story | `CONTACT-STORY-001` |
| Backend Sub-Stories | `CONTACT-BE-001.1`, `CONTACT-BE-001.2` |
| Infrastructure Sub-Stories | `CONTACT-INFRA-001.1`, `CONTACT-INFRA-001.2`, `CONTACT-INFRA-001.3` |
| Architecture References | Chapter 1 FR-1/FR-2, Chapter 2 TC-1/TC-2, Chapter 5 Building Block View — Contact Repository, Chapter 6 Runtime View — Successful Birthday Greeting / No Birthdays Today, Chapter 7 Deployment View — Deployment Steps, Chapter 8 Cross-cutting Concepts — Error Handling / Testability, Chapter 9 ADR-002 / ADR-004, Chapter 12 Glossary — Contact |
| Testable Outcomes | birthday-matched query returns correct contacts; empty list on no match; exception + exit code 1 on DB failure; row-to-Contact mapping; Docker image builds with all dependencies; pytest runs inside container with exit code 0; missing dependency surfaces as import error; DB initialised by `init_db.py` inside container |
