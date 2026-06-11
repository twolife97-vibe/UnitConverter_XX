# REFACTOR Safe — UnitConverter_XX ARRR

`/refactor-smell`에서 식별한 smell **1건**을 **동작 변경 없이** 안전하게 제거한다.

## SSOT

| 문서 | 용도 |
|------|------|
| `.cursorrules` | REFACTOR Phase · 테스트 불변 |
| `docs/PRD.md` | §7 패키지 역할 |
| `Report/STEP3_ValidateLines_Report.md` | API·계약 |

## Phase 선언 (필수)

응답 **첫 줄**:

```
REFACTOR — UnitConverter: safe (<S#> — <한 줄>)
```

## 자동 절차 (/refactor-safe 단독 입력 시)

**질문 없이** 즉시 실행.

1. `python -m pytest tests/ -q` — **전부 pass** 확인 (실패 시 중단 → `/green-minimal`)
2. `src/` 읽고 **S-next** 자동 선택:
   - 직전 `/refactor-smell` 보고가 있으면 → **safe 후보 ✅ 중 심각도 최상위 S#**
   - 없으면 → **S3 Magic number** (registry 밖 하드코딩) 우선, 없으면 **S6 Profile scatter**
3. **한 smell · 한 diff** — extract/rename/move만 (로직·API·assert 불변)
4. `pytest tests/ -q` 회귀
5. 보고 템플릿

## S# → 안전 리팩터 패턴 (고정)

| S# | 허용 작업 | 금지 |
|----|-----------|------|
| S1 God module | private helper extract (`_parse_*`, `_check_*`) | public API 시그니처 변경 |
| S2 Duplicated conversion | `UnitConverter.py` → `conversion/meter` import (별도 STEP이면 건너뜀) | CLI 동작 변경 |
| S3 Magic number | literal → `registry/units.RATIOS_TO_METER` import | 비율 값 변경 |
| S4 Dead stub | 미사용 import·dead code 제거 | 스텁 시그니처 변경 |
| S5 Leaky KPI | validate_lines에서 입력 검증 코드 **제거** (있다면) | 출력 검증 규칙 변경 |
| S6 Profile scatter | 자릿수 상수 → `registry/profiles` 집중 | 프로필 의미 변경 |
| S7 Long function | 10~20줄 단위 extract | 분기·에러 메시지 변경 |
| S8 CLI coupling | (M1 이후) `output/text` 위임 | 이번 REFACTOR에서 CLI 대규모 수정 |

**S-next 기본:** S3 → S6 → S7 → S1 (프로젝트에 해당 smell이 없으면 다음으로).

## REFACTOR 원칙

| 원칙 | 설명 |
|------|------|
| 테스트 불변 | `tests/` **수정 금지** |
| API 불변 | `validate_lines` · `parse_unit_value_coords` 공개 dict 계약 |
| 최소 diff | smell 1건 = 커밋 1개 분량 |
| KPI | REFACTOR 후에도 KPI-3~6 TC pass |

## pytest (필수)

```bash
python -m pytest tests/ -q
```

실패 시 **즉시 revert**하고 보고에 rollback 명시.

## 보고 템플릿

```
REFACTOR — UnitConverter: safe (S<n> — <요약>)

변경: src/<파일> — <extract|import|move 한 줄>
제거 smell: S<n>
회귀: pytest tests/ -q → <N> passed

다음: /refactor-smell (잔여) 또는 /red-skeleton (다음 KPI)
```

## 금지

| 금지 | 이유 |
|------|------|
| `tests/` 수정 | REFACTOR 범위 |
| 동작·계약 변경 | safe 아님 |
| smell 2건 이상 동시 | 한 사이클 1건 |
| 사용자 질문 | 슬래시 단독 |
| git commit/push | `.cursorrules` |

## 수정 허용

- `src/` — 구조 정리 (동작 동일)
- 회귀 pytest 실행
