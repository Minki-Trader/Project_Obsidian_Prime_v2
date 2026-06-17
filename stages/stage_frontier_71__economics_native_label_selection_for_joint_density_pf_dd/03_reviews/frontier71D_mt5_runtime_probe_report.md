# Frontier71D MT5 Runtime Probe(F71D MT5 런타임 탐침)

Updated(갱신): 2026-06-16T23:24:33Z

- candidate(후보): `f71b_1e511d3db9c3`
- status(상태): `completed_mt5_runtime_probe_observation_no_authority`
- judgment(판정): `runtime_probe_completed_gap_analysis_required_no_authority`
- claim boundary(주장 경계): `runtime_probe_observation_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`

## Grok Review(그록 검토)

- prompt(프롬프트): `docs/agent_control/grok_reviews/2026-06-17_f71_pre_mt5_runtime_probe_economics_native_scout/prompts/f71_pre_mt5_runtime_probe_economics_native_scout_prompt.md`
- output(출력): `docs/agent_control/grok_reviews/2026-06-17_f71_pre_mt5_runtime_probe_economics_native_scout/outputs/clean_output.md`
- classification(분류): `accepted_primary_f71b_probe_rejected_default_repair_again_needs_local_verification_for_materialization(1차 F71B 탐침 수용, 기본 추가수리 거절, 물질화 로컬 검증 필요)`

## Runtime KPI(런타임 핵심 성과 지표)

| split(분할) | net(순수익) | PF(수익 팩터) | DD%(손실폭) | trades(거래) | trades/day(일거래) | expected signals(예상 신호) | signal diff(신호 차이) | feature diff(피처 차이) | gap cause(간극 원인) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `validation` | `24.43` | `0` | `0.78` | `1` | `0.0037` | `345` | `-344` | `0` | `signal_count_gap` |
| `oos` | `0.65` | `1.11` | `2.49` | `2` | `0.0103` | `256` | `-254` | `0` | `signal_count_gap` |

## Next Action(다음 행동)

`frontier71E_proxy_runtime_gap_analysis_and_repair_decision_v1`
