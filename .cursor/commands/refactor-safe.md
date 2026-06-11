# REFACTOR Safe — magic_square

**모든 테스트가 green**인 상태에서 smell audit **1순위** 항목만 안전하게 리팩터한다.

## 자동 입력 (질문 금지)

| SSOT | 용도 |
|------|------|
| `.cursorrules` | REFACTOR — 동작 동일, tests 변경 금지 |
| `src/magic_square.py` | 리팩터 대상 |
| `tests/test_magic_square.py` | **변경 금지** |
| `.cursor/commands/refactor-smell.md` | 없으면 S1(하드코딩)을 1순위로 가정 |

**1순위 기본:** S1 하드코딩 제거 → 행·열·대각 **합 검증**으로 일반화 (public API 시그니처 유지).

## Phase 선언 (필수)

응답 **첫 줄**:

```
REFACTOR — magic_square: safe (<S#> — <한 줄>)
```

## 사전 조건

```bash
pytest tests/test_magic_square.py -q
```

- 시작 전·종료 후 **동일하게 전부 통과**.
- 실패 시 즉시 **revert**하고 보고 (질문 없음).

## Safe REFACTOR 절차

1. **베이스라인** — pytest green 확인
2. **한 smell만** — 1순위 1건 (extract function · rename · 상수 추출 등)
3. **작은 diff** — public API `validate_magic_square(grid) -> dict` 불변
4. **회귀** — `pytest tests/test_magic_square.py -q`
5. **동작 동일** — assert 결과 diff 없음

### 허용 리팩터 예

- `_row_sums(grid)` · `_col_sums(grid)` · `_diag_sums(grid)` 추출
- `_magic_constant(n)` · `_is_square(grid)` 추출
- literal → named constant

### 금지 리팩터

- 반환형 `status`/`errors` 키 변경
- 새 기능(fail/invalid 케이스) 추가 → **RED**로
- 테스트 수정·완화

## 완료 보고 형식

```
REFACTOR — magic_square: safe (S1 — 합 검증 일반화)

변경: src/magic_square.py — <추출·이름 변경 요약>
diff 규모: <대략 ±줄>
pytest: passed <N> (before/after 동일)

다음: /refactor-smell — 잔여 스멜, 또는 /red-skeleton — T03 invalid RED
```

## 금지 (REFACTOR Safe)

| 금지 | 이유 |
|------|------|
| `tests/` 수정 | 회귀 기준선 |
| smell 2건 이상 한 번에 | 안전성 |
| API·동작 변경 | REFACTOR 정의 위반 |
| pytest skip | 품질 회피 |
| 사용자에게 smell 선택 질문 | 1순위 자동 |

## 수정 허용

- `src/magic_square.py` (및 동일 모듈 내 private helper)
- REFACTOR 확인용 `pytest` 실행
