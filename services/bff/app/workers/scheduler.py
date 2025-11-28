import time
from datetime import timedelta
from rq_scheduler import Scheduler
from redis import Redis

from ..config import get_settings
from .tasks import sync_all_sources


settings = get_settings()
redis_client = Redis.from_url(settings.redis.url)
scheduler = Scheduler(queue_name="sync", connection=redis_client)


def ensure_jobs() -> None:
    """Ensure the scheduled sync job exists."""
    existing_jobs = scheduler.get_jobs()
    if not any(job.func == sync_all_sources for job in existing_jobs):
        scheduler.schedule(
            scheduled_time=None,
            func=sync_all_sources,
            interval=timedelta(minutes=10).total_seconds(),
            repeat=None,
        )


if __name__ == "__main__":
    ensure_jobs()
    while True:
        time.sleep(60)
