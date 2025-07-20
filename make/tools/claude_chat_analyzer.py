#!/usr/bin/env python3
"""
Claude Chat Analyzer - Selective conversation analysis tool

Usage:
    # Discovery mode - see all projects
    python claude_chat_analyzer.py

    # Processing mode - analyze specific projects
    python claude_chat_analyzer.py --projects "ai-coach-research,other-project" --max-age 2d
"""

import argparse
import os
import sys
import subprocess
import tempfile
from pathlib import Path
from datetime import datetime, timedelta
from urllib.parse import unquote
from typing import List, Dict


class ChatAnalyzer:
    def __init__(self):
        self.projects_dir = Path.home() / ".claude" / "projects"

    def parse_age(self, age_str: str) -> timedelta:
        """Convert age string (1h, 2d, 1w) to timedelta"""
        if not age_str or len(age_str) < 2:
            raise ValueError("Invalid age format. Use format like '1h', '2d', '1w'")

        try:
            value = int(age_str[:-1])
            unit = age_str[-1].lower()

            if unit == "h":
                return timedelta(hours=value)
            elif unit == "d":
                return timedelta(days=value)
            elif unit == "w":
                return timedelta(weeks=value)
            else:
                raise ValueError(
                    f"Unknown time unit: {unit}. Use h (hours), d (days), or w (weeks)"
                )
        except ValueError as e:
            raise ValueError(f"Invalid age format '{age_str}': {e}")

    def format_age(self, timestamp: float) -> str:
        """Format file age as human-readable string"""
        now = datetime.now()
        file_time = datetime.fromtimestamp(timestamp)
        delta = now - file_time

        if delta.days > 7:
            weeks = delta.days // 7
            return f"{weeks} week{'s' if weeks > 1 else ''} ago"
        elif delta.days > 0:
            return f"{delta.days} day{'s' if delta.days > 1 else ''} ago"
        elif delta.seconds > 3600:
            hours = delta.seconds // 3600
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif delta.seconds > 60:
            minutes = delta.seconds // 60
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        else:
            return "just now"

    def get_project_info(self) -> List[Dict]:
        """Scan projects directory and return info for each"""
        projects = []

        if not self.projects_dir.exists():
            return projects

        for project_path in self.projects_dir.iterdir():
            if not project_path.is_dir():
                continue

            # Decode project name
            encoded_name = project_path.name
            decoded_name = unquote(encoded_name)

            # Get .jsonl files
            jsonl_files = list(project_path.glob("*.jsonl"))
            if not jsonl_files:
                continue

            # Calculate stats
            file_count = len(jsonl_files)
            total_size = sum(f.stat().st_size for f in jsonl_files)
            size_mb = total_size / (1024 * 1024)

            # Find latest file
            latest_file = max(jsonl_files, key=lambda f: f.stat().st_mtime)
            latest_age = self.format_age(latest_file.stat().st_mtime)

            projects.append(
                {
                    "name": decoded_name,
                    "path": encoded_name,
                    "files": file_count,
                    "latest": latest_age,
                    "size_mb": size_mb,
                }
            )

        # Sort by latest activity - need to parse the age string for proper sorting
        def age_to_seconds(age_str):
            """Convert age string back to approximate seconds for sorting"""
            if "just now" in age_str:
                return 0
            elif "minute" in age_str:
                minutes = int(age_str.split()[0])
                return minutes * 60
            elif "hour" in age_str:
                hours = int(age_str.split()[0])
                return hours * 3600
            elif "day" in age_str:
                days = int(age_str.split()[0])
                return days * 86400
            elif "week" in age_str:
                weeks = int(age_str.split()[0])
                return weeks * 604800
            return float("inf")  # Unknown format, put at end

        projects.sort(key=lambda p: age_to_seconds(p["latest"]))

        return projects

    def filter_files(self, project_names: List[str], max_age_str: str) -> List[Path]:
        """Filter .jsonl files by project and age"""
        max_age = self.parse_age(max_age_str)
        cutoff_time = datetime.now() - max_age

        # Get all projects to build name mapping
        all_projects = self.get_project_info()
        name_to_path = {p["name"]: p["path"] for p in all_projects}

        filtered_files = []

        for project_name in project_names:
            if project_name not in name_to_path:
                print(f"Warning: Project '{project_name}' not found")
                continue

            encoded_name = name_to_path[project_name]
            project_path = self.projects_dir / encoded_name

            # Get .jsonl files in this project
            for jsonl_file in project_path.glob("*.jsonl"):
                file_time = datetime.fromtimestamp(jsonl_file.stat().st_mtime)
                if file_time >= cutoff_time:
                    filtered_files.append(jsonl_file)

        return filtered_files

    def process_files(self, files: List[Path]) -> Path:
        """Convert files and create repomix archive"""
        # Create temp directory
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Convert each file
            converted_count = 0
            for file in files:
                try:
                    print(f"Converting {file.name}...")
                    subprocess.run(
                        ["claude2md", str(file), str(temp_path)],
                        capture_output=True,
                        text=True,
                        check=True,
                    )
                    converted_count += 1
                except subprocess.CalledProcessError as e:
                    print(f"Warning: Failed to convert {file.name}: {e.stderr}")
                    continue
                except Exception as e:
                    print(f"Warning: Error converting {file.name}: {e}")
                    continue

            if converted_count == 0:
                raise RuntimeError("No files were successfully converted")

            print(f"\nConverted {converted_count}/{len(files)} files")

            # Run repomix to create packed archive
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            output_path = Path(f"/tmp/claude-chats-{timestamp}.txt")

            print("Creating packed archive...")
            try:
                # Change to temp directory for repomix
                original_cwd = os.getcwd()
                os.chdir(temp_path)

                subprocess.run(
                    ["repomix", "-o", str(output_path)],
                    capture_output=True,
                    text=True,
                    check=True,
                )

                os.chdir(original_cwd)

                if output_path.exists():
                    return output_path
                else:
                    raise RuntimeError("Repomix completed but output file not found")

            except subprocess.CalledProcessError as e:
                os.chdir(original_cwd)
                raise RuntimeError(f"Repomix failed: {e.stderr}")
            except FileNotFoundError:
                os.chdir(original_cwd)
                raise RuntimeError(
                    "Repomix not found. Please install it: npm install -g repomix"
                )

    def display_projects(self, projects: List[Dict]):
        """Pretty print project information with highlights"""
        if not projects:
            print("No projects found in ~/.claude/projects/")
            return

        # Calculate column widths
        name_width = max(len(p["name"]) for p in projects)
        name_width = max(name_width, 20)  # Minimum width

        # Identify relevant projects (top 3 most recent + high activity)
        top_3 = projects[:3]
        relevant_projects = []

        print("\n🔍 RECENT ACTIVITY:")
        print(f"{'=' * 80}")

        # Show top 3 most recent
        print(f"\n{'📌 TOP 3 MOST RECENT PROJECTS:'}")
        print(
            f"{'Project':<{name_width}}  {'Files':>6}  {'Latest Activity':<18}  {'Size':>8}"
        )
        print("-" * (name_width + 40))

        for i, project in enumerate(top_3):
            name = project["name"]
            if len(name) > name_width:
                display_name = name[: name_width - 3] + "..."
            else:
                display_name = name

            # Highlight current directory if it's in top 3
            marker = " ⭐" if "ai-coach-research" in name else ""
            print(
                f"{display_name:<{name_width}}  {project['files']:>6}  "
                f"{project['latest']:<18}  {project['size_mb']:>6.1f} MB{marker}"
            )
            relevant_projects.append(name)

        # Suggest projects based on activity
        print(f"\n{'💡 SUGGESTED FOR ANALYSIS:'}")
        suggestions = []
        for proj in projects[:5]:  # Check top 5
            if proj["files"] > 10:  # Active projects
                suggestions.append(proj["name"])

        if suggestions:
            print(
                f"Based on activity, consider exporting: {', '.join(suggestions[:3])}"
            )

        # Show all projects
        print(f"\n{'ALL PROJECTS:'}")
        print(
            f"{'Project':<{name_width}}  {'Files':>6}  {'Latest Activity':<18}  {'Size':>8}"
        )
        print("-" * (name_width + 40))

        # Print all projects
        for project in projects:
            name = project["name"]
            if len(name) > name_width:
                display_name = name[: name_width - 3] + "..."
            else:
                display_name = name

            print(
                f"{display_name:<{name_width}}  {project['files']:>6}  "
                f"{project['latest']:<18}  {project['size_mb']:>6.1f} MB"
            )


def main():
    parser = argparse.ArgumentParser(description="Analyze Claude conversation logs")
    parser.add_argument("--projects", help="Comma-separated project names")
    parser.add_argument("--max-age", help="Maximum file age (e.g., 1h, 2d, 1w)")

    args = parser.parse_args()
    analyzer = ChatAnalyzer()

    if args.projects and args.max_age:
        # Processing mode
        project_names = [p.strip() for p in args.projects.split(",")]

        try:
            files = analyzer.filter_files(project_names, args.max_age)

            if not files:
                print("No matching files found")
                sys.exit(1)

            print(f"Found {len(files)} files to process...")
            output_path = analyzer.process_files(files)
            print(f"\n{'=' * 80}")
            print("✅ EXPORT SUCCESSFUL!")
            print(f"{'=' * 80}")
            print(f"\n📄 Output file: {output_path}")
            print(f"📏 File size: {output_path.stat().st_size / (1024 * 1024):.1f} MB")
            print("\n💡 Next steps:")
            print(f"   1. Copy this path: {output_path}")
            print("   2. Open a new Claude chat")
            print("   3. Attach the file and use one of the suggested analysis prompts")
            print(f"\n{'=' * 80}")

        except ValueError as e:
            print(f"Error: {e}")
            sys.exit(1)
        except RuntimeError as e:
            print(f"Error: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Unexpected error: {e}")
            sys.exit(1)

    else:
        # Discovery mode
        if args.projects or args.max_age:
            print(
                "Error: Both --projects and --max-age are required for processing mode"
            )
            sys.exit(1)

        projects = analyzer.get_project_info()
        analyzer.display_projects(projects)

        if projects:
            print(
                f"\nUsage: python {Path(__file__).name} --projects PROJECT_NAMES --max-age AGE"
            )
            print(
                'Example: python claude_chat_analyzer.py --projects "ai-coach-research" --max-age 2d'
            )

            # Show quick export for top project
            top_project = projects[0]["path"]
            print("\n🚀 QUICK EXPORT (last 2 days from most recent project):")
            print(
                f'   uv run python {Path(__file__).name} --projects="{top_project}" --max-age="2d"'
            )


if __name__ == "__main__":
    main()
