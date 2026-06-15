# Local Verification(로컬 검증)

- feature_contract(피처 계약): raw 58 feature order(원천 58 피처 순서) hash(해시)를 사용.
- label_boundary(라벨 경계): fast-exit execution label(빠른 청산 실행 라벨)은 train split(학습 분할)의 PnL quantile(손익 분위수)과 hold limit(보유 한계)만 사용했다.
- admission_boundary(진입 허용 경계): F57은 sparse admission/runtime veto(희소 진입 허용/런타임 차단)를 쓰지 않고 all-signal direct threshold(전체 신호 직접 임계값)만 MT5에 전달했다.
- model_boundary(모델 경계): `f57_fast_exit_execution_extratrees_d6_l80_short_score3`는 F57에서 새로 학습했고 prior winner/baseline(과거 승자/기준선)을 상속하지 않았다.
- runtime_policy(런타임 정책): `{"InpAtrMaxStopPoints": 180.0, "InpAtrMaxTakeProfitPoints": 260.0, "InpAtrMinStopPoints": 40.0, "InpAtrMinTakeProfitPoints": 60.0, "InpAtrPeriod": 14, "InpAtrSltpEnabled": true, "InpAtrStopMultiplier": 0.8, "InpAtrTakeProfitMultiplier": 1.2, "InpCloseOnFlatSignal": false, "InpEntryTransitionOnly": false, "InpEntryTransitionRearmMinConfidenceDelta": 0.0, "InpMaxHoldBars": 6, "InpReentryCooldownBars": 0, "InpSameDirectionReentryCooldownBars": 0}`
- hold_policy_note(보유 정책 메모): label hold_limit(라벨 보유 한계)과 runtime max_hold(런타임 최대 보유)는 source test(원천 시험)와 execution test(실행 시험)의 분리 축으로 기록한다.
- failure_mode(실패 모드): `{'failure_mode_observed': ['density_align_economics_collapse(밀도 정렬 뒤 경제성 붕괴)', 'source_no_transfer(원천 전이 실패)'], 'density_match_within_30pct': True, 'economics_match': False, 'parity_recheck': 'pass_proxy_onnx_only(프록시 ONNX만 통과)', 'proxy_validation_pf': 0.9406792484315578, 'proxy_oos_pf': 1.0518745268223901, 'comparison_note': 'MT5 rows compared against all-signal proxy rows; filtered proxy kept as secondary context.'}`
- parity(동등성): ONNX(온엑스) fast-exit score output(빠른 청산 점수 출력)과 Python(파이썬) score(점수)는 model_artifact_manifest(모델 산출물 목록)에 기록.
- judgment(판정): `negative_memory_fast_exit_execution_source_did_not_transfer(부정 기억, 빠른 청산 실행 원천이 MT5로 전이되지 않음)`
