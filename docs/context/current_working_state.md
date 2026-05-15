# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `stage56_baseline_adapter_onnx_runtime_reproduction_v1`
- current_run(현재 실행): `run50CA_stage56_baseline_adapter_onnx_runtime_reproduction_v1`
- active_stage(활성 단계): `56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection`
- selected_research_baseline(선택 연구 기준선): `none`
- development_anchor(개발 기준점): `v64_v47_ctxgap14_refill_etfw_h2_no_b`
- backup_anchor(예비 기준점): `v60_v47_et_stable_damage_firewall_h2c0_no_b`
- status(상태): `mt5_runtime_reproduction_attempted`
- claim_boundary(주장 경계): research/development only(연구/개발 전용)

Stage56(56단계)은 BaselineAdapter ONNX runtime reproduction(기준선 어댑터 ONNX 런타임 재현)을 진행했다.
Effect(효과): Python adapter(Python 어댑터)와 ONNX runtime(ONNX 런타임)이 같은 MT5 tester account path(MT5 테스터 계좌 경로)에서 재현되는지 확인한다.

## Latest Runtime Evidence(최신 런타임 근거)

- adapter_id(어댑터 ID): `ba14_no_atr_sd5_lot025`
- runtime_gate_passed(런타임 게이트 통과): `True`
- validation/OOS trades/day(검증/표본외 일 거래 수): `7.420765` / `5.200000`
- validation/OOS PF(검증/표본외 수익 팩터): `1.200000` / `1.300000`
- validation/OOS net(검증/표본외 순손익): `1009.93` / `1048.98`
- validation/OOS drawdown(검증/표본외 손실폭): `362.47` / `319.23`
- validation/OOS same_move(검증/표본외 동일 이동): `0.326215` / `0.349112`
- risk_floor(위험 바닥): validation/OOS `0.000000` / `0.000000`
- ATR SL/TP(ATR 손절/익절): disabled(비활성), open points(개설 포인트) `0.000000` / `0.000000`
- failure_reasons(실패 사유): ``

Forbidden claims(금지 주장): live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), reviewed_closed(검토 종료).
