# Stage267 Experiment Design Receipt(267단계 실험 설계 기록)

- work_packet(작업 묶음): `stage267_baseline_candidate_racing_protocol_v1`
- current_run(현재 실행): `run267A_stage267_baseline_candidate_racing_protocol_v1`
- primary_family(주 작업군): `state_sync` for opening the stage(단계 개방 동기화)
- experiment_design_role(실험 설계 역할): Stage267(267단계)의 R&D racing(연구개발 경주) 규약을 고정한다.
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`

## hypothesis(가설)

The five Baseline candidates(다섯 기준 후보)는 headline KPI(표면 핵심 성과 지표)만으로는 구분할 수 없다.
Effect(효과): R&D racing(연구개발 경주)은 누가 숫자가 제일 좋은지보다, 누가 extended period(확장 기간), feature ablation(피처 제거), similar replacement(유사 대체), time-slice weakness(시간 구간 약점), equity curve(평가금 곡선), trade quality(거래 품질)에서 덜 깨지는지 배운다.

## decision_use(판정 용도)

The result can update the research candidate pool(연구 후보군), drop weak candidates(약한 후보 탈락), open bounded adapter development(경계 있는 어댑터 개발), or record failure memory(실패 기억).
It cannot justify ONNX conversion(ONNX 변환), operating reference(운영 기준), runtime authority(런타임 권위), or production baseline(생산 기준선).

## comparison_baseline(비교 기준)

- pool baseline(후보군 기준): `baseline_candidate_pool.csv`
- defensive control(방어 기준): `s264_lowrank_control`
- validation-heavy reference(검증 중심 참고): `s262_lowrank_inner_half_filter`
- OOS anchor(표본외 앵커): `s264_allow_inner_all_oos_anchor`
- stress challenger(압박 도전자): `s258_short_tight_control`
- primary challenger(주 도전자): `s264_allow_inner_high_quarter`

## control_variables(고정 변수)

- symbol/timeframe(심볼/시간프레임): FPMarkets `US100` `M5`
- current canonical split(현재 정규 분할): preserve existing Stage258/262/264 validation/OOS(검증/표본외) meaning until a new split manifest(분할 목록) is written.
- Tier rule(티어 규칙): Tier A separate(Tier A 분리), Tier B separate(Tier B 분리), Tier A+B combined(Tier A+B 합산) or explicit missing_required(필수 누락).
- risk/ATR surface(위험/ATR 표면): current Stage258/262/264 ATR and model risk parameters remain source identity(원천 정체성) for initial comparison.
- claim boundary(주장 경계): research/development only(연구/개발 전용).

## changed_variables(변경 변수)

- candidate source(후보 원천): five named Baseline candidates(기준 후보).
- period coverage(기간 범위): add 2024 or other past period test(과거 기간 시험) when data/tooling identity is available.
- feature/category ablation(피처/범주 제거): remove or mask feature categories and compare survival.
- similar feature replacement(유사 피처 대체): replace market-meaning neighbors such as trend strength(추세 강도) or volatility strength(변동성 강도) features.
- feature engineering(피처 엔지니어링): create broader structural variants(넓은 구조 변형) before fine search(미세 탐색).
- analysis cuts(분석 구간): day/session/hour/month/chronological segment(요일/세션/시간/월/시간순 구간).

## sample_scope(표본 범위)

Initial scope(초기 범위)는 Stage258/262/264 materialized MT5 evidence(구체화된 MT5 근거)와 Stage265 review evidence(검토 근거)다.
Next execution(다음 실행)은 canonical IS/OOS(정규 표본내/표본외) plus older period such as 2024(2024년 같은 과거 기간)를 별도 split manifest(분할 목록)로 남겨야 한다.

## success_criteria(성공 기준)

- Candidate survives multiple periods(여러 기간) without deep equity holes(깊은 평가금 구멍).
- Trade count(거래 수), net profit(순수익), PF(수익 팩터), DD(drawdown, 손실폭), recovery(회복), expectancy(기대값)가 함께 편안하다.
- Feature ablation/replacement(피처 제거/대체)에서 완전히 무너지지 않는다.
- Adapter structure(어댑터 구조)로 feature order(피처 순서), decision surface(판정 표면), risk/ATR(위험/ATR), handoff(인계)를 추적할 수 있다.
- Failure memory(실패 기억)가 다음 연구 재료로 남는다.

## failure_criteria(실패 기준)

- One period/month/session(한 기간/월/세션)에만 예쁘고 다른 구간에서 무너진다.
- Equity curve(평가금 곡선)가 지저분하거나 확대 구간에서 깊게 파인다.
- Trade count(거래 수)가 너무 적거나, count(수)는 충분하지만 expectancy(기대값)와 DD(손실폭)가 불편하다.
- One feature/category(단일 피처/범주)에 과하게 붙어 있다.
- Repair branch(수리 분기)가 two stages(두 단계)를 넘기며 같은 약점만 미세 조정한다.

## invalid_conditions(무효 조건)

- source data(원천 데이터), split(분할), feature order(피처 순서), model/bundle identity(모델/번들 정체성), MT5 report identity(MT5 보고서 정체성)가 끊긴다.
- Future leakage(미래 누수) 또는 split leakage(분할 누수) 가능성을 설명하지 못한다.
- Synthetic combined result(합성 합산 결과)를 actual routed total(실제 라우팅 전체)처럼 말한다.
- Missing Tier B(티어 B 누락)을 기록하지 않는다.

## stop_conditions(중단 조건)

- Candidate breaks broadly(넓게 깨짐): 탈락 또는 archive(보관)한다.
- Candidate has one narrow weakness(좁은 약점 하나): at most two-stage repair(최대 두 단계 수리)만 허용한다.
- Evidence missing(근거 누락): missing_required(필수 누락), blocked(차단), or out_of_scope_by_claim(주장 범위 밖)로 낮춘다.
- ONNX temptation(ONNX 유혹): Goal Achieve gate(목표 달성 게이트)가 닫히기 전에는 stop(중단)한다.

## evidence_plan(근거 계획)

- candidate_pool_manifest(후보군 목록): `01_inputs/baseline_candidate_pool.csv`
- normalized KPI tables(정규화 핵심 성과 지표 표): validation/OOS/2024/past period(검증/표본외/2024/과거 기간)
- time-slice KPI(시간 구간 핵심 성과 지표): month/day/session/hour/chronological third(월/요일/세션/시간/시간순 삼분할)
- balance/equity curve artifacts(잔액/평가금 곡선 산출물): full and zoomed(전체와 확대)
- ablation/replacement manifests(제거/대체 목록): feature groups(피처 그룹), replacement mapping(대체 매핑)
- adapter manifest(어댑터 목록): feature order(피처 순서), thresholds(임계값), risk/ATR(위험/ATR), source hashes(원천 해시)
- failure_memory(실패 기억): failure reason(실패 이유), salvage value(회수 가치), reopen condition(재개 조건), do-not-repeat note(반복 금지 메모)

## data_integrity_receipt(데이터 무결성 기록)

- data_source(데이터 원천): existing Stage258/262/264 MT5 reports(기존 MT5 보고서), KPI CSV(핵심 성과 지표 CSV), telemetry(기록).
- time_axis(시간축): FPMarkets US100 M5 broker time(브로커 시간) as recorded by prior stage artifacts(이전 단계 산출물 기록 기준).
- split_boundary(분할 경계): existing validation/OOS(기존 검증/표본외) is source evidence; new 2024 or past period requires its own manifest(목록).
- leakage_risk(누수 위험): feature/category replacement(피처/범주 대체) can accidentally use future-aware labels(미래 인식 라벨); every new feature must name its feature-label boundary(피처-라벨 경계).
- integrity_judgment(무결성 판정): usable_with_boundary(경계부 사용 가능) for planning; new execution must re-check data identity(데이터 정체성).

## model_validation_receipt(모델 검증 기록)

- model_family(모델 계열): existing adapter/model surfaces(기존 어댑터/모델 표면) from Stage258/262/264.
- selection_metric(선택 지표): no single primary KPI(단일 주 지표 없음); survival across KPI bundle(묶음 핵심 성과 지표 생존) is required.
- secondary_metrics(보조 지표): segment PF(구간 수익 팩터), monthly net/PF(월별 순수익/수익 팩터), DD(손실폭), recovery(회복), expectancy(기대값), trade count(거래 수), equity smoothness(평가금 매끄러움).
- overfit_risk(과적합 위험): repeated repair(반복 수리), narrow month tuning(좁은 월 조정), threshold micro-tuning(임계값 미세 조정).
- validation_judgment(검증 판정): exploratory_candidate_pool(탐색 후보군), not selected baseline(선택 기준선 아님).
