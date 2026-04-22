# Birthday Greetings

A Python implementation of the [Birthday Greetings kata](https://kata-log.rocks/birthday-greetings-kata) — automatically sending birthday email messages to contacts on their birthday, built using clean architecture and driven by AI agents across all development phases.

## What the Kata Solves

Given a list of contacts with names, birthdays, and email addresses, the system:
- detects which contacts have a birthday today (including leap-year Feb 29 birthdays)
- generates a personalised greeting message
- sends the greeting via email

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.12 |
| Testing | pytest |
| Linting | ruff, black, isort, bandit |
| Containerisation | Docker |
| CI/CD | GitHub Actions |
| Docs | Sphinx + GitHub Pages |

## Architecture Overview

The project follows a layered architecture with clear domain boundaries:

- `app/contact.py` — Contact entity and value objects
- `app/contact_repository.py` — Repository for loading contacts
- `app/birthday_match.py` — Domain logic for birthday detection
- `app/greeting_service.py` — Orchestration service
- `app/email_sender.py` — Email delivery adapter
- `app/message.py` — Greeting message value object

Full arc42 architecture documentation is available in [`docs/architecture/`](docs/architecture/) and rendered at the [Sphinx documentation site](https://cetko4.github.io/sdp-powered-by-ai-agents-aleksandar-cetkovic/).

## Build and Run Locally

**Prerequisites:** Docker

```bash
# Build the image
docker build -t birthday-greetings .

# Run the application
docker run --rm birthday-greetings python main.py
```

## Run Tests

```bash
# Run tests inside Docker
docker run --rm birthday-greetings pytest -q
```

Or locally with Python 3.12:

```bash
pip install -r requirements.txt
pytest -q
```

## Documentation

The full project documentation (architecture + user stories) is published via Sphinx:

🔗 https://cetko4.github.io/sdp-powered-by-ai-agents-aleksandar-cetkovic/

To build docs locally:

```bash
cd docs && make html
```

## Project Structure

```
.
├── app/                  # Application source code
├── tests/                # pytest test suite
├── docs/                 # Sphinx documentation
│   ├── architecture/     # arc42 architecture chapters
│   └── user-stories/     # Story bundles and inventory
├── .github/workflows/    # CI/CD and docs deploy pipelines
├── Dockerfile
├── main.py
└── requirements.txt
```

## Course Progress

- [x] Module 1: Git — workflow agent
- [x] Module 2: Software Architecture — arc42 design agent
- [x] Module 3: Software Requirements — user story derivation agent
- [x] Module 4: CI/CD — deployment pipeline agent
- [x] Module 5: TDD/BDD — multi-agent test system
- [x] Module 6: Birthday Greetings — project using all agents

## Author

**Aleksandar Cetkovic** — [@cetko4](https://github.com/cetko4)
