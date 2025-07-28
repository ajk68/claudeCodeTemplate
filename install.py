#!/usr/bin/env python3
import argparse
import shutil
import subprocess
from pathlib import Path

# --- Configuration ---
# Define the components that can be installed
COMPONENTS = {
    "agents": ".claude/agents",
    "commands": ".claude/commands",
    "hooks": ".claude/hooks",
    "settings": ".claude/settings.json",
    "makefile": ["Makefile", "make/"],
    "docs": "docs/",
    "claudemd": "CLAUDE.md",
}


# --- Utility Functions ---
class Colors:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    END = "\033[0m"


def get_diff(file1, file2):
    """Get the difference between two files."""
    try:
        result = subprocess.run(
            ["diff", "-u", str(file1), str(file2)], capture_output=True, text=True
        )
        return result.stdout
    except FileNotFoundError:
        return "Cannot generate diff. Is 'diff' installed?"


def safe_copy(src_path, dest_path):
    """Copy a file or directory, asking for confirmation if destination exists."""
    if not dest_path.parent.exists():
        dest_path.parent.mkdir(parents=True, exist_ok=True)

    if dest_path.exists():
        if dest_path.is_dir():
            print(
                f"{Colors.YELLOW}Warning: Directory '{dest_path}' already exists. Merging contents.{Colors.END}"
            )
            for item in src_path.iterdir():
                safe_copy(item, dest_path / item.name)
            return

        diff = get_diff(dest_path, src_path)
        if not diff:
            print(
                f"File '{dest_path}' is identical. {Colors.GREEN}Skipping.{Colors.END}"
            )
            return

        print(f"{Colors.YELLOW}Warning: File '{dest_path}' already exists.{Colors.END}")
        print("--- Diff ---")
        print(diff)
        print("------------")

        while True:
            choice = input("Overwrite? [y]es, [n]o, [a]ll, [q]uit: ").lower()
            if choice in ["y", "yes"]:
                shutil.copy2(src_path, dest_path)
                print(f"File '{dest_path}' {Colors.GREEN}overwritten.{Colors.END}")
                return
            elif choice in ["n", "no"]:
                print(f"File '{dest_path}' {Colors.YELLOW}skipped.{Colors.END}")
                return
            elif choice in ["a", "all"]:
                global OVERWRITE_ALL
                OVERWRITE_ALL = True
                shutil.copy2(src_path, dest_path)
                print(f"File '{dest_path}' {Colors.GREEN}overwritten.{Colors.END}")
                return
            elif choice in ["q", "quit"]:
                raise SystemExit("Operation cancelled by user.")

    if OVERWRITE_ALL or not dest_path.exists():
        if src_path.is_dir():
            shutil.copytree(src_path, dest_path, dirs_exist_ok=True)
        else:
            shutil.copy2(src_path, dest_path)
        print(f"Component '{dest_path}' {Colors.GREEN}installed.{Colors.END}")


# --- Main Logic ---
def main():
    parser = argparse.ArgumentParser(
        description="Install Claude Code Framework components into the current project."
    )
    parser.add_argument(
        "components",
        nargs="*",
        default=["all"],
        help=f"Components to install. Options: {', '.join(COMPONENTS.keys())}, all. Default is 'all'.",
    )
    args = parser.parse_args()

    global OVERWRITE_ALL
    OVERWRITE_ALL = False

    script_dir = Path(__file__).parent
    dest_dir = Path.cwd()

    print(f"Installing framework from '{script_dir}' into '{dest_dir}'...")

    components_to_install = args.components
    if "all" in components_to_install:
        components_to_install = list(COMPONENTS.keys())

    for comp_name in components_to_install:
        if comp_name not in COMPONENTS:
            print(
                f"{Colors.RED}Error: Unknown component '{comp_name}'. Skipping.{Colors.END}"
            )
            continue

        print(f"\n--- Installing component: {comp_name} ---")
        sources = COMPONENTS[comp_name]
        if not isinstance(sources, list):
            sources = [sources]

        for src in sources:
            src_path = script_dir / src
            dest_path = dest_dir / src
            if src_path.exists():
                safe_copy(src_path, dest_path)
            else:
                print(
                    f"{Colors.RED}Source file not found: {src_path}. Skipping.{Colors.END}"
                )

    print(f"\n{Colors.GREEN}✨ Framework setup complete!{Colors.END}")


if __name__ == "__main__":
    main()
