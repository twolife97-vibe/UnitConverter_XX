# RED Skeleton — UnitConverter_XX ARRR

**실패하는 테스트 골격 1개**만 `tests/`에 추가한다. `src/`는 건드리지 않는다.

## SSOT

| 문서 | 용도 |
|------|------|
| `.cursorrules` | RED Phase · API · 금지 |
| `docs/PRD.md` | KPI · FR · 테스트 Track |
| `Report/STEP3_ValidateLines_Report.md` | F1~F7 · 프로필 |

## Phase 선언 (필수)

응답 **첫 줄**:

```
RED — UnitConverter: skeleton (<테스트 함수명>)
```

## 자동 절차 (/red-skeleton 단독 입력 시)

**질문 없이** 즉시 실행.

1. SSOT + `tests/` · `src/output/text.py` · `src/session/continuous.py` 읽기
2. **T-next 자동 선택** — `/red-test-plan` 백로그 우선순위(#1→#6)에서 **TC 없음 또는 스텁**인 첫 항목
3. **테스트 1개** AAA 골격 추가 (아래 Track별 규칙)
4. `pytest` 실행 → **의도적 실패** 확인
5. 보고 템플릿으로 응답

## T-next 자동 선택 (고정 우선순위)

| 순위 | 파일 | 함수명 패턴 | KPI |
|------|------|-------------|-----|
| 1 | `tests/test_output_text.py` (없으면 생성) | `test_kpi6_convert_to_lines_default_pass` | KPI-6 |
| 2 | 동일 | `test_kpi5_convert_to_lines_business_pass` | KPI-5 |
| 3 | `tests/test_session_continuous.py` (없으면 생성) | `test_kpi4_run_continuous_two_inputs_pass` | KPI-4 |
| 4 | `tests/test_validate_lines.py` | `test_kpi5_invalid_format_fail` | KPI-5 |
| 5 | `tests/entity/test_d_loc_01.py` | `test_d_loc_01_blank_unit_invalid` | KPI-3 |

**규칙:** 해당 파일에 **동명·동요구 테스트가 이미 있으면** 다음 순위로 내려간다.

## Track별 AAA 템플릿

### output — `convert_to_lines` (KPI-5/6)

```python
from src.output.text import convert_to_lines

def test_kpi6_convert_to_lines_default_pass():
    # Arrange
    value, unit = 2.5, "meter"
    # Act
    lines = convert_to_lines(value, unit, profile="default")
    # Assert
    assert lines == [
        "2.5 meter = 8.2021 feet",
        "2.5 meter = 2.7340 yard",
    ]
```

business (KPI-5):

```python
assert lines == [
    "2.5 meter = 8.2021 feet",
    "2.5 meter = 2.7340 yard",
    "2.5 meter = 98.4252 inch",
    "2.5 meter = 2500 mm",
]
```

### session — `run_continuous` (KPI-4)

```python
from src.session.continuous import run_continuous

def test_kpi4_run_continuous_two_inputs_pass(monkeypatch):
    # Arrange — stdin 시뮬: meter:2.5 → yard:3 → quit
    # Act
    groups = run_continuous(convert_fn=..., min_inputs=2)
    # Assert
    assert len(groups) >= 2
```

(monkeypatch·fixture는 **최소** — I/O는 GREEN에서 구현; RED는 `NotImplementedError` 실패면 충분)

### validate_lines — fail (KPI-5)

```python
from src.validate_lines import validate_lines

def test_kpi5_invalid_format_fail():
    lines = ["2.5meter=8.2021feet"]
    result = validate_lines(lines, profile="default")
    assert result == {"status": "fail", "failed_lines": [...]}  # 엄격 또는 len≥1 + status
```

**pass/incomplete assert는 엄격 dict equality** — `.cursorrules` · `tests/test_validate_lines.py` 기존 스타일 따름.

### entity — KPI-3

```python
def test_d_loc_01_blank_unit_invalid():
    result = parse_unit_value_coords(":2.5")
    assert result["status"] == "invalid"
    assert len(result["errors"]) >= 1
```

## pytest

```bash
python -m pytest <추가한 파일>::<함수명> -q
```

- **기대:** 실패 (`NotImplementedError` · assertion · API 미구현)
- 실패 원인이 의도와 다르면 **tests/만** 수정

## 보고 템플릿

```
RED — UnitConverter: skeleton (<함수명>)

추가: tests/<파일> :: <함수명>
KPI: KPI-<n> · Track: <output|session|validate_lines|entity>
Arrange: <한 줄>
기대 Assert: <한 줄>

pytest:
  <실패 요약 1줄>

다음: /green-minimal
```

## 금지 (RED)

| 금지 | 이유 |
|------|------|
| `src/` 수정 | GREEN까지 연기 |
| assert 완화 · skip · xfail | 요구 희석 |
| 사용자 질문 | 슬래시 단독 |
| git commit/push | `.cursorrules` |
| RED 사이클당 테스트 2개 이상 | 한 Phase 한 사이클 |

## 수정 허용

- `tests/test_validate_lines.py`
- `tests/test_output_text.py` (신규)
- `tests/test_session_continuous.py` (신규)
- `tests/entity/test_d_loc_01.py` · `tests/entity/conftest.py`
