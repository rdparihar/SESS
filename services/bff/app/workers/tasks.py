from __future__ import annotations
import json
from rq import Queue
from redis import Redis

from ..config import get_settings
from ..database import session_scope
from ..connectors.jira import JiraConnector
from ..connectors.servicenow import ServiceNowConnector
from ..connectors.harness import HarnessConnector
from ..connectors.ms_graph import MSGraphConnector
from ..observability import logger, Metrics


settings = get_settings()
redis_client = Redis.from_url(settings.redis.url)
queue = Queue("sync", connection=redis_client)


def sync_all_sources() -> None:
    with session_scope() as session:
        JiraConnector().sync(session)
        ServiceNowConnector().sync(session)
        HarnessConnector().sync(session)
        MSGraphConnector().sync(session)
        Metrics.incr("sync_all_runs")
        logger.info("sync_all_sources_completed")


def handle_webhook(source: str, payload: dict) -> None:
    with session_scope() as session:
        logger.info("webhook_received", extra={"source": source})
        if source == "jira":
            JiraConnector().handle_webhook(session, payload)
        elif source == "servicenow":
            ServiceNowConnector().handle_webhook(session, payload)
        elif source == "harness":
            HarnessConnector().sync(session)
        elif source == "ms_graph":
            MSGraphConnector().sync(session)
        else:
            logger.warning("webhook_source_unknown", extra={"source": source})
        Metrics.incr(f"webhook.{source}")


def enqueue_sync() -> None:
    queue.enqueue(sync_all_sources)


def enqueue_webhook(source: str, payload: dict) -> None:
    queue.enqueue(handle_webhook, source, payload)

