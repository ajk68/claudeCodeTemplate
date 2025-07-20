#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///

import json
import sys
import re
import os
from pathlib import Path
from datetime import datetime


# Simple logging
def log(action, correction):
    log_file = Path.home() / ".claude" / "logs" / "corrections.log"
    log_file.parent.mkdir(parents=True, exist_ok=True)
    with open(log_file, "a") as f:
        f.write(f"{datetime.now():%Y-%m-%d %H:%M:%S} | {action} → {correction}\n")


try:
    data = json.load(sys.stdin)
    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})

    # Bash command replacements
    if tool_name == "Bash":
        command = tool_input.get("command", "")

        # pip → uv
        if "pip install" in command:
            packages = command.split("pip install", 1)[1].strip()
            log("pip install", "uv add")
            print(f"Use 'uv add {packages}' instead of pip install", file=sys.stderr)
            sys.exit(2)

        # python script.py → uv run python script.py
        if re.match(r"^python\s+\S+\.py", command.strip()):
            if not re.search(r"python\s+-[mc]", command):  # Allow python -m, -c
                fixed = command.replace("python ", "uv run python ", 1)
                log("python", "uv run python")
                print(f"Use '{fixed}' instead", file=sys.stderr)
                sys.exit(2)

        # grep → rg
        if re.search(r"\bgrep\s+-r\b|\bgrep\s+.*-r", command):
            log("grep -r", "rg")
            print(
                "Use 'rg' (ripgrep) instead of grep for faster searching",
                file=sys.stderr,
            )
            sys.exit(2)

    # Block _v2 file creation
    elif tool_name in ["Write", "Create"]:
        filename = os.path.basename(tool_input.get("file_path", ""))

        # Check for version suffixes
        if re.search(r"_v\d+\.|_new\.|_copy\.|_old\.", filename, re.IGNORECASE):
            log("version suffix file", "edit original")
            print(
                f"Don't create '{filename}'. Edit the original file instead.",
                file=sys.stderr,
            )
            sys.exit(2)

except Exception:
    pass  # Silent fail to not disrupt Claude

sys.exit(0)
