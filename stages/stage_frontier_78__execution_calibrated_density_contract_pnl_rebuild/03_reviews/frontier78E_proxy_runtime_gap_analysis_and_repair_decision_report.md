# Frontier78E Proxy/Runtime Gap Analysis And Repair Decision Report(F78E 프록시/런타임 간극 분석 및 수리 결정 보고서)

Updated(갱신): 2026-06-17T09:25:19Z

- status(상태): `gap_analysis_completed_entry_timing_deposit_repair_required_no_authority`
- judgment(판정): `runtime_gap_explained_repair_required_no_authority`
- test period(테스트 기간): `2025-01-02..2025-10-01`
- split/view(분할/보기): `validation/Tier A MT5 Runtime Probe(검증/Tier A MT5 런타임 탐침)`
- source candidate(원천 후보): `f78b_02234`
- claim boundary(주장 경계): `gap_analysis_and_repair_decision_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`

## KPI Gap(KPI 간극)

| view(보기) | net(순수익) | gross profit(총이익) | gross loss(총손실) | PF(수익 팩터) | DD%(손실폭) | trades(거래) | trades/day(일 거래) | win rate(승률) | expectancy(기대값) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| next-bar proxy validation(다음 봉 프록시 검증) | `42.453781865295134` | `318.8597751891151` | `-276.40599332382` | `1.1535921177206854` | `0.21303624788330125` | `329` | `1.2140221402214022` | `0.44376899696048633` | `0.1290388506543925` |
| same-bar proxy validation(동일 봉 프록시 검증) | `-10.59193337383514` | `287.4077653256878` | `-297.999698699523` | `0.9644565634795653` | `0.44969587815730844` | `329` | `1.2140221402214022` | `0.4012158054711246` | `-0.03219432636424055` |
| MT5 runtime validation(MT5 런타임 검증) | `-26.53` | `317.63` | `-344.16` | `0.92` | `11.45` | `329` | `1.2095588235294117` | `36.17` | `-0.08` |

## Gap Cause(간극 원인)

- signal count parity(신호 수 동등성): `0` diff(차이).
- feature readiness parity(피처 준비 동등성): `0` diff(차이).
- order fill rate(주문 체결률): `1.0`.
- dominant entry timing gap(주요 진입 시각 간극): `-5.0` minutes(분), MT5 opens earlier(MT5가 더 빠름).
- sign flip(승패 뒤집힘): `91/329`.
- DD denominator(손실폭 분모): same-bar proxy DD(동일 봉 프록시 손실폭)는 balance 10000(잔고 10000) 기준 `0.44969587815730844`%, deposit 500(예치금 500) 기준 `8.99391756314617`%.

## Repair Decision(수리 결정)

Next run(다음 실행): `frontier78F_entry_timing_deposit_calibrated_proxy_repair_v1`

Accepted repairs(수용 수리):
- rebuild labels using runtime-aligned same-bar entry or export features shifted so MT5 entry equals proxy next-bar entry(런타임 정렬 동일 봉 진입 라벨 재구성 또는 MT5 진입이 프록시 다음 봉 진입과 같도록 피처 시프트)
- replace proxy DD denominator 10000 with tester/account deposit 500 or report both amount and percent(프록시 DD 분모 10000을 테스터/계좌 예치금 500으로 교체하거나 금액/퍼센트 둘 다 기록)
- score candidates on runtime-calibrated fill path penalty and loss-side gap(런타임 보정 체결 경로 벌점과 손실 측 간극으로 후보 점수화)

Rejected repairs(거절 수리):
- change model family before fixing execution contract(실행 계약을 고치기 전에 모델 계열만 교체)
- raise threshold only to hide the gap(간극을 숨기기 위해 임계값만 올리기)
- claim runtime authority from matched signal count alone(신호 수 일치만으로 런타임 권위 주장)
