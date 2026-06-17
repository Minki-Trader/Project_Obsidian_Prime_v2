# Frontier72E Proxy/Runtime Gap Analysis(F72E 프록시/런타임 간극 분석)

- status(상태): `lifecycle_repair_proxy_found_pre_mt5_required`
- judgment(판정): `runtime_gap_repair_probe_required_no_authority`
- candidate_count(후보 수): `240`
- runtime_repair_probe_worthy_count(런타임 수리 탐침 가치 후보 수): `1`
- meaningful_candidate_count(의미 후보 수): `0`
- best_candidate(최선 후보): `f72e_0200` / `short_h24_sl0.9_tp1.8` / `mfe_mae_gap_040`
- best lifecycle validation net/PF/DD/trades_day(최선 생명주기 검증 순수익/수익 팩터/손실폭/일거래): `1145.3354118537886` / `1.087383584702364` / `9.753152408599872` / `2.2426470588235294`
- best lifecycle OOS net/PF/DD/trades_day(최선 생명주기 표본외 순수익/수익 팩터/손실폭/일거래): `799.9634399414033` / `1.0623888761175833` / `10.427543191719069` / `2.6822916666666665`

## Gap Cause(간극 원인)

- F72D signal count parity(신호 수 동등성)와 feature readiness parity(피처 준비 동등성)는 통과했다.
- Runtime order/trade count(런타임 주문/거래 수)는 selected signal count(선택 신호 수)의 약 32~38%로 줄었다.
- local_gap_cause(로컬 간극 원인): overlapping signal counting(겹친 신호 집계)이 MT5 single-position lifecycle(MT5 단일 포지션 생명주기)와 맞지 않았다.

Effect(효과): 다음 판단은 신호 생성이 아니라 lifecycle-aligned proxy(생명주기 정렬 프록시)를 기준으로 한다.

## Next Action(다음 행동)

`frontier72F_pre_mt5_lifecycle_repair_runtime_probe_v1`

Claim boundary(주장 경계): `proxy_runtime_gap_analysis_and_repair_proxy_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`
