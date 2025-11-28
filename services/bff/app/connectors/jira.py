from __future__ import annotations
import json
from datetime import datetime
from typing import Iterable
import requests

from ..config import get_settings
from ..models import SyncCursor, Incident, WebhookEvent
from ..observability import logger, traced_operation, Metrics


class JiraConnector:
    def __init__(self):
        self.settings = get_settings().connectors

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.settings.jira_api_token}" if self.settings.jira_api_token else "",
            "Content-Type": "application/json",
        }

    def fetch_incidents(self, session, since: str | None = None) -> Iterable[dict]:
        params = {"expand": "renderedFields", "orderBy": "-updated"}
        if since:
            params["updated"] = since
        with traced_operation("jira_fetch_incidents"):
            response = requests.get(
                f"{self.settings.jira_base_url}/rest/api/3/search",
                headers=self._headers(),
                params=params,
                timeout=30,
            )
            Metrics.incr("jira.http_calls")
            response.raise_for_status()
            return response.json().get("issues", [])

    def ingest_incident(self, session, issue: dict) -> None:
        project_key = issue.get("fields", {}).get("project", {}).get("name", "Unknown")
        summary = issue.get("fields", {}).get("summary", "Untitled")
        incident = Incident(
            external_id=issue.get("id"),
            title=summary,
            status=issue.get("fields", {}).get("status", {}).get("name", "open"),
            severity=issue.get("fields", {}).get("priority", {}).get("name"),
            detected_at=datetime.fromisoformat(issue.get("fields", {}).get("updated")),
        )
        session.add(incident)
        logger.info("jira_issue_ingested", extra={"external_id": issue.get("id"), "project": project_key})

    def sync(self, session) -> None:
        cursor = self._get_cursor(session, stream="incidents")
        since = cursor.cursor_value
        issues = self.fetch_incidents(session, since=since)
        for issue in issues:
            self.ingest_incident(session, issue)
            since = issue.get("fields", {}).get("updated")
        self._update_cursor(session, "incidents", since)

    def handle_webhook(self, session, payload: dict) -> None:
        event = WebhookEvent(source="jira", external_id=payload.get("id"), payload=json.dumps(payload))
        session.add(event)
        self.ingest_incident(session, payload)
        self._update_cursor(session, "incidents", payload.get("fields", {}).get("updated"))

    def _get_cursor(self, session, stream: str) -> SyncCursor:
        cursor = session.query(SyncCursor).filter_by(source="jira", stream=stream).one_or_none()
        if not cursor:
            cursor = SyncCursor(source="jira", stream=stream, cursor_value=None)
            session.add(cursor)
            session.flush()
        return cursor

    def _update_cursor(self, session, stream: str, cursor_value: str | None) -> None:
        cursor = self._get_cursor(session, stream)
        cursor.cursor_value = cursor_value
        Metrics.incr("jira.cursor_updates")
