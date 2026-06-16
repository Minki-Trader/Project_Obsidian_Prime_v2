# F68F Near-Four-Axis ONNX Runtime Repair Probe(F68F 네 축 근접 ONNX 런타임 수리 탐침)

Updated(갱신): 2026-06-16T18:02:30Z

## Action And Effect(행동 및 효과)

Action(행동): F68E repair queue(수리 대기열)의 primary candidate(주 후보) `f68b_0872ddc6192f`를 ONNX export(ONNX 내보내기)하고 MT5 Strategy Tester(MT5 전략 테스터) validation/OOS(검증/표본외)를 실행했다.

Effect(효과): F68D에서 무너진 runtime economics/DD(런타임 경제성/손실폭)가 feature set/trade spacing repair(피처 묶음/거래 간격 수리)로 개선되는지 관찰했다.

- status(상태): `completed_repair_runtime_probe_observation_no_authority(MT5 수리 탐침 관찰 완료, 권위 없음)`
- judgment(판정): `repair_probe_positive_signal_dd_improved_density_still_under_final_target_no_authority(수리 탐침 긍정 신호, 손실폭 개선, 거래 밀도 최종 목표 미달, 권위 없음)`
- export_status(내보내기 상태): `exported_onnx_parity_passed`
- local_verification_passed(로컬 검증 통과): `True`
- duplicate_feature_hash_equal(중복 피처 해시 동일): `True`

## Runtime KPI(런타임 핵심 성과 지표)

| split(분할) | period(기간) | net(순수익) | gross profit(총이익) | gross loss(총손실) | PF(수익 팩터) | DD%(손실폭) | trades(거래) | trades/day(일 거래) | signal diff(신호 차이) | feature diff(피처 차이) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `validation` | `2025-01-02..2025-10-01` | `8.91` | `1701.2` | `-1692.29` | `1.01` | `25.06` | `1081` | `3.974265` | `0` | `0` |
| `oos` | `2025-10-01..2026-04-14` | `241.18` | `1586.79` | `-1345.61` | `1.18` | `19.57` | `932` | `4.779487` | `0` | `0` |

## Boundary(경계)

- This is repair runtime probe evidence only(수리 런타임 탐침 근거 전용).
- F68D density/PF axes(F68D 밀도/수익 팩터 축)는 comparison anchors(비교 기준점)일 뿐이며 selected baseline(선택 기준선)이 아니다.
- If PF/DD improve but trades/day remains below 5, record preserved clue(보존 단서) or inconclusive(불충분), not completion(완성).

Claim boundary(주장 경계): `repair_runtime_probe_observation_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`
