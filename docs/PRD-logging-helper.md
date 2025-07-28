# PRD: Logging Helper Utility
Date: 2025-07-27
Author: planner agent

## Problem Statement
The template currently has centralized logging infrastructure (shoreman.sh, logs/ directory structure) but lacks a programmatic logging utility for Python and TypeScript code. Developers need a simple way to write timestamped log messages with different severity levels that integrate with the existing logging system.

## Success Metrics
- Zero additional dependencies required
- Works seamlessly with existing make logs-* commands
- Sub-100ms overhead per log write
- Developers can add logging with single function call

## User Stories
As a developer, I want to call a simple log function so that my debug messages appear in the centralized logs with proper timestamps and levels.

As a developer, I want the logs directory created automatically so that I don't get file not found errors.

As an operator, I want consistent log formatting across Python and TypeScript so that I can parse logs easily.

## Solution Overview
Create minimal logging helper modules for Python and TypeScript that write to the appropriate logs/ subdirectories with ISO timestamps and standard log levels.

## Constraints & Non-Goals
- NOT doing: Complex log rotation (handled externally)
- NOT doing: Network logging or remote sinks
- NOT doing: Custom formatters or handlers
- NOT doing: Async logging (keep it simple)
- Constraints: Must work with Python 3.12+ and modern TypeScript

## Risks & Mitigations
| Risk | Impact | Mitigation |
|------|--------|------------|
| File I/O blocking | L | Simple synchronous writes are fine for development |
| Log file growth | M | Document need for external rotation/cleanup |
| Concurrent writes | L | OS handles file append operations safely |