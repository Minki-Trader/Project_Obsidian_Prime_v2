# Frontier14C Contrastive Flat Budget Repair(프론티어14C 대비 평면예산 수리)

Updated(갱신): 2026-06-14T01:26:27Z

Status(상태): `density_transfer_preserved_clue_ready_for_closeout_no_authority`

Judgment(판정): `preserved_clue_candidate(보존 단서 후보)`

Action(행동): F14B(F14B)의 quota label(할당량 라벨)과 hold(보유기간)는 유지하고, plain logistic ONNX(평범 로지스틱 온엑스)의 train subset(학습 부분 표본)만 safest flat rows(가장 안전한 평면 행)로 제한했습니다.

Effect(효과): label-side density(라벨 쪽 밀도)는 그대로 두고, 모델이 기회 라벨을 너무 적게 전달하던 문제만 분리해서 시험했습니다.

## Result Summary(결과 요약)

- candidate rows(후보 행): `9`
- strict scout clue rows(엄격 탐색 단서 행): `0`
- preserved clue rows(보존 단서 행): `5`
- best candidate(최고 후보): `f14b_cash_q8_h8__flat8x_safest__lr_plain`
- validation PF/density/DD(검증 수익 팩터/밀도/손실폭): `0.709064` / `0.0983607` / `6.75478%`
- OOS PF/density/DD(표본밖 수익 팩터/밀도/손실폭): `3.35673` / `0.0687023` / `0.388877%`
- worst subperiod DD(최악 하위기간 손실폭): `6.72419%`

## Parent Comparison(부모 비교)

- F14B best(F14B 최고): `f14b_cash_q8_h8__lr_plain`
- F14B validation/OOS density(F14B 검증/표본밖 밀도): `0.0983607` / `0.0687023`
- F14C validation/OOS density(F14C 검증/표본밖 밀도): `0.0983607` / `0.0687023`

## Artifacts(산출물)

- candidate summary(후보 요약): `stages/stage_frontier_14__daily_session_opportunity_budget_onnx_scout/02_runs/frontier14C_contrastive_flat_budget_density_transfer_repair_v1/candidate_summary.csv`
- training subset diagnostics(학습 부분 표본 진단): `stages/stage_frontier_14__daily_session_opportunity_budget_onnx_scout/02_runs/frontier14C_contrastive_flat_budget_density_transfer_repair_v1/training_subset_diagnostics.csv`
- label/model density gap(라벨/모델 밀도 격차): `stages/stage_frontier_14__daily_session_opportunity_budget_onnx_scout/02_runs/frontier14C_contrastive_flat_budget_density_transfer_repair_v1/label_model_density_gap.csv`
- ONNX parity(온엑스 동등성): `stages/stage_frontier_14__daily_session_opportunity_budget_onnx_scout/02_runs/frontier14C_contrastive_flat_budget_density_transfer_repair_v1/onnx_parity.csv`
- run manifest(실행 목록): `stages/stage_frontier_14__daily_session_opportunity_budget_onnx_scout/02_runs/frontier14C_contrastive_flat_budget_density_transfer_repair_v1/run_manifest.json`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
