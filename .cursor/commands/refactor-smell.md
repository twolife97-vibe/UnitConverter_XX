# REFACTOR Smell — UnitConverter_XX ARRR

`src/`의 **코드 스멜만** 식별·목록화한다. **리팩터링 코드 변경은 하지 않는다.**

## SSOT

| 문서 | 용도 |
|------|------|
| `.cursorrules` | SRP · OCP · REFACTOR Phase |
| `docs/PRD.md` | §7 아키텍처 · FR-05/06 |
| `Report/STEP3_ValidateLines_Report.md` | 출력/검증 역할 분리 |

## Phase 선언 (필수)

응답 **첫 줄**:

```
REFACTOR — UnitConverter: smell audit (<n>건)
```

## 자동 절차 (/refactor-smell 단독 입력 시)

**질문 없이** 즉시 실행.

1. `python -m pytest tests/ -q` — **전부 pass** 확인 (실패 시 smell audit 중단 → `/green-minimal` 권고)
2. 분석 대상 읽기:
   - `src/validate_lines.py`
   - `src/registry/` · `src/conversion/`
   - `src/output/text.py` · `src/session/continuous.py`
   - `src/input/entity/d_loc_01.py`
3. 아래 **스멜 체크리스트**로 smell 목록 작성 (코드 변경 **0**)
4. 각 smell에 **S#** · 심각도 · `/refactor-safe` 후보 여부 표시
5. 보고 템플릿 응답

## 스멜 체크리스트 (UnitConverter)

| # | 스멜 | 징후 |
|---|------|------|
| S1 | **God module** | `validate_lines.py`에 파싱·변환·포맷·세션 검증 혼재 |
| S2 | **Duplicated conversion** | `UnitConverter.py`와 `conversion/meter` 비율 중복 |
| S3 | **Magic number** | 3.28084 · 1.09361이 registry 밖 하드코딩 |
| S4 | **Dead stub** | `NotImplementedError` 스텁과 실제 호출 경로 불일치 |
| S5 | **Leaky KPI** | validate_lines가 입력 Invalid·시간 KPI 검증 시도 |
| S6 | **Profile scatter** | 자릿수·타깃 규칙이 registry 외 파일에 분산 |
| S7 | **Long function** | `_collect_errors` 등 40줄+ 단일 함수 |
| S8 | **CLI coupling** | `UnitConverter.py`가 변환·출력·검증 미분리 (FR-06) |

## 심각도

| 등급 | 기준 |
|------|------|
| 높음 | KPI·계약 위반 위험 · 중복 비율 |
| 중간 | SRP/OCP 위반 · 유지보수 비용 |
| 낮음 | 명명·구조 미세 개선 |

## 보고 템플릿

```
REFACTOR — UnitConverter: smell audit (<n>건)

pytest: <N> passed (선행 조건)

| S# | 스멜 | 위치 | KPI/FR | 심각도 | safe 후보 |
|----|------|------|--------|--------|-----------|
| S1 | … | validate_lines.py L… | FR-06 | 높음 | ✅ |

권장 순서: S<n> → S<n> (동작 변경 없음 전제)

다음: /refactor-safe — S<최우선#>
```

## 금지

| 금지 | 이유 |
|------|------|
| `src/` · `tests/` 수정 | smell audit만 |
| pytest 실패 상태에서 audit | 기준선 없음 |
| 사용자 질문 | 슬래시 단독 |
| git commit/push | `.cursorrules` |
