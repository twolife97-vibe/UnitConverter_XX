# UnitConverter_XX — validate_lines 정합 리뷰 채점 프롬프트

```
STEP2_RGIO_Report.md R-G-I-O·성공 기준이 validate_lines 계약과 일치하는지 리뷰해줘. 수정하지 마.

입력:
- Report/STEP2_RGIO_Report.md (R-G-I-O, 성공 기준)
- validate_lines.py (또는 STEP3_ValidateLines_Report.md)

출력:
- 빠지거나 어긋난 항목만 표 (구분 | STEP2 요구 | validate_lines 현황 | 판정)
- 일치 항목은 표에 넣지 않음
- 계약 밖(의도적 분리) 항목은 "범위 밖"으로 표기

체크 (validate_lines 담당 범위만):
- [ ] R — inch / mm 단위 반영
- [ ] G — m 2자리 / mm 정수 (성공 #5)
- [ ] I — inch·mm 출력 gap (Unknown unit, ×1000 후처리)
- [ ] O / #4 — validate_session (2+ 묶음)
- [ ] #5 — business 프로필 자릿수·타깃
- [ ] default 프로필 — 기본 2줄 스냅샷 유지

범위 밖 (표에 넣지 않거나 "범위 밖"만):
- #1 재발주 0건, #2 ≤20분
- #3 bare number 입력
- G 맞다/틀리다/초과 판정
```

---

## 채점 기준 (참고)

| 항목 | Pass 조건 |
|------|-----------|
| 단위 확장 | business에 inch, mm 타깃·비율 |
| 성공 #5 | meter 2자리, mm 정수, 추가 후처리 불필요 형식 |
| 성공 #4 | validate_session 또는 동등 묶음 검증 |
| default 유지 | feet·yard 2줄 4자리 스냅샷 호환 |
| 역할 분리 | 입력·판정·시간 KPI를 validate_lines에 넣지 않음 |

## 어긋남 패턴

- business인데 mm 줄 없음 또는 mm가 소수
- meter 타깃이 4자리 (business)
- 소스 단위가 출력에 포함
- STEP2 #5와 default 4자리만 강제 (프로필 혼동)

## 개선 방향 템플릿

> validate_lines를 STEP2와 맞추려면 **[프로필/단위/validate_session]** 중 **[항목]** 을 **[구체 변경]** 하면 된다.
