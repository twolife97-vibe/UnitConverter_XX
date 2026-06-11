# UnitConverter_XX — STEP 3 validate_lines 계약 보고서

**일자:** 2026-06-11  
**입력:** `STEP2_RGIO_Report.md` (R-G-I-O · 성공 기준) + 기본 CLI 출력 형식  
**구현:** `validate_lines.py` (프로젝트 루트)

---

## 1. 목적

STEP 2 R-G-I-O·성공 기준에서 **구현·TC로 내릴 수 있는 출력 요구**를 코드 계약으로 고정한다.

| 역할 | 설명 |
|------|------|
| **합의의 코드화** | “변환 결과가 이렇게 나와야 한다”를 함수 규칙으로 명시 |
| **SRP** | 출력 생성(`output/`)과 검증(`validate_lines`) 분리 |
| **TC 기준선** | Activity 3 — `assert validate_lines(out) == []` |
| **리팩터 안전망** | OCP/SRP 리팩터 후에도 출력 형태 회귀 검출 |

---

## 2. 계약 요약

### 2.1 출력 줄 형식

```
{입력값} {입력단위} = {변환값} {대상단위}
```

- 좌측은 모든 줄에서 **입력 에코** 동일
- 대상 단위는 **입력 단위와 달라야** 함 (소스 단위 줄 금지)
- 중복 대상 단위 금지

### 2.2 지원 단위 (meter 기준)

| 단위 | 비율 (per 1 meter) |
|------|-------------------|
| meter | 1 |
| feet | 3.28084 |
| yard | 1.09361 |
| inch | 39.37007874015748 |
| mm | 1000 |

### 2.3 프로필

| 프로필 | 용도 | 기대 타깃 | 자릿수 |
|--------|------|-----------|--------|
| **default** | 기본 CLI 스냅샷 (이미지 계약) | feet, yard | 전 단위 4자리 |
| **business** | STEP2 성공 #5 · 발주·재단 출력 | 소스 제외 전 단위 | meter **2**, mm **0(정수)**, 그 외 4 |

**business 예 (`meter:2.5`):**

```
2.5 meter = 8.2021 feet
2.5 meter = 2.7340 yard
2.5 meter = 98.4252 inch
2.5 meter = 2500 mm
```

### 2.4 API

| 함수 | 설명 |
|------|------|
| `parse_line(line)` | 한 줄 파싱 |
| `format_converted(value, unit, profile)` | 프로필별 기대 문자열 |
| `validate_lines(lines, *, profile, ...)` | 출력 묶음 검증 → 위반 메시지 목록 |
| `validate_session(output_groups, *, min_groups=2, ...)` | 성공 #4 — 동일 건 2+ 변환 검증 |

---

## 3. STEP 2 R-G-I-O · 성공 기준과의 대응

| STEP2 | validate_lines 대응 | 상태 |
|-------|----------------------|------|
| **R** — inch / m·mm 혼재 | inch, mm 단위·출력 줄 | ✅ business |
| **G** — m 또는 mm 기준 | meter 2자리, mm 정수 출력 | ✅ business |
| **G** — 맞다/틀리다/초과 판정 | (범위 밖) 판정 레이어 | ❌ 별도 |
| **I** — inch Unknown, mm 후처리 | inch/mm 타깃 포함 | ✅ business |
| **O** — 한 건 다중 치수 대조 | `validate_session` 2+ 묶음 | ✅ |
| **#3** — bare number `2.5` | (범위 밖) 입력 검증기 | ❌ 별도 |
| **#4** — 연속 처리 | `validate_session` | ✅ |
| **#5** — m 2자리 / mm 정수 | `profile="business"` | ✅ |
| **#1, #2** — 재발주 0건, ≤20분 | (범위 밖) 업무 KPI | ❌ 별도 |

---

## 4. Gap (계약 밖 — 의도적 분리)

다음은 `validate_lines`가 **담당하지 않는다.**

| 항목 | 이유 | 후속 |
|------|------|------|
| #1 단위 혼동 발주 0건 | 실무·파일럿 KPI | Mom Test 기준선 문서화만 |
| #2 다단위 1건 ≤20분 | 시간 측정 | E2E·사용성 테스트 |
| #3 `2.5` Invalid / 단위 선택 | **입력** 계약 | `input/` 검증 모듈 |
| G 판정 (맞다/틀리다/초과) | 비즈니스 로직 | 판정 레이어 |

---

## 5. 현재 구현 vs 계약

| 항목 | `UnitConverter.py` (As-Is) | `validate_lines` business |
|------|---------------------------|---------------------------|
| 출력 줄 수 | 3 (meter 포함) | 4 (소스 제외 전 타깃) |
| inch / mm | 미지원 | 기대 타깃 |
| meter 자릿수 | raw float | 2자리 |
| mm | 없음 | 정수 줄 필수 |
| 연속 입력 | 1실행 1입력 | `validate_session` 별도 |

→ **다음 구현 단계:** `output/` + `profile="business"` 출력 생성, pytest TC 연결.

---

## 6. STEP 2 → STEP 3 연결

| STEP 2 | STEP 3 (validate_lines) |
|--------|-------------------------|
| 성공 #5 업무 출력 | `profile="business"` |
| Issue inch/mm gap | inch·mm 타깃·비율 |
| 성공 #4 연속 처리 | `validate_session` |
| R-G-I-O 전체 KPI | 출력 계약만 커버 (§4 Gap 참고) |

---

## 7. 관련 문서

| 파일 | 내용 |
|------|------|
| `STEP2_RGIO_Report.md` | R-G-I-O · 성공 기준 |
| `validate_lines.py` | 계약 구현 |
| `docs/PRD.md` | FR-04, FR-12, KPI-4·5 |
| `Prompt/STEP3_ValidateLines_Prompt.md` | 계약 생성·리뷰 프롬프트 |
| `Prompt/STEP3_ValidateLines_Grading_Prompt.md` | 정합 리뷰 채점 프롬프트 |
