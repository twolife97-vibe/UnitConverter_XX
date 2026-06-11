---
name: magic-square-docs
description: >-
  ARRR 마방진 TDD 세션의 Report·Transcript·Checklist 문서를 생성·갱신한다.
  magic square 실습 보고, 인터뷰 전문, 채점 체크리스트, export-report, 세션
  산출물 저장 시 사용.
---

# Magic Square Docs (ARRR)

ARRR 실습 세션을 **Report/** · **Prompt/** · **Checklist/** 에 저장한다.  
형식 SSOT: `.cursor/commands/export-report.md` (export-session과 동일 절차).

## 자동 입력 (질문 금지)

| SSOT | 용도 |
|------|------|
| `.cursor/commands/export-report.md` | Report/Prompt 명명·절차 |
| `.cursor/skills/magic-square-tdd/SKILL.md` | API·케이스·커맨드 |
| `.cursorrules` | TDD·용어 |
| `docs/PRD.md` | FR-07 테스트 맥락 |
| **현재 대화** | 목표·pytest·변경 파일·Gap |

사용자 추가 입력 없이 세션 맥락에서 주제·일자·Gap을 채운다.

## Phase 선언 (필수)

응답 **첫 줄**:

```
EXPORT — ARRR MagicSquare: <Report|Transcript|Checklist> 저장
```

## 실행 절차

1. **수집** — 이번 세션 RED/GREEN/REFACTOR, 변경 경로, pytest 결과
2. **명명** — 아래 표 (주제 동일 시 **갱신**, 다르면 신규)
3. **작성** — 템플릿 파일을 읽고 placeholder 치환
4. **확인** — 저장 경로·한 줄 요약을 응답 말미에 보고

## 파일 명명

| 유형 | 경로 패턴 | 예 |
|------|-----------|-----|
| Report | `Report/ARRR_MagicSquare_{주제}_Report.md` | `ARRR_MagicSquare_T01Pass_Report.md` |
| Transcript | `Report/ARRR_MagicSquare_{주제}_Transcript.md` | `ARRR_MagicSquare_Session1_Transcript.md` |
| Checklist | `Report/ARRR_MagicSquare_{주제}_Checklist.md` | `ARRR_MagicSquare_TDD_Checklist.md` |
| Prompt | `Prompt/ARRR_MagicSquare_{주제}_Prompt.md` | Report와 쌍 |

- 공백·한글 파일명 금지. PascalCase/snake 주제.
- **Report + Prompt**는 export-report 규칙대로 **쌍**으로 유지.

## 템플릿 (필수 참조)

| 템플릿 | 경로 |
|--------|------|
| Report | [templates/report-template.md](templates/report-template.md) |
| Transcript | [templates/transcript-template.md](templates/transcript-template.md) |
| Checklist | [templates/checklist-template.md](templates/checklist-template.md) |

템플릿의 `<placeholder>`를 세션 사실로 치환. 추측은 Gap 표로 분리.

## 작성 규칙

- **한국어**
- 일자: `YYYY-MM-DD` (오늘)
- TDD 세션이면 §3에 RED/GREEN/REFACTOR 단계별 pytest 결과
- **본 SKILL 범위:** `Report/` · `Prompt/` · (Checklist는 `Report/` 하위)만 수정
- `src/` · `tests/` · git commit — **사용자 요청 시에만**

## 완료 보고 형식

```
EXPORT — ARRR MagicSquare: <주제> 저장

저장 파일:
  - Report/<이름>_Report.md  (<한 줄>)
  - Report/<이름>_Transcript.md  (<선택>)
  - Report/<이름>_Checklist.md  (<선택>)
  - Prompt/<이름>_Prompt.md  (<한 줄>)

핵심 산출: <1문장>
다음 권장: <TDD Phase 또는 슬래시 커맨드>
```

## 금지

| 금지 | 이유 |
|------|------|
| Report/Prompt/Checklist 외 수정 | export 범위 |
| 빈 placeholder만 저장 | 세션 미반영 |
| Prompt에 Report 없는 신규 규칙 | SSOT 불일치 |
| 사용자에게 파일명·주제 질문 | 명명 규칙으로 자율 확정 |
