#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "ruff>=0.1.0",
# ]
# ///

import json
import sys
import subprocess
from pathlib import Path

try:
    # Read hook input
    data = json.load(sys.stdin)

    # Check tool name
    tool_name = data.get("tool_name", "")
    if tool_name not in ["Write", "Edit", "MultiEdit", "mcp__repoprompt__apply_edits"]:
        sys.exit(0)

    # Extract file path based on tool type
    tool_input = data.get("tool_input", {})
    if tool_name == "mcp__repoprompt__apply_edits":
        file_path = tool_input.get("path", "")
    else:
        file_path = tool_input.get("file_path", "")

    if not file_path.endswith((".py", ".pyi")):
        sys.exit(0)

    # Check if file exists
    if not Path(file_path).exists():
        sys.exit(0)

    # First check for issues WITHOUT fixing
    check_result = subprocess.run(
        ["ruff", "check", file_path, "--output-format=json"],
        capture_output=True,
        text=True,
    )

    if check_result.returncode != 0 and check_result.stdout:
        issues = json.loads(check_result.stdout)
        if issues:
            # Auto-fix safe issues
            subprocess.run(
                ["ruff", "check", "--fix", file_path, "--quiet"], capture_output=True
            )

            # Check again to see what couldn't be auto-fixed
            recheck = subprocess.run(
                ["ruff", "check", file_path, "--output-format=json"],
                capture_output=True,
                text=True,
            )

            if recheck.returncode != 0 and recheck.stdout:
                remaining_issues = json.loads(recheck.stdout)
                if remaining_issues:
                    # Write a note for Claude about unfixed issues
                    print(
                        f"\n⚠️  Ruff found issues in {file_path} that need manual fixing:"
                    )
                    for issue in remaining_issues[:3]:  # Show max 3 issues
                        print(
                            f"  Line {issue['location']['row']}: {issue['code']} - {issue['message']}"
                        )
                    if len(remaining_issues) > 3:
                        print(f"  ... and {len(remaining_issues) - 3} more issues")
                    print("  Consider running: ruff check --fix " + file_path)

    # Always format after fixing
    subprocess.run(["ruff", "format", file_path, "--quiet"], capture_output=True)

except Exception as e:
    # Silent failure - we don't want to interrupt Claude
    pass

sys.exit(0)
