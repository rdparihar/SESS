import logging
import time
from contextlib import contextmanager
from typing import Iterator

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)
logger = logging.getLogger("bff")


class Metrics:
    counters: dict[str, int] = {}

    @classmethod
    def incr(cls, name: str, value: int = 1) -> None:
        cls.counters[name] = cls.counters.get(name, 0) + value
        logger.debug("metric_incremented", extra={"metric": name, "value": cls.counters[name]})

    @classmethod
    def snapshot(cls) -> dict[str, int]:
        return dict(cls.counters)


@contextmanager
def traced_operation(operation: str) -> Iterator[None]:
    start = time.time()
    logger.info("starting_operation", extra={"operation": operation})
    try:
        yield
        duration = time.time() - start
        logger.info("operation_completed", extra={"operation": operation, "duration_ms": duration * 1000})
    except Exception:
        logger.exception("operation_failed", extra={"operation": operation})
        raise
