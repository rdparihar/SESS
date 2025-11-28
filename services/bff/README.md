# SESS Backend-for-Frontend (BFF)

A FastAPI-based service that provides a data model for users, teams, projects, incidents, CI events, runbooks, PTO, and allocations. It integrates with Jira, ServiceNow, Harness, and Microsoft Graph for Teams, using Redis/RQ for asynchronous sync and webhook ingestion.

## Running locally

```bash
pip install -r services/bff/requirements.txt
uvicorn app.main:app --reload --app-dir services/bff
```

Provide a PostgreSQL database URL via `DATABASE_URL` or override `services/bff/app/config.py` defaults. Redis is required for the worker queue.

## Seeding data

```bash
python -m services.bff.app.seeds.seed_data
```

## Background workers

Run an RQ worker and the scheduler to process sync jobs and handle webhooks:

```bash
rq worker sync --url redis://localhost:6379/0
python -m services.bff.app.workers.scheduler
```

## Health & Observability

* `GET /health/live` simple liveness
* `GET /health/ready` database connectivity check
* `GET /metrics` in-memory counters for sync/webhook activity
