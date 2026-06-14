# Frontier17 Stage Open Review(전선17 단계 개방 검토)

You are Grok acting as external second opinion(외부 2차 의견). Return one classification(분류): accepted(수용), rejected(거절), or needs_local_verification(로컬 검증 필요).

## Current Truth(현재 진실)

Frontier16(전선16)은 `closed_negative_memory_with_frontier16d_runtime_probe_observation_no_authority(부정 기억 + 런타임 탐침 관찰, 권위 없음)`로 닫혔다.

Key evidence(핵심 근거):
- F16B proxy(프록시): best `f16b_edge_h8_t0p30_cap0p45_early0p25__rf_bal__edge_margin__target8`; validation/OOS PF-density-DD(검증/표본밖 수익 팩터-빈도-손실폭) `1.06795, 5.65574/day, 12.9599%` / `0.942216, 5.45802/day, 12.8032%`; strict rows(엄격 행) `0`, preserved rows(보존 행) `0`.
- F16C closeout(마감): locked edge_margin target8(고정 엣지 마진 목표8) + broad risk-quality labels(넓은 위험 품질 라벨)는 PF and split stability(수익 팩터와 분할 안정성)를 만들지 못했다.
- F16D MT5 runtime probe(런타임 탐침): signal parity(신호 동등성) matched with `signal_diff=0`; validation PF/DD/trades(검증 수익 팩터/손실폭/거래수) `1.37 / 12.2% / 229`; OOS(표본밖) `0.87 / 47.17% / 164`. This confirms runtime observation(런타임 관찰) but no runtime authority(런타임 권위).
- F15 preserved clue(보존 단서): train-only score threshold(학습 전용 점수 임계값)는 5~10/day(일 5~10회) density transfer(빈도 전이)를 만들 수 있었다.
- F15/F16 negative memory(부정 기억): threshold/edge-margin/risk-quality label(임계값/엣지 마진/위험 품질 라벨)만으로 PF/DD/smoothness(수익 팩터/손실폭/매끄러움)를 같이 만들지 못했다.

No completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) is claimed.

## Codex Direction Before Grok(그록 전 코덱스 방향)

Open Frontier17(전선17) as:

`stage_frontier_17__loss_cluster_firewall_profit_persistence_onnx_scout`

Hypothesis(가설):
Instead of first forcing density(빈도)를 맞춘 뒤 edge(거래 우위)를 찾는 방식, train-only loss-cluster firewall(학습 전용 손실 군집 방화벽) and profit-persistence trigger(수익 지속성 트리거)를 결합해 only clean continuation states(깨끗한 지속 상태)에서만 진입하면 5~10/day(일 5~10회)에 가까운 빈도를 유지하면서 PF/DD/smoothness(수익 팩터/손실폭/매끄러움)를 동시에 개선할 수 있다.

Changed variable(변경 변수):
- validation philosophy(검증 철학): density-first threshold/edge-margin(빈도 우선 임계값/엣지 마진) -> drawdown-first hazard firewall + continuation trigger(손실폭 우선 위험 방화벽 + 지속 트리거)
- label/source axis(라벨/원천 축): future path edge label(미래 경로 엣지 라벨) -> train-only adverse cluster state + realized continuation quality(학습 전용 불리 군집 상태 + 실현 지속 품질)

Controls(통제):
- same Tier A dataset(같은 티어 A 데이터), feature order(피처 순서), split boundaries(분할 경계)
- no F15 9-cell grid(F15 9칸 격자 금지)
- no F16 locked `edge_margin__target8` cell(전선16 고정 엣지 마진 목표8 칸 금지)
- no validation/OOS threshold calibration(검증/표본밖 임계값 보정 없음)
- pre-register exactly 3 firewall profiles(방화벽 프로필 3개 사전 등록)
- include MT5 runtime probe(런타임 탐침) before stage closeout(단계 마감)

Pre-registered profiles(사전 등록 프로필):
1. `f17b_firewall_h8_ddq70_contq60`: avoid train adverse cluster worse than q70(학습 불리 군집 q70보다 나쁜 상태 회피), enter continuation above q60(지속성 q60 이상 진입)
2. `f17b_firewall_h10_ddq75_contq65`: stricter loss cluster veto(더 엄격한 손실 군집 배제), mid continuation(중간 지속성)
3. `f17b_firewall_h12_ddq80_contq70`: strongest loss firewall(가장 강한 손실 방화벽), strongest continuation trigger(가장 강한 지속성 트리거)

Success criteria(성공 기준):
- scout clue(탐색 단서): validation and OOS(검증과 표본밖) net positive(순수익 양수), PF >= 1.2(수익 팩터 1.2 이상), density 5~10/day(일 5~10회), DD <= 15%(손실폭 15% 이하), worst subperiod DD <= 25%(최악 하위기간 손실폭 25% 이하), ONNX parity pass(온엑스 동등성 통과)
- seed surface(씨앗 표면): DD/smoothness(손실폭/매끄러움)가 F16B/D보다 명확히 개선되고 density(빈도)가 3~10/day(일 3~10회)에 머무르며 PF axis(수익 팩터 축)가 후퇴하지 않는 경우
- runtime probe observation(런타임 탐침 관찰): before closeout(마감 전) at least one best-or-seed candidate gets narrow MT5 handoff/probe(좁은 MT5 인계/탐침) or exact blocked reason(정확한 차단 사유)

Failure criteria(실패 기준):
- only density(빈도) improves while PF/DD/smoothness(수익 팩터/손실폭/매끄러움) fails
- firewall suppresses trades below 3/day(방화벽이 거래를 일 3회 미만으로 눌러버림)
- train-only hazard thresholds(학습 전용 위험 임계값)가 validation/OOS(검증/표본밖)로 transfer(전이)되지 않음
- MT5 probe(런타임 탐침) shows material runtime collapse(중대한 런타임 붕괴)

Claim boundary(주장 경계):
This is scout clue/seed surface/runtime probe observation(탐색 단서/씨앗 표면/런타임 탐침 관찰) only. No completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), or Goal Achieve(목표 달성).

Review size(검토 크기): small review(소규모 검토).

## Review Questions(검토 질문)

1. Is this novelty delta(신규성 차이) sufficient versus F15-F16(전선15~16), or is it still threshold/edge-margin repair(임계값/엣지 마진 수리) in disguise?
2. Are the 3 pre-registered firewall profiles(사전 등록 방화벽 프로필 3개) safe as exploration(탐색) without becoming a repair ladder(수리 사다리)?
3. What minimum guards(최소 가드) must Codex(코덱스) add before materializing Frontier17A/B(전선17A/B 물질화)?

