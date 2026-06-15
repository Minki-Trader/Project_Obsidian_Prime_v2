# Local Verification(로컬 검증)

- feature_contract(피처 계약): raw 58 feature order(원천 58 피처 순서) hash(해시)를 사용.
- label_boundary(라벨 경계): stop/take threshold(손절/익절 문턱값)는 train split(학습 분할) quantile(분위수)에서만 계산.
- model_boundary(모델 경계): `f53b_logreg_l2_c05_short_q25_q70_s90_short_score3`는 F53에서 새로 학습했고 prior winner/baseline(과거 승자/기준선)을 상속하지 않았다.
- runtime_policy(런타임 정책): `{"InpAtrMaxStopPoints": 180.0, "InpAtrMaxTakeProfitPoints": 260.0, "InpAtrMinStopPoints": 40.0, "InpAtrMinTakeProfitPoints": 60.0, "InpAtrPeriod": 14, "InpAtrSltpEnabled": true, "InpAtrStopMultiplier": 0.8, "InpAtrTakeProfitMultiplier": 1.2, "InpCloseOnFlatSignal": true, "InpEntryTransitionOnly": false, "InpEntryTransitionRearmMinConfidenceDelta": 0.0, "InpMaxHoldBars": 6, "InpReentryCooldownBars": 0, "InpSameDirectionReentryCooldownBars": 0}`
- parity(동등성): ONNX(온엑스) score output(점수 출력)과 Python(파이썬) score(점수) max_abs_diff(최대 절대 차이)는 model_artifact_manifest(모델 산출물 목록)에 기록.
- judgment(판정): `negative_memory_path_quality_proxy_did_not_transfer_to_runtime(부정 기억, 경로 품질 프록시가 런타임으로 전이되지 않음)`
