# Selection Status

## 현재 판독(Current Read, 현재 판독)

- stage(단계): `05_feature_integrity__formula_time_alignment_leakage_audit`
- status(상태): `reviewed_closed_handoff_to_stage06_complete`
- current operating reference(현재 운영 기준): `none`

## 선택된 근거(Selected Evidence, 선택 근거)

- run_id(실행 ID): `20260425_stage05_feature_integrity_audit_v1`
- judgment(판정): `positive_feature_integrity_audit_passed`
- run path(실행 경로): `stages/05_feature_integrity__formula_time_alignment_leakage_audit/02_runs/20260425_stage05_feature_integrity_audit_v1`
- audit summary(감사 요약): `stages/05_feature_integrity__formula_time_alignment_leakage_audit/02_runs/20260425_stage05_feature_integrity_audit_v1/audit_summary.json`
- result summary(결과 요약): `stages/05_feature_integrity__formula_time_alignment_leakage_audit/02_runs/20260425_stage05_feature_integrity_audit_v1/result_summary.md`

## 감사 결과(Audit Result, 감사 결과)

- model input dataset(모델 입력 데이터셋): `model_input_fpmarkets_v2_us100_m5_label_v1_fwd12_split_v1_proxyw58_feature_set_v2`
- model input path(모델 입력 경로): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet`
- feature order hash(피처 순서 해시): `fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2`
- feature frame rows(피처 프레임 행): `54439`
- model input rows(모델 입력 행): `46650`
- formula audit(공식 감사): `pass(통과)`
- time/session audit(시간/세션 감사): `pass(통과)`
- external alignment audit(외부 정렬 감사): `pass(통과)`
- label leakage audit(라벨 누수 감사): `pass(통과)`
- weight boundary(가중치 경계): `MT5 price-proxy weights(MT5 가격 대리 가중치)`, not actual NDX/QQQ weights(실제 NDX/QQQ 가중치 아님)

## 인계(Handoff, 인계)

Stage 06(6단계) `06_runtime_parity__python_mt5_runtime_authority`로 넘긴다.

효과(effect, 효과): 이제 같은 58 feature(58개 피처) 입력을 Python/MT5 parity(파이썬/MT5 동등성)와 runtime authority(런타임 권위) 질문으로 검증할 수 있다.

## 경계(Boundary, 경계)

이 문서는 Stage 05(5단계) feature integrity audit(피처 무결성 감사) 폐쇄 상태다.

아직 model training(모델 학습), alpha-ready(알파 준비 완료), model-ready(모델 준비 완료), runtime authority(런타임 권위), operating promotion(운영 승격)을 뜻하지 않는다.
