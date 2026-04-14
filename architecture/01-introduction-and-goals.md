# 1. Introduction and Goals

## 1.1 Purpose

The Birthday Greetings system automatically detects contacts whose birthday falls on the current date and sends them a personalized greeting email. It is designed as a simple, educational example for Module 2, demonstrating clean separation of concerns in a lightweight Python application.

## 1.2 Functional Requirements

| ID   | Requirement |
|------|-------------|
| FR-1 | The system reads contact data (name, email, date of birth) from a local SQLite database. |
| FR-2 | On each run, the system identifies contacts whose birthday matches today's date. |
| FR-3 | The system sends a greeting email to each identified contact via an external email service. |
| FR-4 | The system can be triggered manually or by a scheduler (e.g., cron). |

## 1.3 Quality Goals

| Priority | Quality Goal | Motivation |
|----------|--------------|------------|
| 1 | Testability | Core logic (birthday detection, message composition) must be unit-testable without network or database access. |
| 2 | Simplicity | The architecture must remain easy to understand and explain in an educational context. |
| 3 | Maintainability | Replacing the email provider or storage backend should require minimal changes. |

## 1.4 Stakeholders

| Role | Expectation |
|------|-------------|
| Developer / Student | Learns clean architecture principles through a concrete, small-scale example. |
| System Operator | Runs the application daily via a scheduler with no manual intervention. |
| Contact (Birthday Person) | Receives a timely, personalized greeting email on their birthday. |
