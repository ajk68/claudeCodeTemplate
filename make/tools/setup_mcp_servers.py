#!/usr/bin/env python3
"""
Simple MCP server setup script - generates shell commands to add MCP servers.
"""

import sys
from pathlib import Path

# Shell commands to add MCP servers
COMMANDS = [
    'claude mcp add-json perplexity \'{"command": "npx", "args": ["-y", "server-perplexity-ask"], "env": {"PERPLEXITY_API_KEY": "${PERPLEXITY_API_KEY}"}}\'',
    'claude mcp add-json context7 \'{"command": "npx", "args": ["-y", "@upstash/context7-mcp"]}\'',
    'claude mcp add-json playwright \'{"command": "npx", "args": ["-y", "@playwright/mcp@latest"]}\'',
    "claude mcp add repoprompt ~/RepoPrompt/repoprompt_cli",
]


def main():
    # Load .env file if it exists
    env_vars = {}
    env_file = Path(__file__).parent.parent.parent / ".env"
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    env_vars[key.strip()] = value.strip().strip('"').strip("'")

    # Execute mode if --auto flag is passed
    if len(sys.argv) > 1 and sys.argv[1] == "--auto":
        import subprocess

        for cmd in COMMANDS:
            # Substitute environment variables
            for key, value in env_vars.items():
                cmd = cmd.replace(f"${{{key}}}", value)

            print(f"Executing: {cmd}")
            subprocess.run(cmd, shell=True)
        print("\nDone! Restart Claude Code to load the MCP servers.")
    else:
        # Display mode
        print("MCP Server Setup Commands")
        print("=" * 50)
        print()

        for cmd in COMMANDS:
            # Substitute environment variables
            for key, value in env_vars.items():
                cmd = cmd.replace(f"${{{key}}}", value)
            print(cmd)
            print()

        print("To use: Copy and run each command above, then restart Claude Code")


if __name__ == "__main__":
    main()
