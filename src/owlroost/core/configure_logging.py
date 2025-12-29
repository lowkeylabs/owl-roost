# src/owlroost/core/configure_logging.py

import sys
from typing import Union

from loguru import logger

try:
    from omegaconf import DictConfig
except ImportError:  # pragma: no cover
    DictConfig = None


LOG_LEVELS = {
    "TRACE",
    "DEBUG",
    "INFO",
    "SUCCESS",
    "WARNING",
    "ERROR",
    "CRITICAL",
}


def configure_logging(
    log_level: Union[str, "DictConfig"] | None = "INFO",
):
    """
    Configure Loguru logging.

    Accepts:
      - string log level (e.g. "INFO", "DEBUG")
      - Hydra DictConfig with cfg.logging.level
    """

    # ------------------------------------------------------------
    # Extract level from Hydra config if provided
    # ------------------------------------------------------------
    if DictConfig and isinstance(log_level, DictConfig):
        log_level = log_level.get("logging", {}).get("level", "INFO")

    if not log_level:
        return

    log_level = str(log_level).upper()

    if log_level not in LOG_LEVELS:
        raise ValueError(f"Invalid log level: {log_level}")

    # ------------------------------------------------------------
    # Reset Loguru handlers
    # ------------------------------------------------------------
    logger.remove()

    # ------------------------------------------------------------
    # Add stderr handler
    # ------------------------------------------------------------
    logger.add(
        sys.stderr,
        level=log_level,
        format=(
            "<level>{level:8}</level> | "
            "<cyan>{name}</cyan>:"
            "<cyan>{function}</cyan>:"
            "<cyan>{line}</cyan> - "
            "<level>{message}</level>"
        ),
        backtrace=(log_level == "TRACE"),
        diagnose=(log_level == "TRACE"),
        enqueue=False,  # IMPORTANT for Hydra multiruns / multiprocessing
    )

    logger.debug("Loguru configured (level={})", log_level)
