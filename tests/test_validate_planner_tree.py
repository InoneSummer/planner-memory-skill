from __future__ import annotations

import importlib.util
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "validate_planner_tree.py"
SPEC = importlib.util.spec_from_file_location("validate_planner_tree", SCRIPT_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC is not None and SPEC.loader is not None
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


VALID_FRONTMATTER = textwrap.dedent(
    """\
    ---
    title: "Sample"
    project: "demo"
    planner_part: "service-planning"
    doc_type: "thinking-note"
    discussion_date: "2026-03-26"
    created_at: "2026-03-26"
    updated_at: "2026-03-26"
    summary: "Summary"
    status: "active"
    shared_with:
      - "planner"
      - "producer"
      - "evaluator"
    source_refs:
      - "conversation:2026-03-26"
    tags:
      - "planning"
    ---
    """
)


class ValidatePlannerTreeTests(unittest.TestCase):
    def create_project(self) -> Path:
        temp_dir = Path(tempfile.mkdtemp())
        planner = temp_dir / "planner"
        planner.mkdir()
        for name in ("notes", "decisions", "open-questions", "presentation-hooks", "distilled"):
            (planner / name).mkdir()

        (planner / "README.md").write_text(
            VALID_FRONTMATTER
            + "\n# Planner\n",
            encoding="utf-8",
        )
        (planner / "distilled" / "README.md").write_text(
            VALID_FRONTMATTER.replace('doc_type: "thinking-note"', 'doc_type: "distilled-index"')
            + "\n# Distilled\n",
            encoding="utf-8",
        )
        (planner / "notes" / "2026-03-26-sample.md").write_text(
            VALID_FRONTMATTER + "\n# Note\n",
            encoding="utf-8",
        )
        return temp_dir

    def test_valid_tree_passes(self) -> None:
        project_root = self.create_project()

        errors = MODULE.validate_planner_tree(project_root / "planner")

        self.assertEqual(errors, [])

    def test_missing_shared_with_fails(self) -> None:
        project_root = self.create_project()
        note_path = project_root / "planner" / "notes" / "2026-03-26-sample.md"
        note_path.write_text(
            VALID_FRONTMATTER.replace(
                'shared_with:\n  - "planner"\n  - "producer"\n  - "evaluator"\n',
                "",
            )
            + "\n# Note\n",
            encoding="utf-8",
        )

        errors = MODULE.validate_planner_tree(project_root / "planner")

        self.assertTrue(any("shared_with" in error.message for error in errors))

    def test_non_prefixed_filename_fails(self) -> None:
        project_root = self.create_project()
        note_path = project_root / "planner" / "notes" / "sample.md"
        note_path.write_text(VALID_FRONTMATTER + "\n# Note\n", encoding="utf-8")

        errors = MODULE.validate_planner_tree(project_root / "planner")

        self.assertTrue(any("date-prefixed" in error.message for error in errors))


if __name__ == "__main__":
    unittest.main()
