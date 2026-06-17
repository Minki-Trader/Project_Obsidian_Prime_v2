# F78 Stage Closeout Report(F78 단계 마감 보고서)

Updated(갱신): 2026-06-17T09:47:01Z

- status(상태): `closed_negative_memory_no_authority`
- judgment(판정): `negative_memory_with_preserved_clue_no_authority`
- closeout label(마감 라벨): `negative_memory(부정 기억)`
- Grok advice(Grok 조언): `accepted_with_conditions(조건부 수용)`
- final Codex direction(최종 Codex 방향): `close_with_boundary_and_next_hypothesis(경계와 다음 가설로 마감)`
- forbidden claim hits(금지 주장 감지): `none(없음)`
- claim boundary(주장 경계): `stage_closeout_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`

## Hypothesis(가설)

Execution-calibrated labels(실행 보정 라벨)이 broker contract P/L(브로커 계약 손익), calendar density(달력 밀도), fill semantics(체결 의미), lifecycle occupancy(생명주기 점유), risk penalty(위험 벌점)를 proxy(프록시)에 내장하면 F77 money/density gap(F77 금액/밀도 간극)을 줄일 수 있다.

## Closeout KPI(마감 핵심 성과 지표)

| test period(기간) | split/view(분할/보기) | net(순수익) | gross profit(총이익) | gross loss(총손실) | PF(수익 팩터) | DD%(손실폭) | trades(거래) | trades/day(일 거래) | win rate(승률) | avg win(평균 이익) | avg loss(평균 손실) | payoff(손익비) | expectancy(기대값) | recovery(회복 계수) | TUW(회복 전 체류) | max loss(최대 연속 손실) | long/short(롱/숏) | gap(간극) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| `2025-01-02..2025-10-01` | `F78B original next-bar proxy validation(F78B 원래 다음 봉 프록시 검증)` | `42.453781865295134` | `318.8597751891151` | `-276.40599332382` | `1.1535921177206854` | `0.21303624788330125` | `329` | `1.2140221402214022` | `0.44376899696048633` | `2.1839710629391447` | `-1.51041526406459` | `1.4459408050882563` | `0.1290388506543925` | `1.9927961690609015` | `105` | `7` | `side=short` | `net_delta=-68.98378186529513;pf_delta=-0.23359211772068533;dd_delta=11.236963752116697;signal_diff=0;feature_diff=0;cause=entry_timing_deposit_denominator_fill_path` |
| `2025-10-01..2026-04-14` | `F78B original next-bar proxy OOS(F78B 원래 다음 봉 프록시 표본외)` | `54.58482783574718` | `249.1854342303418` | `-194.60060639459454` | `1.2804966996097884` | `0.22925237368512172` | `243` | `1.2525773195876289` | `0.4609053497942387` | `2.224869948485195` | `-1.4855008121724773` | `1.4977238182935921` | `0.22462892113476204` | `2.38099291877865` | `107` | `12` | `side=short` | `runtime_not_executed_for_oos_by_scope` |
| `2025-01-02..2025-10-01` | `F78D MT5 validation runtime probe(F78D MT5 검증 런타임 탐침)` | `-26.53` | `317.63` | `-344.16` | `0.92` | `11.45` | `329` | `1.2095588235294117` | `36.17` | `2.669159663865546` | `-1.638857142857143` | `1.628671343014193` | `-0.08` | `-0.45` | `322` | `13` | `long=0;short=329` | `net_delta=-68.98378186529513;pf_delta=-0.23359211772068533;dd_delta=11.236963752116697;signal_diff=0;feature_diff=0;cause=entry_timing_deposit_denominator_fill_path` |
| `2025-01-02..2025-10-01` | `F78F repaired proxy validation(F78F 수리 프록시 검증)` | `2.0225802422398678` | `6.599998685203782` | `-4.577418442963913` | `1.441860465116279` | `0.30516122953092695` | `6` | `0.02214022140221402` | `0.5` | `2.199999561734594` | `-1.5258061476546378` | `1.441860465116279` | `0.33709670703997796` | `1.3255813953488393` | `1` | `1` | `side=long` | `repair_zero_scout_signal` |
| `2025-10-01..2026-04-14` | `F78F repaired proxy OOS(F78F 수리 프록시 표본외)` | `2.199999561734594` | `2.199999561734594` | `0.0` | `999.0` | `0.0` | `1` | `0.005154639175257732` | `1.0` | `2.199999561734594` | `0.0` | `0.0` | `2.199999561734594` | `999.0` | `0` | `0` | `side=long` | `repair_zero_scout_signal` |

## Preserved Clue(보존 단서)

- ONNX/EA feature and signal parity(ONNX/EA 피처와 신호 동등성)는 정확히 맞출 수 있었다.
- Selected-entry veto tape(선택 진입 거부 테이프)은 proxy selected count(프록시 선택 수)와 runtime signal count(런타임 신호 수)를 맞추는 도구로 보존한다.
- Entry timing(진입 시각)과 DD denominator(손실폭 분모)는 proxy label(프록시 라벨) 설계 시작부터 명시해야 한다.

## Negative Memory(부정 기억)

- Next-bar proxy(다음 봉 프록시)는 양수여도 MT5 same-bar execution(MT5 동일 봉 실행)에서는 음수가 될 수 있다.
- Runtime-aligned entry(런타임 정렬 진입)와 tester-deposit DD(테스터 예치금 손실폭) 수리 뒤 F78F는 scout clue(탐색 단서) 0, meaningful signal(의미 신호) 0이었다.
- F78은 threshold-only(임계값 단독)나 model-only(모델 단독) 수리로 계속 밀면 반복 수리가 된다.

## Grok Review(Grok 검토)

- packet(묶음): `docs/agent_control/grok_reviews/2026-06-17_f78g_stage_closeout_execution_calibrated_density_contract_pnl`
- prompt(프롬프트): `docs/agent_control/grok_reviews/2026-06-17_f78g_stage_closeout_execution_calibrated_density_contract_pnl/prompts/f78g_stage_closeout_execution_calibrated_density_contract_pnl_prompt.md` sha256 `80de463c50fafbd07309a4d2bd402eb65c25c2a29008b05657094445acf552d6`
- output(출력): `docs/agent_control/grok_reviews/2026-06-17_f78g_stage_closeout_execution_calibrated_density_contract_pnl/clean_output.md` sha256 `5c09c5dfc85aad53eca32e3756711ca6f51ce3efb34c89e2389cce16033a88bf`

This closeout(마감)은 completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)를 만들지 않는다.
