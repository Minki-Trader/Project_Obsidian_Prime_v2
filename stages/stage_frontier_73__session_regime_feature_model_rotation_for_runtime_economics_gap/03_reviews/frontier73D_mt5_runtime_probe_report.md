# Frontier73D MT5 Runtime Probe(F73D MT5 런타임 탐침)

Updated(갱신): 2026-06-17T02:29:28Z

- status(상태): `completed_mt5_runtime_probe_observation_no_authority`
- judgment(판정): `runtime_probe_completed_gap_analysis_required_no_authority`
- attempts(시도): `2`; completed(완료): `2`
- probability parity pass rows(확률 동등성 통과 행): `3`
- signal parity pass rows(신호 동등성 통과 행): `3`
- materialization_mode(물질화 방식): `bridge_3class_from_f73c_seed`
- model_family_used(사용 모델 계열): `small_nn_16`
- proxy_authority(프록시 권위): `none`
- claim_boundary(주장 경계): `runtime_probe_observation_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`

## Runtime KPI(런타임 핵심 성과 지표)

- best split(최선 분할): `oos`
- net/PF/DD/trades_day(순수익/수익 팩터/손실폭/일거래): `48.84` / `1.09` / `15.33` / `1.0102564102564102`
- expected signal/trade vs runtime signal/trade(예상 신호/거래 대 런타임 신호/거래): `332/332` vs `332/197`
- signal count diff(신호 수 차이): `0`; feature ready diff(피처 준비 차이): `0`
- gap cause(간극 원인): `trade_lifecycle_gap_after_signal_parity`

## Proxy/Bridge Boundary(프록시/연결 경계)

This run is bridge-derived runtime observation(연결 기반 런타임 관찰) only. Effect(효과): F73C binary proxy(이진 프록시)를 MT5에서 직접 재현했다고 말하지 않고, bridge_internal parity(연결 내부 동등성)와 proxy_bridge_delta(프록시-연결 차이)를 분리한다.

## Next Action(다음 행동)

`frontier73E_proxy_runtime_gap_analysis_or_repair_decision_v1`.
