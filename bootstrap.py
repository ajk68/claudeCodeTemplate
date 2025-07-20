#!/usr/bin/env python3
"""
Claude Code Template Bootstrap Script

This script creates a new project from the Claude Code Template.
It can be run directly from GitHub or downloaded and run locally.

Usage:
    # Direct from GitHub:
    curl -sSL https://raw.githubusercontent.com/ajk68/claudeCodeTemplate/main/bootstrap.py | python3 - my-project

    # Or download first:
    python3 bootstrap.py my-project

    # With options:
    python3 bootstrap.py my-project --branch v2.0 --no-setup
"""

import subprocess
import sys
import os
from pathlib import Path
import shutil
import argparse


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


def run_command(cmd, description, cwd=None):
    """Run a command and handle errors"""
    try:
        result = subprocess.run(
            cmd, cwd=cwd, capture_output=True, text=True, check=True
        )
        print_success(description)
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"{description} failed")
        if e.stderr:
            print(f"  Error: {e.stderr}")
        return False
    except Exception as e:
        print_error(f"{description} failed: {str(e)}")
        return False


def check_prerequisites():
    """Check if required tools are installed"""
    print_step("Checking prerequisites")

    required_tools = {
        "git": "Git version control",
        "python3": "Python 3.x",
        "make": "Make build tool",
    }

    all_good = True
    for tool, description in required_tools.items():
        if shutil.which(tool):
            print_success(f"{tool} - {description}")
        else:
            print_error(f"{tool} - {description} - NOT FOUND")
            all_good = False

    return all_good


def update_project_name(project_dir, new_name):
    """Update project name in pyproject.toml"""
    pyproject_path = project_dir / "pyproject.toml"
    if not pyproject_path.exists():
        print_warning("pyproject.toml not found, skipping project name update")
        return

    try:
        content = pyproject_path.read_text()
        # Replace the template name with the new project name
        content = content.replace(
            'name = "claude-dev-template"', f'name = "{new_name}"'
        )
        pyproject_path.write_text(content)
        print_success(f"Updated project name to '{new_name}'")
    except Exception as e:
        print_error(f"Failed to update project name: {e}")


def main():
    # Parse arguments
    parser = argparse.ArgumentParser(
        description="Create a new project from the Claude Code Template"
    )
    parser.add_argument("project_name", help="Name for your new project directory")
    parser.add_argument(
        "--repo",
        default="https://github.com/ajk68/claudeCodeTemplate.git",
        help="Template repository URL",
    )
    parser.add_argument(
        "--branch", default="main", help="Branch or tag to use (default: main)"
    )
    parser.add_argument(
        "--no-setup", action="store_true", help="Skip running setup after cloning"
    )
    parser.add_argument(
        "--local", help="Use a local template directory instead of cloning"
    )

    args = parser.parse_args()

    # Validate project name
    project_dir = Path(args.project_name)
    if project_dir.exists():
        print_error(f"Directory '{args.project_name}' already exists!")
        sys.exit(1)

    # Check prerequisites
    if not check_prerequisites():
        print_error("Missing prerequisites. Please install required tools.")
        sys.exit(1)

    print(f"\n{Colors.BLUE}{'=' * 60}{Colors.END}")
    print(f"{Colors.BLUE}🚀 Creating project from Claude Code Template{Colors.END}")
    print(f"{Colors.BLUE}{'=' * 60}{Colors.END}")

    try:
        if args.local:
            # Use local template
            print_step(f"Copying from local template: {args.local}")
            local_path = Path(args.local)
            if not local_path.exists():
                print_error(f"Local template not found: {args.local}")
                sys.exit(1)

            # Copy template, excluding .git
            shutil.copytree(
                local_path,
                project_dir,
                ignore=shutil.ignore_patterns(
                    ".git", "__pycache__", "*.pyc", ".DS_Store"
                ),
            )
            print_success("Template copied")
        else:
            # Clone from repository
            print_step(f"Cloning template from {args.repo}")
            if not run_command(
                [
                    "git",
                    "clone",
                    "--branch",
                    args.branch,
                    "--depth",
                    "1",  # Shallow clone
                    args.repo,
                    args.project_name,
                ],
                "Template cloned",
            ):
                sys.exit(1)

        # Remove .git directory
        git_dir = project_dir / ".git"
        if git_dir.exists():
            print_step("Removing template git history")
            shutil.rmtree(git_dir)
            print_success("Git history removed")

        # Update project name
        print_step("Configuring project")
        update_project_name(project_dir, args.project_name)

        # Initialize fresh git repository
        print_step("Initializing fresh git repository")
        os.chdir(project_dir)

        if not run_command(["git", "init"], "Git repository initialized"):
            print_warning("Failed to initialize git repository")

        if not run_command(["git", "add", "."], "Files staged"):
            print_warning("Failed to stage files")

        if not run_command(
            ["git", "commit", "-m", "Initial commit from Claude Code Template"],
            "Initial commit created",
        ):
            print_warning("Failed to create initial commit")

        # Run setup if requested
        if not args.no_setup:
            print_step("Running project setup")
            print("This will install dependencies and configure your environment...")

            # Check if make setup exists
            if (project_dir / "Makefile").exists():
                if run_command(["make", "setup"], "Setup completed", cwd=project_dir):
                    setup_success = True
                else:
                    print_warning(
                        "Setup failed - you can run 'make setup' manually later"
                    )
                    setup_success = False
            else:
                print_warning("No Makefile found, skipping setup")
                setup_success = False
        else:
            setup_success = None  # Skipped

        # Success message
        print(f"\n{Colors.GREEN}{'=' * 60}{Colors.END}")
        print(
            f"{Colors.GREEN}✨ Success! Your project '{args.project_name}' is ready!{Colors.END}"
        )
        print(f"{Colors.GREEN}{'=' * 60}{Colors.END}")

        print("\n📝 Next steps:")
        print(f"1. cd {args.project_name}")

        if setup_success is False or args.no_setup:
            print("2. Run 'make setup' to configure your environment")
            print("3. Edit .env and add your API keys")
            print("4. Run 'make help' to see available commands")
            print("5. Start Claude Code with 'claude'")
        else:
            print("2. Edit .env and add your API keys")
            print("3. Run 'make help' to see available commands")
            print("4. Start Claude Code with 'claude'")

        print("\n💡 Tip: Check out the README.md for detailed documentation")

    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user")
        # Clean up partial directory if it exists
        if project_dir.exists() and not args.local:
            shutil.rmtree(project_dir)
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        # Clean up partial directory if it exists
        if project_dir.exists() and not args.local:
            shutil.rmtree(project_dir)
        sys.exit(1)


if __name__ == "__main__":
    # Handle piped input (for curl | python usage)
    if not sys.stdin.isatty() and len(sys.argv) == 1:
        print_error("When piping to Python, provide project name as argument:")
        print("  curl -sSL ... | python3 - my-project")
        sys.exit(1)

    main()
