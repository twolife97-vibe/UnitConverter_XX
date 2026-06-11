# GREEN Minimal — UnitConverter_XX ARRR

현재 **실패 중인** 테스트 **1건**을 통과시키는 **최소** 구현만 `src/`에 추가한다.

## SSOT

| 문서 | 용도 |
|------|------|
| `.cursorrules` | GREEN Phase · 최소 diff |
| `docs/PRD.md` | KPI · 비율 · 프로필 |
| `Report/STEP3_ValidateLines_Report.md` | 출력 형식 · F1~F7 |

## Phase 선언 (필수)

응답 **첫 줄**:

```
GREEN — UnitConverter: minimal (<통과시킨 테스트 함수명>)
```

## 자동 절차 (/green-minimal 단독 입력 시)

**질문 없이** 즉시 실행.

1. `python -m pytest tests/ -q --tb=no` 실행 → **첫 실패 테스트** 1건 식별
2. 실패 없으면 → `NotImplementedError`를 raise하는 `src/` 함수(`output/text` · `session/continuous`) 중 **KPI 우선순위 높은 1건**에 대응 RED가 있는지 확인; 없으면 `/red-skeleton` 권고만 하고 종료
3. 해당 테스트만 통과하도록 **`src/` 최소** 수정
4. `pytest tests/ -q` 전체 회귀 확인
5. 보고 템플릿 응답

## 대상 API (Track별 최소 구현 가이드)

### `src/output/text.py` — `convert_to_lines` (KPI-5/6)

- `src/registry/units.py` · `src/conversion/meter.py` 재사용
- `DEFAULT_TARGETS[profile] - {unit}` 타깃만 출력
- 형식: `{value} {unit} = {formatted} {target}` (`docs/PRD.md` §6.3)
- **hardcode 2.5 meter만 pass** 허용 (T-next 1건 최소 GREEN)

### `src/session/continuous.py` — `run_continuous` (KPI-4)

- 테스트에서 주입한 `convert_fn` 또는 monkeypatch stdin으로 **2회 입력** 시뮬
- `list[list[str]]` 반환 — **테스트가 요구하는 최소**만

### `src/validate_lines.py` (KPI-5 fail)

- 이미 구현된 경우: 실패 원인이 테스트 오류면 **tests/ 수정 금지** — 구현 버그만 수정
- dict API `{status, failed_lines}` 유지

### `src/input/entity/d_loc_01.py` (KPI-3)

- `parse_unit_value_coords` — blank unit `":2.5"` invalid 처리 **최소**

## GREEN 원칙

| 원칙 | 설명 |
|------|------|
| 최소 | 통과 테스트 1개만 목표; 일반화는 `/golden-master` |
| 회귀 | `pytest tests/ -q` **전부** pass |
| SRP | 변환 로직은 `conversion/` · 비율은 `registry/` |
| diff | 요청 밖 파일·주석·리팩터 금지 |

## pytest

```bash
python -m pytest tests/ -q
```

## 보고 템플릿

```
GREEN — UnitConverter: minimal (<함수명>)

변경: src/<모듈> — <한 줄 요약>
통과: tests/<파일> :: <함수명>
회귀: pytest tests/ -q → <N> passed

다음: /red-skeleton (다음 KPI) 또는 /golden-master (일반화)
```

## 금지 (GREEN)

| 금지 | 이유 |
|------|------|
| 테스트 삭제·assert 완화 | 요구 희석 |
| `UnitConverter.py` CLI 연동 | 별도 STEP |
| 사용자 질문 | 슬래시 단독 |
| git commit/push | `.cursorrules` |
| REFACTOR성 대규모 이동 | `/refactor-safe` |

## 수정 허용

- `src/` — 실패 테스트 통과에 필요한 최소
- GREEN 확인용 pytest 실행
