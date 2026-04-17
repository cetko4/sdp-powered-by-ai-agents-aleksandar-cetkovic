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
**AS A** developer
**I WANT** the project structure to support pytest discovery inside the Docker container
**SO THAT** all greeting logic tests are found and executed automatically

**Architecture Reference:** Chapter 8 Cross-cutting Concepts — Testability; Chapter 4 Solution Strategy — Dependency Direction; ADR-004 (Chapter 9 Architecture Decisions)

#### SCENARIO 1: pytest discovers greeting tests inside the container
**Scenario ID**: GREETING-INFRA-001.1-S1
**Architecture Reference**: Chapter 8 Cross-cutting Concepts — Testability; ADR-004 (Chapter 9 Architecture Decisions)

**GIVEN**
- the Docker image has been built
- test files for `GreetingService` follow the `test_*.py` naming convention under the `tests/` directory

**WHEN**
- `docker run <image> pytest` is executed

**THEN**
- pytest discovers all greeting test files without additional configuration
- `GreetingService` tests run using only in-memory objects (no I/O)
- the container exits with code 0 when all tests pass

---

### GREETING-INFRA-001.2
**AS A** developer
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
**I WANT** the full greeting pipeline to be wired and executed by `main.py` in a single container run
**SO THAT** contact loading, birthday detection, message composition, and delivery happen in the correct sequence

**Architecture Reference:** Chapter 5 Building Block View — Main / Runner; Chapter 6 Runtime View — Successful Birthday Greeting; ADR-001 (Chapter 9 Architecture Decisions)

#### SCENARIO 1: Pipeline executes all steps in order inside the container
**Scenario ID**: GREETING-INFRA-001.3-S1
**Architecture Reference**: Chapter 6 Runtime View — Successful Birthday Greeting; ADR-001 (Chapter 9 Architecture Decisions)

**GIVEN**
- the Docker image has been built
- the container is started with the required environment variables set
- the SQLite database file is available (via volume mount or pre-initialised in the image)

**WHEN**
- `docker run <image> python main.py` is executed

**THEN**
- contacts are fetched first
- birthday detection and message composition follow for each matching contact
- delivery is invoked last for each composed message
- the container exits with code 0 on success

---

## Traceability Summary

| Field | Value |
|-------|-------|
| Parent Story | `GREETING-STORY-001` |
| Backend Sub-Stories | `GREETING-BE-001.1`, `GREETING-BE-001.2` |
| Infrastructure Sub-Stories | `GREETING-INFRA-001.1`, `GREETING-INFRA-001.2`, `GREETING-INFRA-001.3` |
| Architecture References | Chapter 1 FR-2/FR-3, Chapter 4 Solution Strategy — Dependency Direction, Chapter 5 Building Block View — Greeting Service / Main Runner, Chapter 6 Runtime View — Successful Birthday Greeting / No Birthdays Today, Chapter 8 Cross-cutting Concepts — Date Handling / Testability, Chapter 9 ADR-001 / ADR-004, Chapter 10 QS-1 / QS-3 |
| Testable Outcomes | birthday match on month/day only (year ignored); no match → no message composed; `GreetingService.compose()` returns correct Message with no I/O; pytest discovers greeting tests inside container; `GreetingService` unit-testable in isolation; pipeline steps execute in correct order inside container; exit code 0 on success |

---

# GREETING Story Bundle — GREETING-STORY-002

## Original Story

### GREETING-STORY-002
**AS A** system
**I WANT** to treat February 28 as the effective birthday for contacts born on February 29 in non-leap years
**SO THAT** those contacts still receive a greeting every year

**Architecture Reference:** Chapter 8 Cross-cutting Concepts — Date Handling

---

### SCENARIO 1: Feb 29 contact is greeted on Feb 28 in a non-leap year
**Scenario ID**: GREETING-STORY-002-S1
**Architecture Reference**: Chapter 8 Cross-cutting Concepts — Date Handling

**GIVEN**
- a contact has a date of birth of February 29
- today's date is February 28 in a non-leap year

**WHEN**
- the birthday check is evaluated for that contact

**THEN**
- the contact is treated as a match
- a greeting message is composed and passed to `EmailSender`

---

### SCENARIO 2: Feb 29 contact is greeted on Feb 29 in a leap year
**Scenario ID**: GREETING-STORY-002-S2
**Architecture Reference**: Chapter 8 Cross-cutting Concepts — Date Handling

**GIVEN**
- a contact has a date of birth of February 29
- today's date is February 29 in a leap year

**WHEN**
- the birthday check is evaluated for that contact

**THEN**
- the contact is matched on their actual birthday
- a greeting message is composed and passed to `EmailSender`

---

### SCENARIO 3: Feb 29 contact is not greeted on Feb 28 in a leap year
**Scenario ID**: GREETING-STORY-002-S3
**Architecture Reference**: Chapter 8 Cross-cutting Concepts — Date Handling

**GIVEN**
- a contact has a date of birth of February 29
- today's date is February 28 in a leap year

**WHEN**
- the birthday check is evaluated for that contact

**THEN**
- the contact is not matched
- no greeting is composed or sent

---

## Frontend Sub-Stories

The Birthday Greetings system has no user-facing interface (Chapter 3 Context and Scope). No frontend sub-stories are applicable.

---

## Backend Sub-Stories

### GREETING-BE-002.1
**AS A** system
**I WANT** the birthday matching logic to apply the Feb 28 substitution rule for Feb 29 birthdays in non-leap years
**SO THAT** the correct effective date is used during comparison

**Architecture Reference:** Chapter 8 Cross-cutting Concepts — Date Handling; Chapter 5 Building Block View — Greeting Service

#### SCENARIO 1: Effective date is Feb 28 when year is non-leap
**Scenario ID**: GREETING-BE-002.1-S1
**Architecture Reference**: Chapter 8 Cross-cutting Concepts — Date Handling

**GIVEN**
- a contact's date of birth is February 29
- the current year is not a leap year

**WHEN**
- the effective birthday date is computed

**THEN**
- the effective date is February 28 of the current year
- the comparison proceeds against February 28

#### SCENARIO 2: Effective date is Feb 29 when year is a leap year
**Scenario ID**: GREETING-BE-002.1-S2
**Architecture Reference**: Chapter 8 Cross-cutting Concepts — Date Handling

**GIVEN**
- a contact's date of birth is February 29
- the current year is a leap year

**WHEN**
- the effective birthday date is computed

**THEN**
- the effective date remains February 29
- no substitution is applied

---

## Infrastructure Sub-Stories

### GREETING-INFRA-002.1
**AS A** developer
**I WANT** the leap-year edge-case tests to run inside the Docker container
**SO THAT** the Feb 28/29 substitution rule is verified in the same environment as all other tests

**Architecture Reference:** Chapter 8 Cross-cutting Concepts — Date Handling; Chapter 8 Cross-cutting Concepts — Testability

#### SCENARIO 1: Leap-year tests are discovered and pass inside the container
**Scenario ID**: GREETING-INFRA-002.1-S1
**Architecture Reference**: Chapter 8 Cross-cutting Concepts — Testability

**GIVEN**
- the Docker image has been built
- test files covering the Feb 28/29 rule follow the `test_*.py` naming convention under `tests/`

**WHEN**
- `docker run <image> pytest` is executed

**THEN**
- pytest discovers and runs the leap-year scenario tests
- all three scenarios (non-leap match, leap match, leap non-match) pass
- the container exits with code 0

---

## Traceability Summary

| Field | Value |
|-------|-------|
| Parent Story | `GREETING-STORY-002` |
| Backend Sub-Stories | `GREETING-BE-002.1` |
| Infrastructure Sub-Stories | `GREETING-INFRA-002.1` |
| Architecture References | Chapter 8 Cross-cutting Concepts — Date Handling / Testability, Chapter 5 Building Block View — Greeting Service |
| Testable Outcomes | Feb 29 contact matched on Feb 28 in non-leap year; Feb 29 contact matched on Feb 29 in leap year; Feb 29 contact not matched on Feb 28 in leap year; leap-year tests run and pass inside Docker container |
