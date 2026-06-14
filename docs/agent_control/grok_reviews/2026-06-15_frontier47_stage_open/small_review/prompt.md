# Frontier47 stage-open Grok review(단계 개방 그록 검토)

Role(역할): external second opinion(외부 2차 의견) only.

Do not claim completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), selected baseline(선택 기준선), or Goal Achieve(목표 달성).
Do not inspect files, call tools, or request whole repo context(전체 저장소 맥락). Answer only from bounded evidence(제한 근거) below.

## Current truth(현재 진실)
- Current closed stage(현재 종료 단계): F46, `negative_memory(부정 기억)`.
- F46 runtime_probe_status(런타임 탐침 상태): `runtime_probe_ineligible_no_scout_seed_or_runtime_candidate_after_f46_sequence_context_proxy`.
- F46 best observed row(최상 관찰 행): `f46b_0001`, event=`event_mfe75_mae50_ratio70`, model=`extratrees_cls_d5_leaf240__base_logreg_c0p25__lagged_score_outcome_q86_w12_36`, train PF=1.3546, forward min PF=0.8051, density=7.38..8.89/day, DD=24.59.
- F46 preserved nonwinner clue(보존 비승자 단서): `f46b_0004`, event=`event_mfe65_mae35_loss_contained`, model=`logreg_balanced_l2_c0p25__base_extratrees_d3_leaf220__lagged_score_outcome_q86_w12_36`, forward min PF=1.0050, density=6.28..7.02/day, forward DD=11.70.
- Boundary(경계): F46 rows are reference-only clue(참조 전용 단서), not winner/baseline/promotion(승자/기준선/승격 아님).

## Codex proposed F47 direction(코덱스 제안 방향)
Hypothesis(가설): Apply train-only sequence state risk budget(학습 전용 순서 상태 위험 예산) to the F46 loss-contained event clue(손실 제한 이벤트 단서). The risk budget uses only entry-known closed-bar features(진입 시점에 알려진 닫힌 봉 피처) and horizon+1 embargoed past outcome tape(예측수평선+1 유예 과거 결과 테이프).

Changed variables(변경 변수):
- loss cluster budget(손실 군집 예산): cap `seq_past_bad_event_rate_fast/slow`.
- volatility state budget(변동성 상태 예산): cap `atr_14_over_atr_50`, `historical_vol_5_over_20`, and optionally `bb_squeeze`.
- cooldown state(휴식 상태): require minimum bars since high score(고점 점수 이후 최소 봉 수).
- score and budget thresholds(점수/예산 임계값): train split only(학습 분할 전용).

Controls(고정 변수):
- US100 M5 short-only(숏 전용).
- Frozen split(고정 분할): train/validation/OOS(학습/검증/표본외).
- Feature order(피처 순서): closed-bar 58-feature contract(닫힌 봉 58피처 계약).
- Validation/OOS(검증/표본외): read-only evaluation(읽기 전용 평가).

Stop conditions(중지 조건):
- runtime candidate(런타임 후보)가 나오면 pre-expensive Grok review(비싼 검증 전 그록 검토) 후 MT5 runtime probe(MT5 런타임 탐침)를 준비한다.
- seed/scout only(씨앗/탐색만)면 preserved clue(보존 단서) 또는 negative memory(부정 기억)로 닫는다.
- no scout(탐색 단서 없음)이면 negative memory(부정 기억)로 닫는다.

Invalid conditions(무효 조건):
- validation/OOS(검증/표본외)를 label/model/threshold/SLTP/rank/risk budget/repair(라벨/모델/임계값/손익절/순위/위험 예산/수리)에 쓰는 경우.
- F46 sequence-context score-only repair(순서 문맥 점수 전용 수리)를 반복하는 경우.
- F45 same-bar threshold-only repair(동일 봉 임계값 전용 수리), F44 continuous regression(연속 회귀), F42 timing gate(타이밍 게이트), F43 trade-shape source(거래 형태 원천)를 primary lever(주 레버)로 되살리는 경우.

## Success criteria for exploration(탐색 성공 기준)
- Scout clue(탐색 단서): forward min PF >= 1.05, density 4..12/day, forward max DD <= 18.
- Seed surface(씨앗 표면): forward min PF >= 1.20, density 5..10/day, forward max DD <= 12.
- Runtime candidate(런타임 후보): seed plus forward min PF >= 1.50 and forward max DD <= 10.
- Final goal hard gate(최종 목표 강제 게이트)는 final completion review(최종 완성 검토)에서만 적용한다.

## Question(질문)
Is this F47 stage-open plan honest and novel enough under reference-not-inheritance(참조이지 상속 아님), train-split-only construction lock(학습 분할 전용 구성 잠금), and claim boundary(주장 경계)?

Return only:
1. verdict: accepted, rejected, or needs_local_verification(수용/거절/로컬 검증 필요)
2. train_split_only_construction_lock: yes/no(학습 분할 전용 구성 잠금 예/아니오)
3. claim_boundary_ok: yes/no(예/아니오)
4. one risk(위험) if any
5. one concrete adjustment(구체 조정) if any
