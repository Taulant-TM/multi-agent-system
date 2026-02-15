# Architecture Notes

The system integrates with external APIs for authentication and billing.
External dependencies increase operational risk if service availability is impacted.

## Architecture Overview

- External Dependencies:
    - Payment API
    - Auth API
    - Billing provider

## Approach A: Monolithic API Layer
Pros:
- Simple deployment
- Easier debugging

Cons:
- Harder to scale

## Approach B: Microservices
Pros:
- Independent scaling
- Better fault isolation

Cons:
- Operational complexity
- Higher infrastructure cost
