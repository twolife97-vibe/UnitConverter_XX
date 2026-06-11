# Golden Master — magic_square

알려진 **정답 격자(Golden)** 와 기대 `status`/`errors`를 테스트로 고정한다. RED(테스트 추가) → GREEN(일반화) 한 사이클로 진행한다.

## 자동 입력 (질문 금지)

| SSOT | 용도 |
|------|------|
| `.cursor/skills/magic-square-tdd/SKILL.md` | Golden 표 · API |
| `tests/test_magic_square.py` | 기존 테스트와 **중복 없이** 1건 추가 |
| `.cursorrules` | RED→GREEN 순서 |

**기본 Golden (이미 RED됐으면 다음 행):**

| ID | grid | status |
|----|------|--------|
| G1 | `[[8,1,6],[3,5,7],[4,9,2]]` | pass |
| G2 | `[[2,7,6],[9,5,1],[4,3,8]]` | pass |
| G3 | `[[1]]` | pass (1×1) |
| G4 | `[[2,7,6],[9,5,1],[4,3,9]]` | fail (합 불일치) |

- 파일에 없는 **첫 Golden ID** 1개만 이번 사이클에 추가.

## Phase 선언 (필수)

**RED 단계** (테스트 추가) 응답 첫 줄:

```
RED — magic_square: golden master (<G#>)
```

**GREEN 단계** (구현 일반화) 응답 첫 줄:

```
GREEN — magic_square: golden master (<G#>)
```

한 번의 `/golden-master` 호출 = **RED 완료 + pytest 실패 확인**까지. GREEN은 같은 세션에서 이어서 수행하거나 `/green-minimal`로 위임.

## Golden 테스트 패턴

```python
@pytest.mark.parametrize(
    "grid,expected",
    [
        (
            [[8, 1, 6], [3, 5, 7], [4, 9, 2]],
            {"status": "pass", "errors": []},
        ),
    ],
)
def test_golden_pass(grid, expected):
    result = validate_magic_square(grid)
    assert result == expected
```

- parametrize **1 케이스** 또는 단일 함수 1개 (RED 1개 원칙).
- Golden grid는 SKILL 표와 **동일 값** 사용 (임의 변경 금지).

## 절차

1. **RED** — `tests/`에 Golden 테스트 1개 추가
2. **실행** — `pytest tests/test_magic_square.py -q` → **의도적 실패**
3. **GREEN** — `src/magic_square.py`를 Golden+기존 통과 테스트 모두 만족하도록 **최소** 일반화
4. **재실행** — 전 테스트 통과

## 완료 보고 형식

```
RED — magic_square: golden master (G2)

추가: tests/test_magic_square.py :: <함수명>
Golden: G2 — 3×3 pass (Lo Shu 변형)
pytest: <실패 한 줄>

GREEN — magic_square: golden master (G2)

변경: src/magic_square.py — <일반화 한 줄>
pytest: passed <N>

다음: /golden-master (G3) 또는 /refactor-smell
```

## 금지

| 금지 | 이유 |
|------|------|
| Golden 값 임의 변경 | 회귀 기준선 파괴 |
| RED·GREEN 동시에 테스트만 추가하고 구현 생략 | Golden은 통과까지가 한 사이클 |
| snapshot 파일 도입 (v1) | 격자 literal이 SSOT |
| 사용자에게 Golden 선택 질문 | G1→G4 순서 고정 |

## 수정 허용

- RED: `tests/` 만
- GREEN: `src/magic_square.py` + pytest
