#!/usr/bin/env python3
"""
Simple MCP server setup script - generates shell commands to add MCP servers.
"""

import sys
import os
from pathlib import Path
import shutil

# Available MCP servers
SERVERS = {
    "perplexity": {
        "description": "Perplexity AI search integration",
        "command": 'claude mcp add-json perplexity \'{"command": "npx", "args": ["-y", "server-perplexity-ask"], "env": {"PERPLEXITY_API_KEY": "${PERPLEXITY_API_KEY}"}}\'',
        "requires_env": ["PERPLEXITY_API_KEY"],
        "url": "https://www.perplexity.ai/settings/api"
    },
    "context7": {
        "description": "Context7 documentation and code context",
        "command": 'claude mcp add-json context7 \'{"command": "npx", "args": ["-y", "@upstash/context7-mcp"]}\'',
        "requires_env": [],
        "url": "https://github.com/upstash/context7-mcp"
    },
    "playwright": {
        "description": "Browser automation and testing",
        "command": 'claude mcp add-json playwright \'{"command": "npx", "args": ["-y", "@playwright/mcp@latest"]}\'',
        "requires_env": [],
        "url": "https://github.com/microsoft/playwright"
    },
    "repoprompt": {
        "description": "Repository analysis and code understanding",
        "command": "claude mcp add repoprompt {path}",
        "requires_env": [],
        "url": "https://github.com/aorwall/RepoPrompt",
        "needs_path": True
    },
    "repomix": {
        "description": "Repository mixing and codebase bundling",
        "command": "claude mcp add repomix -- npx -y repomix --mcp",
        "requires_env": [],
        "url": "https://github.com/yamadashy/repomix"
    }
}


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


def print_usage():
    """Print usage information"""
    print("Usage:")
    print("  python setup_mcp_servers.py [options] [server_names...]")
    print()
    print("Options:")
    print("  --list          List all available MCP servers")
    print("  --install       Install servers automatically")
    print("  --help, -h      Show this help message")
    print()
    print("Examples:")
    print("  python setup_mcp_servers.py --list")
    print("  python setup_mcp_servers.py --install")
    print("  python setup_mcp_servers.py --install perplexity context7")
    print("  python setup_mcp_servers.py")

def list_servers():
    """List all available MCP servers"""
    print("Available MCP Servers")
    print("=" * 50)
    print()
    
    for name, info in SERVERS.items():
        status = "✓" if name in check_existing_servers() else " "
        env_note = ""
        if info["requires_env"]:
            env_note = f" (requires: {', '.join(info['requires_env'])})"
        
        print(f"[{status}] {name:<12} - {info['description']}{env_note}")
    
    print()
    print("Legend: ✓ = already installed")

def get_server_command(name, info, env_vars, repoprompt_path=None):
    """Get the installation command for a server"""
    cmd = info["command"]
    
    # Handle RepoPrompt path substitution
    if name == "repoprompt":
        if repoprompt_path:
            cmd = cmd.format(path=f'"{repoprompt_path}"')
        else:
            return None
    
    # Substitute environment variables
    for key, value in env_vars.items():
        cmd = cmd.replace(f"${{{key}}}", value)
    
    return cmd

def main():
    # Parse command line arguments
    args = sys.argv[1:]
    
    if "--help" in args or "-h" in args:
        print_usage()
        return
    
    if "--list" in args:
        list_servers()
        return

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

    # Check for missing API keys
    missing_keys = []
    for server_name, info in SERVERS.items():
        for env_key in info["requires_env"]:
            if env_key not in env_vars or not env_vars[env_key]:
                missing_keys.append((server_name, env_key, info.get("url", "")))

    if missing_keys:
        print("⚠️  Warning: Missing API keys:")
        for server_name, key, url in missing_keys:
            print(f"   {server_name}: {key}")
            if url:
                print(f"     Get your key from: {url}")
        print()

    # Find RepoPrompt installation
    repoprompt_path = find_repoprompt()
    if not repoprompt_path:
        print("⚠️  Warning: RepoPrompt not found. Install it or provide the path manually.")
        print("   Visit: https://github.com/aorwall/RepoPrompt")
        print()

    # Execute mode if --install flag is passed
    if "--install" in args:
        import subprocess

        # Remove --install from args to get server names
        server_args = [arg for arg in args if arg != "--install"]
        
        # If no specific servers specified, install all
        if not server_args:
            servers_to_install = list(SERVERS.keys())
        else:
            servers_to_install = server_args
            # Validate server names
            invalid_servers = [s for s in servers_to_install if s not in SERVERS]
            if invalid_servers:
                print(f"❌ Invalid server names: {', '.join(invalid_servers)}")
                print(f"Available servers: {', '.join(SERVERS.keys())}")
                return

        # Check existing servers
        existing_servers = check_existing_servers()
        print("Checking for existing MCP servers...")
        if existing_servers:
            print(f"Found existing servers: {', '.join(sorted(existing_servers))}")

        success_count = 0
        skipped_count = 0
        failed_count = 0

        for server_name in servers_to_install:
            info = SERVERS[server_name]
            
            # Skip if already exists
            if server_name in existing_servers:
                print(f"✓ Already installed: {server_name}")
                skipped_count += 1
                continue

            # Skip RepoPrompt if not found
            if server_name == "repoprompt" and not repoprompt_path:
                print("⚠️  Skipping RepoPrompt (not found)")
                failed_count += 1
                continue

            # Skip if missing required environment variables
            missing_env = [key for key in info["requires_env"] if key not in env_vars or not env_vars[key]]
            if missing_env:
                print(f"⚠️  Skipping {server_name} (missing: {', '.join(missing_env)})")
                failed_count += 1
                continue

            # Get installation command
            cmd = get_server_command(server_name, info, env_vars, repoprompt_path)
            if not cmd:
                print(f"⚠️  Skipping {server_name} (could not generate command)")
                failed_count += 1
                continue

            print(f"Installing: {server_name}")
            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                if result.returncode == 0:
                    print("✓ Success")
                    success_count += 1
                else:
                    print(f"✗ Failed: {result.stderr or result.stdout}")
                    failed_count += 1
            except Exception as e:
                print(f"✗ Error: {e}")
                failed_count += 1

        # Print summary
        print("\n📊 Summary:")
        if success_count > 0:
            print(f"   ✅ Added {success_count} new MCP servers")
        if skipped_count > 0:
            print(f"   ⏭️  Skipped {skipped_count} already installed servers")
        if failed_count > 0:
            print(f"   ❌ Failed to install {failed_count} servers")
        
        if success_count > 0:
            print("   🔄 Restart Claude Code to load the new servers")
    else:
        # Display mode
        print("MCP Server Setup Commands")
        print("=" * 50)
        print()

        for server_name, info in SERVERS.items():
            cmd = get_server_command(server_name, info, env_vars, repoprompt_path)
            if cmd:
                print(f"# {server_name}: {info['description']}")
                print(cmd)
                print()
            else:
                print(f"# {server_name}: {info['description']} (unavailable)")
                if server_name == "repoprompt":
                    print("# RepoPrompt not found - install it first")
                print()

        print("To use: Copy and run each command above, then restart Claude Code")
        print()
        print("Or use: python setup_mcp_servers.py --install [server_names...]")


if __name__ == "__main__":
    main()
