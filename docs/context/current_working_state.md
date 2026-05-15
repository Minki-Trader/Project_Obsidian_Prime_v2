# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `stage56_baseline_adapter_mt5_v1`
- current run(현재 실행): `run50BT_stage56_baseline_adapter_v64_mt5_v1`
- active stage(활성 단계): `56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection`
- selected_research_baseline(선택 연구 기준선): `none`
- development_anchor(개발 기준점): `v64_v47_ctxgap14_refill_etfw_h2_no_b`
- backup_anchor(예비 기준점): `v60_v47_et_stable_damage_firewall_h2c0_no_b`
- status(상태): `adapter_first_mt5_validation_oos_completed`
- claim_boundary(주장 경계): research/development only(연구/개발 전용)

Stage56(56단계)은 broad run50 candidate hunting(넓은 run50 후보 사냥)을 멈추고 BaselineAdapter MT5 validation/OOS(기준선 어댑터 MT5 검증/표본외)를 실제로 실행했다.
Effect(효과): 다음 작업은 새 후보 찾기가 아니라 adapter bottleneck(어댑터 병목)인 risk/ATR/cost/same-move(위험/ATR/비용/동일 이동) 수리다.

## Adapter MT5 Evidence(어댑터 MT5 근거)

- validation routed trades/day(검증 라우팅 일 거래): `9.644809`
- OOS routed trades/day(표본외 라우팅 일 거래): `6.794872`
- validation/OOS PF(검증/표본외 수익 팩터): `0.920000` / `1.210000`
- validation/OOS net(검증/표본외 순손익): `-465.96` / `2239.00`
- tier_b_policy(Tier B 정책): disabled(비활성), because prior fallback-only evidence(이전 대체 단독 근거)가 손상됨.

Forbidden claims(금지 주장): live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(운영 기준선), reviewed_closed(검토 종료).
