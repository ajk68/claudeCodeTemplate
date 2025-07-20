#!/usr/bin/env python3
"""
Project Setup Script - Configure environment and dependencies

This script is called by bootstrap.py or 'make setup' to configure
a new project after the template has been cloned.

It handles:
- Checking prerequisites
- Setting up .env file
- Installing dependencies
- Configuring Claude settings
- Setting up MCP servers
"""

import subprocess
import sys
from pathlib import Path
import shutil


class Colors:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    END = "\033[0m"


def print_step(msg):
    print(f"\n{Colors.BLUE}➤ {msg}{Colors.END}")


def print_success(msg):
    print(f"{Colors.GREEN}✓ {msg}{Colors.END}")


def print_warning(msg):
    print(f"{Colors.YELLOW}⚠ {msg}{Colors.END}")


def print_error(msg):
    print(f"{Colors.RED}✗ {msg}{Colors.END}")


def run_command(cmd, description, critical=True):
    """Run a command and handle errors"""
    print(f"  Running: {cmd}")
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            print_success(description)
            return True
        else:
            print_error(f"{description} failed")
            if result.stderr:
                print(f"  Error: {result.stderr}")
            if critical:
                raise SystemExit(1)
            return False
    except subprocess.TimeoutExpired:
        print_error(f"{description} timed out after 30 seconds")
        if critical:
            raise SystemExit(1)
        return False
    except Exception as e:
        print_error(f"{description} failed with error: {str(e)}")
        if critical:
            raise SystemExit(1)
        return False


def check_prerequisites():
    """Check if required tools are installed"""
    print_step("Checking prerequisites")

    tools = {
        "uv": "Python package manager (install from https://github.com/astral-sh/uv)",
        "npm": "Node.js package manager",
        "git": "Version control",
        "rg": "ripgrep for fast searching",
        "claude": "Claude Code CLI",
    }

    all_good = True
    for tool, description in tools.items():
        if shutil.which(tool):
            print_success(f"{tool} - {description}")
        else:
            print_error(f"{tool} - {description} - NOT FOUND")
            all_good = False

    return all_good


def setup_environment():
    """Setup .env file from .env-example"""
    print_step("Setting up environment file")

    env_file = Path(".env")
    env_example = Path(".env-example")

    if env_file.exists():
        print_success(".env file already exists")
    elif env_example.exists():
        shutil.copy(env_example, env_file)
        print_success("Created .env from .env-example")
        print_warning("Please edit .env and add your API keys")
    else:
        # Create a basic .env file
        env_content = """# API Keys
PERPLEXITY_API_KEY=
ANTHROPIC_API_KEY=
OPENAI_API_KEY=
GOOGLE_API_KEY=
GH_TOKEN=

# Database (if needed)
DB_URL=postgresql://
"""
        env_file.write_text(env_content)
        print_success("Created .env file with template")
        print_warning("Please edit .env and add your API keys")


def install_dependencies():
    """Install Python and Node.js dependencies"""
    print_step("Installing dependencies")

    # Check if uv is installed before attempting to use it
    if shutil.which("uv"):
        run_command("uv sync", "Python dependencies installed", critical=False)
    else:
        print_warning("uv not found - skipping Python dependency installation")
        print("  Install uv from: https://github.com/astral-sh/uv")

    # Node.js dependencies
    if Path("package.json").exists():
        if shutil.which("npm"):
            run_command("npm install", "Node.js dependencies installed", critical=False)
        else:
            print_warning("npm not found - skipping Node.js dependency installation")


def setup_mcp_servers():
    """Setup MCP servers for Claude Code"""
    print_step("Setting up MCP servers")

    mcp_script = Path(__file__).parent / "setup_mcp_servers.py"
    if mcp_script.exists():
        if shutil.which("uv") and run_command(
            f"uv run python {mcp_script} --auto",
            "MCP servers configured",
            critical=False,
        ):
            print_warning("Restart Claude Code to load the new MCP servers")
        else:
            print_warning("MCP server setup skipped - install uv to enable")
    else:
        print_error("MCP setup script not found")


def personalize_project():
    """Guide user through personalizing the template"""
    print_step("Personalizing your project")

    files_to_update = {
        "pyproject.toml": [
            "Update project name",
            "Update description",
            "Add your project-specific dependencies",
        ],
        "CLAUDE.md": [
            "Fill in the 'Project Specific Instructions' section",
            "Add your project overview",
            "Document key architectural decisions",
        ],
        ".env": [
            "Add your API keys",
            "Configure any project-specific environment variables",
        ],
    }

    print("\nFiles to update:")
    for file, tasks in files_to_update.items():
        print(f"\n  {Colors.YELLOW}{file}{Colors.END}")
        for task in tasks:
            print(f"    • {task}")


def setup_claude_settings():
    """Setup .claude/settings.json if it doesn't exist"""
    print_step("Setting up Claude Code settings")

    claude_dir = Path(".claude")
    settings_file = claude_dir / "settings.json"

    if not claude_dir.exists():
        claude_dir.mkdir()
        print_success("Created .claude directory")

    if not settings_file.exists():
        settings_content = """{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{
        "type": "command",
        "command": "make format"
      }]
    }]
  }
}"""
        settings_file.write_text(settings_content)
        print_success("Created .claude/settings.json with format hook")


def print_next_steps():
    """Print next steps for the user"""
    print(f"\n{Colors.GREEN}{'=' * 60}{Colors.END}")
    print(f"{Colors.GREEN}✨ Setup Complete!{Colors.END}")
    print(f"{Colors.GREEN}{'=' * 60}{Colors.END}")

    print("\n📝 Next steps:")
    print("1. Edit .env and add your API keys")
    print("2. Update pyproject.toml with your project details")
    print("3. Fill in CLAUDE.md with project-specific instructions")
    print("4. Restart Claude Code to load MCP servers")
    print("5. Run 'make help' to see available commands")
    print("\n🚀 Start developing with: claude")


def main():
    print(f"{Colors.BLUE}{'=' * 60}{Colors.END}")
    print(f"{Colors.BLUE}Claude Code Template - Project Setup{Colors.END}")
    print(f"{Colors.BLUE}{'=' * 60}{Colors.END}")

    # Check we're in the right directory
    if not Path("Makefile").exists() or not Path("TEMPLATE_GUIDE.md").exists():
        print_error("This doesn't look like the template directory!")
        print("Please run this from the root of your cloned template.")
        sys.exit(1)

    # Run setup steps
    if not check_prerequisites():
        print_warning("\nSome prerequisites are missing. Please install them first.")
        if input("\nContinue anyway? (y/N): ").lower() != "y":
            sys.exit(1)

    setup_environment()
    install_dependencies()
    setup_claude_settings()
    setup_mcp_servers()
    personalize_project()
    print_next_steps()


if __name__ == "__main__":
    main()
