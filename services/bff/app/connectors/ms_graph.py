from __future__ import annotations
import requests
from datetime import datetime, timedelta

from ..config import get_settings
from ..models import SyncCursor, Incident
from ..observability import traced_operation, Metrics


class MSGraphConnector:
    def __init__(self):
        self.settings = get_settings().connectors
        self._token: str | None = None
        self._expiry: datetime | None = None

    def _get_token(self) -> str:
        if self._token and self._expiry and datetime.utcnow() < self._expiry:
            return self._token

        data = {
            "client_id": self.settings.ms_graph_client_id,
            "scope": "https://graph.microsoft.com/.default",
            "client_secret": self.settings.ms_graph_client_secret,
            "grant_type": "client_credentials",
        }
        resp = requests.post(
            f"https://login.microsoftonline.com/{self.settings.ms_graph_tenant_id}/oauth2/v2.0/token",
            data=data,
            timeout=30,
        )
        resp.raise_for_status()
        payload = resp.json()
        self._token = payload.get("access_token")
        self._expiry = datetime.utcnow() + timedelta(seconds=int(payload.get("expires_in", 3600)) - 60)
        return self._token

    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self._get_token()}"}

    def fetch_team_messages(self, session, since: str | None = None):
        params = {"$top": 50}
        if since:
            params["$filter"] = f"lastModifiedDateTime gt {since}"
        with traced_operation("msgraph_fetch_messages"):
            resp = requests.get(
                "https://graph.microsoft.com/v1.0/teams/messages",
                headers=self._headers(),
                params=params,
                timeout=30,
            )
            Metrics.incr("msgraph.http_calls")
            resp.raise_for_status()
            return resp.json().get("value", [])

    def sync(self, session) -> None:
        cursor = self._get_cursor(session, "messages")
        since = cursor.cursor_value
        messages = self.fetch_team_messages(session, since)
        for msg in messages:
            incident = Incident(
                external_id=msg.get("id"),
                title=msg.get("subject") or msg.get("body", {}).get("content", "Team message"),
                status="open",
                severity="info",
                detected_at=datetime.fromisoformat(msg.get("lastModifiedDateTime")),
            )
            session.add(incident)
            since = msg.get("lastModifiedDateTime")
        self._update_cursor(session, "messages", since)

    def _get_cursor(self, session, stream: str) -> SyncCursor:
        cursor = session.query(SyncCursor).filter_by(source="ms_graph", stream=stream).one_or_none()
        if not cursor:
            cursor = SyncCursor(source="ms_graph", stream=stream)
            session.add(cursor)
            session.flush()
        return cursor

    def _update_cursor(self, session, stream: str, cursor_value: str | None) -> None:
        cursor = self._get_cursor(session, stream)
        cursor.cursor_value = cursor_value
        Metrics.incr("msgraph.cursor_updates")
