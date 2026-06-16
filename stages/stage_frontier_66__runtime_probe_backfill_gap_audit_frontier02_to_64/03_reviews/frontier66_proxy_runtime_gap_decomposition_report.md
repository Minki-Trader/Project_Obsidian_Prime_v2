# Frontier66 Proxy-Runtime Gap Decomposition(F66 프록시-런타임 간극 해체)

Run(실행): `frontier66C_proxy_signal_mt5_backfill_v1`

Action(행동): Stage11,15,18-49의 proxy signal(프록시 신호)을 MT5 runtime probe(런타임 탐침)로 실행하고 proxy/runtime(프록시/런타임)을 split(분할) 단위로 대조했습니다.

Effect(효과): 기록 부재가 아니라 실제 MT5 실행 결과로 간극 원인을 분리합니다.

Claim boundary(주장 경계): `runtime_probe_observation_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`

## Execution Coverage(실행 커버리지)

- executable MT5 split runs(실행 가능 MT5 분할 실행): `64`
- completed tester/runtime/report(테스터/런타임/보고서 완료): `64`
- blocked(차단): `0`
- exact feature/signal handoff(피처/신호 인계 정확): `64/64`
- logic-zero stages(로직상 신호 0 단계): `F26`, `F34`

## Main Read(핵심 판독)

1. L1 feature readiness parity(피처 준비 동등성)와 L2 signal emission parity(신호 방출 동등성)는 이번 backfilled split set(소급 실행 분할 묶음)에서 성립했습니다. 모든 실행 split(분할)에서 `feature_ready_diff=0`, `signal_count_diff=0`입니다.
2. Residual gap(잔여 간극)은 L3 order intent(주문 의도), L4 fill/cost model(체결/비용 모델), L5 KPI measurement basis(KPI 측정 기준) mismatch(불일치)와 consistent(일관)합니다. Proxy(프록시)는 후보별 이벤트/점수/수익률 기반 평가였고, MT5 runtime(런타임)은 fixed lot(고정 랏), one-position cap(단일 포지션 제한), max hold(최대 보유), SL/TP(손절/익절), spread/cost(스프레드/비용), broker report DD(브로커 보고서 손실폭)를 적용했습니다.
3. DD(drawdown, 손실폭) 간극은 특히 큽니다. Proxy risk percent(프록시 위험 퍼센트)와 MT5 account DD percent(계좌 손실폭 퍼센트)의 기준이 달라, count-level signal parity(개수 기준 신호 동등성)가 맞아도 런타임 DD가 크게 재가격화됩니다.
4. Trade density(거래 밀도)도 재압축됩니다. 많은 proxy signal bar(프록시 신호 봉)가 있어도 MT5는 포지션 보유 중 추가 진입을 하지 않아 실제 trade count(거래 수)가 줄어듭니다.
5. 이 보고서는 L3-L5를 ranked root cause(순위가 있는 근본 원인)로 확정하지 않습니다. 현재 판정은 runtime_probe_observation(런타임 탐침 관찰)과 layered gap hypothesis(계층형 간극 가설)입니다.

## KPI Snapshot(KPI 스냅샷)

- runtime PF >= 2 split(런타임 수익 팩터 2 이상 분할): `1/64`
- runtime DD > 10% split(런타임 손실폭 10% 초과 분할): `60/64`
- executable stages with max runtime DD > 10%(실행 단계 중 최대 런타임 손실폭 10% 초과): `31/32`
- executable stages with min runtime PF < 1(실행 단계 중 최소 런타임 수익 팩터 1 미만): `19/32`

## Best Runtime PF Splits(런타임 수익 팩터 상위 분할)

| stage | split | runtime PF | runtime DD% | trades | primary gap |
|---:|---|---:|---:|---:|---|
| F11 | oos | 2.18 | 10.87 | 61 | signal_compression_execution_gap(신호 압축/실행 간극) |
| F35 | oos | 1.66 | 3.53 | 8 | rule_proxy_execution_economics_gap(규칙 프록시 실행/경제성 간극) |
| F29 | validation_is | 1.47 | 38.83 | 108 | rule_proxy_execution_economics_gap(규칙 프록시 실행/경제성 간극) |
| F20 | validation_is | 1.32 | 24.46 | 261 | rule_proxy_execution_economics_gap(규칙 프록시 실행/경제성 간극) |
| F23 | validation_is | 1.27 | 34.44 | 313 | rule_proxy_execution_economics_gap(규칙 프록시 실행/경제성 간극) |
| F36 | oos | 1.27 | 11.55 | 233 | rule_proxy_execution_economics_gap(규칙 프록시 실행/경제성 간극) |
| F35 | validation_is | 1.25 | 5.78 | 14 | rule_proxy_execution_economics_gap(규칙 프록시 실행/경제성 간극) |
| F39 | oos | 1.24 | 10.67 | 286 | signal_compression_execution_gap(신호 압축/실행 간극) |

## Worst Runtime DD Splits(런타임 손실폭 상위 분할)

| stage | split | runtime PF | runtime DD% | trades | primary gap |
|---:|---|---:|---:|---:|---|
| F23 | oos | 0.81 | 60.81 | 239 | rule_proxy_execution_economics_gap(규칙 프록시 실행/경제성 간극) |
| F11 | validation_is | 0.72 | 59.46 | 92 | signal_compression_execution_gap(신호 압축/실행 간극) |
| F25 | validation_is | 1.02 | 58.53 | 259 | rule_proxy_execution_economics_gap(규칙 프록시 실행/경제성 간극) |
| F27 | oos | 0.89 | 51.63 | 208 | rule_proxy_execution_economics_gap(규칙 프록시 실행/경제성 간극) |
| F30 | oos | 0.89 | 51.63 | 208 | rule_proxy_execution_economics_gap(규칙 프록시 실행/경제성 간극) |
| F25 | oos | 0.90 | 49.49 | 190 | rule_proxy_execution_economics_gap(규칙 프록시 실행/경제성 간극) |
| F27 | validation_is | 1.11 | 46.58 | 275 | rule_proxy_execution_economics_gap(규칙 프록시 실행/경제성 간극) |
| F30 | validation_is | 1.11 | 46.58 | 275 | rule_proxy_execution_economics_gap(규칙 프록시 실행/경제성 간극) |

## Artifacts(산출물)

- runtime rows review copy(런타임 행 검토 복사본): `frontier66_proxy_signal_runtime_rows_review.csv`
- split gap table review copy(분할 간극 표 검토 복사본): `frontier66_proxy_runtime_gap_by_split_review.csv`
- stage gap table review copy(단계 간극 표 검토 복사본): `frontier66_proxy_runtime_gap_by_stage_review.csv`
- summary JSON review copy(요약 JSON 검토 복사본): `frontier66_proxy_runtime_gap_summary_review.json`
- ignored local run root(무시되는 로컬 실행 루트): `../02_runs/frontier66C_proxy_signal_mt5_backfill_v1/`

Judgment(판정): runtime_probe_observation(런타임 탐침 관찰). No completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 주장 없음).
