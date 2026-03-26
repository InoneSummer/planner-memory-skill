from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

REQUIRED_SUBDIRS = (
    "notes",
    "decisions",
    "open-questions",
    "presentation-hooks",
    "distilled",
)

REQUIRED_FIELDS = (
    "title",
    "project",
    "planner_part",
    "doc_type",
    "discussion_date",
    "created_at",
    "updated_at",
    "summary",
    "status",
    "shared_with",
    "source_refs",
    "tags",
)

DATE_PREFIX = re.compile(r"^\d{4}-\d{2}-\d{2}-")
DATE_VALUE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ALLOWED_SHARED_WITH = {"planner", "producer", "evaluator"}


@dataclass
class ValidationError:
    path: Path
    message: str


def resolve_planner_path(raw_path: str) -> Path:
    candidate = Path(raw_path).resolve()
    if candidate.name == "planner":
        return candidate
    return candidate / "planner"


def extract_frontmatter(text: str) -> dict[str, object] | None:
    lines = text.splitlines()
    if len(lines) < 3 or lines[0].strip() != "---":
        return None

    try:
        end_index = next(index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---")
    except StopIteration:
        return None

    fields: dict[str, object] = {}
    current_list_key: str | None = None

    for line in lines[1:end_index]:
        key_match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if key_match:
            key = key_match.group(1)
            value = key_match.group(2).strip()
            if value == "":
                fields[key] = []
                current_list_key = key
            else:
                fields[key] = value.strip("\"'")
                current_list_key = None
            continue

        item_match = re.match(r"^\s*-\s+(.+)$", line)
        if item_match and current_list_key:
            items = fields.setdefault(current_list_key, [])
            if isinstance(items, list):
                items.append(item_match.group(1).strip().strip("\"'"))

    return fields


def validate_planner_tree(planner_path: Path) -> list[ValidationError]:
    errors: list[ValidationError] = []

    if not planner_path.exists():
        return [ValidationError(planner_path, "planner folder does not exist")]

    if not planner_path.is_dir():
        return [ValidationError(planner_path, "planner path is not a directory")]

    for subdir in REQUIRED_SUBDIRS:
        subdir_path = planner_path / subdir
        if not subdir_path.is_dir():
            errors.append(ValidationError(subdir_path, "required subdirectory is missing"))

    markdown_files = sorted(planner_path.rglob("*.md"))
    if not markdown_files:
        errors.append(ValidationError(planner_path, "planner folder does not contain any markdown files"))
        return errors

    for markdown_file in markdown_files:
        if markdown_file.name != "README.md" and not DATE_PREFIX.match(markdown_file.name):
            errors.append(
                ValidationError(markdown_file, "markdown file name must be date-prefixed unless it is README.md")
            )

        frontmatter = extract_frontmatter(markdown_file.read_text(encoding="utf-8"))
        if frontmatter is None:
            errors.append(ValidationError(markdown_file, "markdown file is missing YAML frontmatter"))
            continue

        for field in REQUIRED_FIELDS:
            value = frontmatter.get(field)
            if value in (None, "", []):
                errors.append(ValidationError(markdown_file, f"missing required frontmatter field: {field}"))

        for date_field in ("discussion_date", "created_at", "updated_at"):
            value = frontmatter.get(date_field)
            if isinstance(value, str) and not DATE_VALUE.match(value):
                errors.append(ValidationError(markdown_file, f"{date_field} must use YYYY-MM-DD format"))

        shared_with = frontmatter.get("shared_with")
        if isinstance(shared_with, list):
            invalid = [item for item in shared_with if item not in ALLOWED_SHARED_WITH]
            if invalid:
                errors.append(
                    ValidationError(
                        markdown_file,
                        "shared_with contains unsupported values: " + ", ".join(sorted(invalid)),
                    )
                )
        elif shared_with is not None:
            errors.append(ValidationError(markdown_file, "shared_with must be a YAML list"))

    return errors


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Validate a project planner tree used by the project-planning-distiller skill."
    )
    parser.add_argument(
        "path",
        help="Project root or planner directory to validate",
    )
    args = parser.parse_args(argv)

    planner_path = resolve_planner_path(args.path)
    errors = validate_planner_tree(planner_path)

    if errors:
        for error in errors:
            print(f"ERROR {error.path}: {error.message}")
        return 1

    print(f"OK {planner_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
