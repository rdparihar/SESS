import os
from functools import lru_cache
from pydantic import BaseModel


class DatabaseSettings(BaseModel):
    url: str = os.getenv("DATABASE_URL", "postgresql+psycopg2://sess:sess@localhost:5432/sess")


class RedisSettings(BaseModel):
    url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")


class ConnectorSettings(BaseModel):
    jira_base_url: str = os.getenv("JIRA_BASE_URL", "https://example.atlassian.net")
    jira_api_token: str | None = os.getenv("JIRA_API_TOKEN")
    jira_webhook_secret: str | None = os.getenv("JIRA_WEBHOOK_SECRET")

    servicenow_base_url: str = os.getenv("SERVICENOW_BASE_URL", "https://example.service-now.com")
    servicenow_user: str | None = os.getenv("SERVICENOW_USER")
    servicenow_password: str | None = os.getenv("SERVICENOW_PASSWORD")

    harness_account_id: str | None = os.getenv("HARNESS_ACCOUNT_ID")
    harness_api_key: str | None = os.getenv("HARNESS_API_KEY")

    ms_graph_tenant_id: str | None = os.getenv("MS_GRAPH_TENANT_ID")
    ms_graph_client_id: str | None = os.getenv("MS_GRAPH_CLIENT_ID")
    ms_graph_client_secret: str | None = os.getenv("MS_GRAPH_CLIENT_SECRET")


class Settings(BaseModel):
    app_name: str = "SESS BFF"
    environment: str = os.getenv("ENVIRONMENT", "local")
    database: DatabaseSettings = DatabaseSettings()
    redis: RedisSettings = RedisSettings()
    connectors: ConnectorSettings = ConnectorSettings()

    class Config:
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
