# Input References

## 이전 단계 입력(Previous Inputs, 이전 입력)

- Stage 05(5단계) feature integrity audit(피처 무결성 감사): `stages/05_feature_integrity__formula_time_alignment_leakage_audit/02_runs/20260425_stage05_feature_integrity_audit_v1/audit_summary.json`
- Stage 05(5단계) result summary(결과 요약): `stages/05_feature_integrity__formula_time_alignment_leakage_audit/02_runs/20260425_stage05_feature_integrity_audit_v1/result_summary.md`
- `docs/contracts/mt5_ea_input_order_contract_fpmarkets_v2.md`
- `docs/contracts/runtime_parity_and_artifact_identity_contract_fpmarkets_v2.md`
- `docs/contracts/model_input_feature_set_contract_fpmarkets_v2.md`

## 현재 주의(Current Warning, 현재 주의)

현재 `foundation/mt5`의 old audit tool(낡은 감사 도구)은 58 feature(58개 피처)를 갖고 있지만 `placeholder_equal_weight(임시 동일가중)` 기준이다.

효과(effect, 효과): 그대로 runtime parity(런타임 동등성) 근거로 쓰면 안 된다.

## 선택된 Stage 05 입력(Selected Stage 05 Inputs, 선택된 Stage 05 입력)

- model input dataset(모델 입력 데이터셋): `model_input_fpmarkets_v2_us100_m5_label_v1_fwd12_split_v1_proxyw58_feature_set_v2`
- model input path(모델 입력 경로): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet`
- feature order hash(피처 순서 해시): `fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2`
- Stage 05 judgment(Stage 05 판정): `positive_feature_integrity_audit_passed`

효과(effect, 효과): Stage 06(6단계)은 feature integrity(피처 무결성)가 감사된 입력을 runtime parity(런타임 동등성) 대상으로 삼는다.
