# UnitConverter_XX — STEP 3 validate_lines 프롬프트

## 1. 실행 프롬프트

```
STEP 2 R-G-I-O · 성공 기준 → validate_lines 출력 계약

입력:
- STEP2_RGIO_Report.md (R-G-I-O, 성공 기준 5개)
- 기본 CLI 출력 형식 (예: meter:2.5 → feet/yard 줄)
- validate_lines.py 현재 구현 (선택)

출력 형식:
1. 계약 목적 (1문장) — TC·출력 검증 기준선
2. 출력 줄 형식 규칙 (F1~F7)
3. 지원 단위·비율 표
4. 프로필 표 (default / business)
5. STEP2 성공 기준 ↔ validate_lines 매핑 표
6. Gap 표 (계약 밖 항목 + 후속 모듈)
7. API 요약 (validate_lines, validate_session)

규칙:
- validate_lines는 **출력 줄**만 검증 (입력 Invalid, 판정, 시간 KPI 제외)
- business 프로필은 성공 #5: meter 2자리, mm 정수
- business 프로필은 inch·mm 타깃 포함 (R/I gap)
- validate_session은 성공 #4: 2+ 변환 묶음
- default 프로필은 기본 2줄(feet, yard) 스냅샷 유지
```

---

## 2. 계약 규칙 (참고)

| ID | 규칙 |
|----|------|
| F1 | `{값} {단위} = {값} {단위}` 패턴 |
| F2 | 좌측 값·단위 모든 줄 동일 (입력 에코) |
| F3 | 소스 단위 ≠ 대상 단위 |
| F4 | 지원 단위: meter, feet, yard, inch, mm |
| F5 | 프로필별 자릿수 (business: m 2, mm 0) |
| F6 | meter 기준 비율 일치 |
| F7 | 프로필별 기대 타깃 집합 일치 |

---

## 3. 프로필 템플릿

```
| 프로필 | 기대 타깃 | meter | feet/yard/inch | mm |
|--------|-----------|-------|----------------|-----|
| default | feet, yard | 4 | 4 | 4 |
| business | 소스 제외 전체 | 2 | 4 | 0 (정수) |
```

---

## 4. STEP 2 연계 프롬프트 (선행)

```
STEP 2 R-G-I-O 보고서 완료 후:

다음만 출력:
1. 성공 기준 중 **출력·TC로 내릴 수 있는** 항목 (#4, #5, 단위 gap)
2. validate_lines 프로필 초안 (default + business)
3. Gap — validate_lines 밖 (#1, #2, #3, 판정)

→ 완료 후 STEP 3 구현·리뷰
```

---

## 5. 정합 리뷰 프롬프트 (요약)

```
STEP2_RGIO_Report.md R-G-I-O·성공 기준이 validate_lines 계약과 일치하는지 리뷰.
빠지거나 어긋난 항목만 표로. 파일 수정 금지.

대조 기준: validate_lines.py + 본 프롬프트 §2
```

상세 채점: `STEP3_ValidateLines_Grading_Prompt.md`

---

## 6. 관련 프롬프트

| 파일 | 내용 |
|------|------|
| `STEP2_RGIO_Prompt.md` | R-G-I-O + 성공 기준 |
| `STEP3_ValidateLines_Prompt.md` | validate_lines 계약 (본 문서) |
| `STEP3_ValidateLines_Grading_Prompt.md` | STEP2 ↔ 계약 정합 리뷰 |
