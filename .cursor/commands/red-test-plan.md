# RED Test Plan — UnitConverter_XX ARRR

**PRD §1.4 KPI**·`validate_lines` 계약·entity(FR-01)에 대한 **테스트 계획만** 작성한다.  
코드·테스트 파일·pytest 실행·git 작업은 **하지 않는다**.

## SSOT (필독 — 추가 질문 금지)

| 문서 | 용도 |
|------|------|
| `.cursorrules` | TDD Phase·validate_lines API·수정 범위 |
| `docs/PRD.md` | KPI-1~6 · FR · NFR · 아키텍처 |
| `Report/STEP3_ValidateLines_Report.md` | 출력 줄 계약 F1~F7 · 프로필 |

## Phase 선언 (필수)

응답 **첫 줄**:

```
RED — UnitConverter: test plan (<한 줄 요약>)
```

## 자동 절차 (/red-test-plan 단독 입력 시)

사용자에게 **질문하지 않는다**. 아래 순서를 즉시 실행한다.

1. **SSOT 읽기** — 위 3문서 + `tests/test_validate_lines.py` · `tests/entity/test_d_loc_01.py` · `src/output/text.py` · `src/session/continuous.py` 현황 파악
2. **백로그 산출** — PRD §1.4 KPI별 미커버·`NotImplementedError` 스텁·pytest 미존재 항목을 표로 정리
3. **다음 RED 1건 지정** — 백로그 최상위 1건만 `T-next`로 명명 (Track · KPI · Given/When/Then)
4. **계획 출력** — 아래 §보고 템플릿으로 **채팅만** 응답 (파일 저장·코드 수정 금지)

## 백로그 우선순위 (SSOT 고정)

| # | Track | 대상 | KPI | RED 후보 |
|---|-------|------|-----|----------|
| 1 | `output/` | `convert_to_lines` default | KPI-6 | `meter:2.5` → feet·yard 2줄 |
| 2 | `output/` | `convert_to_lines` business | KPI-5 | `meter:2.5` → 4타깃 줄 |
| 3 | `session/` | `run_continuous` | KPI-4 | 2+ 입력 묶음 반환 |
| 4 | `validate_lines` | fail 케이스 | KPI-5 | 형식 위반 → `status: fail` |
| 5 | `validate_lines` | incomplete 케이스 | KPI-5 | business 타깃 누락 (이미 있으면 skip) |
| 6 | `entity/` | `parse_unit_value_coords` | KPI-3 | blank unit `":2.5"` (PRD 후순위) |

**선택 규칙:** 위에서 **아직 TC가 없거나** `NotImplementedError`인 **첫 행**을 `T-next`로 채택.  
이미 전부 GREEN이면 `T-next: validate_lines fail — invalid format`을 기본으로 한다.

## API 계약 (계획에 반드시 인용)

**validate_lines** (`.cursorrules`)

```python
result = validate_lines(lines, profile="default" | "business", ...)
# {"status": "pass" | "fail" | "incomplete", "failed_lines": [...]}
```

**parse_unit_value_coords** (`docs/PRD.md` FR-01)

```python
# {"status": "ok"|"invalid", "unit": str|None, "value": float|None, "errors": list[str]}
```

**convert_to_lines** (`src/output/text.py` — GREEN 대상)

```python
# list[str] — "{value} {unit} = {result} {target_unit}" 줄 목록
```

## KPI ↔ Track 매핑 (계획 표에 포함)

| KPI | 코드 Track | validate_lines 범위 |
|-----|-----------|---------------------|
| KPI-3 | `tests/entity/` | ❌ 입력 계약 |
| KPI-4 | `session/` · `validate_session` | ✅ 출력 묶음 2+ |
| KPI-5 | `output/` · `validate_lines(profile=…)` | ✅ default/business |
| KPI-6 | `registry/` · `conversion/` · default TC | ✅ 3단위·비율 |
| KPI-1·2 | — | ❌ 실무/E2E |

## 보고 템플릿 (채팅 출력)

```
RED — UnitConverter: test plan (<T-next 요약>)

## 백로그 (PRD §1.4)
| # | Track | KPI | 상태 | RED 필요 |
|---|-------|-----|------|----------|
| … | … | … | GREEN/RED/스텁 | … |

## T-next (다음 RED 1건)
- Track: <output|session|validate_lines|entity>
- KPI: <KPI-n>
- Test ID: <제안 함수명>
- Given: <입력·출력 줄 요약>
- When: <호출 API>
- Then: <status·failed_lines 또는 dict/status>
- Invariant: <계약 F# 또는 FR#>

## AAA 초안
Arrange: …
Act: …
Assert: …

## 금지 (RED 전)
- src/ 수정 · assert 완화 · skip/xfail

다음: /red-skeleton
```

## 금지

| 금지 | 이유 |
|------|------|
| 사용자 추가 질문 | 슬래시 단독 실행 |
| `src/` · `tests/` 수정 | test-plan 범위 |
| pytest 실행 | 계획만 |
| git commit/push | `.cursorrules` |
