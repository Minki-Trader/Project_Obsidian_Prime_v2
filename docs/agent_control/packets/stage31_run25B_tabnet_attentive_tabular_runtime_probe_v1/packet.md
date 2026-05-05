# run25B Runtime Probe Packet(run25B 런타임 탐침 묶음)

## Judgment(판정)

- run(실행): `run25B_tabnet_attentive_tabular_runtime_probe_v1`
- status(상태): `reviewed_runtime_probe_completed`
- judgment(판정): `inconclusive_stage31_runtime_probe_completed`
- external verification(외부 검증): `completed`
- selected variant(선택 변형): `v02_sparse_mask_top20_logistic_proxy`
- boundary(경계): `stage31_exploration_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`

효과(effect, 효과): Stage31(31단계) topic surface(주제 표면)를 MT5 score-table handoff(MT5 점수표 인계)로 관찰한다. native package runtime authority(원본 패키지 런타임 권위)는 주장하지 않는다.

## MT5 KPI(MT5 핵심 성과 지표)

- attempts(시도): `6` / `6`
- MT5 KPI records(MT5 핵심 성과 지표 기록): `10` / `10`
- normalized records(정규화 기록): `6`
- parser errors(파서 오류): `0`
- trade parser errors(거래 파서 오류): `0`

| split(분할) | net profit(순수익) | profit factor(수익 팩터) | trades(거래 수) | max DD(최대 손실) |
|---|---:|---:|---:|---:|
| validation routed(검증 라우팅) | `25.38` | `1.02` | `525` | `282.36` |
| OOS routed(표본외 라우팅) | `-134.86` | `0.89` | `438` | `208.84` |

## Runtime Parity(런타임 동등성)

- Tier A score table parity(Tier A 점수표 동등성): `True`
- Tier B score table parity(Tier B 점수표 동등성): `True`
- known runtime difference(알려진 런타임 차이): original run note(원래 실행 기록) `MT5 runtime_probe(MT5 런타임 탐침)는 native package runtime(원본 패키지 런타임)이 아니라 distilled score-table handoff(증류 점수표 인계)다. torch/pytorch_tabnet(파이토치/파이토치 탭넷) missing; sparse feature-mask proxy(희소 피처 마스크 대체) used and native TabNet retry condition recorded.` Later supplement(이후 보강): `run25C/run25D` native TabNet(원본 탭넷) 재검증 완료.

Forbidden claims(금지 주장): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위).
