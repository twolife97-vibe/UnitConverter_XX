# UnitConverter_XX — STEP 3 Harness · Cursor 워크플로 프롬프트

## 1. 실행 프롬프트

```
STEP 3 validate_lines TDD — pytest Harness + Cursor 워크플로 골격

입력:
- Report/STEP3_ValidateLines_Report.md (출력 계약·프로필)
- 기존 validate_lines.py (있으면 src/로 이동)

출력 형식:
1. pyproject.toml — [project] + pytest (pythonpath=["."], testpaths=["tests"])
2. src/__init__.py (빈), src/validate_lines.py (이동)
3. tests/__init__.py (빈), tests/test_validate_lines.py (import 한 줄만)
4. .cursorrules (40~60줄) — API·TDD·한국어·git 규칙
5. .cursor/commands/tdd-red.md — RED 전용 (AAA, pytest 예시, 금지)
6. .cursor/commands/export-report.md — Report/Prompt 저장

규칙:
- 구현·테스트 본문은 아직 쓰지 않음 — 골격만
- import: from src.validate_lines import validate_lines
- pythonpath = ["."] 필수 (["src"] 아님)
- 목표 API: validate_lines → {status: pass|fail|incomplete, failed_lines:[...]}
- TDD: RED→GREEN→REFACTOR, RED은 tests/만, assert 완화·skip·xfail 금지
- git commit은 사용자 요청 시에만
- pytest -q 체크: 테스트 0개여도 collection/import 에러 없으면 OK
```

---

## 2. 참고

### pyproject.toml 기대값

```toml
[project]
name = "unitconverter_xx"
version = "0.1.0"

[tool.pytest.ini_options]
pythonpath = ["."]
testpaths = ["tests"]
```

### Harness 체크포인트

| 명령 | 기대 |
|------|------|
| `pytest -q` | `no tests ran` (exit 5), import 에러 없음 |
| `from src.validate_lines import validate_lines` | 정상 import |

### TDD Phase 수정 범위

| Phase | 허용 | 금지 |
|-------|------|------|
| RED | `tests/` | `src/` 수정, assert 완화, skip, xfail |
| GREEN | `src/` 최소 | 테스트 삭제·완화 |
| REFACTOR | 구조 (동작 동일) | 테스트·동작 변경 |

### validate_lines 목표 API

```python
result = validate_lines(lines, profile="default" | "business", ...)
# {"status": "pass" | "fail" | "incomplete", "failed_lines": [...]}
```

---

## 3. 연계

| 선행 | 후속 |
|------|------|
| `Report/STEP3_ValidateLines_Report.md` | `Report/STEP3_Harness_Report.md` (본 문서) |
| `Report/STEP2_RGIO_Report.md` | `/tdd-red` → RED 테스트 추가 |
| `Report/STEP3_Harness_Report.md` | GREEN — API dict 전환 + 테스트 통과 |
| `/export-report` | 세션별 `Report/` · `Prompt/` 갱신 |
