# run337EQ Forward KPI Blocked(전진 성과 차단)

## Summary(요약)

- run_id(실행 ID): `run337EQ_forward_kpi_attribution_cost_stress_curve_pocket_without_db_v1`
- status(상태): `blocked_stage337EQ_forward_kpi_missing_or_tester_visibility_gap`
- decision(결정): `Forward Blocked(전진 차단)`
- MT5 reports(MT5 보고서): `7`
- trade rows(거래 행): `351`
- latest_feature_timestamp(최신 피처 시각): `2026-05-28 06:00:00+00:00`
- latest_runtime_timestamp(최신 런타임 시각): `2026-05-27 23:59:58+00:00`
- latest_visibility_gap_minutes(최신 가시성 공백 분): `360.03`
- claim_boundary(주장 경계): `research_development_only_stage337EQ_forward_kpi_attribution_cost_stress_curve_pocket_without_db_no_new_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_no_forward_passed_no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve`

Effect(효과): trading enabled(거래 활성) MT5 Strategy Tester(전략 테스터)는 실행됐지만 최신 `2026-05-28T06:00:00Z` 피처까지 도달하지 못했다. 성과가 나쁘더라도 최신 데이터 누락 때문에 Forward Failed(전진 실패)가 아니라 Forward Blocked(전진 차단)로 닫는다.

## Rank KPI(순위별 성과)

| rank(순위) | net(순손익) | PF(수익 팩터) | trades(거래 수) | DD(낙폭) | recovery(회복) | curve(곡선) |
|---:|---:|---:|---:|---:|---:|---|
| `1` | `-90.71` | `0.66` | `47` | `123.4` | `-0.74` | `negative_or_unprofitable_forward` |
| `2` | `9.31` | `1.04` | `53` | `72.03` | `0.13` | `cost_fragile_forward` |
| `3` | `-60.08` | `0.76` | `56` | `127.33` | `-0.47` | `negative_or_unprofitable_forward` |
| `4` | `-0.39` | `1` | `51` | `99.77` | `0` | `negative_or_unprofitable_forward` |
| `5` | `-24.74` | `0.9` | `60` | `98.24` | `-0.25` | `negative_or_unprofitable_forward` |
| `6` | `-36.94` | `0.84` | `43` | `102.47` | `-0.36` | `negative_or_unprofitable_forward` |
| `7` | `-88.57` | `0.64` | `41` | `132.03` | `-0.67` | `negative_or_unprofitable_forward` |

## Attribution Read(귀속 판독)

- rank1(1순위): net/PF/DD(순손익/수익 팩터/낙폭) `-90.71` / `0.66` / `123.4`; curve_read(곡선 판독) `negative_or_unprofitable_forward`.
- rank2(2순위): net/PF(순손익/수익 팩터) `9.31` / `1.04`로 양수지만 얇고 cost stress(비용 스트레스)에 취약하다.
- direction attribution(방향 귀속): sell/short(매도/숏) bucket(구간)이 전 rank(순위)에서 손실 쪽이다.
- D/B attribution(D/B 귀속): D/B source column(D/B 원천 열)이 없어 direction proxy(방향 대리) 경계만 기록했다.

## Gates(게이트)
- `frozen_identity`: `covered` - ONNX(온엑스), feature order(피처 순서), decision mode(결정 모드), risk/lot parameters(위험/랏 파라미터)는 probe package(탐침 패키지)에서 고정했다.
- `mt5_report`: `covered` - strategy tester report rows(전략 테스터 보고서 행) `7`.
- `trade_list_parse`: `covered` - trade rows(거래 행) `351`, parser errors(파서 오류) `0`.
- `latest_visibility`: `blocked` - feature last(피처 마지막) `2026-05-28 06:00:00+00:00`, runtime last(런타임 마지막) `2026-05-27 23:59:58+00:00`, lag minutes(지연 분) `360.03`.
- `regime_attribution`: `covered` - time/session/volatility/ADX/VIX/USD/rate slices(시간/세션/변동성/ADX/VIX/USD/금리 절편)를 가능한 피처 안에서 생성했다.
- `db_attribution`: `covered_boundary` - D/B source(D/B 원천)는 없고 direction proxy(방향 대리) 경계를 기록했다.
- `lot_normalized`: `covered` - fixed-lot/per-lot result(고정 랏/랏당 결과)를 lot optimization(랏 최적화) 없이 생성했다.
- `cost_stress`: `covered` - spread/slippage point stress(스프레드/슬리피지 포인트 스트레스)를 사후 적용했다.
- `curve_pocket`: `covered` - worst month/chronology/rolling pockets(최악 월/시간 순서/롤링 포켓)를 기록했다.
- `no_goal_achieve`: `covered` - Goal Achieve(목표 달성)는 주장하지 않았다.

## Required Artifacts(필수 산출물)

- frozen forward MT5 report(고정 전진 MT5 보고서): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337EQ/frozen_forward_mt5_report.csv`
- regime attribution report(국면 귀속 보고서): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337EQ/regime_attribution_report.csv`
- D/B attribution report(D/B 귀속 보고서): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337EQ/db_attribution_report.csv`
- lot-normalized report(랏 정규화 보고서): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337EQ/lot_normalized_report.csv`
- cost stress report(비용 스트레스 보고서): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337EQ/cost_stress_report.csv`
- curve pocket report(곡선 포켓 보고서): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337EQ/curve_pocket_report.csv`
- final forward decision report(최종 전진 결정 보고서): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337EQ/final_forward_decision_report.json`

## Boundary(경계)

Forward Passed(전진 통과)와 Forward Failed(전진 실패)는 `not_claimed`다. Forward Blocked(전진 차단)는 `claimed`다. Goal Achieve(목표 달성), runtime authority(런타임 권위), operating promotion(운영 승격), deployment(배포)는 모두 `not_claimed`다.
