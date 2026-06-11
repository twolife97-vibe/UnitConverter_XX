# REFACTOR Smell — magic_square

`src/magic_square.py`의 **코드 스멜**만 식별·목록화한다. 리팩터링 코드 변경은 하지 않는다.

## 자동 입력 (질문 금지)

| SSOT | 용도 |
|------|------|
| `.cursorrules` | REFACTOR Phase 정의 |
| `src/magic_square.py` | 분석 대상 |
| `tests/test_magic_square.py` | 동작 기준 (변경 금지) |
| `docs/PRD.md` § NFR-04 | SRP·유지보수 |

파일이 없으면: "구현 없음 — GREEN 후 재실행"으로 보고하고 **종료** (질문 없음).

## Phase 선언 (필수)

응답 **첫 줄**:

```
REFACTOR — magic_square: smell audit (<n>건)
```

## 사전 조건

```bash
pytest tests/test_magic_square.py -q
```

- **전부 통과**해야 smell audit 시작.
- 실패 중이면: 리팩터 금지, `/green-minimal` 권장만 보고.

## 스멜 점검 체크리스트

| # | 스멜 | 징후 (magic_square) |
|---|------|---------------------|
| S1 | 하드코딩 / 특수 케이스 | `_KNOWN_3X3` 등 literal 비교만으로 pass |
| S2 | 긴 함수 | 행·열·대각 검증이 한 함수에 혼재 |
| S3 | 중복 | 합 계산·범위 검사 반복 |
| S4 | 매직 넘버 | 15, 3, 9 등 의미 없는 상수 |
| S5 | dead code | T01 전용 분기 잔존 |
| S6 | SRP 위반 | parse · validate · sum이 한 모듈에 뒤섞임 |
| S7 | 테스트 결합 | production이 특정 테스트 grid import |

각 항목: **있음 / 없음 / 해당 없음** + 근거 **한 줄** + `src/` **위치(함수·줄)**.

## 산출 형식

```markdown
## Smell 목록

| ID | 스멜 | 위치 | 근거 | 심각도 |
|----|------|------|------|--------|
| S1 | 하드코딩 | validate_magic_square L12 | G1 literal만 pass | 높음 |
| … | … | … | … | … |

## REFACTOR 후보 (우선순위)

1. <S#> — <한 줄 개선 방향>
2. …

## 금지 (이번 Phase)

- src/tests 수정 없음
- pytest 재실행은 사전 조건 확인용만
```

## 완료 보고 형식

```
REFACTOR — magic_square: smell audit (<n>건)

pytest: passed (사전 조건)
스멜: <n>건 (높음 <a> / 중 <b> / 낮 <c>)
1순위: S1 — <한 줄>

다음: /refactor-safe — 1순위만 적용
```

## 금지 (REFACTOR Smell)

| 금지 | 이유 |
|------|------|
| `src/` · `tests/` 코드 수정 | smell audit만 |
| 동작 변경 제안을 코드로 적용 | safe에서 수행 |
| 테스트 없이 audit | 사전 pytest 필수 |
| 사용자에게 우선순위 질문 | 표·심각도로 자율 정렬 |

## 수정 허용

- **없음** (분석 응답만)
