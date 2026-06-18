# Frontier Stage 82 Brief(F82 전선 단계 개요)

Updated(갱신): 2026-06-18T05:15:42Z

Stage id(단계 ID): `stage_frontier_82__density_first_runtime_economic_mechanism_rotation`

Opening run(개방 실행): `frontier82A_stage_open_density_first_runtime_economic_mechanism_rotation_v1`

Status(상태): `opened_hypothesis_lifecycle_design_only_no_authority`

## Frontier Thesis(전선 가설)

density-first two-sided runtime economic mechanism(밀도 우선 양방향 런타임 경제 메커니즘)이 threshold search(임계값 탐색)보다 먼저 deal-level PnL(거래별 손익), session/regime split(세션/장세 분할), exportable model family(내보내기 가능한 모델 계열)를 묶으면 F81 low-density repair(F81 저밀도 수리)를 반복하지 않고 material MT5 candidate(MT5 물질화 후보)를 만들 수 있다는 가설.

Effect(효과): F82(전선82)는 F81(전선81)의 low-density seed(저밀도 씨앗)를 winner(승자)나 baseline(기준선)으로 쓰지 않고, density/runtime economics(밀도/런타임 경제성)를 처음부터 묶는 새 axis(축)로 시작한다.

## Novelty Delta(신규성 차이)

- F81(전선81)은 signal/feature/ONNX parity(신호/피처/온엑스 동등성)가 맞아도 MT5 runtime economics(MT5 런타임 경제성)가 무너질 수 있음을 보였다.
- F81G(전선81G)는 positive low-density seed(양수 저밀도 씨앗)를 남겼지만, materialization-ready candidate(물질화 준비 후보)는 `0`이었다.
- F82(전선82)는 threshold/filter/parameter(임계값/필터/파라미터)를 조금 바꾸는 수리가 아니라, candidate density(후보 밀도), two-sided trade supply(양방향 거래 공급), deal-level economics(거래별 경제성), WFO-aware selection(워크포워드 인식 선택)을 함께 본다.

## Experiment Design(실험 설계)

- hypothesis(가설): density-first two-sided runtime economic mechanism(밀도 우선 양방향 런타임 경제 메커니즘)이 threshold search(임계값 탐색)보다 먼저 deal-level PnL(거래별 손익), session/regime split(세션/장세 분할), exportable model family(내보내기 가능한 모델 계열)를 묶으면 F81 low-density repair(F81 저밀도 수리)를 반복하지 않고 material MT5 candidate(MT5 물질화 후보)를 만들 수 있다는 가설.
- decision_use(결정 용도): F82B가 broad density-first proxy surface(넓은 밀도 우선 프록시 표면)를 만들지, 아니면 F81-style low-density seed(F81식 저밀도 씨앗)만 반복될 때 즉시 rotate(회전)할지 결정하는 데 쓴다.
- comparison_baseline(비교 기준): F81C/F81F MT5 runtime OOS negative(전선81C/F 런타임 표본외 부정): net=-115.71; PF=0.7332887700534759; DD=23.72; trades/day=3.4358974358974357; F81G low-density seed reference(F81G 저밀도 씨앗 참고): net=8.91; PF=1.4312681510164567; DD=0.6830574201295305; trades/day=0.20512820512820512; No-trade baseline(무거래 기준): no risk(위험 없음), no profit(수익 없음), no strategy utility(전략 효용 없음).
- control_variables(고정 변수): symbol/timeframe(심볼/시간프레임): FPMarkets US100 M5(FPMarkets US100 5분봉); frontier inheritance boundary(전선 상속 경계): reference only(참조 전용), no winner/baseline/authority inheritance(승자/기준선/권위 상속 없음); paired tier reporting(쌍 티어 보고): Tier A separate/Tier B separate/Tier A+B combined(티어 A 분리/티어 B 분리/합산) or explicit missing/out_of_scope(명시 누락/범위 밖); claim boundary(주장 경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)
- changed_variables(변경 변수): density target first(밀도 목표 우선): require candidate density before micro threshold search(미세 임계값 탐색 전 후보 밀도 요구); two-sided mechanism(양방향 메커니즘): long/short opportunity balance(롱/숏 기회 균형)를 first-class signal(일급 신호)로 둔다; runtime economics first(런타임 경제성 우선): deal-level PnL and trade-density(거래별 손익과 거래 밀도)를 proxy score(프록시 점수)에 묶는다; model-family openness(모델 계열 개방): tree/linear/calibrated rank/exportable family(트리/선형/보정 순위/내보내기 가능 계열)를 broad sweep(넓은 탐색)한다
- sample_scope(표본 범위): {"symbol": "FPMarkets US100", "timeframe": "M5", "stage": "stage_frontier_82__density_first_runtime_economic_mechanism_rotation", "initial_period_policy": "exact train/validation/OOS windows(정확한 학습/검증/표본외 창)는 F82B에서 명명하고, F82A는 stage-open design(단계 개방 설계)만 담당한다", "tier_scope": "Tier A plus Tier B required if available; if unavailable record missing_required/out_of_scope_by_claim(티어 A와 가능한 티어 B, 없으면 명시)"}
- success_criteria(성공 기준): proxy scout(프록시 탐색)가 materialization candidate(물질화 후보)를 만들고, density(밀도)가 F81G low-density seed(저밀도 씨앗)를 넘어선다; meaningful signal/candidate(의미 신호/후보)가 생기면 MT5 Strategy Tester(전략 테스터)로 물질화한다; WFO/stress/runtime validation(워크포워드/스트레스/런타임 검증)으로 갈 수 있는 근거를 만든다
- failure_criteria(실패 기준): candidate density(후보 밀도)가 F81G 수준처럼 너무 낮아 materialization-ready(물질화 준비)로 볼 수 없다; proxy(프록시)는 좋아 보이나 runtime economics(런타임 경제성)가 F81C처럼 붕괴한다; same threshold/filter/parameter(같은 임계값/필터/파라미터) 반복만 남고 new axis(새 축)가 없다
- invalid_conditions(무효 조건): time-axis or label boundary(시간축 또는 라벨 경계)가 설명되지 않는다; future data leakage(미래 데이터 누수) 또는 split contamination(분할 오염)이 발견된다; model score(모델 점수)를 calibrated probability(보정 확률)처럼 해석하지만 calibration evidence(보정 근거)가 없다
- stop_conditions(중지 조건): zero signal/no trade/mismatch/crash/block(영 신호/무거래/불일치/충돌/차단)은 negative evidence(부정 근거)로 기록하고 원인 축을 분리한다; new evidence/new axis(새 근거/새 축) 없이 threshold-only repair(임계값 전용 수리)가 반복되면 capped repair(상한 수리)로 닫는다; external runtime verification(외부 런타임 검증)이 필요한 claim(주장)은 같은 pass(회차)에서 시도하거나 claim scope(주장 범위)를 낮춘다
- evidence_plan(근거 계획): F82B proxy report(프록시 보고서), candidate table(후보 표), label audit(라벨 감사), tier record audit(티어 기록 감사); run_manifest(실행 목록), run_registry(실행 등록부), alpha_run_ledger(알파 실행 장부), stage_run_ledger(단계 실행 장부); MT5 materialization receipt/report/log/snapshot(MT5 물질화 영수증/보고서/로그/스냅샷) once a meaningful candidate exists(의미 후보 발생 시); proxy/runtime gap analysis(프록시/런타임 간극 분석), WFO/stress evidence(워크포워드/스트레스 근거), closeout KPI(마감 KPI)

## Exploration Mandate(탐색 명령)

- idea_id(아이디어 ID): `IDEA-FR82-DENSITY-FIRST-RUNTIME-ECONOMIC-MECHANISM-ROTATION`
- legacy_relation(레거시 관계): `prior_evidence_only(과거 근거 전용)`
- tier_scope(티어 범위): `mixed Tier A/Tier B with explicit missing/out_of_scope handling(티어 A/B 혼합 및 명시 누락 처리)`
- broad_sweep(넓은 탐색): `model family x density floor x side balance x session/regime split(모델 계열 x 밀도 하한 x 방향 균형 x 세션/장세 분할)`
- extreme_sweep(극단 탐색): `include low/high/absurd-but-legal density and cost-shape boundaries(저/고/합법 극단 밀도와 비용 형태 경계 포함)`
- micro_search_gate(미세 탐색 조건): `only after density and runtime-economic proxy evidence beat F81 low-density failure(밀도와 런타임 경제 프록시가 F81 실패를 넘은 뒤)`
- wfo_plan(워크포워드 계획): `default WFO-aware selection in F82B/F82C unless explicitly downgraded to scout-only(기본 워크포워드 인식 선택)`
- failure_memory(실패 기억): `negative result must record salvage value and reopen condition(부정 결과는 회수 가치와 재개 조건 기록)`
- evidence_boundary(근거 경계): `stage_open_design_only_no_authority(단계 개방 설계 전용, 권위 없음)`

## Data And Model Boundaries(데이터와 모델 경계)

- data_integrity(데이터 무결성): {"data_source": "concrete feature/label sources(구체 피처/라벨 원천)는 F82B에서 확정하고, F82A는 F81 closeout reference(F81 마감 참조)만 소비한다", "time_axis": "proxy scoring(프록시 점수화) 전 US100 M5 closed-bar convention(US100 5분봉 종가 기준)을 명명해야 한다", "missing_or_duplicate_check": "reviewed run claim(검토 완료 실행 주장) 전 F82B에서 missing/duplicate check(누락/중복 검사)가 필요하다", "feature_label_boundary": "features must precede labels; realized PnL labels must not leak future path into entry features(피처는 라벨보다 앞서야 함)", "split_boundary": "train/validation/OOS or WFO window must be explicit before model comparison(모델 비교 전 명시)", "leakage_risk": "deal-level realized labels may accidentally leak exit outcome into entry features(거래 실현 라벨이 진입 피처로 새는 위험)", "data_hash_or_identity": "stage-open has no new dataset; references are path-identified and later hashed(개방에는 새 데이터 없음)", "integrity_judgment": "usable_with_boundary_for_design_only(설계 전용 경계에서 사용 가능)"}
- model_validation(모델 검증): {"model_family": "not_selected_yet_broad_sweep_planned(아직 선택 없음, 넓은 탐색 예정)", "target_and_label": "density-first runtime economic target to be materialized in F82B(F82B에서 물질화할 밀도 우선 런타임 경제 목표)", "split_method": "WFO-aware by default; exact split pending F82B(기본 워크포워드 인식, 정확 분할은 F82B)", "selection_metric": "joint density/economics/risk score; no single PF-only selection(밀도/경제성/위험 결합 점수, PF 단독 금지)", "secondary_metrics": "net/PF/DD/trade count/trades per day/expectancy/recovery/time under water/side breakdown(순손익/수익 팩터/손실폭/거래 수/일 거래/기대값/회복/회복 전 체류/방향 분해)", "threshold_policy": "broad sweep before micro threshold search(미세 임계값 탐색 전 넓은 탐색)", "overfit_risk": "selection after seeing F81 gap could overfit to one failure mode(F81 간극 하나에 과적합 위험)", "calibration_risk": "rank scores are not probabilities until calibration is proven(순위 점수는 보정 전 확률 아님)", "validation_judgment": "exploratory_design_only(탐색 설계 전용)"}

## Prior-Stage Scan(이전 단계 점검)

- F81 closeout(F81 마감): `stages/stage_frontier_81__mt5_native_order_intent_cost_shape_rebuild/03_reviews/stage_closeout_report.md`
- F81 gap attribution(F81 간극 귀속): `stages/stage_frontier_81__mt5_native_order_intent_cost_shape_rebuild/03_reviews/f81d_proxy_runtime_gap_attribution.json`
- F81 deal reconciliation(F81 거래 대조): `stages/stage_frontier_81__mt5_native_order_intent_cost_shape_rebuild/03_reviews/f81f_deal_reconciliation_summary.json`
- F81 realized-label diagnostic(F81 실현 라벨 진단): `stages/stage_frontier_81__mt5_native_order_intent_cost_shape_rebuild/03_reviews/f81g_mt5_realized_label_rebuild_summary.json`
- F81 negative memory(F81 부정 기억): `docs/registers/negative_result_register.md`
- Frontier extra due check(전선 추가 도래 점검): `not_due_after_f81_closeout_next_boundary_f100_e01_closed_for_f050`

## Do Not Repeat(반복 금지)

- Do not reuse F81 low-density seed(F81 저밀도 씨앗)를 selected baseline(선택 기준선)처럼 쓰지 않는다.
- Do not run threshold/filter/parameter-only repair(임계값/필터/파라미터 전용 수리) without new evidence axis(새 근거 축).
- Do not treat proxy PF(프록시 수익 팩터), ONNX parity(온엑스 동등성), or signal count(신호 수)를 runtime economics(런타임 경제성)로 대체하지 않는다.
- Do not skip MT5 Strategy Tester(전략 테스터) once a meaningful candidate(의미 후보)가 exists(존재)한다.

## Hypothesis Lifecycle(가설 생명주기)

1. Hypothesis(가설): density-first two-sided runtime economic mechanism(밀도 우선 양방향 런타임 경제 메커니즘)을 설계한다.
2. Proxy(프록시): F82B에서 broad/extreme sweep(넓은/극단 탐색)을 실행하고 Tier A/Tier B/Tier A+B(티어 A/B/합산)를 기록한다.
3. MT5 runtime materialization(MT5 런타임 물질화): 의미 후보가 있으면 ONNX handoff(온엑스 인계), bundle(번들), Strategy Tester(전략 테스터)를 만든다.
4. Proxy/runtime gap analysis(프록시/런타임 간극 분석): net/PF/DD/density/cost/fill/exit/side/session(순수익/수익 팩터/손실폭/밀도/비용/체결/청산/방향/세션)을 분해한다.
5. WFO/stress/runtime validation(워크포워드/스트레스/런타임 검증): 후보가 유지되면 WFO(워크포워드)와 stress test(스트레스 테스트)를 붙인다.
6. Repair or rotation(수리 또는 회전): 새 evidence(근거)나 axis(축)가 없으면 capped repair(상한 수리)로 닫고 회전한다.
7. Closeout(마감): preserved clue/negative memory/seed surface/reference surface/invalid setup/blocked retry condition/next frontier proposal(보존 단서/부정 기억/씨앗 표면/참고 표면/무효 설정/차단 재시도 조건/다음 전선 제안) 중 하나 이상으로 닫는다.

## Required Records(필수 기록)

F82(전선82)의 run/review(실행/검토)는 hypothesis/test period/proxy KPI/runtime KPI/net profit/PF/DD/trade count/trades per day/parity/gap cause/next action(가설/기간/프록시 KPI/런타임 KPI/순수익/수익 팩터/손실폭/거래 수/일 거래 수/동등성/간극 원인/다음 행동)을 남긴다.

Closeout KPI(마감 KPI)는 가능한 범위에서 gross profit/loss, win rate, avg win/loss, payoff ratio, expectancy, recovery factor, time under water, max consecutive loss, long/short breakdown(총이익/총손실/승률/평균 이익·손실/손익비/기대값/회복 계수/회복 전 체류 시간/최대 연속 손실/롱·숏 분해)을 포함한다.

## Exit Rule(종료 규칙)

F82(전선82)는 run count(실행 수)가 아니라 decision weight(결정 무게)로 닫는다. zero signal/no trade/mismatch/crash/block(영 신호/무거래/불일치/충돌/차단)은 waste(낭비)가 아니라 negative evidence(부정 근거)다.

## Claim Boundary(주장 경계)

Allowed(허용): hypothesis design(가설 설계), proxy scout(프록시 탐색), runtime probe(런타임 탐침), runtime learning(런타임 학습), preserved clue(보존 단서), negative memory(부정 기억), reference surface(참고 표면), seed surface(씨앗 표면).

Forbidden(금지): completion(완성), selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성), git push as validation(깃 원격 반영을 검증으로 간주).

Next run(다음 실행): `frontier82B_density_first_runtime_economic_mechanism_proxy_scout_v1`
