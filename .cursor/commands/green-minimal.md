# GREEN Minimal — magic_square

현재 **실패 중인** `tests/test_magic_square.py` 테스트를 통과시키는 **최소** 구현만 `src/`에 추가한다.

## 자동 입력 (질문 금지)

| SSOT | 용도 |
|------|------|
| `.cursorrules` | GREEN은 `src/` 최소 수정 |
| `.cursor/skills/magic-square-tdd/SKILL.md` | API 반환형·T01 동작 |
| `tests/test_magic_square.py` | **현재 실패 테스트** — 이것만 통과 목표 |

실패 테스트가 없으면: SKILL § T01에 맞는 RED skeleton 1개를 먼저 추가한 뒤 GREEN (RED Phase 선언 후 tests/만).

## Phase 선언 (필수)

응답 **첫 줄**:

```
GREEN — magic_square: minimal (<통과시킨 테스트 함수명>)
```

## 대상 API

```python
def validate_magic_square(grid: list[list[int]]) -> dict:
    return {"status": "pass" | "fail" | "invalid", "errors": list[str]}
```

## GREEN 절차

1. **실패 확인** — `pytest tests/test_magic_square.py -q` 로 대상 1개 실패 재현
2. **최소 구현** — T01(3×3 pass)만 통과하는 코드 (하드코딩·특수 케이스 허용)
3. **회귀** — `pytest tests/test_magic_square.py -q` 전부 통과
4. **범위** — 통과에 불필요한 일반화·리팩터 **금지** (REFACTOR로 미룸)

### 최소 구현 예 (T01만)

```python
_KNOWN_3X3 = [[8, 1, 6], [3, 5, 7], [4, 9, 2]]

def validate_magic_square(grid):
    if grid == _KNOWN_3X3:
        return {"status": "pass", "errors": []}
    return {"status": "fail", "errors": ["not implemented"]}
```

- 위는 **예시**; 실제 코드는 현재 failing assert에 맞출 것.
- fail/invalid 일반 로직은 **다음 RED**까지 미룸.

## 실행

```bash
pytest tests/test_magic_square.py -q
```

- **기대:** 추가·수정한 테스트 **전부 통과**

## 완료 보고 형식

```
GREEN — magic_square: minimal (<함수명>)

변경: src/magic_square.py — <한 줄 요약>
통과 테스트: tests/test_magic_square.py :: <함수명>

pytest 결과:
  <passed N>

다음: /red-skeleton — T02 fail 케이스 RED, 또는 /golden-master
```

## 금지 (GREEN Minimal)

| 금지 | 이유 |
|------|------|
| 테스트 삭제·assert 완화 | 요구 희석 |
| T01 외 케이스 선행 구현 | YAGNI · 다음 RED 위반 |
| REFACTOR (구조 개편) | Phase 혼합 |
| `UnitConverter.py` · `validate_lines.py` 수정 | 범위 밖 |
| 사용자에게 구현 방식 질문 | 최소 통과로 자율 결정 |

## 수정 허용

- `src/magic_square.py` (없으면 생성 + `src/__init__.py` 확인)
- GREEN 확인용 `pytest` 실행
