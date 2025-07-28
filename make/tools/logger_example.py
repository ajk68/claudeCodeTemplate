#!/usr/bin/env python3
"""Example usage of the logger utility."""

from logger import Logger, info, warning, error

# Method 1: Class-based logger with custom name
custom_logger = Logger("my-service")
custom_logger.info("Service started")
custom_logger.warning("Config file missing, using defaults")
custom_logger.error("Failed to connect to database")

# Method 2: Module-level convenience functions (uses script name)
info("Processing batch job")
warning("Low memory detected")
error("Batch job failed")

# Method 3: Multiple loggers for different components
db_logger = Logger("database")
api_logger = Logger("api")

db_logger.info("Connection established")
api_logger.info("Server listening on port 8000")
