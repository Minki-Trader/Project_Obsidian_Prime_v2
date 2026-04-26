# Stage 10 Runs

현재 Stage 10(10단계) run(실행)은 `run01A_logreg_threshold_mt5_scout_v1`이다.

이 폴더(folder, 폴더)는 `single_split_scout(단일 분할 탐색 판독)` 실행 산출물(run outputs, 실행 산출물)을 담는다.

효과(effect, 효과): Stage 10(10단계)이 active(활성) 상태이고 MT5(`MetaTrader 5`, 메타트레이더5) runtime probe(런타임 탐침)를 완료했지만, 아직 alpha quality(알파 품질), WFO(`walk-forward optimization`, 워크포워드 최적화), live readiness(실거래 준비), operating promotion(운영 승격)이 생긴 것은 아니다.

## Active Run(현재 실행)

- run_id(실행 ID): `run01A_logreg_threshold_mt5_scout_v1`
- label(라벨): `stage10_Model__LogReg_MT5Scout`
- boundary(경계): `runtime_probe(런타임 탐침)`
- outputs(산출물): `run_manifest.json`, `kpi_record.json`, ONNX(`Open Neural Network Exchange`, 온닉스) model(모델), Python(파이썬) prediction(예측), MT5 Strategy Tester(전략 테스터) report(리포트)
- judgment(판정): `inconclusive_single_split_scout_mt5_routed_completed`
- routing mode(라우팅 방식): `tier_a_primary_tier_b_partial_context_fallback`

## Pair Record Requirement(쌍 기록 요구)

새 알파 실행(alpha run, 알파 실행)은 Tier A(티어 A), Tier B(티어 B), Tier A+B combined(Tier A+B 합산)를 함께 남긴다.

MT5(`MetaTrader 5`, 메타트레이더5) routed run(라우팅 실행)에서 run01A(실행 01A)의 의미는 Tier A primary(Tier A 우선), Tier B fallback(Tier B 대체), actual routed total(실제 라우팅 전체)이다.

이번 run01A(실행 01A)에서는 Tier B partial-context fallback(Tier B 부분 문맥 대체)이 validation_is(검증/표본내) `2366`행, OOS(표본외) `1062`행을 메웠다. no_tier labelable(티어 없음 라벨 가능)은 validation_is(검증/표본내) `203`행, OOS(표본외) `159`행이다.

효과(effect, 효과): run folder(실행 폴더)의 상세 산출물과 project ledger(프로젝트 장부)의 한 줄 기록이 Tier A primary(Tier A 우선), Tier B fallback(Tier B 대체), no_tier(티어 없음)를 같은 판정으로 가리키게 한다.
