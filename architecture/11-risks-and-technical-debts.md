# 11. Risks and Technical Debts

## 11.1 Risks

| ID   | Risk | Probability | Impact | Mitigation |
|------|------|-------------|--------|------------|
| R-1 | Email service unavailable at send time | Low | Medium | Log the error and exit with code 1 so cron can alert the operator |
| R-2 | Cron job not configured or misconfigured | Medium | High | Document the required cron entry explicitly (Chapter 7); verify with a dry run after deployment |
| R-3 | Leap-year contacts (Feb 29) silently skipped | Low | Low | Explicit policy documented in Chapter 8: send on Feb 28 in non-leap years |
| R-4 | Email credentials exposed via environment | Low | High | Use a secrets manager or `.env` file with restricted file permissions; never commit credentials |

## 11.2 Technical Debts

| ID   | Debt | Impact | Accepted Because |
|------|------|--------|-----------------|
| TD-1 | No retry logic for failed email sends | A transient network error causes a missed greeting | Acceptable for an educational kata; retry logic would add complexity disproportionate to the scope |
| TD-2 | No deduplication guard against double sends | Re-running the script on the same day sends duplicate emails | Out of scope; the operator is responsible for running the script once per day via cron |
| TD-3 | SQLite not suitable for concurrent access | Breaks if two processes run simultaneously | Not a concern for a single-operator, cron-triggered script |
| TD-4 | No input validation on contact data | Malformed email addresses or missing fields cause runtime errors | Acceptable at kata scale; production use would require validation on data entry |
