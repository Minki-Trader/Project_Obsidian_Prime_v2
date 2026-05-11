# Stage56 Input Manifest(56단계 입력 목록)

- manifest_id(목록 ID): `stage56_input_manifest_v1`
- stage_id(단계 ID): `56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection`

## User Design Inputs(사용자 설계 입력)

- `C:/Users/awdse/OneDrive/문서/카카오톡 받은 파일/obsidian_v2_stage56_design_summary_2026-05-11.md`
- `C:/Users/awdse/OneDrive/문서/카카오톡 받은 파일/obsidian_v2_user_concern_summary_2026-05-11.md`

These are local advisory inputs(로컬 조언 입력) and are not copied into the repository as source-of-truth(진실 원천).

## Repository Evidence Inputs(저장소 근거 입력)

- `docs/workspace/workspace_state.yaml`
- `docs/context/current_working_state.md`
- `stages/55_adapter_routing__tier_b_fallback_side_filter_router/04_selected/selection_status.md`
- `docs/agent_control/packets/stage55_run49A_tier_b_fallback_side_filter_router_v1/aggregate_summary.json`
- `stages/10_alpha_scout__default_split_model_threshold_scan/03_reviews/stage_run_ledger.csv`
- `stages/16_model_family_challenge__qda_class_covariance_scout/03_reviews/stage_run_ledger.csv`
- `docs/agent_control/packets/stage18_run12A_catboost_characteristic_mt5_v1/aggregate_summary.json`
- `stages/36_model_selection__cross_model_characteristic_synthesis/02_runs/run30A/results/model_characteristic_matrix.csv`
- `stages/36_model_selection__cross_model_characteristic_synthesis/02_runs/run30A/results/selection_reference_matrix.csv`

## Data Integrity Boundary(데이터 무결성 경계)

The initial audit(초기 감사)는 existing evidence only(기존 근거 전용)이다. It does not create new MT5 runtime evidence(새 MT5 런타임 근거).

Validation/OOS period day estimates(검증/표본외 기간 일수 추정)는 Stage55(55단계) recent split metadata(최신 분할 메타데이터)인 validation(검증) `183` days(일), OOS(표본외) `195` days(일)를 density screening(밀도 선별)용으로 쓴다. 다음 MT5 run(메타트레이더5 실행)에서는 각 manifest(목록)에 실제 기간을 다시 고정한다.
