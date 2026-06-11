# UnitConverter_XX — ARRR Magic Square <제목>

**일자:** YYYY-MM-DD  
**입력:** `.cursor/skills/magic-square-tdd/SKILL.md` · <선행 Report·세션>  
**산출:** <코드·테스트·TDD Phase>

---

## 1. 목적

<이번 ARRR 세션이 해결한 문제 1~3문장 — 마방진 API·TDD Phase>

---

## 2. 요약

| 항목 | 내용 |
|------|------|
| Phase | RED / GREEN / REFACTOR |
| 커맨드 | `/red-skeleton` · `/green-minimal` · … |
| API | `validate_magic_square(grid) -> {status, errors}` |
| pytest | passed <N> / failed <N> |
| 변경 파일 | `src/magic_square.py`, `tests/test_magic_square.py` |

---

## 3. TDD 상세

### 3.1 RED

| 테스트 | 케이스 ID | Arrange | 기대 status | pytest |
|--------|-----------|---------|-------------|--------|
| `test_...` | T01 | 3×3 pass grid | pass | fail → 의도 |

### 3.2 GREEN

<최소 구현 요약 — 하드코딩 여부, 통과 테스트>

### 3.3 REFACTOR (해당 시)

<스멜 ID · 적용 리팩터 · pytest before/after>

---

## 4. API · 계약

```python
result = validate_magic_square(grid)
# {"status": "pass"|"fail"|"invalid", "errors": [...]}
```

| 케이스 | grid | status | errors |
|--------|------|--------|--------|
| … | … | … | … |

---

## 5. 변경·산출물

| 경로 | 변경 |
|------|------|
| `src/magic_square.py` | … |
| `tests/test_magic_square.py` | … |
| `.cursor/commands/...` | (해당 시) |

---

## 6. Gap · 다음 단계

| 항목 | 상태 | 후속 |
|------|------|------|
| T02 fail RED | ❌ | `/red-skeleton` |
| Golden G3 | ❌ | `/golden-master` |
| smell S1 | ❌ | `/refactor-smell` |

**다음 권장:** <슬래시 커맨드 1개>

---

## 7. 연계

| 선행 | 후속 |
|------|------|
| `Report/STEP3_Harness_Report.md` | 본 Report |
| `docs/PRD.md` FR-07 | … |
