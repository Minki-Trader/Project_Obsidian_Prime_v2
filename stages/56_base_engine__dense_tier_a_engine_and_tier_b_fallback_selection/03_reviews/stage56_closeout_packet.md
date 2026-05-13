# Stage56 Closeout Packet(56단계 종료 묶음)

- superseded_status(대체 상태): `non_final_intermediate_evidence_after_stage56_reopen_goal_v1`
- superseded_reason(대체 이유): Stage56(56단계)의 terminal condition(종료 조건)은 selected_research_baseline(선택 연구 기준선) 발견뿐이다.
- current_read(현재 판독): this packet(이 묶음)은 prior evidence(이전 근거)를 보존하지만 final closeout(최종 종료)으로 쓰지 않는다.
- effect(효과): d390h10은 stronger candidate(강화 후보)로 남고, Stage56(56단계)은 active_in_progress(활성 진행 중)로 계속된다.
- stage_id(단계 ID): `56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection`
- closeout_id(종료 ID): `stage56_reopened_closeout_v2`
- final_judgment(최종 판정): `stronger_baseline_candidate_only(강화 기준선 후보 전용)`
- candidate(후보): `d390h10` LogReg(로지스틱 회귀) deep repair suite(조밀 보정 묶음)
- selected_research_baseline(선택 연구 기준선): `none`
- preserved_prior_candidate(보존 이전 후보): `d38h10`
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Decision(결정)

Historical packet text(과거 묶음 문장)는 Stage56(56단계)을 `stronger_baseline_candidate_only(강화 기준선 후보 전용)`로 닫는다고 적었지만, `stage56_reopen_goal_v1` 이후 이 문장은 final terminal decision(최종 종료 결정)이 아니다.

`d390h10`은 실제 MT5(메타트레이더5) strategy tester(전략 테스터) closed trades(청산 거래)에서 validation(검증)과 OOS(표본외) 모두 양수 손익, PF(수익 팩터) 1.10 이상, 최소 검토 밀도 3 trades/day(거래/일) 이상을 충족했다. 또한 prior candidate(이전 후보) `d38h10`보다 total net(총 순손익)과 validation PF(검증 수익 팩터)가 강하다.

하지만 selected_research_baseline(선택 연구 기준선)으로 올리지는 않는다. 이유(reason, 이유)는 A+B actual routed density(A+B 실제 라우팅 밀도)가 preferred target(선호 목표) 5~10 trades/day(거래/일)에 못 미치고, Tier B fallback-only(Tier B 대체 전용) OOS(표본외)는 여전히 음수이기 때문이다.

Superseded effect(대체된 효과): 과거 문장은 Stage56(56단계)을 “이전보다 강한 연구 후보 발견”까지 닫는다고 적었지만, 현재 판독에서는 non-final intermediate evidence(비최종 중간 근거)로만 남긴다.

## Evidence(근거)

| view(보기) | split(분할) | closed trades(청산 거래) | trades/day(일 거래 수) | net(순손익) | PF(수익 팩터) | max DD(최대 손실) |
|---|---:|---:|---:|---:|---:|---:|
| Tier A only(Tier A 단독) | validation | 691 | 3.775956 | 488.03 | 1.19 | 211.98 |
| Tier A only(Tier A 단독) | OOS | 545 | 2.794872 | 204.48 | 1.09 | 190.41 |
| Tier B fallback-only(Tier B 대체 전용) | validation | 60 | NA | 206.37 | 1.66 | 171.18 |
| Tier B fallback-only(Tier B 대체 전용) | OOS | 74 | NA | -225.14 | 0.65 | 383.23 |
| A+B actual routed total(A+B 실제 라우팅 전체) | validation | 748 | 4.087432 | 341.54 | 1.13 | 229.20 |
| A+B actual routed total(A+B 실제 라우팅 전체) | OOS | 594 | 3.046154 | 273.20 | 1.12 | 179.28 |

- preferred density target(선호 밀도 목표): 5~10 actual MT5 closed trades/day(실제 MT5 청산 거래/일)
- minimum review target(최소 검토 목표): 3 actual MT5 closed trades/day(실제 MT5 청산 거래/일)
- d390h10 routed validation density(라우팅 검증 밀도): 4.087432 trades/day(일 거래 수)
- d390h10 routed OOS density(라우팅 표본외 밀도): 3.046154 trades/day(일 거래 수)
- actual routed total(실제 라우팅 전체): one MT5 tester account path(단일 MT5 테스터 계좌 경로), not synthetic sum(합성 합산 아님)

## Comparison Read(비교 판독)

| candidate(후보) | validation density(검증 밀도) | OOS density(표본외 밀도) | validation PF(검증 PF) | OOS PF(표본외 PF) | total net(총 순손익) | read(판독) |
|---|---:|---:|---:|---:|---:|---|
| `d38h10` | 4.464481 | 3.446154 | 1.07 | 1.13 | 492.48 | prior weak candidate(이전 약한 후보) |
| `d385h10` | 4.256831 | 3.194872 | 1.10 | 1.13 | 576.17 | stronger quality candidate(강한 품질 후보) |
| `d390h10` | 4.087432 | 3.046154 | 1.13 | 1.12 | 614.74 | best stronger candidate(최선 강화 후보) |
| `d38short37long39h10` | 4.415301 | 3.302564 | 1.11 | 1.09 | 518.59 | better balance candidate(균형 개선 후보) |
| `d370h10` | 4.907104 | 3.671795 | 1.05 | 1.05 | 290.37 | density repair but weak quality(밀도 보정, 약한 품질) |

run50D(실행50D)는 18개 variant(변형)를 실행했다. selected_research_baseline(선택 연구 기준선) 조건은 어떤 variant(변형)도 충족하지 못했다. stronger_baseline_candidate_only(강화 기준선 후보 전용)는 d390h10이 충족한다.

## Tier B Fallback Damage Control(Tier B 대체 손상 통제)

- `d38h10_b040`: Tier B fallback-only(Tier B 대체 전용) OOS net(표본외 순손익) -257.92, routed OOS PF(라우팅 표본외 수익 팩터) 1.09
- `d38h10_b042`: Tier B fallback-only(Tier B 대체 전용) OOS net(표본외 순손익) -55.18, routed OOS PF(라우팅 표본외 수익 팩터) 1.10
- `d38h10_bmixed`: Tier B fallback-only(Tier B 대체 전용) OOS net(표본외 순손익) -41.95, routed OOS PF(라우팅 표본외 수익 팩터) 1.08

효과(effect, 효과): fallback permission(대체 허용)을 더 엄격하게 하면 손상은 줄일 수 있다. 그러나 그 자체만으로 selected baseline(선택 기준선)의 density/quality(밀도/품질)를 만들지는 못했다.

## Session Slice Check(세션 절편 확인)

| session(세션) | validation trades/day(검증 거래/일) | validation net(검증 순손익) | OOS trades/day(표본외 거래/일) | OOS net(표본외 순손익) | read(판독) |
|---|---:|---:|---:|---:|---|
| early(초반) | 2.278689 | 162.97 | 1.758974 | -188.87 | OOS failed(표본외 실패) |
| mid(중반) | 1.245902 | -17.34 | 1.076923 | -27.97 | failed(실패) |
| late(후반) | 1.010929 | 25.88 | 0.717949 | -89.30 | failed(실패) |

효과(effect, 효과): session gating(세션 제한)은 Stage56(56단계) 종료 안에서 후보를 고치는 충분한 방법이 아니다.

## Market-Weather Attribution(시장 상태 귀속)

- attribution source(귀속 원천): d390h10 actual routed MT5 deal list(실제 라우팅 MT5 거래 목록)
- validation(검증): 748 trades(거래), net(순손익) 341.54, positive_month_ratio(양수 월 비율) 0.666667, avg_hold_bars(평균 보유 봉) 33.461230
- OOS(표본외): 594 trades(거래), net(순손익) 273.20, positive_month_ratio(양수 월 비율) 0.571429, avg_hold_bars(평균 보유 봉) 30.372054
- validation(검증) contribution(기여): early session(초반 세션) +340.19, late session(후반 세션) -75.32, downtrend(하락 추세) +362.36, adx_gt25(ADX 25 초과) +487.32, adx_20_25(ADX 20~25) -124.96
- OOS(표본외) contribution(기여): early session(초반 세션) +257.59, late session(후반 세션) -60.83, range_or_weak_trend(횡보 또는 약추세) +207.79, adx_lt20(ADX 20 미만) +207.79, adx_gt25(ADX 25 초과) -50.29
- hard filter(강제 필터): `none`

효과(effect, 효과): market-weather attribution(시장 상태 귀속)은 후보의 손익 분포를 설명하지만 Stage56(56단계) 안에서 새 operating filter(운영 필터)를 만들지 않는다.

## Forensics(포렌식)

- tester_identity(테스터 정체성): terminal64.exe(터미널 실행 파일), broker terminal(브로커 터미널) FPMarketsSC-Live, symbol(심볼) `US100`, timeframe(시간봉) `M5`, model(모델링 방식) `4`, deposit(예치금) `500`, leverage(레버리지) `1:100`, fixed_lot(고정 랏) `0.1`
- date_range(날짜 범위): validation(검증) `2025.01.01` to `2025.10.01`, OOS(표본외) `2025.10.01` to `2026.04.14`
- EA identity(EA 정체성): `foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5`, tester expert(테스터 전문가 자문) `Project_Obsidian_Prime_v2\foundation\mt5\ObsidianPrimeV2_RuntimeProbeEA.ex5`
- ONNX parity(ONNX 동등성): Tier A(티어 A) and Tier B(티어 B) passed with max abs diff(최대 절대 차이) below `1e-05`
- cost assumptions(비용 가정): MT5 tester report(테스터 보고서) 기준 결과를 사용했고, 별도 commission/slippage(수수료/슬리피지) 분해는 이번 closeout(종료)에서 새로 주장하지 않는다.
- backtest_judgment(백테스트 판정): `usable_with_boundary(경계 포함 사용 가능)`

## Report Identity(보고서 정체성)

| report(보고서) | sha256 |
|---|---|
| `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50D/d390h10/mt5/reports/Project_Obsidian_Prime_v2_run50D_d390h10_logreg_deep_v1_tier_a_only_validation_is.htm` | `ed8604e7297877d3084cfa6ca73d5997c6d90751e36e7587b10de1b2ec90be3b` |
| `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50D/d390h10/mt5/reports/Project_Obsidian_Prime_v2_run50D_d390h10_logreg_deep_v1_tier_b_fallback_only_validation_is.htm` | `5b791ac8862d45ff3dd212cca4547cf4bae5f40ab7667f6875343a82d83a033b` |
| `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50D/d390h10/mt5/reports/Project_Obsidian_Prime_v2_run50D_d390h10_logreg_deep_v1_routed_validation_is.htm` | `7a2b88a8eeafd8e7f381f019ab16d5a8b1e7c208f82f40aabbe949e1e9d236b5` |
| `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50D/d390h10/mt5/reports/Project_Obsidian_Prime_v2_run50D_d390h10_logreg_deep_v1_tier_a_only_oos.htm` | `ea5a37c2c4faf800f6b9413dee1dd96e388194e8237697a52a6371204e87e53e` |
| `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50D/d390h10/mt5/reports/Project_Obsidian_Prime_v2_run50D_d390h10_logreg_deep_v1_tier_b_fallback_only_oos.htm` | `77e2c223aa6280810b375e2c286a84f44f5bdbb8053f207584772960b6550c96` |
| `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50D/d390h10/mt5/reports/Project_Obsidian_Prime_v2_run50D_d390h10_logreg_deep_v1_routed_oos.htm` | `e44426e395dedfe4c3991ded880fe94783ff06ee66dfd4642fb766ccd98fca5b` |

## Artifacts(산출물)

- run50D report(실행50D 보고서): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50D_deep_repair_suite.md`
- run50D summary(실행50D 요약): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50D_deep_repair_suite_summary.csv`
- run50D aggregate summary(실행50D 집계 요약): `docs/agent_control/packets/stage56_run50D_deep_repair_suite_v1/aggregate_summary.json`
- d390h10 market-weather attribution(d390h10 시장 상태 귀속): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/stage56_run50D_d390h10_market_weather_attribution.md`
- stage ledger(단계 장부): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/stage_run_ledger.csv`
- project ledger(프로젝트 장부): `docs/registers/alpha_run_ledger.csv`
- run registry(실행 등록부): `docs/registers/run_registry.csv`

## Judgment Record(판정 기록)

- result_subject(판정 대상): Stage56(56단계) research baseline selection(연구 기준선 선택)
- evidence_available(있는 근거): run50D(실행50D) MT5 strategy tester reports(전략 테스터 보고서), run_manifest(실행 목록), KPI(핵심 성과 지표), stage ledger(단계 장부), project ledger(프로젝트 장부), run registry(실행 등록부), market-weather attribution(시장 상태 귀속)
- evidence_missing(약한 근거): preferred density target(선호 밀도 목표) 5~10 trades/day(거래/일) 미달, Tier B standalone OOS(Tier B 단독 표본외) 음수, full WFO(전체 워크포워드) 반복 검증 없음
- judgment_label(판정 라벨): `stronger_baseline_candidate_only(강화 기준선 후보 전용)`
- claim_boundary(주장 경계): no live readiness(실거래 준비 없음), no runtime authority(런타임 권위 없음), no operating promotion(운영 승격 없음), no operating reference(운영 참조 없음)
- user_explanation_hook(사용자 설명): “d38h10보다 더 강한 후보는 찾았지만, 아직 선택 연구 기준선으로 고정할 만큼 촘촘하지는 않다.”

## Closeout Result(종료 결과)

Superseded read(대체 판독): Stage56(56단계)은 `d390h10`을 stronger candidate intermediate evidence(강화 후보 중간 근거)로 보존하고 계속 진행한다. `selected_research_baseline(선택 연구 기준선)`은 없다.
