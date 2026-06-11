# UnitConverter_XX — STEP 3 Harness · Cursor 워크플로 설정 보고서

**일자:** 2026-06-11  
**입력:** `Report/STEP3_ValidateLines_Report.md` (출력 계약) · 기존 루트 `validate_lines.py`  
**산출:** pytest Harness · `.cursorrules` · Cursor 슬래시 커맨드 2종

---

## 1. 목적

STEP 3 `validate_lines` TDD를 시작하기 전에 **테스트 골격(Harness)** 과 **AI·Cursor 워크플로 규칙**을 고정한다.  
구현·테스트 본문은 아직 작성하지 않고, RED→GREEN→REFACTOR 사이클을 안전하게 돌릴 인프라만 마련한다.

---

## 2. 요약

| 항목 | 내용 |
|------|------|
| 패키지 레이아웃 | `src/`(구현) · `tests/`(pytest) |
| pytest 설정 | `pyproject.toml` — `pythonpath = ["."]`, `testpaths = ["tests"]` |
| import 규칙 | `from src.validate_lines import validate_lines` |
| 목표 API | `{"status": "pass"\|"fail"\|"incomplete", "failed_lines": [...]}` |
| TDD 규칙 | `.cursorrules` — RED는 `tests/`만, assert 완화·skip·xfail 금지 |
| Cursor 커맨드 | `tdd-red`(RED 전용) · `export-report`(Report/Prompt 저장) |
| Harness 검증 | `pytest -q` → 테스트 0개, import/collection 에러 없음 (exit 5) |

---

## 3. 상세

### 3.1 pytest Harness

프로젝트 루트에 `pyproject.toml`을 두고 pytest만 설정한다.

```toml
[project]
name = "unitconverter_xx"
version = "0.1.0"

[tool.pytest.ini_options]
pythonpath = ["."]
testpaths = ["tests"]
```

**핵심:** `pythonpath = ["."]` 가 있어야 `from src.validate_lines import ...` 가 동작한다.  
초기 `pythonpath = ["src"]` 설정은 기대 스펙과 불일치하여 수정함.

| 경로 | 역할 |
|------|------|
| `src/__init__.py` | 빈 패키지 마커 |
| `src/validate_lines.py` | 루트 `validate_lines.py` 이동 (기존 구현 유지) |
| `tests/__init__.py` | 빈 패키지 마커 |
| `tests/test_validate_lines.py` | import 한 줄만 (`validate_lines`) |

### 3.2 Harness 체크포인트

```bash
pytest -q
# no tests ran in 0.03s  (exit code 5 — 수집 0건, 설정 오류 아님)
```

```bash
python -c "from src.validate_lines import validate_lines; print('ok')"
# ok
```

### 3.3 `.cursorrules` (55줄)

프로젝트 전역 AI 규칙:

- **API 목표:** `validate_lines` → dict 반환 (`status`, `failed_lines`)
- **TDD:** RED→GREEN→REFACTOR, Phase별 수정 허용 범위 표
- **AI:** 한국어, TDD 시 첫 줄 Phase 선언, 최소 diff
- **Git:** 사용자 요청 시에만 commit/push

### 3.4 Cursor 슬래시 커맨드

| 커맨드 | 경로 | 용도 |
|--------|------|------|
| `/tdd-red` | `.cursor/commands/tdd-red.md` | validate_lines RED — `tests/`만, AAA·pytest 예시·금지 사항 |
| `/export-report` | `.cursor/commands/export-report.md` | 세션 산출물 → `Report/` + `Prompt/` 저장 |

---

## 4. 변경·산출물

| 경로 | 변경 |
|------|------|
| `pyproject.toml` | 신규 — `[project]` + `[tool.pytest.ini_options]` |
| `src/__init__.py` | 신규 — 빈 파일 |
| `src/validate_lines.py` | 신규 — 루트에서 이동 |
| `tests/__init__.py` | 신규 — 빈 파일 |
| `tests/test_validate_lines.py` | 신규 — `from src.validate_lines import validate_lines` |
| `validate_lines.py` (루트) | 삭제 — `src/`로 이전 |
| `.cursorrules` | 신규 — TDD·API·AI·Git 규칙 |
| `.cursor/commands/tdd-red.md` | 신규 — RED Phase 전용 |
| `.cursor/commands/export-report.md` | 신규 — Report/Prompt export |

---

## 5. Gap · 다음 단계

| 항목 | 상태 | 후속 |
|------|------|------|
| 목표 API (`dict` 반환) | ❌ | As-Is는 `list[str]` — GREEN에서 전환 |
| 테스트 함수 | ❌ | `/tdd-red`로 RED 첫 테스트 추가 |
| `validate_session` TC | ❌ | business 프로필·성공 #4 연계 RED |
| `UnitConverter.py` 연동 | ❌ | 별도 STEP (output/ 모듈) |
| GREEN / REFACTOR 커맨드 | ❌ | 필요 시 `.cursor/commands/` 추가 |

**다음 권장:** `/tdd-red` — `business` 프로필 meter 2.5 → `status: pass` RED 테스트 1개 추가.
