# Selection Status

## 현재 판독(Current Read, 현재 판독)

- stage(단계): `12_model_family_challenge__extratrees_training_effect`
- status(상태): `active_standalone_tier_balance_mt5_supplement_completed(단독 티어 균형 MT5 보강 완료)`
- current run(현재 실행): `run03F_et_v11_tier_balance_mt5_v1`
- source Python package(원천 파이썬 패키지): `run03D_et_standalone_batch20_v1`
- source MT5 reference(원천 MT5 참고): `run03E_et_batch20_top_v11_mt5_probe_v1`
- current model family(현재 모델 계열): `sklearn_extratreesclassifier_multiclass`
- comparison baseline(비교 기준선): `none(없음)`
- Stage 10/11 inheritance(Stage 10/11 계승): `false(아님)`
- external verification status(외부 검증 상태): `completed`

## RUN03B Standalone Source(RUN03B 단독 원천)

- validation signals(검증 신호): `604`
- validation hit rate(검증 적중률): `0.3526490066225166`
- OOS signals(표본외 신호): `463`
- OOS hit rate(표본외 적중률): `0.42764578833693306`

## RUN03C MT5 Probe(RUN03C MT5 탐침)

- validation net/PF(검증 순수익/수익 팩터): `-13.18` / `0.98`
- OOS net/PF(표본외 순수익/수익 팩터): `249.57` / `1.69`

효과(effect, 효과): Stage 12(12단계)는 단독 실험으로 유지되고, RUN03C(실행 03C)는 이전 MT5 연결 근거, RUN03E(실행 03E)는 RUN03D 상위 변형의 이전 MT5 연결 근거, RUN03F(실행 03F)는 최신 Tier A/B/routed(Tier A/B/라우팅) MT5 보강 근거를 담당한다.


## run03D standalone batch20 read(단독 20개 묶음 판독)

- run(실행): `run03D_et_standalone_batch20_v1`
- best structural variant(최상위 구조 변형): `v11_base_leaf20_q85`
- validation/OOS(검증/표본외): `0.392688` / `0.457317`
- judgment(판정): `inconclusive_standalone_batch20_structural_scout`
- MT5(`MetaTrader 5`, 메타트레이더5): `followed_by_run03F_tier_balance_completed(후속 RUN03F 티어 균형 완료)`
- effect(효과): Stage12 단독 후보 압축은 RUN03E 대표 변형 MT5 확인과 RUN03F Tier A/B/routed(Tier A/B/라우팅) 보강까지 확장됐지만 운영 승격이나 런타임 권위는 주장하지 않는다.


## run03E RUN03D top MT5 read(RUN03D 상위 변형 MT5 판독)

- run(실행): `run03E_et_batch20_top_v11_mt5_probe_v1`
- source variant(원천 변형): `v11_base_leaf20_q85`
- external verification(외부 검증): `completed`
- validation net/PF(검증 순손익/수익팩터): `-205.14` / `0.88`
- OOS net/PF(표본외 순손익/수익팩터): `362.83` / `1.44`
- judgment(판정): `inconclusive_run03d_top_variant_mt5_runtime_probe_completed`
- effect(효과): RUN03D 대표 변형은 MT5 검증을 받았지만, 운영 승격이나 알파 품질 주장은 아니다.

## run03F Tier A/B/routed MT5 read(Tier A/B/라우팅 MT5 판독)

- run(실행): `run03F_et_v11_tier_balance_mt5_v1`
- source variant(원천 변형): `v11_base_leaf20_q85`
- external verification(외부 검증): `completed`
- validation routed net/PF/trades(검증 라우팅 순손익/수익팩터/거래수): `-194.48` / `0.90` / `444`
- OOS routed net/PF/trades(표본외 라우팅 순손익/수익팩터/거래수): `546.79` / `1.47` / `368`
- OOS Tier A only net(표본외 Tier A 단독 순손익): `399.59`
- OOS Tier B only net(표본외 Tier B 단독 순손익): `88.69`
- judgment(판정): `inconclusive_runtime_probe_tier_balance_supplement_completed`
- effect(효과): RUN03F(실행 03F)는 최신 MT5 보강 근거다. 하지만 single split runtime_probe(단일 분할 런타임 탐침)이므로 alpha quality(알파 품질), operating promotion(운영 승격), runtime authority(런타임 권위)는 주장하지 않는다.
