# Stage56 Closeout Packet(56단계 종료 묶음)

- stage_id(단계 ID): `56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection`
- closeout_id(종료 ID): `stage56_closeout_v1`
- final_judgment(최종 판정): `baseline_candidate_only(기준선 후보 전용)`
- candidate(후보): `d38h10` LogReg(로지스틱 회귀) bracket micro-grid(구간 미세 격자)
- selected_research_baseline(선택 연구 기준선): `none`
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Decision(결정)

Stage56(56단계)은 `baseline_candidate_only(기준선 후보 전용)`로 닫는다.

`d38h10`은 실제 MT5(메타트레이더5) strategy tester(전략 테스터) closed trades(청산 거래)에서 validation(검증)과 OOS(표본외) 모두 양수 손익과 PF(수익 팩터) 1.05 이상을 보였고, Tier B fallback(Tier B 대체)이 실제 routed run(라우팅 실행) 안에서 사용됐다. 하지만 A+B routed density(A+B 라우팅 밀도)가 preferred target(선호 목표) 5~10 trades/day(일 거래 수)에 못 미치고, Tier B fallback-only(Tier B 대체 전용) standalone(단독) OOS(표본외)가 크게 음수라서 selected_research_baseline(선택 연구 기준선)으로 올리지 않는다.

효과(effect, 효과): Stage56(56단계)은 “쓸 만한 약한 후보 발견”까지 닫고, 운영 의미(operating meaning, 운영 의미)는 만들지 않는다.

## Evidence(근거)

| view(보기) | split(분할) | closed trades(청산 거래) | trades/day(일 거래 수) | net(순손익) | PF(수익 팩터) | max DD(최대 손실) |
|---|---:|---:|---:|---:|---:|---:|
| Tier A only(Tier A 단독) | validation | 751 | 4.103825 | 298.21 | 1.11 | 220.00 |
| Tier A only(Tier A 단독) | OOS | 604 | 3.097436 | 252.87 | 1.11 | 181.39 |
| Tier B fallback-only(Tier B 대체 전용) | validation | 73 | NA | -1.55 | 1.00 | 386.80 |
| Tier B fallback-only(Tier B 대체 전용) | OOS | 80 | NA | -397.38 | 0.55 | 503.01 |
| A+B actual routed total(A+B 실제 라우팅 전체) | validation | 817 | 4.464481 | 190.38 | 1.07 | 292.33 |
| A+B actual routed total(A+B 실제 라우팅 전체) | OOS | 672 | 3.446154 | 302.10 | 1.13 | 179.28 |

- preferred density target(선호 밀도 목표): 5~10 actual MT5 closed trades/day(실제 MT5 청산 거래/일)
- minimum review target(최소 검토 목표): 3 actual MT5 closed trades/day(실제 MT5 청산 거래/일)
- d38h10 routed validation density(라우팅 검증 밀도): 4.464481 trades/day(일 거래 수)
- d38h10 routed OOS density(라우팅 표본외 밀도): 3.446154 trades/day(일 거래 수)
- Tier B fallback bars(Tier B 대체 봉): validation 2366, OOS 1062
- actual routed total(실제 라우팅 전체): one MT5 tester account path(단일 MT5 테스터 계좌 경로), not synthetic sum(합성 합산 아님)

## Forensics(포렌식)

- tester_identity(테스터 정체성): terminal64.exe(터미널 실행 파일), symbol(심볼) `US100`, timeframe(시간봉) `M5`, model(모델링 방식) `4`, deposit(예치금) `500`, leverage(레버리지) `1:100`, fixed_lot(고정 랏) `0.1`
- date_range(날짜 범위): validation(검증) `2025.01.01` to `2025.10.01`, OOS(표본외) `2025.10.01` to `2026.04.14`
- EA identity(EA 정체성): `foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5`, tester expert(테스터 전문가 자문) `Project_Obsidian_Prime_v2\foundation\mt5\ObsidianPrimeV2_RuntimeProbeEA.ex5`
- module hash(모듈 해시): runtime EA(런타임 EA) `1e1f4224387cd45a466fc02d7ea7f192e231bd9d0d84c2ec1d0f214c058f2c7d`
- ONNX parity(ONNX 동등성): Tier A(티어 A) and Tier B(티어 B) passed with max abs diff(최대 절대 차이) below `1e-05`
- cost assumptions(비용 가정): MT5 tester report(테스터 보고서) 기준 결과를 사용했고, 별도 commission/slippage(수수료/슬리피지) 분해는 이번 closeout(종료)에서 새로 주장하지 않는다.
- backtest_judgment(백테스트 판정): `usable_with_boundary(경계 포함 사용 가능)`

## Report Identity(보고서 정체성)

| report(보고서) | sha256 |
|---|---|
| `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50C/d38h10/mt5/reports/Project_Obsidian_Prime_v2_run50C_d38h10_logreg_dense_v1_tier_a_only_validation_is.htm` | `a7a3f75acf775dc2fd7c3291ad87212937832f8cfc11274be081e120a4e444cc` |
| `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50C/d38h10/mt5/reports/Project_Obsidian_Prime_v2_run50C_d38h10_logreg_dense_v1_tier_b_fallback_only_validation_is.htm` | `35a4433de5b7572593736ee60108bfedb0d37f17255e6ae821c6475dfd39069b` |
| `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50C/d38h10/mt5/reports/Project_Obsidian_Prime_v2_run50C_d38h10_logreg_dense_v1_routed_validation_is.htm` | `0b841668c68b56bc29081fb0bac6cb31b3753ad199d1834e176578a53c25df11` |
| `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50C/d38h10/mt5/reports/Project_Obsidian_Prime_v2_run50C_d38h10_logreg_dense_v1_tier_a_only_oos.htm` | `fb90e5d1dc6f1e5060fc820c19eb465ba21a0dbb978535f11e72399529275037` |
| `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50C/d38h10/mt5/reports/Project_Obsidian_Prime_v2_run50C_d38h10_logreg_dense_v1_tier_b_fallback_only_oos.htm` | `87510aa38827e3dec5cdc96f186c0b345b0a8964be736c9a016f500cff6bd8af` |
| `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50C/d38h10/mt5/reports/Project_Obsidian_Prime_v2_run50C_d38h10_logreg_dense_v1_routed_oos.htm` | `b240b11f8b29ef845b5d51ab608ce391964bd83e24c74433ed8a3aee4bda0f23` |

## Comparison Read(비교 판독)

- run50B(실행50B) found density/quality frontier(밀도/품질 경계) but no selected baseline(선택 기준선 없음).
- run50C(실행50C) narrowed the bracket(구간)을 `d35h07` through `d39h11`.
- `d35h07` and `d36h08` met or neared density(밀도) but failed routed quality(라우팅 품질).
- `d37h09` and `d39h11` were inconclusive(불충분) on density/quality balance(밀도/품질 균형).
- `d38h10` was the only weak routed dense engine candidate(약한 라우팅 조밀 엔진 후보).
- QDA(이차 판별 분석)/CatBoost(캣부스트) dense comparison(조밀 비교)은 이번 종료 판정에 필요하지 않았다. 효과(effect, 효과): 실제 MT5(메타트레이더5) 후보가 이미 생겼으므로 Stage56(56단계)의 종료 조건을 더 미루지 않는다.

## Market-Weather Attribution(시장 상태 귀속)

- attribution source(귀속 원천): d38h10 actual routed MT5 deal list(실제 라우팅 MT5 거래 목록)
- validation(검증): 817 trades(거래), net(순손익) 190.38, positive_month_ratio(양수 월 비율) 0.666667, avg_hold_bars(평균 보유 봉) 33.056304
- OOS(표본외): 672 trades(거래), net(순손익) 302.10, positive_month_ratio(양수 월 비율) 0.571429, avg_hold_bars(평균 보유 봉) 29.392857
- validation(검증) contribution(기여): early session(초반 세션) +297.34, late session(후반 세션) -180.57, adx_gt25 +458.79, adx_20_25 -168.02
- OOS(표본외) contribution(기여): early session(초반 세션) +259.50, late session(후반 세션) -4.73, adx_lt20 +203.77, adx_gt25 -48.28
- hard filter(강제 필터): `none`

효과(effect, 효과): market-weather attribution(시장 상태 귀속)은 후보의 손익 분포를 설명하지만 Stage56(56단계) 안에서 새 operating filter(운영 필터)를 만들지 않는다.

## Judgment Record(판정 기록)

- result_subject(판정 대상): Stage56(56단계) research baseline selection(연구 기준선 선택)
- evidence_available(있는 근거): run50C(실행50C) MT5 strategy tester reports(전략 테스터 보고서), run_manifest(실행 목록), KPI(핵심 성과 지표), stage ledger(단계 장부), project ledger(프로젝트 장부), market-weather attribution(시장 상태 귀속)
- evidence_missing(약한 근거): preferred density target(선호 밀도 목표) 5~10 trades/day(일 거래 수) 미달, Tier B standalone OOS(Tier B 단독 표본외) 음수, WFO(워크포워드 최적화) 반복 검증 없음
- judgment_label(판정 라벨): `baseline_candidate_only(기준선 후보 전용)`
- claim_boundary(주장 경계): no live readiness(실거래 준비 없음), no runtime authority(런타임 권위 없음), no operating promotion(운영 승격 없음), no operating reference(운영 참조 없음)
- next_condition(다음 조건): 다음 stage(단계)에서 d38h10을 density/quality repair(밀도/품질 보정) 또는 WFO revalidation(워크포워드 재검증) 대상으로 열 수 있다.
- user_explanation_hook(사용자 설명): “후보는 찾았지만 기준선으로 고정할 만큼 촘촘하고 안정적이지는 않다.”

## Closeout Result(종료 결과)

Stage56(56단계)은 `d38h10`을 `baseline_candidate_only(기준선 후보 전용)`로 보존하고 종료한다. `selected_research_baseline(선택 연구 기준선)`은 없다.
