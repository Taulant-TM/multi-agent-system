# Project Risks Register

## Delivery Risks
- The project depends on a third-party payment provider.
- Any delay from the vendor may impact the delivery timeline.
- Third-party payment provider integration may delay release by 2 weeks.
- Mitigation: Early vendor coordination + fallback provider shortlist.

## Security Risks
- A full security review is scheduled for the next sprint.
- Potential vulnerabilities may require rework or delay release.
- Authentication module pending penetration testing.
- Mitigation: Pre-review checklist + security audit dry run.

## Resource Risks
- Limited availability of senior engineers during peak periods.
- Senior engineers unavailable during Q4 peak sprint.
- Mitigation: Temporary contractor onboarding.

## Operational Risks
- Billing API uptime dependency (99.5% SLA).
  Mitigation: Retry logic + circuit breaker.