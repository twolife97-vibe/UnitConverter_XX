# RED Test Plan — magic_square

**마방진(Magic Square)** `validate_magic_square` API에 대한 **테스트 계획**만 작성한다. 코드·테스트 파일은 아직 추가하지 않는다.

## 자동 입력 (질문 금지)

사용자 추가 입력 없이 아래 SSOT를 **읽고** 계획을 확정한다.

| SSOT | 용도 |
|------|------|
| `.cursorrules` | TDD Phase·수정 허용 범위 |
| `docs/PRD.md` | FR-07 테스트·품질 맥락 |
| `.cursor/skills/magic-square-tdd/SKILL.md` | 마방진 계약·RED 규칙 |
| `Report/STEP2_RGIO_Report.md` | 성공 기준·R-G-I-O (참고) |

## Phase 선언 (필수)

응답 **첫 줄**:

```
RED — magic_square: test plan (<한 줄 요약>)
```

## 대상 API

```python
result = validate_magic_square(grid)
# result == {"status": "pass" | "fail" | "invalid", "errors": [...]}
```

| status | 의미 |
|--------|------|
| pass | 유효한 마방진 |
| fail | 형식은 맞으나 마방진 조건 불충족 |
| invalid | 빈 격자·비정방·범위 밖·중복 등 입력 무효 |

계약 상세: `.cursor/skills/magic-square-tdd/SKILL.md` § API

## 실행 절차

1. **SSOT 읽기** — 위 표 파일을 열어 계약·금지 사항 확인
2. **케이스 도출** — happy path → invalid → fail → 경계(n=1, n=3) 순
3. **우선순위** — RED 사이클당 **테스트 1개** 원칙으로 1순위 케이스 표시
4. **AAA 초안** — 각 케이스별 Arrange / Act / Assert를 **문장**으로만 적기 (코드 X)
5. **산출** — 아래 보고 템플릿으로 **채팅 응답** (파일 저장은 `/export-report` 또는 magic-square-docs)

## 테스트 계획 표 (필수)

| ID | 케이스 | grid 요약 | 기대 status | 기대 errors | RED 순서 |
|----|--------|-----------|-------------|-------------|----------|
| T01 | 3×3 정답 | `[[8,1,6],[3,5,7],[4,9,2]]` | pass | `[]` | 1 |
| T02 | 행 합 불일치 | (3×3, 한 행만 틀림) | fail | ≥1 | 2 |
| T03 | 빈 격자 | `[]` | invalid | ≥1 | … |
| … | … | … | … | … | … |

- 최소 **6건** (pass 1 · fail 2 · invalid 2 · 경계 1).
- `errors`는 사람이 읽을 수 있는 **한국어 또는 영문** 짧은 문장 목록.

## AAA 예시 (계획용 — 코드 아님)

**T01 pass**

- Arrange: 3×3 정답 격자 준비
- Act: `validate_magic_square(grid)` 호출
- Assert: `status == "pass"`, `errors == []`

## 완료 보고 형식

```
RED — magic_square: test plan (<요약>)

케이스 수: <n> (pass <a> / fail <b> / invalid <c>)
1순위 RED: T01 — <한 줄>
다음 RED: /red-skeleton — T01 AAA 테스트 골격 추가

금지 준수: src/ 미수정 · tests/ 미추가 · pytest 미실행
```

## 금지 (RED Test Plan)

| 금지 | 이유 |
|------|------|
| `tests/` · `src/` 파일 생성·수정 | 계획 단계 |
| `pytest` 실행 | 구현·테스트 없음 |
| 사용자에게 케이스·우선순위 질문 | SSOT·표로 자율 확정 |
| assert 완화 전제의 모호한 Assert | RED 품질 저하 |

## 수정 허용

- **없음** (응답 텍스트만). 파일 저장이 필요하면 export 계열 커맨드 사용.
