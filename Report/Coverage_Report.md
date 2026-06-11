# UnitConverter_XX — Coverage Report

**일자:** 2026-06-11  
**명령:** `python -m pytest tests/ --cov=src --cov-report=term-missing --cov-report=json`  
**테스트:** 16 passed  
**전체 커버리지:** **90%** (148 / 164 statements)

---

## 1. 요약

| 항목 | 값 | 이전 |
|------|-----|------|
| 대상 | `src/` | — |
| pytest | 16 passed | 9 passed |
| Statements | 164 | 151 |
| Covered | 148 | 126 |
| Missing | 16 | 25 |
| **Total** | **90%** | 83% |

---

## 2. 모듈별 커버리지

| 모듈 | Stmts | Miss | Cover | KPI |
|------|-------|------|-------|-----|
| `src/conversion/meter.py` | 13 | 0 | **100%** | KPI-6 |
| `src/registry/units.py` | 3 | 0 | **100%** | KPI-6 |
| `src/registry/profiles.py` | 6 | 0 | **100%** | KPI-5/6 |
| `src/output/text.py` | 6 | 0 | **100%** | KPI-5/6 |
| `src/input/entity/d_loc_01.py` | 11 | 0 | **100%** | KPI-3 |
| `src/session/continuous.py` | 13 | 1 | **92%** | KPI-4 |
| `src/validate_lines.py` | 101 | 15 | **85%** | KPI-4/5 |
| `__init__.py` 등 | 11 | 0 | **100%** | — |

---

## 3. 미커버 상세

### 3.1 `src/session/continuous.py` — 92% (KPI-4)

| 라인 | 분기 | 후속 |
|------|------|------|
| 21 | `convert_fn is None` → `continue` | convert_fn 미주입 TC |

### 3.2 `src/validate_lines.py` — 85% (KPI-5 fail 분기)

| 라인 | 분기 | 후속 RED |
|------|------|----------|
| 61 | `parse_line` — empty line | 빈 줄 incomplete |
| 68-69 | `parse_line` — invalid number | 숫자 파싱 fail |
| 92 | 빈 줄 skip | whitespace-only |
| 104, 106 | source value/unit mismatch | 옵션 override fail |
| 116, 121, 123, 125 | echo·unsupported·same unit | F2/F3/F4 위반 |
| 133, 139, 143, 151 | conversion mismatch / duplicate / extra | fail |
| 195 | `validate_session` min_groups 미달 | session incomplete |

> `test_kpi5_invalid_format_fail` 추가로 fail 분기 일부 커버됨 (이전 80% → 85%).

---

## 4. KPI ↔ 커버리지

| KPI | Track | Cover | 상태 |
|-----|-------|-------|------|
| KPI-3 | `input/entity` | 100% | ✅ |
| KPI-4 | `session/` + `validate_session` | 92% / 86% | ✅ 구현·TC |
| KPI-5 | `output/` + validate fail | 100% / 85%* | ✅ fail TC 1건 |
| KPI-6 | `registry` + `conversion` + `output` + FR-07 통합 | 100% | ✅ |
| KPI-1·2 | — | — | 실무/E2E (범위 밖) |

\* `_collect_errors` fail/incomplete 분기 85%

---

## 5. 산출물

| 파일 | 설명 |
|------|------|
| `coverage.json` | pytest-cov JSON (루트) |
| `Report/Coverage_Report.md` | 본 문서 |

```bash
python -m pytest tests/ --cov=src --cov-report=term-missing
```

> HTML 리포트(`htmlcov/`)는 coverage 패키지 정적 파일 오류로 생성 실패 (환경 이슈).

---

## 6. 다음 권장 (커버리지 Gap)

1. `/red-skeleton` — `validate_session` min_groups 미달 (L195)
2. `/red-skeleton` — validate_lines empty line / invalid number
3. `/refactor-smell` — `UnitConverter.py` vs `src/` 중복 (S2)
