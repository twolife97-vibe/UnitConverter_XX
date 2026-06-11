---
name: magic-square-tdd
description: >-
  마방진 validate_magic_square TDD 실습(ARRR). RED test-plan/skeleton, GREEN
  minimal/golden-master, REFACTOR smell/safe 슬래시 커맨드와 연동. magic square,
  마방진, ARRR, TDD RED GREEN REFACTOR, validate_magic_square 작업 시 사용.
---

# Magic Square TDD (ARRR)

UnitConverter_XX **부가 실습** — 마방진 검증 API를 **RED → GREEN → REFACTOR**로 구현한다.  
도메인 SSOT는 본 SKILL; 프로젝트 TDD·품질 규칙은 `.cursorrules` · `docs/PRD.md` FR-07.

## ARRR 슬래시 커맨드

| Phase | 커맨드 | 역할 |
|-------|--------|------|
| RED | `/red-test-plan` | 케이스·AAA 계획 (코드 X) |
| RED | `/red-skeleton` | T01 failing test 1개 |
| GREEN | `/green-minimal` | 현재 실패 테스트 최소 통과 |
| RED→GREEN | `/golden-master` | Golden grid 회귀 1건 |
| REFACTOR | `/refactor-smell` | 스멜 목록 (코드 X) |
| REFACTOR | `/refactor-safe` | 1순위 스멜만 안전 리팩터 |

**규칙:** 커맨드는 **추가 입력·질문 없이** SSOT만 읽고 실행.

## 레이아웃

```
src/magic_square.py      # validate_magic_square
tests/test_magic_square.py
```

```bash
pytest tests/test_magic_square.py -q
```

import: `from src.magic_square import validate_magic_square`  
(`pyproject.toml` — `pythonpath = ["."]`, `testpaths = ["tests"]`)

## API 계약

```python
def validate_magic_square(grid: list[list[int]]) -> dict:
    ...
```

| 키 | 타입 | 설명 |
|----|------|------|
| `status` | `"pass"` \| `"fail"` \| `"invalid"` | 판정 |
| `errors` | `list[str]` | pass면 `[]` |

| status | 조건 |
|--------|------|
| **pass** | n×n, 1..n² 각 1회, 모든 행·열·두 대각선 합 = n(n²+1)/2 |
| **fail** | 정방형·숫자 집합은 유효하나 합 조건 불충족 |
| **invalid** | 빈 grid, 비정방, 범위 밖, 중복, 비정수 등 |

### 마방진 상수

- n×n magic constant: `M = n * (n*n + 1) // 2`
- 3×3: M = 15

## 기본 테스트 케이스 (RED plan)

| ID | grid | status |
|----|------|--------|
| T01 | `[[8,1,6],[3,5,7],[4,9,2]]` | pass |
| T02 | `[[2,7,6],[9,5,1],[4,3,9]]` | fail |
| T03 | `[]` | invalid |
| T04 | `[[1,2],[3,4]]` | fail (2×2, 1..4 미사용) |
| T05 | `[[1]]` | pass |
| T06 | `[[1,2,3],[4,5,6],[7,8,10]]` | fail (10 > 9) |

Golden Master 표(G1~G4): `.cursor/commands/golden-master.md`

## TDD Phase (`.cursorrules` 정합)

| Phase | 수정 | 금지 |
|-------|------|------|
| RED | `tests/` | `src/`, skip, assert 완화 |
| GREEN | `src/` 최소 | tests 삭제·완화, REFACTOR |
| REFACTOR | `src/` 구조 | tests·동작·API 변경 |

응답 **첫 줄** Phase 선언: `RED` / `GREEN` / `REFACTOR`.

## AAA 템플릿

```python
def test_<케이스>():
    # Arrange
    grid = [...]
    # Act
    result = validate_magic_square(grid)
    # Assert
    assert result == {"status": "...", "errors": [...]}
```

## UnitConverter와의 관계

- `validate_lines` · `UnitConverter.py`와 **독립** 모듈.
- 동일 Harness(`src/` + `tests/` + pytest)만 공유.
- 세션 문서화: `.cursor/skills/magic-square-docs/SKILL.md` · `/export-report`

## 실습 순서 (권장)

1. `/red-test-plan`
2. `/red-skeleton` → `/green-minimal`
3. `/golden-master` (G2→G4 반복)
4. `/red-skeleton` (T02 invalid/fail) …
5. `/refactor-smell` → `/refactor-safe`
