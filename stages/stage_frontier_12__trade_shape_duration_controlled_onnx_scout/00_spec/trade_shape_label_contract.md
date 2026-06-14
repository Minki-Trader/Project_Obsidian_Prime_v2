# Trade Shape Label Contract(거래 형상 라벨 계약)

Action(행동): Frontier12B(프론티어12B)는 trade-shape constrained labels(거래 형상 제약 라벨)을 만들기 전에 label knobs(라벨 파라미터)를 run_manifest(실행 목록)에 고정합니다.

Effect(효과): validation/OOS(검증/표본밖) 성과를 본 뒤 라벨을 다시 맞추는 hidden threshold search(숨은 임계값 탐색)를 막습니다.

## Required Label Concepts(필수 라벨 개념)

- early adverse excursion veto(초기 불리 이동 배제)
- favorable path confirmation(유리 경로 확인)
- capped hold duration(상한 보유 기간)
- MAE/MFE quality(최대 불리/유리 이동 품질)
- density-aware neutral class(빈도 인식 중립 클래스)

## Pre-registered Knobs(사전 등록 파라미터)

- all knobs must be declared in the Frontier12B manifest before validation/OOS metrics(모든 파라미터는 검증/표본밖 지표 전 프론티어12B 실행 목록에 기록)
- train-only quantiles may define MAE/MFE cut points(학습 전용 분위수는 최대 불리/유리 이동 절단점 정의 가능)
- no validation-driven knob changes(검증 기반 파라미터 변경 없음)
- argmax-only signal with no threshold search(임계값 탐색 없는 최대확률 전용 신호)

## Forbidden Knobs(금지 파라미터)

- validation-driven MAE/MFE cuts(검증 기반 최대 불리/유리 이동 절단)
- OOS-driven density repair(표본밖 기반 빈도 수리)
- post-fit selector replacement(적합 후 선택기 대체)
- threshold micro-search(임계값 미세 탐색)

## Signal Contract(신호 계약)

The output schema(출력 스키마)는 `[p_short, p_flat, p_long]`이고 signal(신호)은 argmax-only(최대확률 전용)입니다. Effect(효과): label experiment(라벨 실험)이 runtime authority(런타임 권위)나 live readiness(실거래 준비)로 과장되지 않습니다.
