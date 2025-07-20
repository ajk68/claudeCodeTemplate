#!/usr/bin/env python3
"""
Simple MCP server setup script - generates shell commands to add MCP servers.
"""

import sys
import os
from pathlib import Path
import shutil

# Shell commands to add MCP servers
COMMANDS = [
    'claude mcp add-json perplexity \'{"command": "npx", "args": ["-y", "server-perplexity-ask"], "env": {"PERPLEXITY_API_KEY": "${PERPLEXITY_API_KEY}"}}\'',
    'claude mcp add-json context7 \'{"command": "npx", "args": ["-y", "@upstash/context7-mcp"]}\'',
    'claude mcp add-json playwright \'{"command": "npx", "args": ["-y", "@playwright/mcp@latest"]}\'',
    "claude mcp add repoprompt ~/RepoPrompt/repoprompt_cli",
]


def find_repoprompt():
    """Find RepoPrompt installation"""
    possible_paths = [
        Path.home() / "RepoPrompt/repoprompt_cli",
        Path.home() / ".local/bin/repoprompt",
        Path("/usr/local/bin/repoprompt"),
    ]
    for path in possible_paths:
        if path.exists():
            return str(path)

    # Check if it's in PATH
    if shutil.which("repoprompt"):
        return "repoprompt"

    return None


def check_existing_servers():
    """Check which MCP servers are already installed"""
    try:
        import subprocess

        result = subprocess.run(
            ["claude", "mcp", "list"], capture_output=True, text=True
        )
        if result.returncode == 0:
            # Parse output like "perplexity: npx -y server-perplexity-ask"
            servers = set()
            for line in result.stdout.strip().split("\n"):
                if ":" in line:
                    server_name = line.split(":")[0].strip()
                    servers.add(server_name.lower())
            return servers
        return set()
    except Exception:
        return set()


def main():
    # Load .env file if it exists
    env_vars = {}
    env_file = Path(__file__).parent.parent.parent / ".env"
    if env_file.exists():
        try:
            with open(env_file) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, value = line.split("=", 1)
                        env_vars[key.strip()] = value.strip().strip('"').strip("'")
        except Exception as e:
            print(f"Warning: Could not read .env file: {e}")

    # Also check environment variables
    for key in ["PERPLEXITY_API_KEY", "ANTHROPIC_API_KEY", "OPENAI_API_KEY"]:
        if key in os.environ and key not in env_vars:
            env_vars[key] = os.environ[key]

    # Check for missing API key
    if "PERPLEXITY_API_KEY" not in env_vars or not env_vars["PERPLEXITY_API_KEY"]:
        print("⚠️  Warning: PERPLEXITY_API_KEY not found in .env or environment")
        print("   The Perplexity MCP server will not work without this key.")
        print("   Get your API key from: https://www.perplexity.ai/settings/api")
        if len(sys.argv) > 1 and sys.argv[1] == "--auto":
            env_vars["PERPLEXITY_API_KEY"] = "YOUR_API_KEY_HERE"

    # Find RepoPrompt installation
    repoprompt_path = find_repoprompt()
    if repoprompt_path:
        # Update the RepoPrompt command with the actual path
        COMMANDS[3] = f'claude mcp add repoprompt "{repoprompt_path}"'
    else:
        print(
            "⚠️  Warning: RepoPrompt not found. Install it or provide the path manually."
        )
        print("   Visit: https://github.com/aorwall/RepoPrompt")

    # Execute mode if --auto flag is passed
    if len(sys.argv) > 1 and sys.argv[1] == "--auto":
        import subprocess

        # Check existing servers
        existing_servers = check_existing_servers()
        print("Checking for existing MCP servers...")
        if existing_servers:
            print(f"Found existing servers: {', '.join(sorted(existing_servers))}")

        success_count = 0
        skipped_count = 0

        for cmd in COMMANDS:
            # Extract server name from command
            server_name = None
            if "claude mcp add-json" in cmd:
                # Extract name between add-json and the JSON
                parts = cmd.split()
                for i, part in enumerate(parts):
                    if part == "add-json" and i + 1 < len(parts):
                        server_name = parts[i + 1].lower()
                        break
            elif "claude mcp add" in cmd:
                # For repoprompt: claude mcp add repoprompt ...
                if "repoprompt" in cmd:
                    server_name = "repoprompt"

            # Skip if already exists
            if server_name and server_name in existing_servers:
                print(f"✓ Already installed: {server_name}")
                skipped_count += 1
                continue

            # Skip RepoPrompt if not found
            if "repoprompt" in cmd and not repoprompt_path:
                print("⚠️  Skipping RepoPrompt (not found)")
                continue

            # Substitute environment variables
            for key, value in env_vars.items():
                cmd = cmd.replace(f"${{{key}}}", value)

            print(f"Installing: {server_name or 'unknown'}")
            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                if result.returncode == 0:
                    print("✓ Success")
                    success_count += 1
                else:
                    print(f"✗ Failed: {result.stderr or result.stdout}")
            except Exception as e:
                print(f"✗ Error: {e}")

        if success_count > 0 or skipped_count > 0:
            print("\n✅ Summary:")
            if success_count > 0:
                print(f"   - Added {success_count} new MCP servers")
            if skipped_count > 0:
                print(f"   - Skipped {skipped_count} already installed servers")
            if success_count > 0:
                print("   - Restart Claude Code to load the new servers")
        else:
            print("\n❌ No MCP servers were added. Check the errors above.")
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
