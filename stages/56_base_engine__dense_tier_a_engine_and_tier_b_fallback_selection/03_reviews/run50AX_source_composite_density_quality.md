# Stage56 run50AX Source Composite Density Quality(원천 합성 밀도 품질)

- run_id(실행 ID): `run50AX_stage56_source_composite_density_quality_v1`
- packet_id(묶음 ID): `stage56_run50AX_source_composite_density_quality_v1`
- selected_research_baseline(선택 연구 기준선): `none`
- external_verification_status(외부 검증 상태): `completed`
- claim_boundary(주장 경계): `research_baseline_selection_only_no_operating_claim`

Action(행동): run50AW(실행50AW)의 independent source(독립 원천) 두 개를 composite signal(합성 신호)로 묶어 실제 MT5 routed path(라우팅 경로)에서 시험했다.
Effect(효과): 단일 원천의 OOS density(표본외 밀도) 병목이 source union/filter(원천 합산/필터)로 완화되는지 확인한다.

## Best Read(최선 판독)

- best_variant(최선 변형): `v02_s45_primary_s47_flatfill_h4c6`
- validation/OOS trades/day(검증/표본외 일 거래): `7.770492` / `5.046154`
- validation/OOS PF(검증/표본외 수익 팩터): `1.010000` / `1.020000`
- validation/OOS net(검증/표본외 순손익): `34.380000` / `34.010000`
- failure_reasons(실패 사유): `validation_pf;oos_pf;cost_stressed_expectancy;same_move_density`

## Variant Summary(변형 요약)

| variant | mode | val day | oos day | val PF | oos PF | val net | oos net | failures |
|---|---|---:|---:|---:|---:|---:|---:|---|
| v02_s45_primary_s47_flatfill_h4c6 | primary_flatfill | 7.770492 | 5.046154 | 1.010000 | 1.020000 | 34.380000 | 34.010000 | validation_pf;oos_pf;cost_stressed_expectancy;same_move_density |
| v01_s47_primary_s45_flatfill_h4c6 | primary_flatfill | 7.606557 | 4.948718 | 1.010000 | 1.000000 | 26.960000 | 3.140000 | oos_density;validation_pf;oos_pf;cost_stressed_expectancy;same_move_density |
| v03_s47_s45_no_conflict_union_h3c6 | no_conflict_union | 7.224044 | 4.574359 | 1.040000 | 0.850000 | 80.110000 | -288.97 | oos_density;oos_net_positive;validation_pf;oos_pf;cost_stressed_expectancy;same_move_density |
| v04_s47_s45_agreement_only_h4c3 | agreement_only | 2.595628 | 1.661538 | 1.100000 | 1.220000 | 113.26 | 160.52 | validation_density;oos_density;cost_stressed_expectancy;same_move_density |

## Audit Summary(감사 요약)

| variant | split | MFE capture | same move | cooldown day | cost-stressed exp |
|---|---|---:|---:|---:|---:|
| v01_s47_primary_s45_flatfill_h4c6 | validation_is | 0.567187 | 0.516523 | 3.677596 | -0.480632 |
| v01_s47_primary_s45_flatfill_h4c6 | oos | 0.588645 | 0.553368 | 2.210256 | -0.496746 |
| v02_s45_primary_s47_flatfill_h4c6 | validation_is | 0.562854 | 0.521097 | 3.721311 | -0.475823 |
| v02_s45_primary_s47_flatfill_h4c6 | oos | 0.579995 | 0.558943 | 2.225641 | -0.465437 |
| v03_s47_s45_no_conflict_union_h3c6 | validation_is | 0.590707 | 0.503026 | 3.590164 | -0.439402 |
| v03_s47_s45_no_conflict_union_h3c6 | oos | 0.609845 | 0.535874 | 2.123077 | -0.823957 |
| v04_s47_s45_agreement_only_h4c3 | validation_is | 0.649082 | 0.216842 | 2.032787 | -0.261558 |
| v04_s47_s45_agreement_only_h4c3 | oos | 0.632755 | 0.191358 | 1.343590 | -0.004568 |

Judgment(판정): `in_progress_no_selected_research_baseline`.
Effect(효과): run50AX(실행50AX)는 progress evidence(진행 근거)이고 Stage56(56단계)은 계속 open(열림)이다.
