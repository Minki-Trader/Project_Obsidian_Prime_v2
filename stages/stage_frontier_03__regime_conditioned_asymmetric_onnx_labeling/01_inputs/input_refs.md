# Frontier03 Input Refs(전선03 입력 참조)

## Current Truth(현재 진실)

- workspace_state(작업공간 상태): `docs/workspace/workspace_state.yaml`
- current_working_state(현재 작업 상태): `docs/context/current_working_state.md`
- Frontier02 closeout report(전선02 마감 보고서): `stages/stage_frontier_02__four_axis_joint_onnx_proxy_scout/03_reviews/frontier02F_stage_closeout_preserved_clue_negative_memory_v1_report.md`
- Frontier02 selection status(전선02 선택 상태): `stages/stage_frontier_02__four_axis_joint_onnx_proxy_scout/04_selected/selection_status.md`

## Data Identity(데이터 정체성)

- model input dataset(모델 입력 데이터셋): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet`
- dataset sha256(데이터셋 해시): `c30eb033f104f0b1682964b546593e8b18125760c37ce2b945f7ab0f447ae38f`
- feature order(피처 순서): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_feature_order.txt`
- feature order sha256(피처 순서 해시): `18c83876fe3c3a9f74d2a207cd236b1d746447af43108a5b554f2d54eea264cb`
- feature manifest(피처 목록): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/feature_set_manifest.json`
- model input summary(모델 입력 요약): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_summary.json`

## Archive Reference(보관 참조)

- Stage41 directional asymmetric labels(Stage41 방향 비대칭 라벨): `stage_pipelines/stage41/directional_asymmetric_label_horizon_probe.py`
- Stage347 cash-open asymmetric source(Stage347 현금장 개방 비대칭 원천): `stage_pipelines/stage347/design_cash_open_asymmetric_long_short_source_without_db.py`
- Stage364 evaluation/runtime boundary(Stage364 평가/런타임 경계): `stage_pipelines/stage364/train_timestamp_context_cost_filter_model_without_db.py`
- reusable label helper(재사용 라벨 헬퍼): `foundation/labels/directional_asymmetric.py`

Effect(효과): these are reference-only(참조 전용) inputs. They do not import winner/baseline/promotion authority(승자/기준선/승격 권위)를 만들지 않습니다.

## Grok Review(그록 검토)

- prompt(프롬프트): `docs/agent_control/grok_reviews/2026-06-14_frontier03_stage_open/medium_review/prompt.md`
- output(출력): `docs/agent_control/grok_reviews/2026-06-14_frontier03_stage_open/medium_review/clean_output.md`

Effect(효과): Frontier03(전선03)은 Frontier02(전선02)를 baseline(기준선)으로 상속하지 않고, dataset identity(데이터 정체성)와 preserved clue(보존 단서)만 참조합니다.
