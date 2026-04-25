# Input References

## 이전 단계 입력(Previous Inputs, 이전 입력)

- Stage 06(6단계) blocked runtime parity handoff(차단된 런타임 동등성 인계): `stages/06_runtime_parity__python_mt5_runtime_authority/02_runs/20260425_stage06_runtime_parity_blocked_v1/runtime_parity_report.json`
- Stage 04(4단계) 58 feature model input(58개 피처 모델 입력)
- Stage 05(5단계) audit reports(감사 보고서)
- `docs/policies/kpi_measurement_standard.md`
- `docs/policies/run_result_management.md`
- `docs/policies/result_judgment_policy.md`

## 필요 산출물(Needed Outputs, 필요 산출물)

- preprocessing policy(전처리 정책)
- training run contract(학습 실행 계약)
- smoke training report(스모크 학습 보고서)
- model artifact manifest(모델 산출물 목록)

## 현재 경계(Current Boundary, 현재 경계)

Stage 06(6단계)은 runtime authority(런타임 권위)를 닫지 않았다.

효과(effect, 효과): Stage 07(7단계)의 baseline smoke training(기준선 스모크 학습)은 Python-side reproducibility(파이썬 측 재현성)와 model artifact identity(모델 산출물 정체성)를 다룬다. MT5 live-like readiness(MT5 실거래 유사 준비)를 주장하지 않는다.
