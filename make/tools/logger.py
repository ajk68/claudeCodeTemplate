#!/usr/bin/env python3
"""Simple logging utility for writing to centralized logs directory."""

import sys
from datetime import datetime
from pathlib import Path


class Logger:
    """Zero-dependency logger that writes to logs/backend/ directory."""

    def __init__(self, name=None):
        """Initialize logger with optional name (defaults to script name)."""
        self.name = name or Path(sys.argv[0]).stem or "unknown"
        self.log_dir = Path(__file__).parent.parent.parent / "logs" / "backend"
        self._ensure_log_dir()

    def _ensure_log_dir(self):
        """Create log directory if it doesn't exist."""
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def _write_log(self, level, message):
        """Write timestamped log message to file."""
        # Use UTC timestamp in ISO format
        # Note: utcnow() is deprecated in Python 3.12+ but still works
        # Using it for simplicity and zero-dependency requirement
        import warnings

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        log_entry = f"[{timestamp}] [{level}] [{self.name}] {message}\n"

        log_file = self.log_dir / f"{self.name}.log"
        try:
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(log_entry)
                f.flush()
        except Exception as e:
            # Fall back to stderr if file writing fails
            sys.stderr.write(f"Failed to write log: {e}\n")
            sys.stderr.write(log_entry)

    def info(self, message):
        """Log info level message."""
        self._write_log("INFO", message)

    def warning(self, message):
        """Log warning level message."""
        self._write_log("WARNING", message)

    def error(self, message):
        """Log error level message."""
        self._write_log("ERROR", message)


# Module-level convenience functions
_default_logger = None


def get_logger(name=None):
    """Get or create a logger instance."""
    global _default_logger
    if name:
        return Logger(name)
    if _default_logger is None:
        _default_logger = Logger()
    return _default_logger


def info(message):
    """Log info message using default logger."""
    get_logger().info(message)


def warning(message):
    """Log warning message using default logger."""
    get_logger().warning(message)


def error(message):
    """Log error message using default logger."""
    get_logger().error(message)


if __name__ == "__main__":
    # Simple test
    logger = Logger("test")
    logger.info("Test info message")
    logger.warning("Test warning message")
    logger.error("Test error message")

    # Test module-level functions
    info("Module-level info")
    warning("Module-level warning")
    error("Module-level error")
