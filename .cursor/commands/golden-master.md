# Golden Master — UnitConverter_XX ARRR

**Golden 표 1건**을 RED 테스트로 추가한 뒤, **GREEN 최소 일반화**까지 한 사이클로 수행한다.

## SSOT

| 문서 | 용도 |
|------|------|
| `.cursorrules` | RED→GREEN · API |
| `docs/PRD.md` | §3·§6.2 비율 · KPI-6 |
| `Report/STEP3_ValidateLines_Report.md` | business 예 · F6 |

## Phase 선언

RED 단계:

```
RED — UnitConverter: golden master (<G#>)
```

GREEN 단계 (같은 응답 또는 후속):

```
GREEN — UnitConverter: golden master (<G#>)
```

## 자동 절차 (/golden-master 단독 입력 시)

**질문 없이** 즉시 실행.

1. SSOT에서 **Golden 표** 확정 (아래 §고정 표)
2. **G-next** — 아직 TC에 없는 Golden **첫 행** 선택
3. RED: `tests/`에 Golden assert 테스트 **1개** 추가
4. `pytest` → 의도적 실패 확인
5. GREEN: `src/` **최소 일반화** (literal-only 제거, 비율·프로필 재사용)
6. `pytest tests/ -q` 전체 pass 확인
7. 보고 (RED+GREEN 요약)

## Golden 표 (SSOT — `docs/PRD.md` · STEP3)

| G# | 입력 | profile | 기대 출력 줄 (요약) | KPI |
|----|------|---------|---------------------|-----|
| G1 | `meter:2.5` | default | feet 8.2021 · yard 2.7340 | KPI-6 |
| G2 | `meter:2.5` | business | + inch 98.4252 · mm 2500 | KPI-5 |
| G3 | `feet:12` | default | yard 4.0000 (타깃 yard만) | KPI-6 |
| G4 | `yard:2.5` | default | feet 7.5000 (타깃 feet만) | KPI-6 |
| G5 | `meter:1` | business | mm 1000 (정수) | KPI-5 |

**G-next 규칙:** `tests/`에 해당 입력·profile assert가 **없는 첫 G#**.  
`convert_to_lines` Track이 없으면 `validate_lines`용 `lines` assert로 동일 Golden 적용.

## RED 템플릿 — output Track

```python
def test_golden_g1_meter_default():
    lines = convert_to_lines(2.5, "meter", profile="default")
    assert lines == [
        "2.5 meter = 8.2021 feet",
        "2.5 meter = 2.7340 yard",
    ]
```

## RED 템플릿 — validate_lines Track

```python
def test_golden_g2_meter_business():
    lines = [
        "2.5 meter = 8.2021 feet",
        "2.5 meter = 2.7340 yard",
        "2.5 meter = 98.4252 inch",
        "2.5 meter = 2500 mm",
    ]
    result = validate_lines(lines, profile="business")
    assert result == {"status": "pass", "failed_lines": []}
```

(G2는 기존 `test_kpi5_*`와 중복이면 **G3**로 자동 승급)

## GREEN 일반화 원칙

| Before (minimal) | After (golden) |
|------------------|----------------|
| `if value == 2.5 and unit == "meter"` | `registry` + `conversion/meter` |
| 단일 profile | `profile` 파라미터 분기 |
| 단일 타깃 | `DEFAULT_TARGETS[profile] - {source}` |

**공개 API 시그니처 변경 금지** — `.cursorrules` 계약 유지.

## pytest

```bash
python -m pytest tests/ -q
```

## 보고 템플릿

```
RED — UnitConverter: golden master (G<n>)
추가: tests/<파일> :: <함수명>
pytest: FAILED — <한 줄>

GREEN — UnitConverter: golden master (G<n>)
변경: src/<모듈> — <일반화 한 줄>
pytest: <N> passed

다음: /red-skeleton 또는 /golden-master (G<n+1>)
```

## 금지

| 금지 | 이유 |
|------|------|
| Golden 2건 동시 RED | 한 사이클 1건 |
| assert 완화 | Golden 엄격 유지 |
| 사용자 질문 | 슬래시 단독 |
| git commit/push | `.cursorrules` |

## 수정 허용

- RED: `tests/`만
- GREEN: `src/` 최소 + pytest
