# User Stories Overview

This document provides the story inventory for the Birthday Greetings kata.
It identifies the story domains, maps them to the architecture, and tracks prioritization and progress for requirements decomposition.

## Story Domains

The following domains are derived from the architecture and the kata requirements:

- `CONTACT` - responsible for retrieving and managing person data from the configured source
- `GREETING` - responsible for detecting birthdays and generating birthday greetings
- `DELIVERY` - responsible for sending greetings through the configured communication channel
- `REMINDER` - responsible for notifying other people about birthdays when reminder flows are enabled

## Domain-Driven Design Building Blocks

### CONTACT
Handles access to person records, including first name, last name, date of birth, and email address.
This domain isolates data access concerns from greeting and delivery logic.

### GREETING
Encapsulates the core business rules for deciding whether a greeting should be created.
It includes birthday date matching and special handling for edge cases such as leap-year birthdays.

### DELIVERY
Represents the outbound communication mechanism used to send messages.
This domain makes it possible to support multiple delivery channels without changing the greeting rules.

### REMINDER
Supports additional notification flows beyond direct birthday greetings.
This includes sending reminders to other people and grouping multiple birthdays into a single reminder.

## Prioritized Story Inventory

### Core Stories (Pareto 20%)

These stories provide the essential end-to-end value of the system:

- `CONTACT-STORY-001`
  **AS A** system
  **I WANT** to retrieve person records from the configured data source
  **SO THAT** I can determine whose birthday is today

- `GREETING-STORY-001`
  **AS A** system
  **I WANT** to detect when a person has a birthday today and generate a greeting
  **SO THAT** the person receives a birthday message on the correct day

- `DELIVERY-STORY-001`
  **AS A** system
  **I WANT** to send the generated greeting through the configured delivery channel
  **SO THAT** the recipient receives the birthday message

### Supporting Stories

These stories extend flexibility, robustness, and non-core scenarios:

- `GREETING-STORY-002`
  **AS A** system
  **I WANT** to treat February 28 as the effective birthday for February 29 birthdays in non-leap years
  **SO THAT** leap-year birthdays are still recognized every year

- `CONTACT-STORY-002`
  **AS A** system
  **I WANT** to support multiple contact data sources
  **SO THAT** the application can switch between flat files and databases

- `DELIVERY-STORY-002`
  **AS A** system
  **I WANT** to support multiple delivery channels
  **SO THAT** greetings can be sent by email or SMS

- `REMINDER-STORY-001`
  **AS A** system
  **I WANT** to send birthday reminders to other people
  **SO THAT** they are informed about current birthdays

- `REMINDER-STORY-002`
  **AS A** system
  **I WANT** to group multiple birthdays into a single reminder
  **SO THAT** notifications are more efficient and easier to read

## Pareto Prioritization

The minimum valuable flow of the Birthday Greetings kata is covered by these three core stories:

1. `CONTACT-STORY-001`
2. `GREETING-STORY-001`
3. `DELIVERY-STORY-001`

These stories together deliver the main outcome of the system:

- load person records
- detect today's birthdays
- generate a greeting
- send the greeting

All other stories are supporting stories because they improve extensibility, edge-case handling, or additional notification behavior, but are not required for the primary end-to-end flow.

## Progress Tracking

📊 Pareto Progress: 1/3 core stories drafted
🎯 Core functionality coverage: ~33% of MVP story definition completed

### Current Status

- `CONTACT-STORY-001` - not yet drafted
- `GREETING-STORY-001` - drafted manually in `docs/user-stories/greeting.md`
- `DELIVERY-STORY-001` - not yet drafted

## Traceability Approach

Each story bundle must maintain traceability to the architecture and to testable outcomes.

Every story should include:

- a unique story ID following the required naming convention
- architecture references to real sections from `architecture/`
- scenarios written in GIVEN-WHEN-THEN format
- traceable decomposition into Original, FE, BE, and INFRA stories where applicable

## Story Bundle Files

Story bundles are stored in separate files under `docs/user-stories/` by domain.

Current and planned files:

- `docs/user-stories/greeting.md`
- `docs/user-stories/contact.md`
- `docs/user-stories/delivery.md`
- `docs/user-stories/reminder.md`
