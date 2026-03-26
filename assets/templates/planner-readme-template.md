---
title: "Planner Folder"
project: ""
planner_part: "shared-planning-memory"
doc_type: "planner-readme"
discussion_date: "YYYY-MM-DD"
created_at: "YYYY-MM-DD"
updated_at: "YYYY-MM-DD"
summary: "This folder stores shared planning memory for the project."
status: "active"
shared_with:
  - "planner"
  - "producer"
  - "evaluator"
source_refs:
  - "planner/*"
tags:
  - "planner"
  - "shared-memory"
---

# Planner Folder

이 폴더는 프로젝트의 `기획자 파트`가 관리하지만, 결국 팀 전체가 참고하는 공유 기획 자산을 보관하는 작업 공간이다.

## Purpose

- 서비스 기획 단계의 고민 보관
- 하네스 기획 단계의 고민 보관
- 발표 자료로 발전시킬 수 있는 훅과 비유 보관
- 최신 기획 상태를 재구성할 수 있는 중간 산출물 보관
- 생산자와 평가자가 나중에 참조할 수 있는 기획 맥락 보관

## Subfolders

- `notes/`
  - 아직 닫히지 않은 고민, 긴장, 가설
- `decisions/`
  - 현재 기준으로 채택한 결정
- `open-questions/`
  - 아직 남아 있는 질문과 재검토 조건
- `presentation-hooks/`
  - 발표용 문장, 비유, 시각화 아이디어
- `distilled/`
  - planner markdown을 바탕으로 생성한 요약 md/html

## Naming Rule

- planner markdown: `YYYY-MM-DD-<topic>.md`
- distilled markdown: `YYYY-MM-DD-<project-slug>-planner-distill.md`
- distilled html: `YYYY-MM-DD-<project-slug>-planner-distill.html`

## Source Of Truth Rule

- markdown이 원본이다
- HTML은 markdown에서 재구성한 결과물이다
- 중요한 중간 고민은 루트 폴더에 흩뿌리지 말고 `planner/` 아래에 둔다

## Team Asset Rule

- planner 기록은 planner만의 개인 메모가 아니다
- producer와 evaluator도 나중에 이 기록을 읽고 재사용할 수 있어야 한다
- 그래서 메모는 가능한 한 맥락, 결정 이유, 후속 영향이 드러나게 작성한다
