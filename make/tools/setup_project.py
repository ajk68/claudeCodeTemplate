#!/usr/bin/env python3
"""
Project Setup Script - Initialize a new project from this template
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


def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"  Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print_success(description)
        return True
    else:
        print_error(f"{description} failed")
        if result.stderr:
            print(f"  Error: {result.stderr}")
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


def setup_git():
    """Initialize git and protect against template pollution"""
    print_step("Setting up Git")

    # Check if this is the template repository
    if Path(".git").exists():
        # Get current remote URL
        result = subprocess.run(
            "git remote get-url origin 2>/dev/null",
            shell=True,
            capture_output=True,
            text=True,
        )
        current_remote = result.stdout.strip()

        if (
            "claudeCodeTemplate" in current_remote
            or "claude-code-template" in current_remote
        ):
            print_error("⚠️  WARNING: This appears to be the template repository!")
            print_warning("You should not use the template directly. Instead:")
            print("\n  1. Use GitHub: Click 'Use this template' button")
            print("  2. Or clone to a new directory:")
            print(f"     git clone {current_remote} ../my-new-project")
            print("     cd ../my-new-project")
            print("     make setup\n")

            if (
                input(
                    "Do you want to disconnect from template and continue? (y/N): "
                ).lower()
                == "y"
            ):
                run_command("git remote remove origin", "Removed template remote")
                print_success("Disconnected from template repository")
                print_warning("Remember to add your own repository as origin:")
                print("  git remote add origin <your-repo-url>")
            else:
                print("Setup cancelled to protect template.")
                sys.exit(0)
        else:
            print_success("Git repository already initialized")
    else:
        # Fresh setup - no .git directory
        if run_command("git init", "Git repository initialized"):
            run_command("git add .", "Added files to git")
            run_command(
                'git commit -m "Initial commit from Claude Code template"',
                "Created initial commit",
            )
            print_warning("Remember to add your repository as origin:")
            print("  git remote add origin <your-repo-url>")


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

    # Python dependencies
    if run_command("uv sync", "Python dependencies installed"):
        pass
    else:
        print_warning("Failed to install Python dependencies")

    # Node.js dependencies
    if Path("package.json").exists():
        if run_command("npm install", "Node.js dependencies installed"):
            pass
        else:
            print_warning("Failed to install Node.js dependencies")


def setup_mcp_servers():
    """Setup MCP servers for Claude Code"""
    print_step("Setting up MCP servers")

    mcp_script = Path(__file__).parent / "setup_mcp_servers.py"
    if mcp_script.exists():
        if run_command(f"uv run python {mcp_script} --auto", "MCP servers configured"):
            print_warning("Restart Claude Code to load the new MCP servers")
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

    setup_git()
    setup_environment()
    install_dependencies()
    setup_claude_settings()
    setup_mcp_servers()
    personalize_project()
    print_next_steps()


if __name__ == "__main__":
    main()
