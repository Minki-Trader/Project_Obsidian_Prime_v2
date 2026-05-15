# Stage56 run50BU BaselineAdapter Repair Batch(Stage56 run50BU 기준선 어댑터 수리 배치)

- terminal_label(종료 라벨): `adapter_mt5_repair_completed`
- development_anchor(개발 기준점): `run50BR/v64_v47_ctxgap14_refill_etfw_h2_no_b`
- backup_anchor(예비 기준점): `run50BQ/v60_v47_et_stable_damage_firewall_h2c0_no_b`
- selected_research_baseline(선택 연구 기준선): `none`
- external_verification_status(외부 검증 상태): `completed`
- best_adapter(최선 어댑터): `ba02_control_no_atr_fixed_lot`
- phase_a_eligible_for_onnx(Phase A ONNX 적격): `False`

Action(행동): first adapter(첫 어댑터)의 validation damage(검증 손상)를 no-ATR control(ATR 없는 대조군), ATR fixed-lot(ATR 고정 랏), wide-ATR fixed-lot(넓은 ATR 고정 랏)으로 실제 MT5 validation/OOS(검증/표본외)에서 나눠 실행했다.
Effect(효과): entry/route translation(진입/라우팅 번역) 문제인지, ATR bracket(ATR 브래킷) 문제인지, dynamic risk(동적 위험) 문제인지 다음 repair branch(수리 갈래)를 좁힐 수 있다.

## References(참조)

| item(항목) | val day(검증 일거래) | OOS day(표본외 일거래) | val PF(검증 PF) | OOS PF(표본외 PF) | val net(검증 손익) | OOS net(표본외 손익) |
|---|---:|---:|---:|---:|---:|---:|
| development_anchor(개발 기준점) | 8.918033 | 6.358974 | 1.210000 | 1.220000 | 478.850000 | 397.640000 |
| backup_anchor(예비 기준점) | 9.617486 | 6.948718 | 1.180000 | 1.220000 | 462.210000 | 436.330000 |
| first_adapter(첫 어댑터) | 9.6448087432 | 6.7948717949 | 0.9200000000 | 1.2100000000 | -465.9600000000 | 2239.0000000000 |

## Repair Results(수리 결과)

| adapter(어댑터) | split(구간) | view(보기) | day(일거래) | PF | net(손익) | DD | cost exp(비용 기대값) | same move(동일 이동) | MFE | floor(바닥) | lot(랏) | SL | TP |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ba02_control_no_atr_fixed_lot | validation_is | tier_a_only | 8.918033 | 1.190000 | 448.13 | 147.10 |  |  |  | 0.000000 | 0.021191 | 0.000000 | 0.000000 |
| ba02_control_no_atr_fixed_lot | validation_is | actual_routed_total | 8.918033 | 1.190000 | 448.13 | 147.10 | -0.225411 | 0.465074 | 0.606496 | 0.000000 | 0.021191 | 0.000000 | 0.000000 |
| ba02_control_no_atr_fixed_lot | oos | tier_a_only | 6.358974 | 1.200000 | 370.74 | 157.18 |  |  |  | 0.000000 | 0.020741 | 0.000000 | 0.000000 |
| ba02_control_no_atr_fixed_lot | oos | actual_routed_total | 6.358974 | 1.200000 | 370.74 | 157.18 | -0.201016 | 0.517742 | 0.619639 | 0.000000 | 0.020741 | 0.000000 | 0.000000 |
| ba03_atr_fixed_lot | validation_is | tier_a_only | 9.644809 | 1.060000 | 139.24 | 141.71 |  |  |  | 0.000000 | 0.021191 | 5451.60 | 7268.80 |
| ba03_atr_fixed_lot | validation_is | actual_routed_total | 9.644809 | 1.060000 | 139.24 | 141.71 | -0.421110 | 0.464589 | 0.623806 | 0.000000 | 0.021191 | 5451.60 | 7268.80 |
| ba03_atr_fixed_lot | oos | tier_a_only | 6.794872 | 1.200000 | 358.26 | 152.09 |  |  |  | 0.000000 | 0.020741 | 5855.05 | 7806.73 |
| ba03_atr_fixed_lot | oos | actual_routed_total | 6.794872 | 1.200000 | 358.26 | 152.09 | -0.229615 | 0.509434 | 0.642758 | 0.000000 | 0.020741 | 5855.05 | 7806.73 |
| ba04_wide_atr_fixed_lot | validation_is | tier_a_only | 9.229508 | 1.080000 | 201.65 | 149.29 |  |  |  | 0.000000 | 0.021191 | 9085.99 | 12720.39 |
| ba04_wide_atr_fixed_lot | validation_is | actual_routed_total | 9.229508 | 1.080000 | 201.65 | 149.29 | -0.380610 | 0.448194 | 0.613961 | 0.000000 | 0.021191 | 9085.99 | 12720.39 |
| ba04_wide_atr_fixed_lot | oos | tier_a_only | 6.553846 | 1.200000 | 366.82 | 103.68 |  |  |  | 0.000000 | 0.020741 | 9758.41 | 13661.78 |
| ba04_wide_atr_fixed_lot | oos | actual_routed_total | 6.553846 | 1.200000 | 366.82 | 103.68 | -0.212973 | 0.492175 | 0.634981 | 0.000000 | 0.020741 | 9758.41 | 13661.78 |

## Phase A Gate(Phase A 게이트)

- phase_a_eligible_for_onnx(ONNX 적격): `False`
- failure_reasons(실패 사유): `validation_cost_stressed_expectancy_not_positive;oos_cost_stressed_expectancy_not_positive`

## Diagnosis(진단)

- entry_translation_mismatch(진입 번역 불일치): `unlikely_if_control_reproduces_anchor_directionally`
- route_translation_mismatch(라우팅 번역 불일치): `unlikely; Tier B remains disabled and tier_a_only/routed paths share Tier A primary rows`
- tier_b_logic(Tier B 논리): `explicitly_disabled_due_prior_damage`
- risk_sizing(위험 크기): `first_adapter_dynamic_risk_changed lot exposure; repair batch disables dynamic risk to isolate`
- atr_bracket_behavior(ATR 브래킷 동작): `{"atr_fixed_lot_oos_net": 358.26, "atr_fixed_lot_validation_net": 139.24, "control_no_atr_oos_net": 370.74, "control_no_atr_validation_net": 448.13, "first_adapter": {"oos_net": "2239.0000000000", "validation_net": "-465.9600000000"}, "wide_atr_oos_net": 366.82, "wide_atr_validation_net": 201.65}`

## Next Branch(다음 갈래)

If Phase A fails(Phase A 실패 시), do not start ONNX(ONNX 시작 금지). Continue adapter repair(어댑터 수리 지속): keep the anchor(기준점 유지) only if the no-ATR control(ATR 없는 대조군) reproduces anchor quality(기준점 품질 재현); otherwise demote anchor(기준점 강등) and switch branch(갈래 전환).

No live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), reviewed_closed(검토 종료) claim(주장) is made.
