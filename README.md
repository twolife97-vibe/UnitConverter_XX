# Unit Converter (Python)

![unit-converter](./unit-converter.jpg)

길이 단위(`단위:값`)를 입력하면 등록된 다른 단위로 변환해 출력하는 CLI 프로그램입니다.

---

## Overview

- 사용자가 입력한 길이(`단위:값`)를 기반으로, 해당 값을 **다른 모든 단위**로 변환해 출력합니다.
- 새 단위 추가 시 기존 코드 변경을 최소화하도록 설계합니다 (**OCP**).
- 변환 로직과 입·출력 책임을 분리합니다 (**SRP**).
- 단위 변환·입력 검증은 **테스트 코드**로 검증합니다.

### 문제 정의 (요약)

수입·국내 자재 견적·발주 시 feet/yard/inch/m/mm가 카탈로그·발주서·메모마다 섞여, 수동 환산·교차 확인에 시간이 들고 단위 미확인 시 발주 오류로 이어집니다.  
상세: [`Report/01.UnitConverter_ProblemDefinition_Report.md`](./Report/01.UnitConverter_ProblemDefinition_Report.md) · PRD: [`docs/PRD.md`](./docs/PRD.md)

---

## 현재 구현 상태

| 항목 | 상태 |
|------|------|
| `unit:value` 입력 (meter / feet / yard) | ✅ |
| 형식·숫자·unknown unit 검증 | ✅ (부분) |
| OCP / SRP 구조 | ❌ |
| 음수 검증 | ❌ |
| 테스트 코드 | ❌ |
| 설정 외부화 (JSON/YAML) | ❌ |
| 동적 단위 등록 | ❌ |
| JSON / CSV / 표 출력 | ❌ |
| 연속 입력 (동일 세션 다중 변환) | ❌ |

현재 코드: [`UnitConverter.py`](./UnitConverter.py)

---

## 가상환경 설정 및 실행

```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화 (Windows)
venv\Scripts\activate

# 가상환경 활성화 (macOS/Linux)
source venv/bin/activate

# 실행
python UnitConverter.py

# 가상환경 비활성화
deactivate
```

실행 예:

```
Insert value for converting (ex: meter:2.5): meter:2.5
2.5 meter = 2.5 meter
2.5 meter = 8.2021 feet
2.5 meter = 2.734025 yard
```

---

## 요구사항

### 기본 요구사항

1. 사용자 입력 예시:
   ```
   meter:2.5
   ```
   → 출력:
   ```
   2.5 meter = 8.2 feet
   2.5 meter = 2.7 yard
   ...
   ```

2. 현재 지원 단위:
   - meter
   - feet
   - yard

3. 새로운 단위가 추가될 때도 기존 코드의 변경이 최소화되도록 할 것.

4. 각 단위 간 변환이 정확히 계산되도록 테스트 코드를 작성할 것.

### 비즈니스 로직

- `1 meter = 3.28084 feet`
- `1 meter = 1.09361 yard`
- feet/yard 간의 비율은 meter 기준으로 계산.

### 품질 요구사항

- OCP를 만족하는 설계
- SRP를 만족하는 클래스 구성
- 입력 값 검증 (음수, 잘못된 형식, 없는 단위)

### 추가 요구사항

- **설정 외부화** — 변환 비율을 외부 설정 파일(JSON/YAML)에서 로드
- **동적 단위 등록** — `1 cubit = 0.4572 meter` 형태로 등록·사용
- **출력 포맷 선택** — JSON / CSV / 표 형태 출력

우선순위·KPI·릴리스 계획은 [`docs/PRD.md`](./docs/PRD.md) 참고.

---

## 프로젝트 문서

| 경로 | 설명 |
|------|------|
| [`docs/PRD.md`](./docs/PRD.md) | 제품 요구사항 (PRD v0.1) |
| [`Report/01.UnitConverter_ProblemDefinition_Report.md`](./Report/01.UnitConverter_ProblemDefinition_Report.md) | 문제 정의 (Mom Test + R-G-I-O) |
| [`Report/STEP1_MomTest_Report.md`](./Report/STEP1_MomTest_Report.md) | Mom Test 워크북 |
| [`Report/STEP2_RGIO_Report.md`](./Report/STEP2_RGIO_Report.md) | R-G-I-O · 성공 기준 |
| [`Prompt/`](./Prompt/) | Mom Test · R-G-I-O · 채점 프롬프트 |

---

## 생성형AI를 활용한 Activities (6시간)

1. **문제 코드 및 기본 요구사항 분석** (0.5시간)
   - 기본 코드 구조, 로직 이해
   - Mom Test · 문제 정의 · PRD 작성
2. **기본 요구사항 및 품질 요구사항 구현** (2시간)
   - OCP를 만족하는 인터페이스 구현
   - SRP를 만족하도록 클래스 구현
   - 입력값 검증 구현
3. **TC 구현** (0.5시간)
   - 단위 변환 기능 검증 및 입력 값 검증 TC 작성
4. **추가 요구사항 구현** (2시간)
   - 설정 외부화, 동적 단위 등록, 출력 포맷 구현 및 TC 작성
5. **회고 및 발표** (1시간)
   - 실습 목표와 달성도
   - AI 활용 — 도움이 된 순간과 한계
   - TC 추가가 개선에 미친 영향, TC 작성 팁
   - 클린코드·리팩토링 장점과 어려운 점
