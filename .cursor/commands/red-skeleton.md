# RED Skeleton — magic_square

`validate_magic_square`에 대한 **실패하는 테스트 골격**을 `tests/`에 추가한다. 구현은 건드리지 않는다.

## 자동 입력 (질문 금지)

| SSOT | 용도 |
|------|------|
| `.cursorrules` | RED는 `tests/`만 |
| `.cursor/skills/magic-square-tdd/SKILL.md` | API·import·첫 RED 케이스(T01) |
| `.cursor/commands/red-test-plan.md` | 없으면 SKILL § 기본 케이스 T01 사용 |

**1순위 RED:** T01 — 3×3 정답 → `status: pass`, `errors: []`

## Phase 선언 (필수)

응답 **첫 줄**:

```
RED — magic_square: skeleton (<테스트 함수명>)
```

## 대상 API

```python
from src.magic_square import validate_magic_square

result = validate_magic_square(grid)
# {"status": "pass" | "fail" | "invalid", "errors": [...]}
```

## AAA 절차

1. **Arrange** — T01 격자 `[[8,1,6],[3,5,7],[4,9,2]]`
2. **Act** — `result = validate_magic_square(grid)`
3. **Assert** — `result == {"status": "pass", "errors": []}` (**엄격**, 완화 금지)

```python
def test_3x3_valid_pass():
    # Arrange
    grid = [
        [8, 1, 6],
        [3, 5, 7],
        [4, 9, 2],
    ]
    # Act
    result = validate_magic_square(grid)
    # Assert
    assert result == {"status": "pass", "errors": []}
```

## 파일 규칙

| 경로 | 내용 |
|------|------|
| `tests/test_magic_square.py` | 없으면 생성; 있으면 함수 **1개** 추가 |
| `tests/__init__.py` | 없으면 빈 파일 |
| `src/magic_square.py` | **수정 금지** (없어도 RED 유지 — import/collection 실패 허용) |

- RED 사이클당 테스트 **1개**만 추가.
- `@pytest.mark.skip` · `xfail` · `pytest.raises`로 RED 회피 금지.

## 실행

```bash
pytest tests/test_magic_square.py -q
```

- **기대:** 새 테스트 **실패** (모듈 없음 · NotImplemented · status 불일치 등 **의도된** 실패)
- 실패 원인이 Assert와 다르면 `tests/`만 수정.

## 완료 보고 형식

```
RED — magic_square: skeleton (<함수명>)

추가: tests/test_magic_square.py :: <함수명>
케이스: T01 — 3×3 pass
Arrange: 3×3 정답 격자
기대 Assert: status=pass, errors=[]

pytest 결과:
  <실패 한 줄 요약>

다음: /green-minimal — 위 테스트 통과 최소 구현
```

## 금지 (RED Skeleton)

| 금지 | 이유 |
|------|------|
| `src/` 수정 | GREEN까지 연기 |
| assert 완화 (`status in ...`, `errors` 길이만 등) | 요구 희석 |
| skip / xfail | RED 회피 |
| 한 사이클에 테스트 2개 이상 | TDD 단위 위반 |
| 사용자에게 케이스 선택 질문 | T01 고정 |

## 수정 허용

- `tests/test_magic_square.py` (및 필요 시 `tests/` 픽스처)
- RED 확인용 `pytest` 실행
