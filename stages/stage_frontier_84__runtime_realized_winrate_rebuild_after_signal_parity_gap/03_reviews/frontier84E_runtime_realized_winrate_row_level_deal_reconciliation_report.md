# F84E Runtime Realized Winrate Row-Level Deal Reconciliation(F84E 런타임 실현 승률 행 단위 거래 조정)

Status(상태): `f84e_row_level_deal_reconciliation_completed_proxy_win_runtime_loss_dominant_no_authority`

Judgment(판정): `row_level_reconciliation_shows_proxy_win_to_runtime_loss_dominant_risk_shape_failure_likely_no_authority`

Claim boundary(주장 경계): `row_level_reconciliation_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`

Action(행동): F84B proxy outcome(프록시 결과), F84C veto tape(차단 테이프), telemetry(원격 측정), MT5 deal report(거래 보고서)를 selected entry(선택 진입) 행 단위로 결합했다.

Effect(효과): aggregate KPI(집계 핵심 성과 지표)가 아니라 어떤 proxy win(프록시 승리)이 runtime loss(런타임 손실)로 바뀌었는지 기록했다.

## Readout(판독)

| split(구간) | selected(선택) | filled(체결) | ticket matched(티켓 결합) | proxy win -> runtime loss(프록시 승리 -> 런타임 손실) | runtime win rate(런타임 승률) | runtime PF(런타임 수익 팩터) |
|---|---:|---:|---:|---:|---:|---:|
| validation(검증) | 2340 | 2326 | 2326 | 795 / 1089 (73.00%) | 27.43% | 0.7122 |
| OOS(표본외) | 1805 | 1801 | 1801 | 560 / 821 (68.21%) | 30.87% | 0.8598 |

## Attribution(귀속)

Accepted(수용): F84C signal/feature/ONNX parity(신호/피처/온엑스 동등성)는 보존됐고, row-level(행 단위) MT5 ticket match(티켓 결합)는 validation(검증) 2326/2326, OOS(표본외) 1801/1801로 닫혔다.

Rejected(거절): fill gap(체결 간극)만으로 PF/DD collapse(수익 팩터/손실폭 붕괴)를 설명하는 주장, F84C parity pass(동등성 통과)를 runtime authority(런타임 권위)로 보는 주장, threshold-only repair(임계값만 수리)로 바로 가는 주장은 거절한다.

Needs local verification(로컬 검증 필요): F84F(전선84F)는 this row evidence(이 행 근거)를 보고 capped repair(상한 있는 수리) 또는 rotation(회전)을 골라야 한다. completion(완성)이나 selected baseline(선택 기준선)은 없다.

Preserved clue(보존 단서): `density preserved in MT5 but not economics`.

Negative memory(부정 기억): `proxy row winners frequently become runtime row losses after signal/feature/ONNX parity`.

Next action(다음 행동): `frontier84F_runtime_realized_winrate_repair_or_rotation_decision_v1`.
