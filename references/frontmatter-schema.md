# Planner Frontmatter Schema

Use this frontmatter in planner markdown files.

```yaml
---
title: ""
project: ""
planner_part: "service-planning"
doc_type: "thinking-note"
discussion_date: "2026-03-26"
created_at: "2026-03-26"
updated_at: "2026-03-26"
summary: ""
status: "active"
shared_with:
  - "planner"
  - "producer"
  - "evaluator"
source_refs:
  - "conversation:YYYY-MM-DD"
tags:
  - "service-design"
---
```

## Field Notes

- `title`: Human-readable title
- `project`: Project slug or project folder name
- `planner_part`: Suggested values:
  - `service-planning`
  - `harness-planning`
  - `presentation-planning`
  - `tooling-planning`
  - `shared-planning-memory`
- `doc_type`: Suggested values:
  - `thinking-note`
  - `decision-note`
  - `open-question`
  - `presentation-hook`
  - `distilled-brief`
  - `planner-readme`
  - `distilled-index`
- `discussion_date`: The main date the discussion happened
- `created_at`: File creation date
- `updated_at`: Last update date
- `summary`: One-sentence summary for quick scanning
- `status`: Suggested values:
  - `active`
  - `decided`
  - `open`
  - `parked`
  - `distilled`
- `shared_with`: Team consumers for this note. Suggested values:
  - `planner`
  - `producer`
  - `evaluator`
- `source_refs`: Conversation dates, note ids, or related docs
- `tags`: Useful retrieval keywords
