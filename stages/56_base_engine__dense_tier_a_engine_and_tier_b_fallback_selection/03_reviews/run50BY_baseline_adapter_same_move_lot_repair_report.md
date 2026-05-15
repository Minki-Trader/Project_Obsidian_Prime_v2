# Stage56 run50BY BaselineAdapter Repair Batch(Stage56 run50BY 기준선 어댑터 수리 배치)

- terminal_label(종료 라벨): `adapter_mt5_repair_completed`
- development_anchor(개발 기준점): `run50BR/v64_v47_ctxgap14_refill_etfw_h2_no_b`
- backup_anchor(예비 기준점): `run50BQ/v60_v47_et_stable_damage_firewall_h2c0_no_b`
- selected_research_baseline(선택 연구 기준선): `none`
- external_verification_status(외부 검증 상태): `completed`
- best_adapter(최선 어댑터): `ba14_no_atr_sd5_lot025`
- phase_a_eligible_for_onnx(Phase A ONNX 적격): `True`

Action(행동): first adapter(첫 어댑터)의 validation damage(검증 손상)를 `no_atr_same_direction_cooldown5_lot025(ba14_no_atr_sd5_lot025), no_atr_close_only_same_direction_cooldown3_lot025(ba15_no_atr_close_only_sd3_lot025), no_atr_close_only_same_direction_cooldown2_lot025(ba16_no_atr_close_only_sd2_lot025)` repair variants(수리 변형)로 실제 MT5 validation/OOS(검증/표본외)에서 나눠 실행했다.
Effect(효과): entry/route translation(진입/라우팅 번역), ATR bracket(ATR 브래킷), dynamic risk(동적 위험), cooldown/re-entry(쿨다운/재진입) 중 다음 repair branch(수리 갈래)를 좁힐 수 있다.

## References(참조)

| item(항목) | val day(검증 일거래) | OOS day(표본외 일거래) | val PF(검증 PF) | OOS PF(표본외 PF) | val net(검증 손익) | OOS net(표본외 손익) |
|---|---:|---:|---:|---:|---:|---:|
| development_anchor(개발 기준점) | 8.918033 | 6.358974 | 1.210000 | 1.220000 | 478.850000 | 397.640000 |
| backup_anchor(예비 기준점) | 9.617486 | 6.948718 | 1.180000 | 1.220000 | 462.210000 | 436.330000 |
| first_adapter(첫 어댑터) | 9.6448087432 | 6.7948717949 | 0.9200000000 | 1.2100000000 | -465.9600000000 | 2239.0000000000 |

## Repair Results(수리 결과)

| adapter(어댑터) | split(구간) | view(보기) | day(일거래) | PF | net(손익) | DD | cost exp(비용 기대값) | same move(동일 이동) | MFE | floor(바닥) | lot(랏) | SL | TP |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ba14_no_atr_sd5_lot025 | validation_is | tier_a_only | 7.420765 | 1.200000 | 1009.93 | 362.47 |  |  |  | 0.000000 | 0.052976 | 0.000000 | 0.000000 |
| ba14_no_atr_sd5_lot025 | validation_is | actual_routed_total | 7.420765 | 1.200000 | 1009.93 | 362.47 | 0.243689 | 0.326215 | 0.611745 | 0.000000 | 0.052976 | 0.000000 | 0.000000 |
| ba14_no_atr_sd5_lot025 | oos | tier_a_only | 5.200000 | 1.300000 | 1048.98 | 319.23 |  |  |  | 0.000000 | 0.051853 | 0.000000 | 0.000000 |
| ba14_no_atr_sd5_lot025 | oos | actual_routed_total | 5.200000 | 1.300000 | 1048.98 | 319.23 | 0.534497 | 0.349112 | 0.616732 | 0.000000 | 0.051853 | 0.000000 | 0.000000 |
| ba15_no_atr_close_only_sd3_lot025 | validation_is | tier_a_only | 7.076503 | 1.210000 | 896.10 | 343.89 |  |  |  | 0.000000 | 0.052976 | 0.000000 | 0.000000 |
| ba15_no_atr_close_only_sd3_lot025 | validation_is | actual_routed_total | 7.076503 | 1.210000 | 896.10 | 343.89 | 0.191969 | 0.328185 | 0.603542 | 0.000000 | 0.052976 | 0.000000 | 0.000000 |
| ba15_no_atr_close_only_sd3_lot025 | oos | tier_a_only | 5.056410 | 1.150000 | 561.82 | 312.84 |  |  |  | 0.000000 | 0.051853 | 0.000000 | 0.000000 |
| ba15_no_atr_close_only_sd3_lot025 | oos | actual_routed_total | 5.056410 | 1.150000 | 561.82 | 312.84 | 0.069797 | 0.358012 | 0.611317 | 0.000000 | 0.051853 | 0.000000 | 0.000000 |
| ba16_no_atr_close_only_sd2_lot025 | validation_is | tier_a_only | 7.202186 | 1.230000 | 993.73 | 340.65 |  |  |  | 0.000000 | 0.052976 | 0.000000 | 0.000000 |
| ba16_no_atr_close_only_sd2_lot025 | validation_is | actual_routed_total | 7.202186 | 1.230000 | 993.73 | 340.65 | 0.253968 | 0.336115 | 0.604673 | 0.000000 | 0.052976 | 0.000000 | 0.000000 |
| ba16_no_atr_close_only_sd2_lot025 | oos | tier_a_only | 5.148718 | 1.220000 | 768.02 | 328.15 |  |  |  | 0.000000 | 0.051853 | 0.000000 | 0.000000 |
| ba16_no_atr_close_only_sd2_lot025 | oos | actual_routed_total | 5.148718 | 1.220000 | 768.02 | 328.15 | 0.264960 | 0.374502 | 0.612942 | 0.000000 | 0.051853 | 0.000000 | 0.000000 |

## Phase A Gate(Phase A 게이트)

- phase_a_eligible_for_onnx(ONNX 적격): `True`
- failure_reasons(실패 사유): ``

## Diagnosis(진단)

- entry_translation_mismatch(진입 번역 불일치): `unlikely_if_control_reproduces_anchor_directionally`
- route_translation_mismatch(라우팅 번역 불일치): `unlikely; Tier B remains disabled and tier_a_only/routed paths share Tier A primary rows`
- tier_b_logic(Tier B 논리): `explicitly_disabled_due_prior_damage`
- risk_sizing(위험 크기): `first_adapter_dynamic_risk_changed lot exposure; repair batch disables dynamic risk to isolate`
- atr_bracket_behavior(ATR 브래킷 동작): `{"atr_fixed_lot_oos_net": null, "atr_fixed_lot_validation_net": null, "control_no_atr_oos_net": null, "control_no_atr_validation_net": null, "first_adapter": {"oos_net": "2239.0000000000", "validation_net": "-465.9600000000"}, "wide_atr_oos_net": null, "wide_atr_validation_net": null}`

## Next Branch(다음 갈래)

If Phase A fails(Phase A 실패 시), do not start ONNX(ONNX 시작 금지). Continue adapter repair(어댑터 수리 지속): keep the anchor(기준점 유지) only if the no-ATR control(ATR 없는 대조군) reproduces anchor quality(기준점 품질 재현); otherwise demote anchor(기준점 강등) and switch branch(갈래 전환).

No live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), reviewed_closed(검토 종료) claim(주장) is made.
