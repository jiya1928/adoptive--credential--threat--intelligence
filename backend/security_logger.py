from loguru import logger
import os

os.makedirs(
    "logs",
    exist_ok=True
)

logger.add(
    "logs/security.log",
    rotation="10 MB",
    retention="30 days",
    level="INFO"
)


def log_security_event(
    event_type,
    details
):

    logger.info(
        f"{event_type}: {details}"
    )