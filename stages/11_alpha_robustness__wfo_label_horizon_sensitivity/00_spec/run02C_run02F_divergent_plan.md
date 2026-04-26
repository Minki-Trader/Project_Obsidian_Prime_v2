# RUN02C-RUN02F Divergent Plan

## 의도(Intent, 의도)

RUN02C~RUN02F(실행 02C~02F)는 RUN01(실행 01)의 threshold/hold/slice(임계값/보유/구간) 근처 탐색을 반복하지 않고, LightGBM(`LightGBM`, 라이트GBM)의 실패 구조를 서로 다른 축으로 발산시켜 확인한다.

효과(effect, 효과): `run01Y(실행 01Y)`를 anchor(기준축)가 아니라 comparison scoreboard(비교 점수판)로만 두고, LGBM(라이트GBM)이 어디서 무너지는지 direction(방향), confidence(확신), context(문맥)로 나눠 본다.

## 계획(Plan, 계획)

| run(실행) | idea_id(아이디어 ID) | hypothesis(가설) | broad sweep(넓은 탐색) | evidence boundary(근거 경계) |
|---|---|---|---|---|
| RUN02C(실행 02C) | `IDEA-ST11-LGBM-DIRECTION-LONG-ONLY` | LGBM(라이트GBM) 실패가 direction-asymmetric(방향 비대칭)일 수 있고, short(숏)을 제거하면 회복할 수 있다 | long-only(롱만), Tier A/B routed(티어 A/B 라우팅) | `runtime_probe_only(런타임 탐침 전용)` |
| RUN02D(실행 02D) | `IDEA-ST11-LGBM-DIRECTION-SHORT-ONLY` | 반대로 long(롱)이 문제일 수 있으므로 short-only(숏만)를 본다 | short-only(숏만), Tier A/B routed(티어 A/B 라우팅) | `runtime_probe_only(런타임 탐침 전용)` |
| RUN02E(실행 02E) | `IDEA-ST11-LGBM-EXTREME-CONFIDENCE` | LGBM(라이트GBM)은 극단 확률과 high margin(높은 마진)에서만 쓸 수 있을 수 있다 | q0.99(99분위), high margin(높은 마진) | `runtime_probe_only(런타임 탐침 전용)` |
| RUN02F(실행 02F) | `IDEA-ST11-LGBM-CALM-TREND-GATE` | calm trend context(차분한 추세 문맥)에서만 신호가 깨끗할 수 있다 | `adx_14 >= 25`, `historical_vol_5_over_20 <= 1.25` | `runtime_probe_only(런타임 탐침 전용)` |

## 탐색 규율(Exploration Discipline, 탐색 규율)

- legacy_relation(과거 관계): `none(없음)`
- tier_scope(티어 범위): `Tier A + Tier B mixed(Tier A + Tier B 혼합)`
- extreme_sweep(극단 탐색): RUN02E(실행 02E)는 q0.99/high margin(99분위/높은 마진)
- micro_search_gate(세부 탐색 관문): validation/OOS(검증/표본외)가 함께 RUN02A/RUN02B(실행 02A/02B)의 손실 패턴을 멈출 때만 세부 조정한다.
- wfo_plan(WFO 계획): 이번 묶음은 explicit single-window runtime_probe exception(명시적 단일 구간 런타임 탐침 예외)이다. WFO(`walk-forward optimization`, 워크포워드 최적화)는 구조적으로 살아남은 아이디어가 있을 때 뒤에서 한다.
- failure_memory(실패 기억): 약하면 negative result(부정 결과)로 남기고, 새 label/model/context(라벨/모델/문맥)가 있을 때만 재개한다.
