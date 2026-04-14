# 12. Glossary

| Term | Definition |
|------|------------|
| arc42 | A template for documenting software architectures, structured into 12 chapters. |
| C4 Model | A hierarchical approach to visualising software architecture using four levels: Context, Container, Component, and Code. |
| Contact | A person stored in the system with a name, email address, and date of birth. |
| ContactRepository | The module responsible for querying the SQLite database and returning contacts whose birthday matches today. |
| Container | In C4 terminology, a deployable or runnable unit within a system (e.g., the Python application, the SQLite database). |
| Cron | A Unix-based OS scheduler used to trigger the application once per day at a configured time. |
| Dependency Injection | A design technique where a component's dependencies are passed in from outside rather than created internally, enabling easier testing and substitution. |
| EmailSender | The module responsible for sending a composed greeting message via the external email service. |
| External Email Service | A third-party SMTP server or API (e.g., SendGrid) used to deliver emails to recipients. |
| GreetingService | The module responsible for composing a personalised greeting message for a given contact. |
| Kata | A small, self-contained coding exercise used to practise software design principles. |
| Pipeline | A sequential flow of processing steps where the output of one step is the input of the next. |
| PlantUML | A text-based diagramming tool used to render architecture diagrams from plain-text descriptions. |
| SQLite | A lightweight, file-based relational database engine available in Python's standard library. |
