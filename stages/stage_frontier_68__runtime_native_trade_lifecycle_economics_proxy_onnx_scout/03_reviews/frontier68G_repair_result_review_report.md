# F68G Repair Result Review(F68G 수리 결과 검토)

Updated(갱신): 2026-06-16T18:16:36Z

## Action And Effect(행동 및 효과)

Action(행동): F68F runtime repair probe(F68F 런타임 수리 탐침)를 F68D density axis(F68D 밀도 축)와 비교하고 다음 수리 가설을 정했다.

Effect(효과): signal/feature parity(신호/피처 동등성)는 유지된 채 DD(drawdown, 손실폭)와 PF(profit factor, 수익 팩터)가 개선됐는지 분리하고, 다음 MT5 probe(MT5 탐침)를 risk envelope(위험 봉투) 수리로 좁혔다.

- status(상태): `completed_repair_result_review_next_runtime_repair_plan_no_authority(수리 결과 검토 및 다음 런타임 수리 계획 완료, 권위 없음)`
- judgment(판정): `preserved_clue_risk_envelope_repair_required_no_authority(보존 단서, 위험 봉투 수리 필요, 권위 없음)`

## F68F vs F68D Runtime KPI(F68F 대 F68D 런타임 핵심 성과 지표)

| split(분할) | F68F net(순수익) | net delta(순수익 차이) | F68F PF(수익 팩터) | PF delta(차이) | F68F DD%(손실폭) | DD delta(차이) | F68F trades/day(일 거래) | density delta(밀도 차이) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `validation` | `8.91` | `303.37` | `1.01` | `0.1` | `25.06` | `-46.07` | `3.974265` | `-2.863971` |
| `oos` | `241.18` | `137.7` | `1.18` | `0.14` | `19.57` | `-7.27` | `4.779487` | `-3.676923` |

## Target Read(목표 판독)

- scout clue(탐색 단서): F68F improved OOS net/PF/DD(F68F 표본외 순수익/수익 팩터/손실폭 개선) versus F68D density axis(F68D 밀도 축).
- missing axis(빠진 축): validation/OOS DD(검증/표본외 손실폭)는 `10%` 위이고, PF(수익 팩터)는 final target(최종 목표) 아래다.
- density note(거래 밀도 메모): OOS trades/day(표본외 일 거래)는 `4.779487`로 5/day 하한에 가깝지만 아직 미달이다.
- parity note(동등성 메모): signal_count_diff/feature_ready_diff(신호 수/피처 준비 차이)는 `0`이다.

## Next Runtime Repair(다음 런타임 수리)

Hypothesis(가설): exact F68F ONNX signal path(정확한 F68F ONNX 신호 경로)에 ATR SL/TP risk envelope(평균진폭 손절/익절 위험 봉투)를 붙이면 DD를 더 압축할 수 있다.

| variant(변형) | role(역할) | ATR stop(손절) | ATR TP(익절) | reentry(재진입) | same-dir cooldown(동방향 쿨다운) |
|---|---|---:|---:|---:|---:|
| `f52_atr08_tp12_re3_sd6` | `preserved_clue_atr_sltp_replay` | `0.8` | `1.2` | `3` | `6` |
| `tight_atr06_tp10_re3_sd6` | `dd_compression_pressure` | `0.6` | `1.0` | `3` | `6` |
| `wide_atr10_tp16_re3_sd6` | `pf_preservation_pressure` | `1.0` | `1.6` | `3` | `6` |

Next action(다음 행동): run Grok pre-probe review(Grok 탐침 전 검토) and then F68H MT5 Runtime Probe(F68H MT5 런타임 탐침).

Claim boundary(주장 경계): `repair_result_review_and_next_runtime_repair_plan_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`
