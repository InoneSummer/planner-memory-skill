---
name: planner-memory
description: Use when project-planning context is spreading across chats, notes, or meetings and the team needs a shared planner folder with reusable markdown records and dated distilled summaries.
---

# Planner Memory

Preserve planning-stage thinking as shared project memory. Keep project-specific context in a dedicated `planner/` folder, then periodically distill it into dated markdown and HTML summaries that other roles can reuse.

## When to Use

Use this skill when:

- service-planning or harness-planning discussions are accumulating across chats
- important middle-stage reasoning may be lost as the context window grows
- a project needs reusable planning records for later docs, decks, or demos
- a human wants current thinking separated from production code and implementation notes
- planner notes should later inform producer or evaluator work without relying on chat memory

Do not use this skill for:

- code implementation plans that belong in `docs/plans/`
- one-off meeting notes with no future reuse value
- product-specific runtime logs or test artifacts

## Core Rule

Store project-specific planning memory in project markdown files.
Store the reusable process for capturing and distilling that memory in this skill.

In short:

- memory lives in markdown
- structure lives in the planner folder
- distillation lives in the skill
- distill output is a markdown and HTML pair by default
- HTML is a generated output, not the source of truth
- planner records are written as team assets, not private planner notes

## Folder Contract

For each project root, create or maintain this structure:

```text
<project>/
  planner/
    README.md
    notes/
    decisions/
    open-questions/
    presentation-hooks/
    distilled/
```

Interpret this as the planner part of a wider harness triad:

- `planner/` for planning memory
- `producer/` for build and execution work
- `evaluator/` for verification and critique work

This skill manages only `planner/`, but its records should be readable and reusable by the wider triad.

## Metadata Contract

Every planner markdown file should begin with YAML frontmatter.
Use the schema in `references/frontmatter-schema.md`.

At minimum include:

- `title`
- `project`
- `planner_part`
- `doc_type`
- `discussion_date`
- `created_at`
- `updated_at`
- `summary`
- `status`
- `shared_with`

This metadata lets future runs sort by recency and reconstruct the project narrative quickly.
Use `shared_with` to show which team roles should consume the note.

## Capture Rules

### 1. Notes

Use `planner/notes/` for unresolved reasoning, tensions, tradeoffs, and evolving hypotheses.

File name pattern:

```text
YYYY-MM-DD-<topic>.md
```

Exception:

- keep `README.md` for folder index files

Use the template in `assets/templates/thinking-note-template.md`.

### 2. Decisions

Use `planner/decisions/` for choices that the project is now treating as current truth.

File name pattern:

```text
YYYY-MM-DD-<decision>.md
```

Use the template in `assets/templates/decision-note-template.md`.

### 3. Open Questions

Use `planner/open-questions/` for unresolved issues that deserve explicit revisit triggers.

Use the template in `assets/templates/open-question-template.md`.

### 4. Presentation Hooks

Use `planner/presentation-hooks/` for analogies, memorable lines, slide ideas, and audience-facing reframes.

Use the template in `assets/templates/presentation-hook-template.md`.

Write hooks so they still help producer or evaluator roles understand why a framing matters.

## Distillation Rules

When asked to distill project planning, default to producing both markdown and HTML in the same run unless the human explicitly asks for markdown only:

1. Read all markdown files under the project `planner/` folder.
2. Sort primarily by `discussion_date`, then `updated_at`.
3. Give more weight to recent documents, but carry forward still-open questions from older files.
4. Separate the output into:
   - stable principles
   - recent shifts
   - open tensions
   - producer implications
   - evaluator implications
   - candidate presentation angles
5. Write a new dated markdown brief to:

```text
planner/distilled/YYYY-MM-DD-<project-slug>-planner-distill.md
```

Use `assets/templates/distilled-brief-template.md`.

6. Write a matching HTML summary to:

```text
planner/distilled/YYYY-MM-DD-<project-slug>-planner-distill.html
```

Use `assets/templates/distilled-html-template.html` as the starting structure when a local project-specific HTML style does not already exist.

Do not overwrite older distills unless the human explicitly asks for replacement.

## HTML Output Rule

Generate the HTML from the same planner sources or from the matching markdown distill created in the same run.

If a local Ask Dori HTML skill exists, use it.
If not, still keep the same naming convention and generate a self-contained HTML summary.

The HTML should emphasize:

- what changed
- what remains unresolved
- what downstream roles should act on
- what would make a strong presentation narrative
- enough visual hierarchy that the page is presentation-ready without another formatting pass

## Project README Rule

Each project `planner/README.md` should:

- explain the folder purpose
- describe the subfolders
- explain the naming convention
- state that markdown is the source of truth
- state that HTML in `distilled/` is generated output
- state that planner notes are shared team assets for planner, producer, and evaluator

Use `assets/templates/planner-readme-template.md`.

## Common Mistakes

- Do not leave planning notes loose in the project root.
- Do not treat HTML as the canonical planning artifact.
- Do not mix implementation TODOs into planner notes if they belong in build plans.
- Do not omit metadata. Missing dates and summaries make later distillation weak.
- Do not collapse service, harness, and presentation thinking into one giant undifferentiated file.
- Do not write notes as if only the planner will read them. Producer and evaluator should be able to reuse them.
- Do not stop at markdown if the human asked for distillation. The default finish line is the md/html pair.

## Validation

Before claiming the planner setup is done:

- verify `planner/` exists
- verify each markdown file has frontmatter
- verify every non-README markdown file name is date-prefixed
- verify at least one distilled output path is reserved under `planner/distilled/`

When possible, run `scripts/validate_planner_tree.py` against the project root or planner path.

For future skill hardening, use the pressure scenarios in `references/pressure-scenarios.md`.
