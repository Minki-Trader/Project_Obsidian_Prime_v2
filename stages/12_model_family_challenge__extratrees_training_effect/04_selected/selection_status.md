# Selection Status

## 현재 판독(Current Read, 현재 판독)

- stage(단계): `12_model_family_challenge__extratrees_training_effect`
- status(상태): `active_standalone_mt5_runtime_probe_open(단독 MT5 런타임 탐침 활성)`
- current run(현재 실행): `run03C_et_standalone_mt5_runtime_probe_v1`
- source Python run(원천 파이썬 실행): `run03B_et_standalone_fwd12_v1`
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

효과(effect, 효과): Stage 12(12단계)는 단독 실험으로 유지되고, RUN03C(실행 03C)가 MT5 연결 근거를 담당한다.


## run03D standalone batch20 read(단독 20개 묶음 판독)

- run(실행): `run03D_et_standalone_batch20_v1`
- best structural variant(최상위 구조 변형): `v11_base_leaf20_q85`
- validation/OOS(검증/표본외): `0.392688` / `0.457317`
- judgment(판정): `inconclusive_standalone_batch20_structural_scout`
- MT5(`MetaTrader 5`, 메타트레이더5): `out_of_scope_by_claim`
- effect(효과): Stage12 단독 후보 압축은 가능하지만 운영 승격이나 런타임 권위는 주장하지 않는다.
