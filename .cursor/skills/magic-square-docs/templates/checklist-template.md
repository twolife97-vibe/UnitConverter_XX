# UnitConverter_XX — ARRR Magic Square TDD Checklist

**일자:** YYYY-MM-DD  
**대상:** `validate_magic_square` · `tests/test_magic_square.py`  
**SSOT:** `.cursorrules` · `.cursor/skills/magic-square-tdd/SKILL.md`

---

## A. Harness · 사전 조건

- [ ] `pyproject.toml` — `pythonpath = ["."]`, `testpaths = ["tests"]`
- [ ] `from src.magic_square import validate_magic_square` import 가능
- [ ] `pytest tests/test_magic_square.py -q` collection 오류 없음

---

## B. RED

- [ ] `/red-test-plan` — 케이스 ≥6 (pass/fail/invalid/경계)
- [ ] 응답 첫 줄 `RED — magic_square: ...`
- [ ] `/red-skeleton` — 테스트 **1개** 추가
- [ ] AAA 주석 (Arrange / Act / Assert)
- [ ] assert **엄격** (`result == {...}`), 완화 없음
- [ ] `src/` **미수정**
- [ ] skip / xfail **없음**
- [ ] pytest **의도적 실패** 확인

---

## C. GREEN

- [ ] 응답 첫 줄 `GREEN — magic_square: ...`
- [ ] **현재 failing** 테스트만 통과 목표
- [ ] `src/magic_square.py` 최소 diff
- [ ] tests 삭제·완화 **없음**
- [ ] pytest **전부 통과**
- [ ] T01 외 케이스 선행 구현 **없음** (minimal)

---

## D. Golden Master

- [ ] `/golden-master` — G1~G4 중 **미커버 1건**
- [ ] Golden grid 값 SKILL·커맨드와 **동일**
- [ ] RED 실패 → GREEN 통과 한 사이클

---

## E. REFACTOR

- [ ] `/refactor-smell` — pytest green **후** audit
- [ ] 스멜 표 (S1~S7) 채움, **코드 변경 없음**
- [ ] `/refactor-safe` — **1순위 1건**만
- [ ] API 시그니처·반환형 불변
- [ ] pytest before/after **동일 passed**

---

## F. 문서 · Export

- [ ] Report — `Report/ARRR_MagicSquare_<주제>_Report.md`
- [ ] Transcript — (선택) `_Transcript.md`
- [ ] Prompt — `Prompt/ARRR_MagicSquare_<주제>_Prompt.md`
- [ ] Report ↔ Prompt 규칙 **정합**

---

## G. 금지 사항 (`.cursorrules`)

- [ ] RED에서 `src/` 수정 안 함
- [ ] GREEN에서 REFACTOR 혼합 안 함
- [ ] REFACTOR에서 tests 수정 안 함
- [ ] git commit — **사용자 요청 시에만**

---

## H. 채점 메모

| 영역 | 만점 | 획득 | 비고 |
|------|------|------|------|
| RED 품질 | | | |
| GREEN 최소성 | | | |
| REFACTOR 안전 | | | |
| 문서 | | | |
| **합계** | | | |

**코멘트:** <1~3문장>

---

## I. 다음 액션

1. <슬래시 커맨드 또는 Gap>
2. …
