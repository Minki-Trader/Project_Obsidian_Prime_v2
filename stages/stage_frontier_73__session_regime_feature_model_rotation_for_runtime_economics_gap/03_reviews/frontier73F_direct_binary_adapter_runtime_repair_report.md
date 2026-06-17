# Frontier73F Direct Binary Adapter Runtime Repair(F73F 직접 이진 어댑터 런타임 수리)

Updated(갱신): 2026-06-17T02:51:06Z

- status(상태): `completed_direct_binary_adapter_runtime_repair_observation_no_authority`
- judgment(판정): `direct_binary_adapter_runtime_repair_completed_gap_or_closeout_required_no_authority`
- attempts(시도): `2`; completed(완료): `2`
- probability parity pass rows(확률 동등성 통과 행): `3`
- signal parity pass rows(신호 동등성 통과 행): `3`
- source reproduction min overlap(원천 재현 최소 중복): `1.0`
- export_status(내보내기 상태): `direct_binary_adapter_parity_passed`
- claim_boundary(주장 경계): `direct_binary_adapter_runtime_repair_observation_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`

## Runtime KPI(런타임 핵심 성과 지표)

- best split(최선 분할): `oos`
- net/PF/DD/trades_day(순수익/수익 팩터/손실폭/일거래): `88.88` / `1.32` / `5.16` / `0.6307692307692307`
- expected signal/trade vs runtime signal/trade(예상 신호/거래 대 런타임 신호/거래): `195/195` vs `195/123`
- signal/feature diff(신호/피처 차이): `0` / `0`
- gap cause(간극 원인): `trade_lifecycle_gap_after_signal_parity`

## Proxy Reproduction(프록시 재현)

- source_candidate_id(원천 후보 ID): `f73c_0002`
- graph patch schema(그래프 패치 스키마): `[p_short=0,p_flat,p_long]`
- threshold(임계값): `0.4489733874797821`
- patched_onnx_sha256(패치 ONNX 해시): `0b89a81c0be43a7fdc2b598815875c88a43deb0c8446e7826c9812ebaffa5d00`

Effect(효과): F73C binary signal(이진 신호)을 3-column ONNX output(3열 ONNX 출력)으로 직접 연결해서 bridge divergence(연결 분기)를 제거했고, 남는 간극이 lifecycle/execution economics(생명주기/실행 경제성)인지 확인한다.

## Next Action(다음 행동)

`frontier73G_direct_binary_adapter_gap_or_closeout_decision_v1`.
