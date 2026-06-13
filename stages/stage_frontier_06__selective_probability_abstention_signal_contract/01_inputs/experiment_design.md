# Frontier06 Experiment Design(전선06 실험 설계)

- hypothesis(가설): A selective probability abstention contract may convert weak path-label model scores into fewer, cleaner trades(선택적 확률 기권 계약은 약한 경로 라벨 모델 점수를 더 적고 깨끗한 거래로 바꿀 수 있음).
- decision_use(결정 사용): Controls whether Frontier06B selective signal scout should run(Frontier06B 선택 신호 탐색 실행 여부 결정).
- primary_family(주 작업군): experiment_design(실험 설계)
- primary_skill(주 스킬): obsidian-experiment-design(옵시디언 실험 설계)
- support_skills(보조 스킬): ["obsidian-data-integrity(옵시디언 데이터 무결성)", "obsidian-model-validation(옵시디언 모델 검증)", "obsidian-grok-collaboration(옵시디언 그록 협업)", "obsidian-artifact-lineage(옵시디언 산출물 계보)"]
- required_gates(필수 게이트): ["work_packet_schema_lint(작업 묶음 스키마 점검)", "external_review_packet(외부 검토 묶음)"]
- comparison_baseline(비교 기준): argmax-only Frontier04D/F05 model behavior as reference-only negative memory(최대 확률 전용 전선04D/F05 모델 행동을 참조 전용 부정 기억으로 사용).
- control_variables(고정 변수): ["feature_set_v2 58-feature input(피처 세트 v2 58개 입력)", "fixed locked path label reference target(고정 경로 라벨 참조 목표)", "same chronological train/validation/OOS split(같은 시간순 학습/검증/표본밖 분할)", "same small model families before WFO/MT5(워크포워드/MT5 전 같은 작은 모델군)"]
- changed_variables(변경 변수): ["output-to-trade abstention contract(출력-거래 기권 계약)", "train-only threshold calibration(학습 전용 임계값 보정)", "density-targeted no-trade rule(밀도 목표 무거래 규칙)"]
- success_criteria(성공 기준): ["validation and OOS both improve four-axis distance versus argmax(검증/표본밖 모두 최대 확률 대비 네 축 거리 개선)", "density approaches 5-10/day without OOS DD blow-up(표본밖 손실폭 폭증 없이 밀도 5-10/일 접근)", "ONNX parity remains passed for model probabilities(모델 확률 온엑스 동등성 유지)"]
- failure_criteria(실패 기준): ["only low-density cherry-picks pass(저밀도 선별만 통과)", "OOS PF or DD worsens versus argmax baseline(표본밖 수익 팩터나 손실폭이 최대 확률 기준보다 악화)", "thresholds require validation/OOS fitting(임계값이 검증/표본밖 적합을 요구)"]
- invalid_conditions(무효 조건): ["threshold search uses validation/OOS labels to set rules(검증/표본밖 라벨로 규칙 설정)", "signal rule reads future returns or realized PnL at entry(신호 규칙이 진입 시 미래 수익이나 실현 손익을 읽음)"]
- stop_conditions(중지 조건): ["no variant improves simultaneous density/PF/DD target distance(밀도/PF/DD 동시 목표 거리 개선 변형 없음)", "Stage364-style low-density probability-bin trap repeats(364단계식 저밀도 확률 구간 함정 반복)"]
