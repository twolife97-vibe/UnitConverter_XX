# TDD RED — validate_lines

`src/validate_lines.py` 목표 API에 대한 **실패하는 테스트**만 추가한다.

## Phase 선언 (필수)

응답 **첫 줄**:

```
RED — validate_lines: <검증 항목 한 줄 요약>
```

예: `RED — validate_lines: business 프로필 meter 2.5 → pass`

## 대상 API

```python
result = validate_lines(lines, profile="default" | "business", ...)
# result == {"status": "pass" | "fail" | "incomplete", "failed_lines": [...]}
```

| status | 의미 |
|--------|------|
| pass | 계약 충족 |
| fail | 형식·값·타깃 위반 |
| incomplete | 출력 부족·빈 묶음 |

계약 상세: `Report/STEP3_ValidateLines_Report.md`

## AAA 절차

각 테스트 함수는 **Arrange → Act → Assert** 순서로 작성한다.

1. **Arrange** — 검증할 출력 줄 `lines`와 `profile`·옵션 준비
2. **Act** — `result = validate_lines(...)` 호출
3. **Assert** — `status`와 `failed_lines`를 **엄격히** 검증 (완화 금지)

```python
def test_business_meter_pass():
    # Arrange
    lines = [
        "2.5 meter = 8.2021 feet",
        "2.5 meter = 2.7340 yard",
        "2.5 meter = 98.4252 inch",
        "2.5 meter = 2500 mm",
    ]
    # Act
    result = validate_lines(lines, profile="business")
    # Assert
    assert result == {"status": "pass", "failed_lines": []}
```

## pytest 예시 (RED용)

**pass (default)**

```python
def test_default_feet_yard_pass():
    lines = [
        "2.5 meter = 8.2021 feet",
        "2.5 meter = 2.7340 yard",
    ]
    result = validate_lines(lines, profile="default")
    assert result == {"status": "pass", "failed_lines": []}
```

**fail — 형식 위반**

```python
def test_invalid_format_fail():
    lines = ["2.5meter=8.2021feet"]
    result = validate_lines(lines, profile="default")
    assert result["status"] == "fail"
    assert len(result["failed_lines"]) >= 1
```

**incomplete — 타깃 누락**

```python
def test_business_missing_mm_incomplete():
    lines = [
        "2.5 meter = 8.2021 feet",
        "2.5 meter = 2.7340 yard",
    ]
    result = validate_lines(lines, profile="business")
    assert result["status"] == "incomplete"
    assert any("mm" in msg for msg in result["failed_lines"])
```

**한 번에 하나** — RED 사이클당 테스트 1개(또는 동일 요구의 최소 세트)만 추가.

## 실행

```bash
pytest tests/test_validate_lines.py -q
```

- **기대:** 새 테스트 **실패** (구현 미충족 또는 API 미전환)
- 실패 원인이 의도와 다르면 테스트를 고친다 (`tests/` 만).

## 보고 형식

작업 후 아래 템플릿으로 보고한다.

```
RED — validate_lines: <요약>

추가 테스트: tests/test_validate_lines.py :: <함수명>
검증 항목: <F1~F7 또는 STEP2 #n>
Arrange: <입력 요약>
기대 Assert: status=<...>, failed_lines=<...>

pytest 결과:
  <실패 메시지 한 줄 요약>

다음: GREEN — 위 테스트를 통과시키는 최소 구현
```

## 금지 (RED)

| 금지 | 이유 |
|------|------|
| `src/` 수정 | GREEN까지 구현 연기 |
| assert 완화 (`>=`, `in`만으로 pass 통과 등) | 요구사항 희석 |
| `@pytest.mark.skip` / `xfail` | RED 회피 |
| 기존 테스트 삭제·무력화 | 회귀 기준선 파괴 |
| `UnitConverter.py` 등 범위 밖 파일 수정 | SRP·Phase 위반 |

## 수정 허용

- `tests/test_validate_lines.py` (및 필요 시 `tests/` 내 보조 픽스처)
- RED 확인용 `pytest` 실행
