# Pressure Scenarios

Use these scenarios later to test whether the skill really improves planner capture quality.

## Scenario 1: Context Window Pressure

Prompt:
`We've talked about this product for a week. Summarize the important design tensions.`

Expected failure without skill:
- Important middle-stage reasoning is omitted
- Old but still-open tensions are forgotten

Expected success with skill:
- Planner notes are discovered first
- Summary cites recent shifts and older unresolved issues

## Scenario 2: Presentation Prep Pressure

Prompt:
`I'm making slides tomorrow. What were the interesting planning debates?`

Expected failure without skill:
- Output is generic and over-smoothed
- Memorable hooks are missing

Expected success with skill:
- Presentation hooks are recovered from planner records
- Distill separates stable principles from open tensions

## Scenario 3: Implementation Drift Pressure

Prompt:
`Let's just build it.`

Expected failure without skill:
- Planning nuance gets skipped
- No record is created before implementation

Expected success with skill:
- New reasoning is captured into planner notes
- Decision or open-question files are created before execution
