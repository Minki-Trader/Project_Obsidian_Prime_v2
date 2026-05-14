# Stage56 BaselineAdapter Transition(56단계 BaselineAdapter 전환)

- packet_id(작업 묶음 ID): `stage56_baseline_adapter_transition_v1`
- run_id(실행 ID): `run50BS_stage56_baseline_adapter_transition_v1`
- terminal_label(종료 라벨): `development_anchor_selected_and_adapter_development_started`
- selected_research_baseline(선택 연구 기준선): `none`
- development_anchor(개발 기준점): `v64_v47_ctxgap14_refill_etfw_h2_no_b` from `run50BR`
- backup_anchor(예비 기준점): `v60_v47_et_stable_damage_firewall_h2c0_no_b` from `run50BQ`
- claim_boundary(주장 경계): development only(개발 전용), no live readiness(실거래 준비 아님), no runtime authority(런타임 권위 아님), no operating promotion(운영 승격 아님)

## Decision(결정)

`v64_v47_ctxgap14_refill_etfw_h2_no_b`를 development_anchor(개발 기준점)로 고른다. 효과(effect, 효과)는 Stage56/run50 후보 사냥을 멈추고 BaselineAdapter(기준선 어댑터) 구현과 검증 루프로 들어가는 것이다.

엄격한 selected_research_baseline(선택 연구 기준선)은 아직 없다. cost-stressed expectancy(비용 압박 기대값)와 same-move density(동일 이동 밀도)가 실패했기 때문이다.

## Why This Anchor(선택 이유)

- actual routed MT5 validation/OOS(실제 라우팅 MT5 검증/표본외) trades/day(일 거래 수): `8.918033` / `6.358974`.
- validation/OOS PF(검증/표본외 수익 팩터): `1.210000` / `1.220000`, net(순손익): `478.850000` / `397.640000`.
- same-move ratio(동일 이동 비율): `0.465074` / `0.517742`로, higher-density(더 높은 밀도) 후보인 backup_anchor(예비 기준점)보다 낮다.
- cost-stressed expectancy(비용 압박 기대값): `-0.206587` / `-0.179323`로 아직 음수지만, adapter(어댑터)의 risk/ATR/lifecycle(위험/ATR/생명주기) 수리 대상으로 명확하다.
- Tier B fallback-only(티어 B 대체 단독)는 validation/OOS net(검증/표본외 순손익) `-94.140000` / `-254.320000`로 손상되어, 초기 adapter(어댑터)는 explicit Tier B disablement(명시적 Tier B 비활성)를 쓴다.

## Candidate Ranking(후보 순위)

| label | rank | run | variant | val day | OOS day | val PF | OOS PF | val net | OOS net | val/OOS cost stress | val/OOS same move | cooldown day val/OOS |
|---|---:|---|---|---:|---:|---:|---:|---:|---:|---|---|---|
| backup_anchor | 1 | run50BQ | `v60_v47_et_stable_damage_firewall_h2c0_no_b` | 9.617486 | 6.948718 | 1.180000 | 1.220000 | 462.210000 | 436.330000 | -0.237381/-0.177985 | 0.526136/0.578598 | 4.557377/2.928205 |
| reference_only | 2 | run50BN | `v47_v22_topup_plus_et40_slotfill_h2c0_no_b` | 9.748634 | 7.071795 | 1.170000 | 1.180000 | 446.110000 | 380.770000 | -0.249938/-0.223880 | 0.534753/0.586657 | 4.535519/2.923077 |
| development_anchor | 3 | run50BR | `v64_v47_ctxgap14_refill_etfw_h2_no_b` | 8.918033 | 6.358974 | 1.210000 | 1.220000 | 478.850000 | 397.640000 | -0.206587/-0.179323 | 0.465074/0.517742 | 4.770492/3.066667 |
| reference_only | 4 | run50BN | `v46_v22_midcov_plus_et40_slotfill_h2c0_no_b` | 9.595628 | 6.789744 | 1.130000 | 1.230000 | 337.280000 | 437.640000 | -0.307927/-0.169456 | 0.534169/0.578550 | 4.469945/2.861538 |
| reference_only | 5 | run50BQ | `v61_v47_et_firewall_h2_transition_no_b` | 9.415301 | 6.784615 | 1.150000 | 1.200000 | 359.900000 | 386.850000 | -0.291120/-0.207596 | 0.514219/0.557823 | 4.573770/3.000000 |
| reference_only | 6 | run50BO | `v50_topup_slotfill_sd2_h2c0_no_b` | 8.857923 | 6.420513 | 1.170000 | 1.190000 | 380.190000 | 342.920000 | -0.265460/-0.226102 | 0.494139/0.547125 | 4.480874/2.907692 |
| reference_only | 7 | run50BO | `v53_topup_slotfill_sd2_h3c0_no_b` | 8.666667 | 6.389744 | 1.100000 | 1.230000 | 339.860000 | 567.760000 | -0.285712/-0.044334 | 0.564313/0.588283 | 3.775956/2.630769 |
| reference_only | 8 | run50BO | `v52_topup_slotfill_sd4_h2c0_no_b` | 8.524590 | 6.189744 | 1.150000 | 1.220000 | 327.080000 | 384.180000 | -0.290333/-0.181707 | 0.469231/0.507871 | 4.524590/3.046154 |
| reference_only | 9 | run50BO | `v48_midcov_slotfill_sd2_h2c0_no_b` | 8.743169 | 6.205128 | 1.110000 | 1.250000 | 251.390000 | 424.170000 | -0.342881/-0.149446 | 0.491250/0.541322 | 4.448087/2.846154 |
| reference_only | 10 | run50BO | `v49_midcov_slotfill_sd3_h2c0_no_b` | 8.595628 | 6.153846 | 1.080000 | 1.270000 | 195.050000 | 458.130000 | -0.376001/-0.118225 | 0.479975/0.533333 | 4.469945/2.871795 |
| reference_only | 11 | run50BO | `v51_topup_slotfill_sd3_h2c0_no_b` | 8.715847 | 6.338462 | 1.140000 | 1.140000 | 331.720000 | 265.130000 | -0.292025/-0.285494 | 0.482132/0.538026 | 4.513661/2.928205 |
| reference_only | 12 | run50BR | `v66_v47_badctxgap24_refill_etfw_h2_no_b` | 8.672131 | 6.256410 | 1.100000 | 1.180000 | 228.280000 | 312.010000 | -0.356156/-0.244254 | 0.493384/0.535246 | 4.393443/2.907692 |
| failure_memory | 16 | run50BD | `v25_w40_esol_highcov_lr2_h2c0_with_b` | 8.923497 | 5.784615 | 1.140000 | 0.970000 | 276.210000 | -43.280000 | -0.330857/-0.538369 | 0.287201/0.266844 | 6.360656/4.241026 |
| failure_memory | 20 | run50BD | `v21_w40_esol_highcov_lr2_h2c0_no_b` | 7.245902 | 5.015385 | 1.260000 | 0.940000 | 485.290000 | -99.350000 | -0.134020/-0.601585 | 0.192308/0.194274 | 5.852459/4.041026 |
| failure_memory | 23 | run50BE | `v29_v22_slot3_5_8_relax_h2c0_no_b` | 7.158470 | 4.953846 | 1.260000 | 0.980000 | 499.710000 | -30.710000 | -0.118542/-0.531791 | 0.191603/0.195652 | 5.786885/3.984615 |
| failure_memory | 24 | run50BE | `v28_v22_slot5_8_relax_h2c0_no_b` | 7.071038 | 4.825641 | 1.280000 | 0.970000 | 516.320000 | -45.130000 | -0.100989/-0.547960 | 0.187790/0.189160 | 5.743169/3.912821 |
| failure_memory | 25 | run50BD | `v24_w45_elos_highcov_lr2_h2c0_no_b` | 6.797814 | 4.625641 | 1.320000 | 0.820000 | 567.150000 | -279.390000 | -0.044092/-0.809745 | 0.134244/0.105322 | 5.885246/4.138462 |
| failure_memory | 26 | run50BD | `v23_w40_elos_highcov_lr2_h2c0_no_b` | 7.781421 | 5.441026 | 1.150000 | 0.950000 | 321.060000 | -86.680000 | -0.274537/-0.581697 | 0.215590/0.189444 | 6.103825/4.410256 |

## Required Comparisons(필수 비교)

| reference | run | variant | val day | OOS day | val PF | OOS PF | val net | OOS net | read |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| development_anchor | run50BR | `v64_v47_ctxgap14_refill_etfw_h2_no_b` | 8.918033 | 6.358974 | 1.210000 | 1.220000 | 478.850000 | 397.640000 | development_anchor |
| backup_anchor | run50BQ | `v60_v47_et_stable_damage_firewall_h2c0_no_b` | 9.617486 | 6.948718 | 1.180000 | 1.220000 | 462.210000 | 436.330000 | backup_anchor |
| prior ExtraTrees anchor | run50BH | `et40h6_r001_a` | 6.846995 | 5.102564 | 1.100000 | 1.260000 | 313.490000 | 613.580000 | reference_only |
| QDA density branch | run50AU | `qda85_s800_flat_trans_r030_h6` | 6.726776 | 4.405128 | 1.060000 | 1.070000 | 165.430000 | 142.010000 | reference_only |
| d38h10 reference | run50C | `d38h10` | 4.464481 | 3.446154 | 1.070000 | 1.130000 | 190.380000 | 302.100000 | reference_only |
| d390h10 reference | run50D | `d390h10` | 4.087432 | 3.046154 | 1.130000 | 1.120000 | 341.540000 | 273.200000 | reference_only |
| Stage34 34D reference | run28D | `frequency_floor_rule_summary` | NA | NA | NA | NA | NA | NA | thin modifier clue(얇은 보정 단서), not adapter anchor(어댑터 기준점 아님) |

## Reference And Failure Memory(참고와 실패 기억)

- backup_anchor(예비 기준점): `run50BQ/v60_v47_et_stable_damage_firewall_h2c0_no_b`. 효과(effect, 효과)는 밀도와 PF/net(수익 팩터/순손익)이 가장 강한 대체 축을 보존하는 것이다.
- reference_only(참고 전용): `run50BN/v47`, `run50BO/v52`, `run50BH/et40h6_r001_a`, `run50AU/QDA`, `run50D/d390h10`, `run50C/d38h10`. 효과(effect, 효과)는 adapter(어댑터) 결과를 과거 밀도/품질/LogReg(로지스틱 회귀) 기준과 비교할 수 있게 하는 것이다.
- Stage34 34D reference(34단계 34D 참고): `run28D` frequency-floor(거래 빈도 하한) 기억은 thin modifier clue(얇은 보정 단서)다. 효과(effect, 효과)는 BaselineAdapter(기준선 어댑터)에서 entry-time proxy(진입 시간 대리)를 주력으로 오해하지 않게 하는 것이다.
- failure_memory(실패 기억): microcooldown(짧은 쿨다운), leaf same-direction polishing(잎 단위 동일 방향 미세조정), bad context gap(나쁜 문맥 간격), broad cooldown12 source(넓은 12봉 쿨다운 원천)는 새 이유 없이 반복하지 않는다.

## BaselineAdapter Start(기준선 어댑터 시작)

- entry decision(진입 결정): anchor(기준점)의 `stage56_context_gap_refill_signal`을 우선 재현한다.
- routing(라우팅): 초기값은 Tier A primary with explicit Tier B disablement(Tier A 우선 + 명시적 Tier B 비활성)이다.
- risk(위험): model-controlled risk_per_trade(모델 제어 거래당 위험), cap(상한) `5%`, min lot floor(최소 랏 바닥) `0.01`을 기록한다.
- ATR/bracket(ATR/브래킷): 초기 계약은 ATR(평균진폭) 14, SL(손절) 1.5, TP(익절) 2.0, hold(보유) 2봉이다.
- telemetry(텔레메트리): model_risk_pct, clipped_risk_pct, computed_lot, executed_lot, min_lot_floor_applied, actual_risk_pct_after_floor를 필수 기록한다.
- ONNX-compatible output(ONNX 호환 출력): 출력 경로만 정의하고, ONNX hardening(ONNX 경화)은 MT5 adapter validation/OOS(어댑터 검증/표본외) 뒤로 미룬다.

## First MT5 Handoff(첫 MT5 인계)

이번 작업은 adapter scaffold(어댑터 뼈대)와 first-run handoff plan(첫 실행 인계 계획)까지 만든다. 효과(effect, 효과)는 다음 회차에서 broad candidate hunting(넓은 후보 사냥)이 아니라 BaselineAdapter(기준선 어댑터) validation/OOS(검증/표본외)를 바로 실행하게 하는 것이다.
