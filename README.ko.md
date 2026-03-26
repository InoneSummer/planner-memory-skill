# Planner Memory

`planner-memory`는 흩어지는 프로젝트 기획 대화를 `공유 가능한 planning memory 시스템`으로 바꾸기 위한 재사용형 스킬입니다.

이 스킬은 각 프로젝트 안에 `planner/` 폴더를 만들고 유지하며, markdown을 원본으로 보관하고, 기획 맥락을 날짜 기반의 markdown + HTML 산출물로 distill해서 나중에 구현, 평가, 발표 자료까지 이어질 수 있게 돕습니다.

## 왜 만들었나

대부분의 기획 맥락은 채팅 기록, 회의 메모, 혹은 한 세션의 컨텍스트 윈도 안에서 사라집니다. 이건 특히 아래 같은 상황에서 크게 불편합니다.

- 프로젝트가 며칠, 몇 주에 걸쳐 진화할 때
- 마지막 결론보다 중간 reasoning이 더 중요할 때
- 나중에 producer와 evaluator가 planner의 맥락을 이어받아야 할 때
- 발표 자료용 요약을 만들고 싶은데 매번 처음부터 다시 정리해야 할 때

이 스킬은 바로 그 문제를 해결하기 위해 만들었습니다.

즉, 기획을 `일회성 대화`가 아니라 `팀의 자산`으로 다루기 위해 만든 스킬입니다.

## 어떤 문제를 푸나

`planner-memory`는 아래처럼 `중간 단계의 고민`이 중요한 프로젝트에 맞춰져 있습니다.

- 서비스 기획
- 하네스 기획
- 에이전트 워크플로 설계
- 발표 메시지 프레이밍
- 제품 트레이드오프 기록

특히 다음이 동시에 필요한 프로젝트에 적합합니다.

- 기획 기록을 위한 안정적인 폴더 구조
- 나중에 정렬 가능한 메타데이터가 들어간 markdown
- 구현 계획과 분리된 기획 메모리
- 슬라이드, 문서, HTML 산출물로 재활용 가능한 distilled 결과

## 핵심 설계 원칙

이 스킬은 몇 가지 강한 원칙을 기준으로 설계했습니다.

1. markdown이 source of truth다.
2. HTML은 generated output이지 원본이 아니다.
3. planner 기록은 planner만의 개인 메모가 아니라 planner, producer, evaluator가 함께 참고하는 팀 자산이다.
4. 나중에 재구성할 수 있도록 모든 기록에는 날짜 메타데이터가 필요하다.
5. distillation의 기본 종료 조건은 markdown + HTML 한 쌍이다.
6. 검증 가능해야 하므로 planner 구조를 검사하는 deterministic script를 둔다.

## 어떤 산출물을 만드나

이 스킬은 대상 프로젝트 안에 아래 구조를 관리합니다.

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

주요 산출물 종류:

- `notes/`
  아직 닫히지 않은 고민, 긴장, 가설
- `decisions/`
  현재 기준으로 채택한 결정
- `open-questions/`
  아직 열려 있는 질문과 revisit trigger
- `presentation-hooks/`
  발표용 문장, 비유, 시각화 훅
- `distilled/*.md`
  날짜가 박힌 planning distill 문서
- `distilled/*.html`
  날짜가 박힌 발표용 HTML 요약 페이지

예시 파일 이름:

- `2026-03-26-lifestyle-aware-meal-occasion-design.md`
- `2026-03-26-model-shopping-as-household-automation.md`
- `2026-03-26-shopping-planner-distill.md`
- `2026-03-26-shopping-planner-distill.html`

## 어떻게 작동하나

이 스킬은 다음 흐름으로 동작합니다.

1. 기획 대화 내용을 메타데이터가 있는 markdown 기록으로 남긴다.
2. 기록 종류별로 planner 하위 폴더에 나눠 저장한다.
3. YAML frontmatter로 날짜, 요약, downstream relevance를 남긴다.
4. planner 기록을 planner, producer, evaluator가 함께 보는 shared memory로 다룬다.
5. planner 전체를 읽고 날짜 기반 markdown distill을 만든다.
6. 같은 실행에서 짝이 되는 HTML distill도 함께 만든다.
7. 필요하면 Python validator로 planner 구조를 검사한다.

최소 frontmatter 계약:

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

## 저장소 구조

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

## 설치 방법

먼저 저장소를 clone합니다.

```bash
git clone https://github.com/<your-account>/planner-memory-skill.git
cd planner-memory-skill
```

### Codex 설치 방법 (macOS / Linux)

Codex가 `$CODEX_HOME`을 쓴다면:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills/planner-memory"
cp -R ./* "${CODEX_HOME:-$HOME/.codex}/skills/planner-memory/"
```

### Codex 설치 방법 (Windows PowerShell)

```powershell
$target = if ($env:CODEX_HOME) { Join-Path $env:CODEX_HOME "skills\\planner-memory" } else { Join-Path $HOME ".codex\\skills\\planner-memory" }
New-Item -ItemType Directory -Force $target | Out-Null
Copy-Item -Recurse -Force .\* $target
```

설치 후에는 새 Codex 세션이나 새 채팅을 시작하는 편이 안전합니다.

### Claude Code 설치 방법 (macOS / Linux)

```bash
mkdir -p "$HOME/.claude/skills/planner-memory"
cp -R ./* "$HOME/.claude/skills/planner-memory/"
```

### Claude Code 설치 방법 (Windows PowerShell)

```powershell
$target = Join-Path $HOME ".claude\\skills\\planner-memory"
New-Item -ItemType Directory -Force $target | Out-Null
Copy-Item -Recurse -Force .\* $target
```

설치 후 새 Claude Code 세션을 시작합니다.

## 사용 방법

Codex나 Claude에서 이렇게 명시 호출하면 됩니다.

```text
$planner-memory 이 프로젝트의 기획 대화를 planner 파일로 정리하고 distill md/html 한 쌍까지 만들어줘
```

예시:

```text
$planner-memory 이 새 프로젝트용 planner 폴더를 만들어줘
```

```text
$planner-memory 이 프로젝트의 planner 폴더를 읽고 오늘 날짜의 distilled markdown과 HTML을 만들어줘
```

```text
$planner-memory 이 기획 대화를 notes, decisions, open questions, presentation hooks로 정리해줘
```

## 검증과 테스트

validator 실행:

```bash
python scripts/validate_planner_tree.py /path/to/project
```

테스트 실행:

```bash
python tests/test_validate_planner_tree.py
```

Windows PowerShell에서는:

```powershell
python .\scripts\validate_planner_tree.py C:\path\to\project
python .\tests\test_validate_planner_tree.py
```

## 설계할 때 무엇을 고려했나

이 스킬은 아래의 균형을 맞추기 위해 설계했습니다.

- 라이브 기획 대화 중에도 가볍게 쓸 수 있어야 한다
- 동시에 나중에 재구성할 수 있을 만큼 구조화되어 있어야 한다
- HTML은 발표 친화적이어야 하지만 원본을 대체하면 안 된다
- planner 기록이 나중에 producer와 evaluator의 작업에도 도움이 되어야 한다
- 하나의 프로젝트가 거대한 단일 markdown 파일로 붕괴하면 안 된다
- 검증 가능한 deterministic script가 있어야 한다

## GitHub에 올릴 때 권장 흐름

이 스킬만 독립 저장소로 올리고 싶다면:

```bash
git init
git add .
git commit -m "Initial release: planner-memory skill"
gh repo create planner-memory-skill --public --source=. --remote=origin --push
```

비공개 저장소로 올리고 싶다면 `--public` 대신 `--private`를 쓰면 됩니다.

## 메모

- 이 저장소는 의도적으로 스킬과 지원 파일만 포함합니다.
- 프로젝트별 planner 데이터는 포함하지 않습니다.
- 공개 배포 시 재사용 조건을 명확히 하려면 LICENSE 파일을 추가하는 것을 권장합니다.
