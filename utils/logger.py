import logging
import os
from logging.handlers import RotatingFileHandler

from config.settings import settings


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    logger.setLevel(log_level)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Check if we're running in a production environment (like Render)
    # where file system is ephemeral/read-only
    is_production = os.getenv("RENDER") or os.getenv("RAILWAY") or os.getenv("FLY_APP_NAME")
    
    # Only add file handler in local development
    if not is_production:
        try:
            os.makedirs("logs", exist_ok=True)
            file_handler = RotatingFileHandler(
                "logs/access.log", maxBytes=5_000_000, backupCount=3
            )
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except (OSError, PermissionError) as e:
            # If file logging fails, just log to console
            print(f"Warning: Could not setup file logging: {e}")

    # Always add console handler (works everywhere)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


def setup_logger(name: str) -> logging.Logger:
    return get_logger(name)