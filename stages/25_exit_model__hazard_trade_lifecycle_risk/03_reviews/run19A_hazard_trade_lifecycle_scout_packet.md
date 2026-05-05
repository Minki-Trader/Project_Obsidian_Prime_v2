# RUN19A Hazard Trade Lifecycle Scout Packet(실행19A 위험률 거래 생애주기 탐색 묶음)

## Judgment(판정)

- run(실행): `run19A_hazard_trade_lifecycle_risk_scout_v1`
- status(상태): `reviewed_structural_scout_completed(검토된 구조 탐색 완료)`
- judgment(판정): `inconclusive_hazard_trade_lifecycle_risk_scout_completed`
- selected variant(선택 변형): `v04_logit_core24_reversal_after_favorable_1x`
- boundary(경계): `hazard_trade_lifecycle_structural_scout_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`
- MT5 runtime_probe(MT5 런타임 탐침): `not_attempted_in_run19A_next_milestone_run19B_hazard_trade_lifecycle_runtime_probe_v1(실행19A에서는 미시도, 다음 마일스톤은 run19B_hazard_trade_lifecycle_runtime_probe_v1)`

효과(effect, 효과): Hazard model(위험률 모델)을 entry score(진입 점수)가 아니라 bar-by-bar loss/reversal risk(봉별 손실/반전 위험)로 탐색했다. edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

## Experiment Design(실험 설계)

- hypothesis(가설): entry-time features(진입 시점 피처)와 elapsed bar(경과 봉)가 adverse/reversal event(불리/반전 사건)의 hazard risk(위험률 위험)를 분리할 수 있다.
- decision use(결정 용도): Stage25(25단계) MT5 runtime_probe(MT5 런타임 탐침)에서 hazard score(위험률 점수)를 flat/close pressure(평탄/청산 압력)로 넘길지 판단한다.
- comparison baseline(비교 기준): time-only hazard(시간 전용 위험률)와 core/volatility feature hazard(핵심/변동성 피처 위험률)를 같은 split(분할)에서 비교한다.
- stop condition(중지 조건): hazard characteristic(위험률 특성)이 보이면 미세탐색 없이 runtime_probe(런타임 탐침)로 넘어간다.

## Evidence(근거)

- variants(변형): `5`
- completed variants(완료 변형): `5`
- selected event(선택 사건): `reversal_after_favorable_1x`
- validation ROC AUC(검증 ROC AUC): `0.704654661378204`
- OOS ROC AUC(표본외 ROC AUC): `0.6908297000122845`
- validation lift(검증 고위험-저위험 사건 비율 차): `0.11199446940891808`
- OOS lift(표본외 고위험-저위험 사건 비율 차): `0.09907514450867053`
- Tier A rows(Tier A 행): `285864`
- Tier B fallback rows(Tier B 대체 행): `69723`

## Preserved Clues(보존 단서)

- discrete-time hazard(이산 시간 위험률)는 event row(사건 행)와 at-risk row(위험 노출 행)를 분리해 loss/reversal timing(손실/반전 시점)을 볼 수 있다.
- selected variant(선택 변형)의 top features(주요 피처)는 `['hazard_elapsed_bar', 'hazard_elapsed_frac', 'close_ema20_ratio', 'historical_vol_20', 'hl_range']`다.
- Tier A separate(Tier A 분리), Tier B separate(Tier B 분리), Tier A+B combined(Tier A+B 합산)를 모두 기록했다.

## Invalid Or Negative Memory(무효 또는 부정 기억)

- run19A(19A실행)는 Python structural scout(파이썬 구조 탐색)이므로 MT5 runtime evidence(MT5 런타임 근거)가 아니다.
- adverse/reversal event(불리/반전 사건)는 future path(미래 경로)에서 만든 label(라벨)이며 feature(피처)에 미래값을 넣지 않는다.
- hazard_risk(위험률 위험)는 calibrated probability(보정 확률)가 아니라 ranking/shape read(순위/모양 판독)로만 본다.

## Next Exact Action(다음 정확한 행동)

Create and run(생성 및 실행) `run19B_hazard_trade_lifecycle_runtime_probe_v1` as the narrow MT5 runtime_probe(좁은 MT5 런타임 탐침).
