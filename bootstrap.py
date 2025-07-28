#!/usr/bin/env python3
"""
Claude Code Template Bootstrap Script

This script creates a new project from the Claude Code Template.
It supports two modes: shared (uses dotfiles) or complete (self-contained).

Usage:
    # Direct from GitHub (will prompt for mode):
    curl -sSL https://raw.githubusercontent.com/ajk68/claudeCodeTemplate/main/bootstrap.py | python3 - my-project

    # With explicit mode:
    python3 bootstrap.py my-project --mode shared
    python3 bootstrap.py my-project --mode complete

    # Upgrade shared to complete:
    python3 bootstrap.py --upgrade-to-complete --local /path/to/template

    # Other options:
    python3 bootstrap.py my-project --branch v2.0 --no-setup --local /path/to/template
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
    CYAN = "\033[96m"
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


def get_installation_mode():
    """Interactively get installation mode from user"""
    print(f"\n{Colors.CYAN}Choose installation mode:{Colors.END}\n")

    print(f"{Colors.YELLOW}Shared:{Colors.END}")
    print("  - Uses ~/.claude and ~/ai_tools from your dotfiles")
    print("  - Best for: Personal projects, maintaining consistency")
    print("  - Smaller project footprint")
    print()

    print(f"{Colors.YELLOW}Complete:{Colors.END}")
    print("  - Everything included in the project directory")
    print("  - Best for: Team projects, self-contained deployments")
    print("  - Fully portable\n")

    print("If unsure, choose 'complete' for a fully self-contained project.\n")

    while True:
        choice = input("Your choice [shared/complete]: ").lower().strip()
        if choice in ["shared", "complete"]:
            return choice
        print(f"{Colors.RED}Please enter 'shared' or 'complete'{Colors.END}")


def copy_shared_mode_files(src_dir, dest_dir):
    """Copy only the essential files for shared mode"""
    # Files to copy for shared mode
    shared_files = [
        "CLAUDE.md",
        "Makefile",
        ".gitignore",
        ".repomixignore",
        ".env-example",
        "pyproject.toml",
        "package.json",
        "Procfile.example",
        "repomix.config.json",
        "README.md",
        "SETUP_CHECKLIST.md",
        "TEMPLATE_GUIDE.md",
    ]

    # Directories to copy (with their contents)
    shared_dirs = ["docs", "backend", "frontend", "logs", "tests"]

    # Copy individual files
    for file in shared_files:
        src_file = src_dir / file
        if src_file.exists():
            dest_file = dest_dir / file
            shutil.copy2(src_file, dest_file)
            print(f"  Copied: {file}")

    # Copy directories
    for dir_name in shared_dirs:
        src_subdir = src_dir / dir_name
        if src_subdir.exists():
            dest_subdir = dest_dir / dir_name
            shutil.copytree(src_subdir, dest_subdir, dirs_exist_ok=True)
            print(f"  Copied: {dir_name}/")

    print_success("Shared mode files copied")


def upgrade_to_complete(template_dir):
    """Upgrade a shared mode project to complete mode"""
    print_step("Checking current installation mode")

    # Check if already in complete mode
    if Path(".claude").exists() or Path("make").exists():
        print_warning("This project already has .claude or make directories.")
        print("It appears to already be in complete mode.")
        return False

    print_success("This appears to be a shared mode project")

    # Confirm upgrade
    print(f"\n{Colors.CYAN}This will add:{Colors.END}")
    print("  - .claude/ directory (agents, commands, hooks)")
    print("  - make/ directory (build tools)")

    if input("\nProceed with upgrade? [y/N]: ").lower() != "y":
        print("Upgrade cancelled.")
        return False

    # Copy directories
    print_step("Copying directories from template")

    claude_src = template_dir / ".claude"
    make_src = template_dir / "make"

    if claude_src.exists():
        shutil.copytree(claude_src, Path(".claude"), dirs_exist_ok=True)
        print_success("Copied .claude directory")
    else:
        print_error(".claude directory not found in template")

    if make_src.exists():
        shutil.copytree(make_src, Path("make"), dirs_exist_ok=True)
        print_success("Copied make directory")
    else:
        print_error("make directory not found in template")

    print(f"\n{Colors.GREEN}✨ Upgrade complete!{Colors.END}")
    print("Your project is now in complete mode.")
    return True


def main():
    # Parse arguments
    parser = argparse.ArgumentParser(
        description="Create a new project from the Claude Code Template"
    )

    # Create a mutually exclusive group for project creation vs upgrade
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "project_name", nargs="?", help="Name for your new project directory"
    )
    group.add_argument(
        "--upgrade-to-complete",
        action="store_true",
        help="Upgrade existing shared mode project to complete mode",
    )

    parser.add_argument(
        "--mode",
        choices=["shared", "complete"],
        help="Installation mode (if not specified, will prompt interactively)",
    )
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

    # Handle upgrade mode
    if args.upgrade_to_complete:
        template_dir = Path(args.local) if args.local else Path(__file__).parent
        if not template_dir.exists():
            print_error(f"Template directory not found: {template_dir}")
            sys.exit(1)

        success = upgrade_to_complete(template_dir)
        sys.exit(0 if success else 1)

    # Validate project name
    project_dir = Path(args.project_name)
    if project_dir.exists():
        print_error(f"Directory '{args.project_name}' already exists!")
        sys.exit(1)

    # Get installation mode if not specified
    mode = args.mode
    if not mode:
        mode = get_installation_mode()

    print_success(f"Using {mode} mode installation")

    # Check prerequisites
    if not check_prerequisites():
        print_error("Missing prerequisites. Please install required tools.")
        sys.exit(1)

    print(f"\n{Colors.BLUE}{'=' * 60}{Colors.END}")
    print(
        f"{Colors.BLUE}🚀 Creating project from Claude Code Template ({mode} mode){Colors.END}"
    )
    print(f"{Colors.BLUE}{'=' * 60}{Colors.END}")

    try:
        if args.local:
            # Use local template
            print_step(f"Copying from local template: {args.local}")
            local_path = Path(args.local)
            if not local_path.exists():
                print_error(f"Local template not found: {args.local}")
                sys.exit(1)

            # Create project directory first
            project_dir.mkdir(exist_ok=True)

            if mode == "shared":
                # Copy only shared mode files
                copy_shared_mode_files(local_path, project_dir)
            else:
                # Copy everything for complete mode
                # Get the absolute path of the destination to avoid recursive copy
                dest_name = project_dir.name
                shutil.copytree(
                    local_path,
                    project_dir,
                    dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns(
                        ".git",
                        "__pycache__",
                        "*.pyc",
                        ".DS_Store",
                        dest_name,
                        "test-*",
                        "node_modules",
                    ),
                )
                print_success("Template copied")
        else:
            # Clone from repository
            if mode == "shared":
                # For shared mode, clone to temp directory and copy selective files
                print_step(f"Cloning template from {args.repo}")
                import tempfile

                with tempfile.TemporaryDirectory() as temp_dir:
                    temp_path = Path(temp_dir) / "template"
                    if not run_command(
                        [
                            "git",
                            "clone",
                            "--branch",
                            args.branch,
                            "--depth",
                            "1",
                            args.repo,
                            str(temp_path),
                        ],
                        "Template cloned to temporary directory",
                    ):
                        sys.exit(1)

                    # Create project directory and copy shared files
                    project_dir.mkdir(exist_ok=True)
                    copy_shared_mode_files(temp_path, project_dir)
            else:
                # For complete mode, clone directly
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

        # Remove bootstrap.py from the new project
        bootstrap_file = project_dir / "bootstrap.py"
        if bootstrap_file.exists():
            print_step("Cleaning up bootstrap file")
            bootstrap_file.unlink()
            print_success("Bootstrap script removed (no longer needed)")

        # Success message
        print(f"\n{Colors.GREEN}{'=' * 60}{Colors.END}")
        print(
            f"{Colors.GREEN}✨ Success! Your {mode} mode project '{args.project_name}' is ready!{Colors.END}"
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

        if mode == "shared":
            print("\n🔗 Shared mode notes:")
            print("  - Using ~/.claude for agents, commands, and hooks")
            print("  - Using ~/ai_tools for make commands")
            print(
                "  - To upgrade to complete mode later: python3 bootstrap.py --upgrade-to-complete"
            )

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
