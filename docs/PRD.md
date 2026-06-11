# UnitConverter_XX — PRD (Product Requirements Document)

| 항목 | 내용 |
|------|------|
| **문서** | docs/PRD.md |
| **버전** | 0.1 (초안) |
| **작성일** | 2026-06-11 |
| **상태** | Draft |
| **문제 정의** | `Report/01.UnitConverter_ProblemDefinition_Report.md` |

---

## 1. 개요

### 1.1 제품 한 줄

**길이 단위가 섞인 견적·발주 현장에서, 입력한 치수를 등록된 모든 단위로 정확히 변환·출력하는 CLI 도구.**

### 1.2 배경·문제

수입·국내 자재 견적·발주 시 **feet/yard/inch/m/mm**가 카탈로그·발주서·메모마다 섞여, 수동 환산·교차 확인에 **시간(최대 1시간 20분)** 과 **발주 오류(최대 약 35만 원)** 가 발생한다. (Mom Test 가상 인터뷰 기준선)

**진짜 문제:** 단위 혼재 + 숫자만 옮김 + 반복 환산 → 단위 미확인 시 재발주·공기 손실.

**주제:** 한 발주 건 안에서 치수를 **하나의 기준(m/mm)** 으로 맞춰 **판정**하는 일.

### 1.3 목표 (R-G-I-O)

| | 내용 |
|---|------|
| **Goal** | 견적·발주·발송 판정 전 치수를 m/mm 기준으로 대조 |
| **Outcome** | 다중 치수 빠른 대조, 단위 미확인 발주 없음, 재발주 재발 없음 |

### 1.4 성공 기준 (KPI — v1 검증 목표)

| ID | 기준 | 목표 |
|----|------|------|
| KPI-1 | 단위 혼동 발주 | 숫자만 복사 재발주 **0건** (기준선: 35만 원/건) |
| KPI-2 | 다단위 1건 처리 | **≤ 20분** (기준선: 80분) |
| KPI-3 | 단위 없는 입력 | Invalid 0 또는 단위 선택 **1단계** (기준선: `2.5` 실패) |
| KPI-4 | 연속 처리 | 동일 세션 **2+ 입력** (기준선: 2회 재실행) |
| KPI-5 | 출력 포맷 | **default:** feet·yard **4자리**; **business:** m **2자리**·mm **정수**; 추가 계산 없음 |
| KPI-6 | 기본 3단위 변환 | meter/feet/yard **동시 출력**, README 비율(§3·§6.2) 일치, FR-07 TC **pass** |

**KPI 역할:** KPI-1~4·KPI-5(business)는 Mom Test **업무 결과**; KPI-5(default)·KPI-6는 **기능·정확도** 검증. 상세는 FR-02/03/07, NFR-01, `Report/STEP3_ValidateLines_Report.md` 프로필.

---

## 2. 사용자

### 2.1 Primary Persona

- **소형 가구 공방 실무** — 수입 몰딩·합판 스펙(feet/yard/inch), 국내 발주(m/mm)
- **CLI 실행 가능** (PC 공방·사무실)
- 메모·발주서에 **숫자만** 적는 습관

### 2.2 사용 시나리오

1. **단일 환산:** 카탈로그 `feet:12` → m/feet/yard 동시 확인  
2. **동일 건 다중 환산:** `feet:12` → `yard:2.5` 연속 (재시작 최소화)  
3. **발주서 기록:** m 2자리 또는 mm 정수로 CSV/표 출력  
4. **신규 단위:** `1 cubit = 0.4572 meter` 런타임 등록  

---

## 3. 현재 상태 (As-Is)

`UnitConverter.py` — 프로토타입 수준.

| 기능 | 상태 |
|------|------|
| `unit:value` 입력 | ✅ |
| meter / feet / yard 변환 | ✅ |
| 형식·숫자·unknown unit 검증 | ✅ (부분) |
| inch, mm | ❌ |
| 음수 검증 | ❌ (README 요구) |
| OCP / SRP 구조 | 🔄 (input/entity 분리 진행) |
| 테스트 코드 | 🔄 (FR-01 entity RED 진행) |
| 설정 외부화 | ❌ |
| 동적 단위 등록 | ❌ |
| JSON / CSV / 표 출력 | ❌ |
| 연속 입력 (루프) | ❌ |

**변환 비율 (현재 하드코딩)**

- `1 meter = 3.28084 feet`
- `1 meter = 1.09361 yard`

---

## 4. 요구사항

### 4.1 Must Have (P0) — README 기본·품질

| ID | 요구사항 | 상세 | KPI |
|----|----------|------|-----|
| FR-01 | 단위:값 입력 | `meter:2.5` 형식; 오류 시 명확한 메시지 | KPI-3 |
| FR-02 | 등록 단위 전량 출력 | 입력 단위 → **모든** 등록 단위 변환 출력 | KPI-2, KPI-6 |
| FR-03 | meter 기준 변환 | feet/yard 비율은 meter 기준 계산 | KPI-6 |
| FR-04 | 입력 검증 | 음수, 잘못된 형식, 없는 단위 | KPI-3 |
| FR-05 | OCP | 새 단위 추가 시 기존 코드 변경 최소 | — |
| FR-06 | SRP | 변환·입력·출력 책임 분리 | — |
| FR-07 | 테스트 | 단위 변환 정확도 + 입력 검증 TC | KPI-6 |

**FR-02 출력 예 (README)**

```
입력: meter:2.5
2.5 meter = 8.2 feet
2.5 meter = 2.7 yard
…
```

#### FR-01 테스트 계획 (entity · Logic Track)

FR-01 `unit:value` 파싱을 **entity 레이어** `parse_unit_value_coords`로 분리하고, TDD RED→GREEN으로 검증한다.  
Layer: **entity** · Track: **Logic** (Domain Mock·I/O emit 금지).

**목표 API** (`src/input/entity/d_loc_01.py`)

```python
def parse_unit_value_coords(raw: str) -> dict:
    # {"status": "ok"|"invalid", "unit": str|None, "value": float|None, "errors": list[str]}
```

**C2C 추적**

| Rule | 적용 |
|------|------|
| Rule 1 — Requirement Trace | Test ID `D-LOC-01-00n` → FR-01 + NFR-05 |
| Rule 2 — Observable Contract | 공개 반환 dict만 Assert |
| Rule 3 — Fail for Right Reason | skip/xfail·assert 완화 금지 |

**Track B (D-*) RED 설계**

| Test ID | 대상 함수 | Given → Then | Invariant | TDD 상태 |
|---------|-----------|--------------|-----------|----------|
| D-LOC-01-001 | `parse_unit_value_coords` | `"meter:"` → invalid, `Invalid number: ` | 순수 함수; invalid ⇒ errors ≥ 1 | **GREEN** |
| D-LOC-01-002 | 동일 | `"meter:2.5"` → ok, unit/value 일치 | ok ⇒ unit 비공백 & value 유한 float | **RED** |
| D-LOC-01-003 | 동일 | `"2.5"` → invalid, `Invalid format…` | 콜론 없으면 ok 불가 | **RED** |

**Given / When / Then**

| Test ID | Given | When | Then |
|---------|-------|------|------|
| D-LOC-01-001 | raw `"meter:"` | `parse_unit_value_coords(raw)` | `status=="invalid"`, `errors`에 blank value 관련 ≥1 |
| D-LOC-01-002 | fixture `g1_valid_input` = `"meter:2.5"` | `parse_unit_value_coords(g1_valid_input)` | `status=="ok"`, `unit=="meter"`, `value==2.5`, `errors==[]` |
| D-LOC-01-003 | raw `"2.5"` | `parse_unit_value_coords(raw)` | `status=="invalid"`, `errors`에 format 관련 ≥1 |

**테스트 파일**

| 항목 | 경로 |
|------|------|
| 테스트 | `tests/entity/test_d_loc_01.py` |
| 픽스처 | `tests/entity/conftest.py` — `g1_valid_input` (`"meter:2.5"`, 로직 없음) |

**pytest**

```bash
python -m pytest tests/entity/test_d_loc_01.py -v
python -m pytest tests/entity/test_d_loc_01.py::test_d_loc_01_blank_coords_row_major -v
```

**판단 (To-Do 확정):** 1순위 RED는 blank value `"meter:"`(D-LOC-01-001). blank unit `":2.5"`는 후속 RED로 연기.

### 4.2 Should Have (P1) — README 추가 + Mom Test Gap

| ID | 요구사항 | 상세 | KPI |
|----|----------|------|-----|
| FR-08 | 설정 외부화 | JSON/YAML에서 변환 비율 로드 | — |
| FR-09 | 동적 단위 등록 | `1 cubit = 0.4572 meter` 입력 등록·사용 | — |
| FR-10 | 출력 포맷 | JSON / CSV / 표(table) 선택 | KPI-5 |
| FR-11 | 연속 입력 | 동일 실행에서 **다중** `unit:value` (quit까지) | KPI-4 |
| FR-12 | 출력 정밀도 | m **소수 2자리**, mm **정수** 옵션 | KPI-5 |

### 4.3 Could Have (P2) — 문제 정의 연계

| ID | 요구사항 | 상세 | KPI |
|----|----------|------|-----|
| FR-13 | inch / mm 단위 | 설정 또는 기본 단위 집합 확장 | KPI-2, KPI-5 |
| FR-14 | bare number 처리 | `2.5` 입력 시 **단위 선택 프롬프트** (1단계) | KPI-3 |
| FR-15 | 배치 파일 | 한 줄에 `feet:12;yard:2.5` 또는 CSV in | KPI-4 |

### 4.4 Won't Have (v0.1)

- GUI / PyQt
- 클라우드·API
- 택배사 규정 자동 연동
- 실 사용자 3개월 파일럿 (문서화만)

---

## 5. 비기능 요구사항 (NFR)

| ID | 항목 | 기준 |
|----|------|------|
| NFR-01 | 정확도 | README 비율; TC로 회귀 검증 (KPI-6) |
| NFR-02 | 실행 환경 | Python 3.x, venv, `python UnitConverter.py` |
| NFR-03 | 확장성 | OCP — 단위·포맷 플러그인 방식 추가 |
| NFR-04 | 유지보수 | SRP — 클래스·모듈 분리 |
| NFR-05 | 오류 메시지 | `Invalid format`, `Invalid number`, `Unknown unit` 유지·개선 |

---

## 6. 데이터·인터페이스

### 6.1 CLI 입력

| 패턴 | 예 | 처리 |
|------|-----|------|
| 단위:값 | `meter:2.5` | 변환 |
| 값만 (P2) | `2.5` | 단위 선택 후 변환 |
| 등록 (P1) | `register 1 cubit = 0.4572 meter` | 단위 추가 |
| 종료 | `quit` / `exit` | 연속 모드 종료 |

### 6.2 설정 파일 (FR-08) — 초안 스키마

```json
{
  "base_unit": "meter",
  "units": {
    "meter": 1,
    "feet": 3.28084,
    "yard": 1.09361
  },
  "display": {
    "meter_decimals": 2,
    "include_mm": true
  }
}
```

### 6.3 출력 (FR-10)

- **text (default):** `{value} {unit} = {result} {target_unit}`
- **json:** `{ "input": {...}, "conversions": [...] }`
- **csv:** `source_unit,source_value,target_unit,target_value`
- **table:** 고정폭 또는 markdown 표

---

## 7. 아키텍처 방향 (초안)

```
UnitConverter.py (entry)
├── input/              # 파싱·검증 (SRP)
│   └── entity/
│       └── d_loc_01.py # parse_unit_value_coords (FR-01)
├── registry/           # 단위 등록·설정 로드 (OCP)
├── conversion/         # meter 기준 변환
├── output/             # text | json | csv | table (OCP)
└── tests/
    └── entity/         # FR-01 entity TC (D-LOC-01)
```

README 품질 요구(OCP/SRP)와 추가 요구(설정·동적 등록·포맷)를 **역할별 패키지**로 분리.

---

## 8. 릴리스 계획 (초안)

| 단계 | 범위 | FR |
|------|------|-----|
| **M1** | 리팩토링 + P0 + TC | FR-01~07 |
| **M2** | 설정·동적 등록·포맷·연속 입력 | FR-08~12 |
| **M3** | inch/mm·bare number (선택) | FR-13~15 |

---

## 9. 리스크·가정

| 구분 | 내용 |
|------|------|
| **가정** | Mom Test 페르소나·수치는 **가상**; KPI는 실습·내부 검증용 |
| **리스크** | CLI·`unit:value`만으로 KPI-3 완전 충족 어려움 → FR-14 필요 |
| **리스크** | inch/mm 없이 KPI-2(20분) 달성 제한 |
| **의존** | `Report/01.UnitConverter_ProblemDefinition_Report.md` 갱신 시 PRD KPI 재검토 |

---

## 10. 참고 문서

| 문서 | 경로 |
|------|------|
| 문제 정의 | `Report/01.UnitConverter_ProblemDefinition_Report.md` |
| Mom Test | `Report/STEP1_MomTest_Report.md` |
| R-G-I-O | `Report/STEP2_RGIO_Report.md` |
| 실습 README | `README.md` |
| 현재 코드 | `UnitConverter.py` |
