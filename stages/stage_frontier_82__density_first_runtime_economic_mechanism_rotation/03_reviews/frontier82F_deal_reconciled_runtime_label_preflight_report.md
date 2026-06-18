# F82F Deal-Reconciled Runtime Label Preflight(F82F 거래 손익 대조 런타임 라벨 사전확인)

Updated(갱신): 2026-06-18T06:27:35Z

- run id(실행 ID): `frontier82F_deal_reconciled_runtime_label_preflight_v1`
- parent run(부모 실행): `frontier82E_capped_repair_or_rotation_decision_v1`
- runtime source(런타임 원천): `frontier82C_mt5_runtime_materialization_v1`
- target(대상): `f82b_07295` / `extra_trees_d7_l120`
- status(상태): `f82f_deal_level_report_evidence_reconciled_label_rebuild_ready_no_authority`
- judgment(판정): `deal_level_pnl_recovered_and_reconciled_runtime_label_rebuild_required_no_authority`
- next run(다음 실행): `frontier82G_mt5_realized_label_rebuild_v1`
- claim boundary(주장 경계): `runtime_deal_evidence_preflight_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`

## Action And Effect(행동과 효과)

Action(행동): F82C MT5 Strategy Tester report(F82C MT5 전략 테스터 보고서)에서 deal/trade rows(딜/거래 행)를 파싱하고 F82C runtime receipt(런타임 영수증)와 대조했다.

Effect(효과): EA telemetry patch(EA 텔레메트리 패치) 없이도 deal-level PnL evidence(거래별 손익 근거)를 회수했으므로, F82G(전선81G)는 threshold-only tweak(임계값만 바꾸기)이 아니라 MT5-realized label rebuild(MT5 실현 손익 라벨 재구축)로 갈 수 있다.

## Reconciliation KPI(대조 KPI)

| split(구간) | net(순손익) | PF(수익 팩터) | DD %(손실폭 %) | trades(거래 수) | trades/day(일 거래) | win %(승률 %) | gross profit(총이익) | gross loss(총손실) | max consecutive loss(최대 연속 손실) | time under water trades(회복 전 체류 거래) | reconciled(대조) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| validation | `-278.9800` | `0.7841` | `57.0000` | `1963` | `7.2169` | `32.8069` | `1013.4800` | `-1292.4600` | `20` | `1962` | `True` |
| oos | `-55.2100` | `0.9333` | `20.3600` | `1338` | `6.8615` | `36.7713` | `772.4300` | `-827.6400` | `11` | `1319` | `True` |

Deal rows(딜 행): `6602`. Trade rows(거래 행): `3301`.

Next condition(다음 조건): `Use reconciled MT5 report trades to rebuild a MT5-realized label(대조 완료된 MT5 보고서 거래로 MT5 실현 손익 라벨 재구축).`

Forbidden claims(금지 주장): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
