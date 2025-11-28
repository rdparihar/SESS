from __future__ import annotations
import json
from datetime import datetime, timedelta
import requests

from ..config import get_settings
from ..models import SyncCursor, Incident, WebhookEvent
from ..observability import logger, traced_operation, Metrics


class ServiceNowConnector:
    def __init__(self):
        self.settings = get_settings().connectors

    def _auth(self) -> tuple[str | None, str | None]:
        return self.settings.servicenow_user, self.settings.servicenow_password

    def fetch_incidents(self, session, since: str | None = None):
        params = {"sysparm_query": "ORDERBYDESCsys_updated_on"}
        if since:
            params["sysparm_query"] += f"^sys_updated_on>{since}"
        with traced_operation("servicenow_fetch_incidents"):
            resp = requests.get(
                f"{self.settings.servicenow_base_url}/api/now/table/incident",
                auth=self._auth(),
                params=params,
                timeout=30,
            )
            Metrics.incr("servicenow.http_calls")
            resp.raise_for_status()
            return resp.json().get("result", [])

    def sync(self, session) -> None:
        cursor = self._get_cursor(session, "incidents")
        since = cursor.cursor_value
        incidents = self.fetch_incidents(session, since)
        for record in incidents:
            incident = Incident(
                external_id=record.get("sys_id"),
                title=record.get("short_description"),
                status=record.get("state"),
                severity=record.get("priority"),
                detected_at=datetime.fromisoformat(record.get("sys_created_on")),
            )
            session.add(incident)
            since = record.get("sys_updated_on")
        self._update_cursor(session, "incidents", since)

    def handle_webhook(self, session, payload: dict) -> None:
        event = WebhookEvent(source="servicenow", external_id=payload.get("sys_id"), payload=json.dumps(payload))
        session.add(event)
        self.sync(session)

    def rate_limit_wait(self, session, stream: str) -> None:
        cursor = self._get_cursor(session, stream)
        if cursor.rate_limit_reset and cursor.rate_limit_reset > datetime.utcnow():
            Metrics.incr("servicenow.rate_limited")
            raise RuntimeError("ServiceNow rate limit in effect")

    def set_rate_limit(self, session, stream: str, retry_after_seconds: int) -> None:
        cursor = self._get_cursor(session, stream)
        cursor.rate_limit_reset = datetime.utcnow() + timedelta(seconds=retry_after_seconds)

    def _get_cursor(self, session, stream: str) -> SyncCursor:
        cursor = session.query(SyncCursor).filter_by(source="servicenow", stream=stream).one_or_none()
        if not cursor:
            cursor = SyncCursor(source="servicenow", stream=stream)
            session.add(cursor)
            session.flush()
        return cursor

    def _update_cursor(self, session, stream: str, cursor_value: str | None) -> None:
        cursor = self._get_cursor(session, stream)
        cursor.cursor_value = cursor_value
