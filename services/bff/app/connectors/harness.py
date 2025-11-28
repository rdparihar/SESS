from __future__ import annotations
from datetime import datetime
import requests

from ..config import get_settings
from ..models import SyncCursor, CIEvent
from ..observability import traced_operation, Metrics


class HarnessConnector:
    def __init__(self):
        self.settings = get_settings().connectors

    def _headers(self) -> dict[str, str]:
        return {
            "x-api-key": self.settings.harness_api_key or "",
            "Content-Type": "application/json",
            "x-account-id": self.settings.harness_account_id or "",
        }

    def fetch_ci_events(self, session, since: str | None = None):
        params = {"page": 0, "pageSize": 50}
        if since:
            params["startingTime"] = since
        with traced_operation("harness_fetch_ci_events"):
            resp = requests.get(
                "https://app.harness.io/gateway/pipeline/api/pipelines/executions",
                headers=self._headers(),
                params=params,
                timeout=30,
            )
            Metrics.incr("harness.http_calls")
            resp.raise_for_status()
            return resp.json().get("data", [])

    def sync(self, session) -> None:
        cursor = self._get_cursor(session, "ci_events")
        since = cursor.cursor_value
        events = self.fetch_ci_events(session, since)
        for event in events:
            record = CIEvent(
                external_id=event.get("planExecutionId"),
                provider="harness",
                status=event.get("status"),
                occurred_at=datetime.fromtimestamp(event.get("startTs", datetime.utcnow().timestamp()) / 1000),
                project_id=event.get("projectIdentifier"),
            )
            session.add(record)
            since = event.get("startTs")
        self._update_cursor(session, "ci_events", str(since) if since else None)

    def _get_cursor(self, session, stream: str) -> SyncCursor:
        cursor = session.query(SyncCursor).filter_by(source="harness", stream=stream).one_or_none()
        if not cursor:
            cursor = SyncCursor(source="harness", stream=stream)
            session.add(cursor)
            session.flush()
        return cursor

    def _update_cursor(self, session, stream: str, cursor_value: str | None) -> None:
        cursor = self._get_cursor(session, stream)
        cursor.cursor_value = cursor_value
        Metrics.incr("harness.cursor_updates")
