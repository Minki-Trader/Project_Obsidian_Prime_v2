# Frontier71B Economics-Native Proxy Scout(F71B 경제성 네이티브 프록시 탐색)

Updated(갱신): 2026-06-16T23:02:24Z

- stage(단계): `stage_frontier_71__economics_native_label_selection_for_joint_density_pf_dd`
- run(실행): `frontier71B_economics_native_proxy_scout_v1`
- status(상태): `completed_proxy_scout_scout_clue_repair_required_no_authority`
- judgment(판정): `proxy_scout_clue_without_meaningful_joint_gate_needs_repair_no_authority`
- claim boundary(주장 경계): `proxy_scout_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`

## Hypothesis(가설)

Economics-native lifecycle labels(경제성 네이티브 생명주기 라벨) and joint selection objectives(공동 선택 목표) can find a seed surface(씨앗 표면) that keeps density/PF/DD(밀도/수익 팩터/손실폭) together better than post-hoc threshold/tape repair(사후 임계값/테이프 수리).

Effect(효과): this run changes what is selected(무엇을 선택하는지) through label/target(라벨/목표), feature set(피처 묶음), model family(모델 계열), trade shape(거래 형태), and risk shape(위험 형태).

## Test Period(테스트 기간)

- period(기간): `2022-09-01 16:40:00+00:00` to `2026-04-13 22:00:00+00:00`
- split counts(분할 행 수): `{"oos": 7584, "train": 29222, "validation": 9844}`

## Proxy Expectation(프록시 예상)

- scout clue(탐색 단서): validation/OOS(검증/표본외) net>0, PF>=1.10, DD<=15%, trades/day>=1.
- meaningful candidate(의미 후보): validation/OOS(검증/표본외) PF>=1.20, DD<=10%, trades/day>=3.
- density lift fracture(밀도 상승 균열): relaxed density(완화 밀도)에서도 PF>=1.10, DD<=12%.

## Proxy KPI(프록시 핵심 성과 지표)

- candidates tested(시험 후보): `1620`
- scout clue count(탐색 단서 수): `9`
- meaningful candidate count(의미 후보 수): `0`
- meaningful with fracture count(밀도 균열 통과 의미 후보 수): `0`
- final-like reference-only count(최종 유사 참조 전용 수): `0`

## Top Proxy Row(상위 프록시 행)

- candidate(후보): `f71b_1e511d3db9c3`
- validation net/PF/DD/trades/day(검증 순수익/수익 팩터/손실폭/일거래): `1098.0743` / `1.2316` / `2.605` / `1.272`
- OOS net/PF/DD/trades/day(표본외 순수익/수익 팩터/손실폭/일거래): `899.1492` / `1.2505` / `3.5373` / `1.3129`
- label/feature/model/selection(라벨/피처/모델/선택): `econ_slow_payoff_first_hit_net_h18_tp105_sl70` / `econ_macro_context_v1` / `extratrees_shallow_v1` / `vol_expansion_q45`

## Runtime Probe KPI(런타임 탐침 핵심 성과 지표)

- status(상태): `pending_not_executed_in_f71b_proxy_scout(프록시 탐색에서는 대기)`.
- reason(이유): MT5 Runtime Probe(MT5 런타임 탐침)는 proxy signal(프록시 신호) 뒤 transfer check(전이 확인)로 실행한다.

## Proxy/Runtime Gap(프록시/런타임 간극)

- current(현재): `not_available_until_mt5_runtime_probe(MT5 런타임 탐침 전까지 없음)`.

## Tier Records(티어 기록)

- Tier A separate(Tier A 분리): completed proxy scout(프록시 탐색 완료).
- Tier B separate(Tier B 분리): missing_required(필수 누락).
- Tier A+B combined(Tier A+B 합산): out_of_scope_by_claim(주장 범위 밖).

## Next Action(다음 행동)

`frontier71C_economics_native_repair_recombine_proxy_v1`
