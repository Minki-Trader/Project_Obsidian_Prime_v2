# F76 Stage Closeout Report(F76 단계 마감 보고서)

Updated(갱신): 2026-06-17T06:31:16Z

- status(상태): `closed_preserved_clue_negative_memory_no_authority`
- judgment(판정): `preserved_clue_negative_memory_no_authority`
- closeout label(마감 라벨): `preserved_clue_negative_memory`
- Grok advice(그록 조언): `accepted_with_conditions(조건부 수용)`
- final Codex direction(최종 Codex 방향): `close_as_preserved_clue_negative_memory(보존 단서/부정 기억으로 마감)`
- forbidden claim hits(금지 주장 감지): `none(없음)`
- next action(다음 행동): `frontier77A_stage_open_runtime_lifecycle_label_density_rebuild_v1`
- claim boundary(주장 경계): `stage_closeout_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`

## Hypothesis and Proxy(가설과 프록시)

Hypothesis(가설): feature/label/model/trade/risk/session axes(피처/라벨/모델/거래/위험/세션 축)를 넓게 바꾸면 runtime economics(런타임 경제성)의 원천을 찾을 수 있다.

Best F76B proxy(최선 F76B 프록시): `f76b_06637` axes `mega_cap_removed/extra_trees_d7_l60/long_fwd12_q60/cash_open/trend_aligned`.
Proxy validation net/PF/DD/tpd/trades(프록시 검증 순수익/수익 팩터/손실폭/일거래/거래): `1760.3101806640625/1.594854315978897/6.4446875/1.0601092896174864/194`.
Proxy OOS net/PF/DD/tpd/trades(프록시 표본외 순수익/수익 팩터/손실폭/일거래/거래): `1471.7918701171875/1.6893374882536825/7.8916796875/1.1755725190839694/154`.

## Closeout KPI(마감 핵심 성과 지표)

| split/view(분할/보기) | test period(테스트 기간) | net(순수익) | gross profit(총이익) | gross loss(총손실) | PF(수익 팩터) | DD%(손실폭) | trades(거래) | trades/day(일거래) | win%(승률) | avg win(평균 이익) | avg loss(평균 손실) | payoff(손익비) | expectancy(기대값) | recovery(회복) | TUW(회복 전 체류) | max loss streak(최대 연속 손실) | long/short(롱/숏) | proxy/runtime gap(프록시/런타임 간극) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|
| `validation` | `2025-01-02..2025-10-01` | `152.99` | `294.13` | `-141.14` | `2.08` | `6.6` | `50` | `0.18382352941176472` | `64.0` | `9.1915625` | `-7.84111111111111` | `1.1722270440697182` | `3.06` | `4.36` | `not_available_in_runtime_receipt(런타임 영수증에 없음)` | `not_available_in_runtime_receipt(런타임 영수증에 없음)` | `long=50;short=0` | `proxy_net=1760.31;runtime_net=152.99;proxy_pf=1.59485;runtime_pf=2.08;proxy_dd=6.44469;runtime_dd=6.6;proxy_tpd=1.06011;runtime_tpd=0.183824` |
| `oos` | `2025-10-01..2026-04-14` | `66.09` | `206.2` | `-140.11` | `1.47` | `10.04` | `38` | `0.19487179487179487` | `63.16` | `8.591666666666667` | `-10.007857142857144` | `0.8584921371303499` | `1.74` | `1.13` | `not_available_in_runtime_receipt(런타임 영수증에 없음)` | `not_available_in_runtime_receipt(런타임 영수증에 없음)` | `long=38;short=0` | `proxy_net=1471.79;runtime_net=66.09;proxy_pf=1.68934;runtime_pf=1.47;proxy_dd=7.89168;runtime_dd=10.04;proxy_tpd=1.17557;runtime_tpd=0.194872` |

## Gap and Repair(간극과 수리)

- F76E primary gap cause(주 간극 원인): `same_direction_hold_compression_after_signal_parity`
- max same-direction hold share(최대 동방향 보유 비율): `0.7532467532467533`
- F76F repair candidates(수리 후보): `5120`
- F76F meaningful/density/near counts(F76F 의미/밀도/근접 수): `0/0/0`
- F76F best OOS net/PF/DD/tpd(최선 표본외 순수익/수익 팩터/손실폭/일거래): `-924.4258422851562/0.8767163964311262/15.959394531250002/3.9236641221374047`

## Closeout Judgment(마감 판정)

Preserved clue(보존 단서): independent proxy(독립 신호 프록시)는 mega-cap removed/trend/session(대형주 제거/추세/세션) 축에서 PF 1.5~1.7, DD 10% 미만의 신호를 만들 수 있다.

Negative memory(부정 기억): 신호마다 독립 거래로 계산한 proxy(프록시)는 MT5 single-position max-hold runtime(단일 포지션 최대 보유 런타임)에서 거래 수를 약 4~6배 과대평가했다. lifecycle-aware repair(생명주기 인식 수리)를 넣으면 고밀도 후보의 PF와 DD가 무너졌다.

Next action(다음 행동): 다음 frontier stage(전선 단계)는 label/target/trade shape(라벨/목표/거래 형태)를 처음부터 runtime lifecycle(런타임 생명주기)에 맞춰 설계한다.

## Grok Closeout Receipt(그록 마감 영수증)

- packet(묶음): `docs/agent_control/grok_reviews/2026-06-17_f76g_stage_closeout_axis_ablation`
- prompt(프롬프트): `docs/agent_control/grok_reviews/2026-06-17_f76g_stage_closeout_axis_ablation/prompts/f76g_stage_closeout_axis_ablation_prompt.md` sha256 `e1c8dad317e215c9a1a5c628dd7dad5ccffae0a921ee85282731beb93e3786d9`
- output(출력): `docs/agent_control/grok_reviews/2026-06-17_f76g_stage_closeout_axis_ablation/clean_output.md` sha256 `e81f52a6bf0f7fcf2fb7ff6e1ed5731cec6691d425373d3831c8bbf614bf10e8`
- success(성공): `True` returncode `0`
