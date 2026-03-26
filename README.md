# Planner Memory

`planner-memory` is a reusable skill for turning messy project-planning conversations into a durable, shared planning memory system.

It creates and maintains a `planner/` folder inside a project, keeps markdown as the source of truth, and distills planning context into a dated markdown + HTML pair that can later support implementation, evaluation, demos, and presentations.

## Quick Start

1. Install the skill into your Codex or Claude skills directory.
2. Start a new session and call the skill explicitly.
3. When returning later, load the existing `planner/` folder first and continue from that state.

```text
$planner-memory Capture this project planning discussion into planner files and generate the distill md/html pair.
```

```text
$planner-memory Read this project's existing planner folder, summarize the current state, and continue the discussion from there.
```

## Why This Exists

Most planning context disappears into chat history, meeting notes, or the context window of a single agent session. That is painful when:

- a project evolves over several days or weeks
- product reasoning is more important than a single final answer
- producer and evaluator roles need to inherit planner context later
- a team wants presentation-ready summaries without rewriting everything from scratch

This skill was created to solve that exact problem.

Instead of treating planning as disposable conversation, it treats planning as a team asset.

## What Problem It Solves

`planner-memory` is designed for projects where the middle-stage reasoning matters:

- service planning
- harness planning
- agent workflow design
- presentation framing
- product tradeoff logging

It is especially useful when a project needs all of the following:

- a stable folder for planning records
- metadata-rich markdown files that can be sorted later
- separation between planning memory and implementation plans
- distilled outputs that are easy to reuse in slides, docs, and HTML artifacts

## Core Design Decisions

This skill was built with a few strong opinions:

1. Markdown is the source of truth.
2. HTML is generated output, not the canonical artifact.
3. Planning notes are not private planner notes; they are shared team memory for planner, producer, and evaluator.
4. Recency matters, so every note carries date metadata.
5. Distillation should end in a markdown + HTML pair by default.
6. Validation matters, so the planner tree can be checked with a deterministic script.

## What It Produces

Inside any target project, the skill manages this structure:

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

Typical output types:

- `notes/`
  unresolved thinking, tensions, tradeoffs, hypotheses
- `decisions/`
  choices currently treated as true
- `open-questions/`
  unresolved questions with revisit triggers
- `presentation-hooks/`
  memorable lines, framing ideas, visual hooks
- `distilled/*.md`
  dated planning distills
- `distilled/*.html`
  dated presentation-ready HTML summaries

Typical file names:

- `2026-03-26-lifestyle-aware-meal-occasion-design.md`
- `2026-03-26-model-shopping-as-household-automation.md`
- `2026-03-26-shopping-planner-distill.md`
- `2026-03-26-shopping-planner-distill.html`

## How It Works

The skill follows a simple operating model:

1. Capture planning-stage context into metadata-rich markdown records.
2. Separate raw planning memory by note type.
3. Preserve dates, summaries, and downstream relevance using YAML frontmatter.
4. Treat planner records as shared memory for planner, producer, and evaluator.
5. Distill all planner records into a dated markdown brief.
6. Generate a matching dated HTML summary in the same run.
7. Validate the planner tree with a Python script when needed.

The minimum frontmatter contract includes:

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

## Repository Layout

```text
planner-memory-skill/
  SKILL.md
  README.md
  README.ko.md
  .gitignore
  agents/
    openai.yaml
  assets/
    templates/
      decision-note-template.md
      distilled-brief-template.md
      distilled-html-template.html
      distilled-readme-template.md
      open-question-template.md
      planner-readme-template.md
      presentation-hook-template.md
      thinking-note-template.md
  references/
    frontmatter-schema.md
    pressure-scenarios.md
  scripts/
    validate_planner_tree.py
  tests/
    test_validate_planner_tree.py
```

## Installation

Clone the repository first:

```bash
git clone https://github.com/InoneSummer/planner-memory-skill.git
cd planner-memory-skill
```

### Install For Codex On macOS / Linux

If your Codex setup uses `$CODEX_HOME`, use:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills/planner-memory"
cp -R ./* "${CODEX_HOME:-$HOME/.codex}/skills/planner-memory/"
```

### Install For Codex On Windows PowerShell

```powershell
$target = if ($env:CODEX_HOME) { Join-Path $env:CODEX_HOME "skills\\planner-memory" } else { Join-Path $HOME ".codex\\skills\\planner-memory" }
New-Item -ItemType Directory -Force $target | Out-Null
Copy-Item -Recurse -Force .\* $target
```

After installation, start a new Codex session or new chat so the skill list refreshes.

### Install For Claude Code On macOS / Linux

```bash
mkdir -p "$HOME/.claude/skills/planner-memory"
cp -R ./* "$HOME/.claude/skills/planner-memory/"
```

### Install For Claude Code On Windows PowerShell

```powershell
$target = Join-Path $HOME ".claude\\skills\\planner-memory"
New-Item -ItemType Directory -Force $target | Out-Null
Copy-Item -Recurse -Force .\* $target
```

Then start a new Claude Code session.

## Usage

In Codex or Claude, call the skill explicitly:

```text
$planner-memory Capture this project planning discussion into planner files and generate the distill md/html pair.
```

A particularly useful pattern is starting a fresh session by asking the skill to load the existing planner state first.

### Continuing In A New Session

If you are returning to a project in a new chat or agent session, start like this:

```text
$planner-memory Read this project's existing planner folder, summarize the current state, and continue the discussion from there.
```

For a concrete project example:

```text
$planner-memory Read shopping/planner, summarize the current state of the agent shopping project, and continue the architecture discussion.
```

Examples:

```text
$planner-memory Create a planner folder for this new project.
```

```text
$planner-memory Read this project's planner folder and create today's distilled markdown and HTML summary.
```

```text
$planner-memory Turn this planning conversation into notes, decisions, open questions, and presentation hooks.
```

## Validation And Tests

Run the validator against a project root or `planner/` directory:

```bash
python scripts/validate_planner_tree.py /path/to/project
```

Run tests:

```bash
python tests/test_validate_planner_tree.py
```

On Windows PowerShell:

```powershell
python .\scripts\validate_planner_tree.py C:\path\to\project
python .\tests\test_validate_planner_tree.py
```

## What Was Considered While Designing It

This skill was built to balance a few competing needs:

- planning should stay lightweight enough to use during live conversations
- notes should still be structured enough to reconstruct later
- HTML should be presentation-ready, but not become the source of truth
- planning memory should help later implementation and evaluation work
- a single project should not collapse all thinking into one giant markdown file
- the system should still be deterministic enough to validate with a script
