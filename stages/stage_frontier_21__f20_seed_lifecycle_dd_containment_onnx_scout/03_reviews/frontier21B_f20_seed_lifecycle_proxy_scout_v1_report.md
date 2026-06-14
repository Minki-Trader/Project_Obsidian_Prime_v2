# Frontier21B F20 Seed Lifecycle Proxy Scout Report(전선21B F20 씨앗 생명주기 프록시 탐색 보고서)

Updated(갱신): 2026-06-14T06:18:48Z

Status(상태): `lifecycle_proxy_no_forward_clue_repair_or_closeout_required`

Judgment(판정): `negative_pressure_needs_repair_or_closeout(부정 압력, 수리 또는 마감 필요)`

Action(행동): fixed F20 entry(고정 F20 진입)에 5개 pre-registered lifecycle profiles(사전 등록 생명주기 프로필)를 적용했습니다.

Effect(효과): DD(손실폭) 변화가 entry retuning(진입 재조정)이 아니라 lifecycle/risk stack(생명주기/위험 묶음)에서 왔는지 분리했습니다.

Entry signal(진입 신호): `vix_zscore_20 <= q30 & close_ema50_ratio >= q70`, `long(롱)`

Scout/seed/handoff rows(탐색/씨앗/인계 행): `0` / `0` / `0`

Best profile by forward read(전진 읽기 기준 최상 프로필): `f21b_hold10_atr1p5_tp3p0_cd6`

Best validation PF/density/DD(최상 검증 수익 팩터/빈도/손실폭): `1.34955` / `2.09774/day` / `4.80425%`

Best OOS PF/density/DD(최상 표본외 수익 팩터/빈도/손실폭): `1.25047` / `2.27174/day` / `3.19186%`

DD reduction vs F20 report(전선20 보고 대비 손실폭 감소): validation(검증) `26.9401`, OOS(표본외) `17.5847`.

Runtime probe status(런타임 탐침 상태): `out_of_scope_by_claim_no_handoff_candidate_yet(인계 후보 전이라 주장 범위 밖)`

Artifacts(산출물): `stages/stage_frontier_21__f20_seed_lifecycle_dd_containment_onnx_scout/02_runs/frontier21B_f20_seed_lifecycle_proxy_scout_v1/candidate_summary.csv`, `stages/stage_frontier_21__f20_seed_lifecycle_dd_containment_onnx_scout/02_runs/frontier21B_f20_seed_lifecycle_proxy_scout_v1/metrics_by_split.csv`, `stages/stage_frontier_21__f20_seed_lifecycle_dd_containment_onnx_scout/02_runs/frontier21B_f20_seed_lifecycle_proxy_scout_v1/trade_log.csv`

Next action(다음 행동): `frontier21C_lifecycle_repair_or_closeout_decision_v1`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
