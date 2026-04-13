# ADR-001: Technology Decisions for Birthday Greetings

## Status
Accepted

## Context
The Birthday Greetings kata requires a small system that can store contact data, check birthdays, and send greeting emails. The solution should be simple, easy to understand, and suitable for architectural documentation.

## Decision
The system will use Python as the implementation language, a simple application layer without a heavy web framework, and SQLite as the data storage solution. Email delivery will be handled through an external email service.

## Rationale
Python is easy to read and suitable for a small educational project. A lightweight application structure keeps the kata simple and focused on architecture rather than framework complexity. SQLite is sufficient because the system has limited data and does not require distributed storage.

## Consequences
The solution will be easy to implement and document, but it will not be optimized for large-scale production workloads. If the system grows, a more robust framework and database may be needed.
