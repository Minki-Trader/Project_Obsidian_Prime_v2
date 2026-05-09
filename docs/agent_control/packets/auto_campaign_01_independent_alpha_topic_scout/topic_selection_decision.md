# AUTO-CAMPAIGN-01 Topic Selection Decision(AUTO-CAMPAIGN-01 주제 선택 결정)

- campaign_id(캠페인 ID): `AUTO-CAMPAIGN-01-INDEPENDENT-ALPHA-TOPIC-SCOUT`
- campaign_mode(캠페인 방식): `independent_topic_scout`
- branch(브랜치): `codex/auto-campaign-01-independent-alpha-topic-scout`
- budget(예산): stage candidates(단계 후보) 3개, selected new stage(선택 신규 단계) 1개, MT5 candidates(MT5 후보) 최대 68개
- claim boundary(주장 경계): `exploration_only_until_explicit_promotion_packet`

효과(effect, 효과): 새 stage(단계)를 만들기 전에 independent topic(독립 주제) 후보 3개를 먼저 고정해서 Stage36/38/39가 rail(레일)이 되지 않게 한다.

## Required Re-Entry Evidence(필수 재진입 근거)

- `AGENTS.md`: 탐색(exploration, 탐색)은 가능하지만 운영 주장(operating claim, 운영 주장)은 금지된다는 규칙을 확인했다.
- `docs/workspace/workspace_state.yaml`: Stage38(38단계)은 inconclusive runtime probe(불충분 런타임 탐침), Stage39(39단계)는 negative memory runtime probe(부정 기억 런타임 탐침)로 확인했다.
- `docs/context/current_working_state.md`: Stage36(36단계)은 map(지도)으로만 사용하고, Stage38/39를 follow-up(후속 작업)으로 쓰지 않는 경계를 확인했다.
- `docs/policies/stage_structure.md`: stage_id(단계 ID)는 `NN_area__specific_question` 형식이어야 하고, alpha transition(알파 전환)은 baseline selection(기준선 선택)이 아니라 topic pivot(주제 전환)임을 확인했다.
- Stage38 run32A packet(38단계 run32A 묶음): permission/abstention(허용/기권) overlap(겹침)은 검증과 OOS(표본밖) 불일치가 컸다.
- Stage39 run33A packet(39단계 run33A 묶음): non-entry exit overlay(비진입 청산 덮개)는 OOS(표본밖)에서 부정 기억으로 닫혔다.
- Stage36 synthesis(36단계 종합): seed clue(씨앗 단서)와 negative memory(부정 기억)만 사용했다.
- run registries(실행 장부): model family(모델군), permission/abstention(허용/기권), exit overlay(청산 덮개), state context(상태 문맥) 계열의 반복 실패를 확인했다.
- MT5 infrastructure(MT5 기반): `foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5`, `.ini/.set` 생성 helper(도우미), Tier A/B routing(Tier A/B 라우팅), Strategy Tester(전략 테스터) 실행 helper(도우미)가 현재 존재한다.
- code-surface debt(코드 표면 부채): global audit(전역 감사)는 기존 부채가 있으므로 selected-stage focused checks(선택 단계 집중 검사)를 별도로 기록한다.

## Three Independent Topic Candidates(독립 주제 후보 3개)

| stage_id(단계 ID) | idea_id(아이디어 ID) | topic family(주제군) | score(점수) | decision(결정) |
|---|---|---:|---:|---|
| `40_feature_interaction__volatility_squeeze_expansion_scout` | `IDEA-ST40-VOLATILITY-SQUEEZE-EXPANSION` | volatility/squeeze/expansion mechanism(변동성/수축/확장 메커니즘), feature interaction(피처 상호작용) | 86 | selected(선택) |
| `40_session_structure__cash_open_close_behavior_scout` | `IDEA-ST40-CASH-OPEN-CLOSE-BEHAVIOR` | session/time-of-day structure(세션/시간대 구조) | 78 | rejected(제외) |
| `40_direction_asymmetry__long_short_specialist_rebuild` | `IDEA-ST40-LONG-SHORT-SPECIALIST-REBUILD` | direction asymmetry(방향 비대칭), long/short specialization(롱/숏 특화) | 76 | rejected(제외) |

## Candidate 1: Selected(후보 1: 선택)

- proposed stage number(제안 단계 번호): `40`
- proposed canonical stage_id(제안 정식 단계 ID): `40_feature_interaction__volatility_squeeze_expansion_scout`
- proposed idea_id(제안 아이디어 ID): `IDEA-ST40-VOLATILITY-SQUEEZE-EXPANSION`
- proposed first run_id(제안 첫 실행 ID): `run34A_volatility_squeeze_expansion_broad_mt5_probe_v1`
- independent research question(독립 연구 질문): Bollinger squeeze(볼린저 수축), volatility expansion(변동성 확장), trend pressure(추세 압력) interaction(상호작용)이 Tier A primary + Tier B fallback(Tier A 우선 + Tier B 대체) 라우팅에서 validation(검증)과 OOS(표본밖)를 모두 버티는가?
- why not continuation(직접 후속이 아닌 이유): permission/abstention(허용/기권), exit overlay(청산 덮개), state context router(상태 문맥 라우터)를 쓰지 않는다.
- source clues used(사용 단서): Stage36(36단계) feature shape(피처 형태) 단서, Stage38/39의 실패 계열 회피, Tier B fallback(대체) 가능성, 기존 EBM table(EBM 표) MT5 runtime(런타임) 경로.
- expected data/artifact inputs(예상 입력 산출물): `model_input_dataset.parquet`, feature order(피처 순서), raw MT5 bars(raw MT5 봉), Tier B core42(Tier B 핵심 42) materialization(물질화), MT5 RuntimeProbeEA(런타임 탐침 EA).
- MT5 feasibility(MT5 가능성): one-feature discrete EBM table(한 피처 이산 EBM 표)과 candidate feature CSV(후보 피처 CSV)를 기존 `.ini/.set` 실행 경로로 넣을 수 있다.
- likely failure mode(예상 실패 양상): validation-only(검증 전용) 양호, OOS negative(OOS 음수), squeeze thinness(수축 구간 얇음), Tier B fallback dependence(Tier B 대체 의존).
- expected candidate grid size(예상 후보 격자 크기): broad sweep(넓은 탐색) 12개, micro-search(미세 탐색)는 gate(게이트) 통과 시 최대 12개.
- expected runtime cost(예상 실행 비용): broad MT5 attempts(MT5 시도) 24개, micro-search 발생 시 총 48개 이하.
- promotion-candidate potential(승격 후보 가능성): 중간이다. 메커니즘은 명확하지만 OOS(표본밖) 안정성이 관건이다.
- why selected(선택 이유): novelty(새로움), mechanism clarity(메커니즘 명확성), MT5 feasibility(MT5 가능성), robust negative memory(튼튼한 부정 기억) 생산력이 가장 균형 있다.

## Candidate 2: Rejected(후보 2: 제외)

- proposed stage number(제안 단계 번호): `40`
- proposed canonical stage_id(제안 정식 단계 ID): `40_session_structure__cash_open_close_behavior_scout`
- proposed idea_id(제안 아이디어 ID): `IDEA-ST40-CASH-OPEN-CLOSE-BEHAVIOR`
- proposed first run_id(제안 첫 실행 ID): `run34A_cash_open_close_behavior_broad_mt5_probe_v1`
- independent research question(독립 연구 질문): US cash open/close(미국 현금장 개장/마감) 구조가 Tier A/B(Tier A/B) 라우팅 후에도 validation/OOS(검증/표본밖)에서 살아남는가?
- why not continuation(직접 후속이 아닌 이유): Stage38/39의 decision layer(의사결정층)나 exit overlay(청산 덮개)를 쓰지 않는다.
- source clues used(사용 단서): session variables(세션 변수), registry(장부)상 session-age(세션 나이) 실패 기억, existing feature set(기존 피처 세트).
- expected data/artifact inputs(예상 입력 산출물): model input dataset(모델 입력 데이터셋), session columns(세션 열), Tier B fallback(Tier B 대체), MT5 runtime probe(런타임 탐침).
- MT5 feasibility(MT5 가능성): 높다. 시간대 rule(규칙)은 CSV feature(피처)로 쉽게 전달된다.
- likely failure mode(예상 실패 양상): session window(세션 창) 과적합, OOS regime shift(OOS 체제 변화), trade thinning(거래 얇아짐).
- expected candidate grid size(예상 후보 격자 크기): 10~14개.
- expected runtime cost(예상 실행 비용): broad MT5 attempts(MT5 시도) 20~28개.
- promotion-candidate potential(승격 후보 가능성): 낮음~중간이다.
- why rejected(제외 이유): 독립적이지만 과거 session-age(세션 나이) 실패 기억과 겹쳐 novelty(새로움)가 낮다.

## Candidate 3: Rejected(후보 3: 제외)

- proposed stage number(제안 단계 번호): `40`
- proposed canonical stage_id(제안 정식 단계 ID): `40_direction_asymmetry__long_short_specialist_rebuild`
- proposed idea_id(제안 아이디어 ID): `IDEA-ST40-LONG-SHORT-SPECIALIST-REBUILD`
- proposed first run_id(제안 첫 실행 ID): `run34A_long_short_specialist_rebuild_broad_mt5_probe_v1`
- independent research question(독립 연구 질문): long specialist(롱 특화)와 short specialist(숏 특화)를 분리하면 symmetric entry(대칭 진입)보다 validation/OOS(검증/표본밖)가 안정적인가?
- why not continuation(직접 후속이 아닌 이유): Stage38/39의 overlap(겹침), overlay(덮개), entry-count fix(진입 수 보정)를 주제로 삼지 않는다.
- source clues used(사용 단서): directional asymmetry(방향 비대칭) 가능성, repeated model-family failures(반복 모델군 실패), low-complexity rebuild(저복잡도 재구축) 필요성.
- expected data/artifact inputs(예상 입력 산출물): feature order(피처 순서), label class(라벨 클래스), Tier A/B routing(Tier A/B 라우팅), MT5 handoff bundle(MT5 인계 묶음).
- MT5 feasibility(MT5 가능성): 중간이다. long/short(롱/숏) 분리 rule(규칙)을 한 signal feature(신호 피처)로 압축할 수 있다.
- likely failure mode(예상 실패 양상): entry-count instability(진입 수 불안정), one-side thinness(한쪽 얇음), split asymmetry(분할 비대칭).
- expected candidate grid size(예상 후보 격자 크기): 12~16개.
- expected runtime cost(예상 실행 비용): broad MT5 attempts(MT5 시도) 24~32개.
- promotion-candidate potential(승격 후보 가능성): 중간이다.
- why rejected(제외 이유): 독립적이지만 entry-count instability(진입 수 불안정)를 다시 중심에 둘 위험이 있어 이번 campaign(캠페인) 목적과 덜 맞는다.

## Selected Topic(선택 주제)

Selected stage(선택 단계): `40_feature_interaction__volatility_squeeze_expansion_scout`

Selected idea(선택 아이디어): `IDEA-ST40-VOLATILITY-SQUEEZE-EXPANSION`

Selected run(선택 실행): `run34A_volatility_squeeze_expansion_broad_mt5_probe_v1`

효과(effect, 효과): 선택 기준은 expected profit(예상 수익)만이 아니라 novelty(새로움), mechanism clarity(메커니즘 명확성), MT5 feasibility(MT5 가능성), robustness(견고성)를 함께 본 것이다.
