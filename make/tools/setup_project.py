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


def get_project_info():
    """Interactively collect project information"""
    print_step("Project Configuration")

    # Get current directory name as default project name
    current_dir = Path.cwd().name

    print("\nLet's configure your project:")

    # Project name
    project_name = input(f"Project name [{current_dir}]: ").strip() or current_dir

    # Project description
    description = input("Brief project description: ").strip()
    if not description:
        description = "A new project built with Claude Code Template"

    # Author info
    author_name = input("Your name: ").strip()
    author_email = input("Your email: ").strip()

    # Python version (with default)
    python_version = input("Python version [3.12]: ").strip() or "3.12"

    return {
        "name": project_name,
        "description": description,
        "author_name": author_name,
        "author_email": author_email,
        "python_version": python_version,
    }


def update_pyproject_toml(project_info):
    """Update pyproject.toml with project information"""
    pyproject_path = Path("pyproject.toml")

    if not pyproject_path.exists():
        print_warning("pyproject.toml not found, skipping update")
        return

    try:
        content = pyproject_path.read_text()

        # Update project metadata
        content = content.replace(
            'name = "claude-dev-template"', f'name = "{project_info["name"]}"'
        )
        content = content.replace(
            'description = "A template for AI-assisted development with Claude"',
            f'description = "{project_info["description"]}"',
        )

        # Add author info if provided (insert after description line)
        if project_info["author_name"] and project_info["author_email"]:
            authors_line = f'authors = [{{name = "{project_info["author_name"]}", email = "{project_info["author_email"]}"}}]'
            # Find the description line and add authors after it
            lines = content.split("\n")
            for i, line in enumerate(lines):
                if line.startswith("description = "):
                    lines.insert(i + 1, authors_line)
                    content = "\n".join(lines)
                    break

        # Update Python version
        content = content.replace(
            'requires-python = ">=3.12"',
            f'requires-python = ">={project_info["python_version"]}"',
        )

        pyproject_path.write_text(content)
        print_success("Updated pyproject.toml with your project information")

    except Exception as e:
        print_error(f"Failed to update pyproject.toml: {e}")


def personalize_project():
    """Guide user through personalizing the template"""
    print_step("Additional Configuration")

    files_to_update = {
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

    print("\nDon't forget to update these files:")
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

    # Get project information interactively
    project_info = get_project_info()
    update_pyproject_toml(project_info)

    setup_environment()
    install_dependencies()
    setup_claude_settings()
    setup_mcp_servers()
    personalize_project()
    print_next_steps()


if __name__ == "__main__":
    main()
