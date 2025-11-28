from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy import text

from .config import get_settings
from .database import engine, Base
from .observability import Metrics
from .workers.tasks import enqueue_sync, enqueue_webhook


Base.metadata.create_all(bind=engine)
settings = get_settings()
app = FastAPI(title=settings.app_name)


@app.get("/health/live")
def liveness() -> dict[str, str]:
    return {"status": "live"}


@app.get("/health/ready")
def readiness() -> JSONResponse:
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return JSONResponse({"status": "ready"})
    except Exception as exc:
        return JSONResponse({"status": "degraded", "detail": str(exc)}, status_code=503)


@app.get("/metrics")
def metrics():
    return {"counters": Metrics.snapshot()}


@app.post("/webhooks/{source}")
async def handle_webhook(source: str, request: Request):
    payload = await request.json()
    enqueue_webhook(source, payload)
    return {"queued": True}


@app.post("/sync")
def trigger_sync():
    enqueue_sync()
    return {"queued": True}


@app.get("/config")
def config_view():
    return {
        "environment": settings.environment,
        "database": settings.database.url,
        "redis": settings.redis.url,
    }
