# run338G Runtime-Collapsed MT5 Probe Package(런타임 축약 MT5 탐침 패키지)

## Summary(요약)

- run_id(실행 ID): `run338G_materialize_runtime_collapsed_onnx_mt5_probe_package_without_db_v1`
- status(상태): `completed_stage338G_runtime_collapsed_onnx_mt5_probe_package_materialized_no_mt5_execution`
- judgment(판정): `mt5_runtime_probe_package_ready_proxy_mt5_comparison_required_no_selection`
- gates(게이트): `10/10`
- attempt(시도): `g01_logreg_balanced_c025_p60_m00`
- model_id(모델 ID): `logreg_balanced_c025`
- rows(행): `5827`
- features(피처): `53`
- feature_order_hash(피처 순서 해시): `870630295e4a4f15a168230f75a27726e910d8ba141270e1b2140cdd4519ba0c`
- tester_range(테스터 구간): `2024.07.30` to `2025.01.01`
- next_run(다음 실행): `run338H_execute_runtime_collapsed_onnx_mt5_probe_without_db_v1`

## Action(행동)

run338F(338F 실행)의 timestamp-unique proxy(시각 고유 프록시)를 MT5 runtime probe package(MT5 런타임 탐침 패키지)로 물질화했다.
Effect(효과): run338H(338H 실행)가 같은 ONNX(온엑스), feature CSV(피처 CSV), threshold(임계값), expected tape(예상 테이프)를 들고 실제 MT5(메타트레이더5)를 실행할 수 있다.

## Runtime Parity(런타임 동등성)

- research_path(연구 경로): `stages/338_runtime_trade_lifecycle__proxy_positive_mt5_negative_repair/02_runs/run338E/final_decision.json`
- runtime_path(런타임 경로): `stages/338_runtime_trade_lifecycle__proxy_positive_mt5_negative_repair/02_runs/run338G/runtime_probe_attempt_package.csv`
- shared_contract(공유 계약): `stages/338_runtime_trade_lifecycle__proxy_positive_mt5_negative_repair/02_runs/run338G/runtime_parity_contract.csv`
- known_differences(알려진 차이): Python proxy path(파이썬 프록시 경로)와 MT5 Common Files path(MT5 공용 파일 경로)는 다르다.
- parity_check(동등성 검사): run338H(338H 실행)의 telemetry-vs-expected tape(런타임 기록 대 예상 테이프) 비교가 필요하다.
- runtime_claim_boundary(런타임 주장 경계): runtime_probe_package_only(런타임 탐침 패키지 전용)

## Backtest Forensics(백테스트 포렌식)

- tester_identity(테스터 정체성): `stages/338_runtime_trade_lifecycle__proxy_positive_mt5_negative_repair/02_runs/run338G/tester_identity_contract.csv`
- report_identity(보고서 정체성): not_available_until_run338H(338H 전까지 없음)
- trade_evidence(거래 근거): not_available_no_mt5_execution(실행 없음)
- cost_assumptions(비용 가정): actual tester output required(실제 테스터 출력 필요)

## Boundary(경계)

run338G(338G 실행)는 package only(패키지 전용)이다. MT5 execution(MT5 실행), candidate selection(후보 선택), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 없다.
