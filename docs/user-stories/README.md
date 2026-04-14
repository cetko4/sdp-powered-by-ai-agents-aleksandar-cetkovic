# User Stories Overview

This document provides the story inventory for the Birthday Greetings kata.
It identifies the main story domains, maps them to the architecture, and defines the prioritized stories for implementation.

## Story Domains

The following domains are derived from the architecture and core kata requirements:

- `CONTACT` - responsible for retrieving and managing person data from the configured data source
- `GREETING` - responsible for deciding when a birthday greeting should be created and what it should contain
- `DELIVERY` - responsible for sending messages through the selected communication channel
- `REMINDER` - responsible for notifying other people about upcoming or current birthdays

## Domain-Driven Design Building Blocks

### CONTACT
Handles access to person records, including name, birth date, and email address.

### GREETING
Encapsulates the business rules for birthday greeting generation, including special cases such as leap year birthdays.

### DELIVERY
Represents the message delivery mechanism, such as email or SMS, and isolates communication concerns from business logic.

### REMINDER
Supports additional notification flows, such as sending birthday reminders to others or grouping multiple birthday notifications into one message.

## Prioritized Story Inventory

### Core Stories (Pareto 20%)

These stories deliver the main business value of the kata:

- `CONTACT-STORY-001`
  **AS A** system
  **I WANT** to retrieve people from the data source
  **SO THAT** I can determine whose birthday is today

- `GREETING-STORY-001`
  **AS A** system
  **I WANT** to identify when a person has a birthday today
  **SO THAT** I can generate a birthday greeting

- `DELIVERY-STORY-001`
  **AS A** system
  **I WANT** to send a birthday greeting through the configured channel
  **SO THAT** the recipient receives the message

### Supporting Stories

These stories add flexibility and completeness but are not part of the minimal core flow:

- `GREETING-STORY-002`
  **AS A** system
  **I WANT** to treat February 28 as the birthday for February 29 birthdays in non-leap years
  **SO THAT** leap-year birthdays are still recognized every year

- `REMINDER-STORY-001`
  **AS A** system
  **I WANT** to send birthday reminders to other people
  **SO THAT** they are informed about birthdays

- `REMINDER-STORY-002`
  **AS A** system
  **I WANT** to group multiple birthdays into a single reminder
  **SO THAT** notifications are more efficient and easier to read

- `DELIVERY-STORY-002`
  **AS A** system
  **I WANT** to support multiple delivery channels
  **SO THAT** greetings can be sent by email or SMS

- `CONTACT-STORY-002`
  **AS A** system
  **I WANT** to support multiple contact data sources
  **SO THAT** the application can switch between flat files and databases

## Pareto Prioritization

The following stories represent the minimum valuable product and should be implemented first:

1. `CONTACT-STORY-001`
2. `GREETING-STORY-001`
3. `DELIVERY-STORY-001`

These stories cover the essential end-to-end scenario:

- read contacts
- detect birthdays
- send greetings

All remaining stories extend the system with flexibility, edge-case handling, and additional notification features.

## Progress Tracking

📊 Pareto Progress: 0/3 core stories completed
🎯 Core functionality coverage: 0% of MVP flow implemented

## Traceability Approach

Each story must be traceable to:

- an architecture section from Module 2
- a story ID
- acceptance criteria in GIVEN-WHEN-THEN format
- testable assertions

Story bundles will be stored in separate files under `docs/user-stories/` by domain.

Planned files:

- `docs/user-stories/contact.md`
- `docs/user-stories/greeting.md`
- `docs/user-stories/delivery.md`
- `docs/user-stories/reminder.md`
