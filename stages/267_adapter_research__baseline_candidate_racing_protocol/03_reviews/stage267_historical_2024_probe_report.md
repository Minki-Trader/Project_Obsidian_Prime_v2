# Stage267 Historical 2024 Probe Report(267단계 2024 과거 압박 보고)

- action(행동): Stage56 v41(56단계 v41) Tier A(티어 A) 2024 train-era(학습 기간) source signal(원천 신호)을 다시 만들고, 후보별 3-feature(3개 피처) MT5 input(입력)을 생성했다.
- effect(효과): 다섯 후보를 같은 2024 historical stress(2024 과거 압박) 조건에서 실행할 수 있게 되었지만, 아직 MT5 KPI(MT5 성과 지표)는 없다.
- candidates(후보): `s264_allow_inner_high_quarter`, `s264_lowrank_control`, `s262_lowrank_inner_half_filter`, `s264_allow_inner_all_oos_anchor`, `s258_short_tight_control`
- attempts(시도): `10` MT5 tester set/ini(테스터 설정/초기화) files(파일)
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`

## Data Integrity(데이터 무결성)

- data_source(데이터 원천): Stage56(56단계) `v41_v22_midcov_et40_agree_h2c0_no_b` regenerated frame(재생성 프레임), plus source model CSV(원천 모델 CSV) copied from Stage258/262/264(258/262/264단계).
- time_axis(시간축): `timestamp` is UTC(UTC), `bar_time_server` is written as `YYYY.MM.DD HH:MM:SS` for MT5(MetaTrader 5, 메타트레이더5) timestamp match(시간 일치).
- sample_scope(표본 범위): US100 M5, Tier A(티어 A), train split(학습 분할), `2024-01-02T16:40:00Z` to `2024-12-31T22:00:00Z`, rows(행) `11651`.
- missing_or_duplicate_check(누락/중복 확인): duplicate timestamps(중복 시간) `0`, missing signal rows(신호 누락 행) `0`.
- feature_label_boundary(피처/라벨 경계): this pass(이번 회차)는 label(라벨)을 새로 붙이지 않고 existing source signal/gate(기존 원천 신호/게이트)만 재생성한다.
- split_boundary(분할 경계): 2024 is train-era historical stress(학습 기간 과거 압박) only; it is not OOS(표본외)가 아니다.
- leakage_risk(누수 위험): high(높음) if interpreted as OOS(표본외) or used for promotion(승격); acceptable only as break-resistance probe(깨짐 저항 탐침).
- data_hash_or_identity(데이터 해시/정체성): feature manifest(피처 목록) `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267B/historical_2024/features.csv` and gate summary(게이트 요약) `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267B/historical_2024/gates.csv`.
- integrity_judgment(무결성 판정): `usable_with_boundary`.

## Gate Read(게이트 판독)

This is not performance attribution(성과 귀속) yet. It only tells how much signal supply(신호 공급)가 each candidate(각 후보) blocks(차단) before MT5 execution(실행).

| candidate(후보) | signal_rows(신호 행) | allowed_signal_rows(허용 신호 행) | blocked_signal_ratio(차단 비율) |
| --- | ---: | ---: | ---: |
| `s264_allow_inner_high_quarter` | 540 | 362 | 0.3296 |
| `s264_lowrank_control` | 540 | 359 | 0.3352 |
| `s262_lowrank_inner_half_filter` | 540 | 361 | 0.3315 |
| `s264_allow_inner_all_oos_anchor` | 540 | 363 | 0.3278 |
| `s258_short_tight_control` | 540 | 388 | 0.2815 |

## Performance Attribution Boundary(성과 귀속 경계)

- observed_change(관측 변화): none(없음), because MT5 KPI(MT5 성과 지표) has not run.
- comparison_baseline(비교 기준): Stage267(267단계) initial scoreboard(초기 점수판) and existing validation/OOS(검증/표본외) MT5 reports(보고서).
- likely_drivers(가능 동인): unknown(미상) until 2024 tester reports(테스터 보고서), balance/equity curve(잔액/평가금 곡선), trade count(거래 수)가 나온다.
- segment_checks(구간 확인): monthly gate supply(月별 게이트 공급)는 materialized(산출물화)됨; monthly KPI(月별 성과 지표)는 missing_required(필수 누락).
- trade_shape(거래 형태): missing_required(필수 누락), because no tester output(테스터 출력) yet.
- attribution_confidence(귀속 신뢰도): `inconclusive`.
- next_probe(다음 탐침): execute MT5(메타트레이더5 실행) 2024 historical stress(2024 과거 압박) for all attempts(전체 시도), then grade balance/equity full and zoom(전체/확대 평가금 곡선).

## Judgment(판정)

- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준선): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- operating meaning(운영 의미): `none`
