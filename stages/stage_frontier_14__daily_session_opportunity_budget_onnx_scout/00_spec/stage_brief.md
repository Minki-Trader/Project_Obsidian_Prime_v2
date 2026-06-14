# Frontier14 Stage Brief(프론티어14 단계 개요)

Stage id(단계 ID): `stage_frontier_14__daily_session_opportunity_budget_onnx_scout`

Question(질문): Can daily/session opportunity-budget labels(일별/세션별 기회 예산 라벨) make US100 M5 ONNX(US100 5분봉 온엑스) learn the 5~10/day density axis(일 5~10회 빈도 축) without post-fit threshold search(적합 후 임계값 탐색 없이)?

## Frontier Thesis(프론티어 가설)

US100 M5 fixed 3-class ONNX(US100 5분봉 고정 3클래스 온엑스)는 label wrapping(라벨 감싸기)보다 upstream entry opportunity generation(상류 진입 기회 생성)을 바꾸면 density/PF/DD(빈도/수익 팩터/손실폭) 균형에 가까워질 수 있습니다.

## Novelty Delta(신규성 차이)

Frontier12/13(프론티어12/13)은 trade-shape label wrapping and regime-scale repair(거래 형상 라벨 감싸기와 국면 척도 수리)를 시험했습니다. Frontier14(프론티어14)는 daily/session quota opportunity labels(일별/세션별 할당 기회 라벨)로 label source(라벨 원천)를 바꿉니다.

## Do Not Repeat(반복 금지)

- same label knob loosening(같은 라벨 파라미터 완화)
- same regime-scale wrapping(같은 국면 척도 감싸기)
- class-weight density forcing(클래스 가중 빈도 강제)
- threshold micro-search(임계값 미세 탐색)
- quota/horizon retuning after metrics(지표 확인 뒤 할당량/지평 재조정)

## Exit Rule(종료 규칙)

label quota(라벨 할당량)는 맞지만 model argmax(모델 최대확률)가 density cliff(빈도 절벽), DD explosion(손실폭 폭발), or PF collapse(수익 팩터 붕괴)를 만들면 negative memory(부정 기억).

## Claim Boundary(주장 경계)

completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 forbidden(금지)입니다.
