# User Stories Overview

This document provides the story inventory for the Birthday Greetings kata.
It identifies the story domains, maps them to the architecture, and tracks prioritization and progress for requirements decomposition.

---

## Story Domains

Derived from the bounded responsibilities in Chapter 5 Building Block View and Chapter 3 Context and Scope:

| Domain | Responsibility |
|--------|---------------|
| `CONTACT` | Retrieving and managing person records (name, email, date of birth) from the SQLite data source |
| `GREETING` | Detecting today's birthdays and composing personalized greeting messages |
| `DELIVERY` | Sending composed messages via the external email service |

> `REMINDER` is not present in the architecture and is excluded.

---

## DDD Building Blocks

### Entities
- `Contact` — a person with identity tracked by their record in the SQLite database; carries name, email, and date of birth (Chapter 5 Building Block View — Contact Repository; Chapter 12 Glossary)

### Aggregates
- None explicitly identified from the architecture

### Value Objects
- `Message` — the composed greeting content produced by `GreetingService`; defined entirely by its text value, not by identity (Chapter 5 Building Block View — Greeting Service; Chapter 6 Runtime View — Successful Birthday Greeting)
- `BirthdayDate` — month/day pair used for birthday matching, ignoring year (Chapter 8 Cross-cutting Concepts — Date Handling)

### Domain Services
- `GreetingService` — domain logic for composing a greeting for a given contact; does not belong to the Contact entity itself (Chapter 5 Building Block View — Greeting Service)
- `ContactRepository` — domain service for querying contacts whose birthday matches today (Chapter 5 Building Block View — Contact Repository)

---

## Prioritized Story Inventory

### Core Stories (Pareto 20%)

| ID | Story | Rationale |
|----|-------|-----------|
| `CONTACT-STORY-001` | Retrieve contacts from SQLite whose birthday matches today | Required first step of the pipeline; nothing else runs without it |
| `GREETING-STORY-001` | Detect birthday and compose greeting message | Core business logic; directly delivers the system's primary value |
| `DELIVERY-STORY-001` | Send composed greeting via external email service | Final step; completes the end-to-end flow |

### Supporting Stories (Remaining 80%)

| ID | Story |
|----|-------|
| `GREETING-STORY-002` | Treat Feb 28 as effective birthday for Feb 29 in non-leap years |
| `CONTACT-STORY-002` | Handle missing or malformed contact records gracefully |
| `DELIVERY-STORY-002` | Handle email delivery failure with logging and non-zero exit |

---

## Pareto Prioritization

The minimum valuable flow of the Birthday Greetings system is covered by exactly three core stories:

1. `CONTACT-STORY-001` — loads the data
2. `GREETING-STORY-001` — applies the business rule and composes the message
3. `DELIVERY-STORY-001` — delivers the result

These three stories exercise every component in Chapter 5 Building Block View (`ContactRepository`, `GreetingService`, `EmailSender`, `main.py`), cover the primary runtime scenario in Chapter 6 Runtime View — Successful Birthday Greeting, and satisfy FR-1 through FR-3 from Chapter 1 Introduction and Goals.

All supporting stories address edge cases (leap year, bad data, delivery failure) or extensibility concerns. They add robustness but are not required for the core flow.

---

## Progress Tracking

📊 Pareto Progress: 3/3 core stories drafted
🎯 Core functionality coverage: ~100% of MVP story definition completed

| Story ID | Status | File |
|----------|--------|------|
| `GREETING-STORY-001` | ✅ Drafted | `docs/user-stories/greeting.md` |
| `CONTACT-STORY-001` | ✅ Drafted | `docs/user-stories/contact.md` |
| `DELIVERY-STORY-001` | ✅ Drafted | `docs/user-stories/delivery.md` |

---

## Traceability Approach

Every story bundle maintains traceability to the architecture and to testable outcomes:

- unique story ID following the `{DOMAIN}-STORY-{N}` convention
- architecture references to real sections from `architecture/`
- scenarios in GIVEN-WHEN-THEN format with a `Scenario ID`
- decomposition into Original, BE, and INFRA sub-stories (no FE — the system has no user-facing interface per Chapter 3 Context and Scope)

## Story Bundle Files

| File | Domain | Status |
|------|--------|--------|
| `docs/user-stories/greeting.md` | GREETING | ✅ Complete |
| `docs/user-stories/contact.md` | CONTACT | ✅ Complete |
| `docs/user-stories/delivery.md` | DELIVERY | ✅ Complete |
