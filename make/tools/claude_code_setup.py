#!/usr/bin/env python3
"""
Simple wrapper to pack Claude Code files with repomix.
"""

import subprocess
import sys
from datetime import datetime

# Files to include from current project
PROJECT_PATTERNS = ".claude/**,CLAUDE.md,tools/**"

# Files to include from home directory
HOME_PATTERNS = (
    "~/.claude/settings.json,~/.claude/hooks/**,~/.claude/ide/**,~/.claude/CLAUDE.md"
)


def main():
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_file = f"/tmp/claude-code-setup-{timestamp}.txt"

    # Build the repomix command
    cmd = [
        "repomix",
        "--include",
        f"{PROJECT_PATTERNS},{HOME_PATTERNS}",
        "--output",
        output_file,
        ".",
    ]

    print(f"🚀 Running: {' '.join(cmd)}")

    # Run it
    result = subprocess.run(cmd)

    if result.returncode == 0:
        print(f"\n✅ Packed to: {output_file}")

    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
