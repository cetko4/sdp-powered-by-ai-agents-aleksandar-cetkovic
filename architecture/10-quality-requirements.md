# 10. Quality Requirements

## 10.1 Quality Tree

The three quality goals from Chapter 1 are refined into concrete, measurable scenarios.

## 10.2 Quality Scenarios

### Testability

| ID   | Scenario | Stimulus | Expected Response |
|------|----------|----------|-------------------|
| QS-1 | Unit test birthday detection | Call `GreetingService.compose()` with a contact object | Returns correct message with no database or network access |
| QS-2 | Unit test contact filtering | Call `ContactRepository` with a fake in-memory connection | Returns only contacts matching today's month and day |
| QS-3 | Unit test full pipeline | Run `main` pipeline with fake repository and fake sender | Fake sender receives exactly the expected messages; no real I/O occurs |

### Simplicity

| ID   | Scenario | Stimulus | Expected Response |
|------|----------|----------|-------------------|
| QS-4 | New developer onboarding | Developer reads the codebase for the first time | Can understand the full flow by reading four files in under 10 minutes |
| QS-5 | Running the system | Operator executes `python main.py` | System runs end-to-end with a single command and no configuration beyond env vars |

### Maintainability

| ID   | Scenario | Stimulus | Expected Response |
|------|----------|----------|-------------------|
| QS-6 | Swap email provider | Replace SMTP with a REST API provider | Only `email_sender.py` needs to change; no other module is touched |
| QS-7 | Change greeting message format | Update the greeting text or template | Only `greeting_service.py` needs to change |
| QS-8 | Replace SQLite with another store | Migrate contact storage to a CSV file or remote DB | Only `contact_repository.py` needs to change |
