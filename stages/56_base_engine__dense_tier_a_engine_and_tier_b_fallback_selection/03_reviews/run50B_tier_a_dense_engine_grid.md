# Run50B Tier A Dense Engine Grid(50B 실행 Tier A 두꺼운 엔진 격자)

- stage_id(단계 ID): `56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection`
- parent_run_id(상위 실행 ID): `run50B_tier_a_dense_engine_grid_v1`
- model_family(모델군): `LogReg(로지스틱 회귀)` Stage07 full-context Tier A model(Stage07 전체 문맥 Tier A 모델)
- mt5_attempted(MT5 시도): `True`
- routed_fallback_enabled(라우팅 대체 활성): `False`
- best_current_read(현재 최선 판독): `d34h06` / `density_or_quality_inconclusive_runtime_probe_only`
- boundary(주장 경계): `runtime_probe_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Design(설계)

- hypothesis(가설): Stage07 LogReg(로지스틱 회귀) Tier A 모델의 threshold(임계값)를 낮추면 MT5 closed trades(닫힌 거래) 밀도가 Stage56 최소 검토선에 접근할 수 있다.
- decision_use(결정 용도): selected_research_baseline(선택 연구 기준선) 후보가 있는지 보기 위한 1차 격자다.
- comparison_baseline(비교 기준): run50A 기존 근거 감사에서 가장 촘촘했던 QDA 후보와 Stage55 routed adapter(라우팅 어댑터) 후보.
- controls(통제): 같은 데이터 분할, 같은 Stage07 Tier A 모델, 같은 MT5 EA(전문가 자문), 같은 US100 M5 계약을 쓴다.
- changed_variables(변경 변수): Tier A short/long threshold(숏/롱 임계값)와 max_hold_bars(최대 보유 봉 수)만 바꾼다.

## Results(결과)

| variant(변형) | validation trades/day(검증 거래/일) | OOS trades/day(표본외 거래/일) | validation PF(검증 수익 팩터) | OOS PF(표본외 수익 팩터) | judgment(판정) |
|---|---:|---:|---:|---:|---|
| d34h06 | 6.633880 | 4.958974 | 1.08 | 1.01 | `density_or_quality_inconclusive_runtime_probe_only` |
| d36h06 | 6.169399 | 4.676923 | 1.08 | 1.0 | `density_or_quality_inconclusive_runtime_probe_only` |
| d38h09 | 4.355191 | 3.271795 | 1.03 | 1.04 | `density_or_quality_inconclusive_runtime_probe_only` |
| d40h12 | 3.218579 | 2.369231 | 1.12 | 1.06 | `density_or_quality_inconclusive_runtime_probe_only` |

## Read(판독)

- d34h06은 density frontier(밀도 경계)다. validation(검증) `6.63/day`, OOS(표본외) `4.96/day`로 Stage56 minimum review target(최소 검토 목표)에 가장 가깝지만 OOS PF(표본외 수익 팩터)가 `1.01`이라 quality target(품질 목표)을 통과하지 못한다.
- d40h12는 quality frontier(품질 경계)다. validation PF(검증 수익 팩터) `1.12`, OOS PF(표본외 수익 팩터) `1.06`이지만 OOS density(표본외 밀도)가 `2.37/day`라 Stage56 minimum review target(최소 검토 목표) 아래다.
- result(결과): selected_research_baseline(선택 연구 기준선)은 아직 `none`이다. 다음 실행은 d34h06과 d40h12 사이를 좁히는 bracket micro-grid(구간 미세 격자)여야 한다.

## Judgment Boundary(판정 경계)

이 보고서는 research baseline selection(연구 기준선 선택) 안의 runtime probe(런타임 탐침)만 말한다.
live readiness(실거래 준비), runtime authority(런타임 권위), operating promotion(운영 승격), operating reference(운영 참조)는 주장하지 않는다.
