import logging
from datetime import UTC, datetime


class _UTCFormatter(logging.Formatter):
    def formatTime(self, record: logging.LogRecord, datefmt: str | None = None) -> str:  # noqa: N802
        return datetime.fromtimestamp(record.created, UTC).strftime(datefmt or "%Y-%m-%dT%H:%M:%S")


def configure_logging(level: str) -> None:
    handler = logging.StreamHandler()
    handler.setFormatter(_UTCFormatter("%(asctime)sZ %(levelname)s %(name)s %(message)s", "%Y-%m-%dT%H:%M:%S"))
    logging.basicConfig(level=level.upper(), handlers=[handler], force=True)
