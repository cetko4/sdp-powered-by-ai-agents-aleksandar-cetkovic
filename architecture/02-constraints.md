# 2. Architecture Constraints

## 2.1 Technical Constraints

| ID   | Constraint | Rationale |
|------|------------|-----------|
| TC-1 | Implementation language is Python. | Educational context; Module 2 assumes Python. |
| TC-2 | Storage is SQLite. | No infrastructure setup required; suitable for a single-process application. |
| TC-3 | Email delivery is delegated to an external email service (e.g., SMTP / SendGrid). | Avoids building a mail server; keeps the system focused on its core responsibility. |
| TC-4 | The application runs as a single process, triggered externally (e.g., cron). | Keeps deployment simple; no long-running daemon or web server needed. |

## 2.2 Organizational Constraints

| ID   | Constraint | Rationale |
|------|------------|-----------|
| OC-1 | The system is a self-contained kata, not a production service. | Scope is intentionally limited to support learning objectives. |
| OC-2 | No authentication or multi-user support is required. | Single-operator use case; out of scope for this exercise. |

## 2.3 Conventions

| ID   | Convention |
|------|------------|
| CV-1 | Code follows PEP 8 style guidelines. |
| CV-2 | Architecture is documented using the arc42 template and C4 model. |
| CV-3 | Diagrams are written in PlantUML using the C4-PlantUML library. |
