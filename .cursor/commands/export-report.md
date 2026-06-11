# Export Report — 세션 산출물보내기

현재 대화·작업 내용을 정리해 **Report/** 보고서와 **Prompt/** 재실행 프롬프트를 저장한다.

## Phase 선언 (필수)

응답 **첫 줄**:

```
EXPORT — <STEP 또는 주제>: Report + Prompt 저장
```

## 실행 절차

1. **수집** — 이번 세션의 목표, 입력, 산출, 변경 파일, 미해결 Gap
2. **명명** — 아래 규칙으로 파일명 확정 (사용자가 주제를 주지 않으면 세션 맥락에서 추론)
3. **작성** — `Report/<이름>_Report.md` 먼저, 이어서 `Prompt/<이름>_Prompt.md`
4. **확인** — 두 파일 경로·제목·일자를 응답 말미에 보고

## 파일 명명 규칙

| 유형 | 패턴 | 예 |
|------|------|-----|
| STEP 보고서 | `STEP{n}_{주제}_Report.md` | `STEP3_ValidateLines_Report.md` |
| STEP 프롬프트 | `STEP{n}_{주제}_Prompt.md` | `STEP3_ValidateLines_Prompt.md` |
| 채점·리뷰 | `STEP{n}_{주제}_Grading_Report.md` / `_Grading_Prompt.md` | |
| 초기 정의 | `01.UnitConverter_{주제}_Report.md` | |

- 공백·한글 파일명 금지. PascalCase 또는 snake 주제.
- **같은 STEP을 덮어쓸지** 사용자에게 확인하지 않고, 세션 주제가 기존 파일과 같으면 **해당 파일을 갱신**한다.
- 주제가 다르면 **새 파일**을 만든다.

## Report/ 보고서 템플릿

`Report/<이름>_Report.md`:

```markdown
# UnitConverter_XX — <제목>

**일자:** YYYY-MM-DD
**입력:** <선행 보고서·파일·세션 맥락>
**산출:** <코드·설계·테스트 등>

---

## 1. 목적

<이번 작업이 해결한 문제 1~3문장>

## 2. 요약

| 항목 | 내용 |
|------|------|
| ... | ... |

## 3. 상세

### 3.1 <소제목>

<결정·계약·구현·테스트 결과>

## 4. 변경·산출물

| 경로 | 변경 |
|------|------|
| `src/...` | ... |
| `tests/...` | ... |

## 5. Gap · 다음 단계

| 항목 | 상태 | 후속 |
|------|------|------|
| ... | ... | ... |
```

- 사실만 기록. 추측은 Gap으로 분리.
- 코드·API·pytest 결과가 있으면 표·코드 블록으로 인용.
- TDD 세션이면 RED/GREEN/REFACTOR 단계별 결과를 §3에 포함.

## Prompt/ 프롬프트 템플릿

`Prompt/<이름>_Prompt.md`:

```markdown
# UnitConverter_XX — <제목> 프롬프트

## 1. 실행 프롬프트

\```
<한 블록으로 복사 가능한 재실행 지시문>

입력:
- <필수 파일·보고서 목록>

출력 형식:
1. ...
2. ...

규칙:
- ...
\```

---

## 2. 참고 (선택)

<계약 표·체크리스트·채점 기준 등 Report에서 반복 쓰는 규칙>

---

## 3. 연계

| 선행 | 후속 |
|------|------|
| `Report/...` | `Report/...` |
```

- §1 실행 프롬프트는 **다른 세션에서 그대로 붙여 넣어** 동일 작업을 재현할 수 있어야 한다.
- Report에 없는 새 규칙을 Prompt에만 넣지 않는다 (Report ↔ Prompt 정합 유지).

## 작성 규칙

- **한국어**로 작성.
- 일자는 오늘 날짜 (`YYYY-MM-DD`).
- `.cursorrules`·도메인 용어(validate_lines, profile, STEP2 성공 기준 등)와 맞출 것.
- **이 커맨드는 `Report/`와 `Prompt/` 파일만 생성·수정**한다. `src/`, `tests/` 등은 건드리지 않는다.
- git commit은 사용자 요청 시에만.

## 완료 보고 형식

```
EXPORT — <주제>: Report + Prompt 저장

저장 파일:
  - Report/<이름>_Report.md  (<한 줄 요약>)
  - Prompt/<이름>_Prompt.md  (<한 줄 요약>)

핵심 산출: <1문장>
다음 권장: <후속 STEP 또는 TDD Phase>
```

## 금지

| 금지 | 이유 |
|------|------|
| Report/Prompt 외 파일 수정 | export 범위 한정 |
| 빈 템플릿·플레이스홀더만 저장 | 세션 내용 반영 필수 |
| Prompt에 솔루션명만 나열 | Mom Test·R-G-I-O 규칙 위반 |
| 중복 파일 무단 생성 | 명명 규칙·주제 일치 여부 확인 |
