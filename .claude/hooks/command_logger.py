#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///

import json
import sys
from datetime import datetime
from pathlib import Path

try:
    # Read hook input
    data = json.load(sys.stdin)

    # Create structured log entry
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "session_id": data.get("session_id", "unknown"),
        "tool_name": data.get("tool_name", ""),
        "tool_input": data.get("tool_input", {}),
    }

    # Extract the most relevant info based on tool type
    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})

    if tool_name == "Bash":
        log_entry["command"] = tool_input.get("command", "")
        log_entry["description"] = tool_input.get("description", "")
    elif tool_name in ["Write", "Edit", "MultiEdit"]:
        log_entry["file_path"] = tool_input.get("file_path", "")
        log_entry["action"] = tool_name
    else:
        log_entry["summary"] = f"{tool_name} action"

    # Append to JSON Lines file
    log_file = Path.home() / ".claude" / "logs" / "session_activity.jsonl"
    log_file.parent.mkdir(parents=True, exist_ok=True)

    with open(log_file, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

    # Also create a human-readable log
    simple_log = Path.home() / ".claude" / "logs" / "activity.log"
    with open(simple_log, "a") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if tool_name == "Bash":
            f.write(f"{timestamp} | {tool_name} | {log_entry.get('command', 'N/A')}\n")
        elif tool_name in ["Write", "Edit", "MultiEdit"]:
            f.write(
                f"{timestamp} | {tool_name} | {log_entry.get('file_path', 'N/A')}\n"
            )
        else:
            f.write(f"{timestamp} | {tool_name}\n")

except Exception as e:
    # Log errors but don't block Claude
    error_log = Path.home() / ".claude" / "logs" / "hook_errors.log"
    with open(error_log, "a") as f:
        f.write(f"{datetime.now()}: Logger error: {e}\n")
    sys.exit(0)

# Success - exit silently
sys.exit(0)
