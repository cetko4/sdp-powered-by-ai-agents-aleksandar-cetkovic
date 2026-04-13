# 7. Deployment View

## 7.1 Overview

The system runs on a single machine. There is no server, container runtime, or cloud infrastructure required. The SQLite database is a file on the same machine. The only external dependency is the email service, reached over the network.

See [`diagrams/deployment.puml`](diagrams/deployment.puml).

## 7.2 Deployment Nodes

| Node | Description |
|------|-------------|
| Developer / Operator Machine | Any machine with Python 3.x installed; runs the script and hosts the SQLite file |
| OS Scheduler (cron) | Triggers `main.py` once per day at a configured time |
| External Email Service | Third-party SMTP server or API (e.g., SendGrid); reached over HTTPS or SMTP |

## 7.3 Deployment Steps

1. Clone the repository onto the target machine.
2. Install dependencies: `pip install -r requirements.txt`
3. Initialise the database: `python init_db.py`
4. Add a cron entry to run daily:
   ```
   0 8 * * * /usr/bin/python3 /path/to/main.py
   ```
5. Configure email credentials via environment variables (see Chapter 8).
