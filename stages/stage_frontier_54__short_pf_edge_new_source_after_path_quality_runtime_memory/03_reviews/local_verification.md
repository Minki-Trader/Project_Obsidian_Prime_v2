# Local Verification(로컬 검증)

- feature_contract(피처 계약): raw 58 feature order(원천 58 피처 순서) hash(해시)를 사용.
- label_boundary(라벨 경계): runtime-shaped payoff label(런타임형 손익 라벨)은 train split(학습 분할)의 label quantile(라벨 분위수)만 사용했다.
- model_boundary(모델 경계): `f54b_extratrees_d6_l80_short_runtimepay_s70_short_score3`는 F54에서 새로 학습했고 prior winner/baseline(과거 승자/기준선)을 상속하지 않았다.
- runtime_policy(런타임 정책): `{"InpAtrMaxStopPoints": 180.0, "InpAtrMaxTakeProfitPoints": 260.0, "InpAtrMinStopPoints": 40.0, "InpAtrMinTakeProfitPoints": 60.0, "InpAtrPeriod": 14, "InpAtrSltpEnabled": true, "InpAtrStopMultiplier": 0.8, "InpAtrTakeProfitMultiplier": 1.2, "InpCloseOnFlatSignal": false, "InpEntryTransitionOnly": false, "InpEntryTransitionRearmMinConfidenceDelta": 0.0, "InpMaxHoldBars": 6, "InpReentryCooldownBars": 0, "InpSameDirectionReentryCooldownBars": 0}`
- parity(동등성): ONNX(온엑스) score output(점수 출력)과 Python(파이썬) score(점수)는 model_artifact_manifest(모델 산출물 목록)에 기록.
- judgment(판정): `negative_memory_runtime_shaped_payoff_proxy_did_not_transfer(부정 기억, 런타임형 손익 프록시가 MT5로 전이되지 않음)`
