import subprocess
import re
from pathlib import Path


def _save_todo_file(todo_lines):
    """Helper function to save todo lines to file"""
    file_path = Path(__file__).parent.parent / "todo.md"
    with open(file_path, "w") as f:
        f.write("\n".join(todo_lines))


def replace_row(todo_lines, row, content):
    if row < 1 or row > len(todo_lines):
        return f"ERROR: Row {row} is out of range (1-{len(todo_lines)})"

    old_content = todo_lines[row - 1]
    todo_lines[row - 1] = content
    _save_todo_file(todo_lines)
    return f"SUCCESS: Replaced row {row} with: {content}"


def delete_row(todo_lines, row):
    if row < 1 or row > len(todo_lines):
        return f"ERROR: Row {row} is out of range (1-{len(todo_lines)})"

    deleted_content = todo_lines.pop(row - 1)
    _save_todo_file(todo_lines)
    return f"SUCCESS: Deleted row {row}: {deleted_content}"


def insert_row(todo_lines, row, content):
    if row < 1 or row > len(todo_lines) + 1:
        return f"ERROR: Row {row} is out of range (1-{len(todo_lines) + 1})"

    todo_lines.insert(row - 1, content)
    _save_todo_file(todo_lines)
    return f"SUCCESS: Inserted at row {row}: {content}"


def move_row(todo_lines, row, to):
    if row < 1 or row > len(todo_lines):
        return f"ERROR: Source row {row} is out of range (1-{len(todo_lines)})"
    if to < 1 or to > len(todo_lines):
        return f"ERROR: Destination row {to} is out of range (1-{len(todo_lines)})"

    line = todo_lines.pop(row - 1)
    if to > row:
        to -= 1
    todo_lines.insert(to - 1, line)
    _save_todo_file(todo_lines)
    return f"SUCCESS: Moved row {row} to position {to}"


def rollback_previous_commit(todo_lines):
    try:
        result = subprocess.run(
            ["git", "log", "--oneline", "-1"],
            capture_output=True,
            text=True,
            check=True,
        )
        if not result.stdout.strip():
            return "ERROR: No commits to rollback"

        commit_line = result.stdout.strip()
        if "Update todo:" not in commit_line:
            return "ERROR: Latest commit was not made by this app, cannot rollback"

        subprocess.run(
            ["git", "reset", "--hard", "HEAD~1"], capture_output=True, check=True
        )

        file_path = Path(__file__).parent.parent / "todo.md"
        with open(file_path, "r") as f:
            todo_lines.clear()
            todo_lines.extend(f.read().splitlines())

        return "SUCCESS: Successfully rolled back the previous change"

    except subprocess.CalledProcessError as e:
        return f"ERROR: Rollback failed - {e}"


def create_view(todo_lines, name, regex):
    """Create a new view by applying regex pattern to todo.md and saving matches to a view file"""
    try:
        # Compile the regex pattern
        pattern = re.compile(regex)
        
        # Find matching lines
        matches = []
        for line in todo_lines:
            if pattern.search(line):
                matches.append(line)
        
        # Create views directory if it doesn't exist
        views_dir = Path(__file__).parent.parent / "views"
        views_dir.mkdir(exist_ok=True)
        
        # Update views.md with the new view definition
        views_md_path = views_dir / "views.md"
        view_entry = f"{name}: {regex}"
        
        # Read existing views.md content
        existing_views = []
        if views_md_path.exists():
            with open(views_md_path, "r") as f:
                existing_views = f.read().splitlines()
        
        # Check if view already exists and update it, otherwise add new entry
        view_updated = False
        for i, line in enumerate(existing_views):
            if line.startswith(f"{name}:"):
                existing_views[i] = view_entry
                view_updated = True
                break
        
        if not view_updated:
            existing_views.append(view_entry)
        
        # Write updated views.md
        with open(views_md_path, "w") as f:
            f.write("\n".join(existing_views))
        
        # Create/update the view file
        view_file_path = views_dir / f"{name}.md"
        with open(view_file_path, "w") as f:
            f.write("\n".join(matches))
        
        return f"SUCCESS: Created view '{name}' with {len(matches)} matches. View saved to {view_file_path}"
        
    except re.error as e:
        return f"ERROR: Invalid regex pattern - {e}"
    except Exception as e:
        return f"ERROR: Failed to create view - {e}"
