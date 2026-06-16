# F68H ATR SL/TP Runtime Repair Probe(F68H 평균진폭 손절/익절 런타임 수리 탐침)

Updated(갱신): 2026-06-16T18:22:31Z

## Action And Effect(행동 및 효과)

Action(행동): F68F ONNX/feature/signal path(F68F 온엑스/피처/신호 경로)를 고정하고 ATR SL/TP risk envelope(평균진폭 손절/익절 위험 봉투) 세 변형을 MT5 Strategy Tester(MT5 전략 테스터)에서 실행했다.

Effect(효과): F68F의 남은 DD(drawdown, 손실폭) 문제를 모델 변화가 아닌 런타임 위험 로직 변화로 분리해서 관찰했다.

- status(상태): `completed_atr_sltp_runtime_repair_probe_observation_no_authority(MT5 평균진폭 손절/익절 런타임 수리 탐침 관찰 완료, 권위 없음)`
- judgment(판정): `risk_envelope_repair_negative_or_inconclusive_no_authority(위험 봉투 수리 부정 또는 불충분, 권위 없음)`
- local verification(로컬 검증): `True`
- attempts(시도 수): `6`
- receipt rows(영수증 행): `6`

## Runtime KPI Versus F68F(F68F 대비 런타임 핵심 성과 지표)

| variant(변형) | split(분할) | net(순수익) | net delta(차이) | PF(수익 팩터) | PF delta(차이) | DD%(손실폭) | DD delta(차이) | trades/day(일 거래) | density delta(밀도 차이) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `f52_atr08_tp12_re3_sd6` | `validation` | `-488.58` | `-497.49` | `0.39` | `-0.62` | `97.72` | `72.66` | `15.220588` | `11.246324` |
| `f52_atr08_tp12_re3_sd6` | `oos` | `-302.33` | `-543.51` | `0.6` | `-0.58` | `60.51` | `40.94` | `24.405128` | `19.625641` |
| `tight_atr06_tp10_re3_sd6` | `validation` | `-488.58` | `-497.49` | `0.39` | `-0.62` | `97.72` | `72.66` | `15.220588` | `11.246324` |
| `tight_atr06_tp10_re3_sd6` | `oos` | `-302.33` | `-543.51` | `0.6` | `-0.58` | `60.51` | `40.94` | `24.405128` | `19.625641` |
| `wide_atr10_tp16_re3_sd6` | `validation` | `-488.58` | `-497.49` | `0.39` | `-0.62` | `97.72` | `72.66` | `15.220588` | `11.246324` |
| `wide_atr10_tp16_re3_sd6` | `oos` | `-302.33` | `-543.51` | `0.6` | `-0.58` | `60.51` | `40.94` | `24.405128` | `19.625641` |

## Grok Classification(Grok 조언 분류)

- accepted(수용): risk-envelope-only capped repair(위험 봉투 전용 상한 수리), three variants(세 변형), validation+OOS(검증+표본외).
- rejected(거절): threshold/model/feature changes(임계값/모델/피처 변경), completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성).
- needs_local_verification(로컬 검증 필요): handoff hash(인계 해시), .set binding(설정 바인딩), tester parity(테스터 동등성), KPI deltas(KPI 차이).

## Boundary(경계)

This is runtime probe observation only(런타임 탐침 관찰 전용). ATR SL/TP(평균진폭 손절/익절)는 new PF source(새 수익 팩터 원천)가 아니라 risk shape repair(위험 형태 수리)다.

Claim boundary(주장 경계): `atr_sltp_runtime_repair_probe_observation_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`
