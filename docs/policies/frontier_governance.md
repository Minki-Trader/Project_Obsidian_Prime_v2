# Frontier Governance(전선 운영 규칙)

이 문서는 Stage364(364단계) 이후 연구를 `stage_frontier_NN(전선 단계 번호)`로 여는 규칙을 정한다.

효과(effect, 효과)는 Stage12~364(12~364단계)의 긴 수리 연쇄(repair chain, 수리 연쇄)를 그대로 이어받지 않고, 필요한 기억(memory, 기억)만 참고하면서 새 연구 전선(research frontier, 연구 전선)을 독립적으로 시작하게 하는 것이다.

## Core Rule(핵심 규칙)

`stage_frontier_NN(전선 단계 번호)`은 independent campaign(독립 캠페인)이다.

기존 stage(단계)는 reference archive(참고 보관소)로 읽는다. 기존 stage(단계)의 winner(승자), baseline(기준선), promotion history(승격 이력), runtime authority(런타임 권위), live readiness(실거래 준비)는 가져오지 않는다.

짧은 규칙은 다음이다.

`reference, not inheritance(참조이지 상속 아님)`

## Folder Rule(폴더 규칙)

새 최상위 `frontiers/` folder(폴더)는 만들지 않는다.

Frontier stage(전선 단계)는 기존 stage artifact(단계 산출물) 구조를 쓴다.

```text
stages/stage_frontier_NN__specific_question/
  00_spec/
  01_inputs/
  02_runs/
  03_reviews/
  04_selected/
```

효과(effect, 효과)는 기존 `stages/*` 장부(ledger, 장부), 검토(review, 검토), 선택 상태(selection status, 선택 상태), 경로 규칙(path rule, 경로 규칙)을 유지하는 것이다.

## Opening Contract(개방 계약)

Frontier stage(전선 단계)를 열기 전에는 아래 항목을 먼저 적는다.

- `frontier_thesis(전선 가설)`: 이번 전선이 시험하는 큰 질문.
- `novelty_delta(신규성 차이)`: Stage12~364(12~364단계)와 무엇이 다른지.
- `prior_stage_scan(이전 단계 점검)`: 관련 이전 단계, 장부, 실패 기억을 무엇으로 확인했는지.
- `do_not_repeat(반복 금지)`: 같은 축을 반복하지 않기 위한 금지 목록.
- `exit_rule(종료 규칙)`: 어떤 조건이면 닫을지.
- `claim_boundary(주장 경계)`: 이번 전선에서 말할 수 있는 것과 금지되는 것.

## Prior-Stage Scan(이전 단계 점검)

Prior-stage scan(이전 단계 점검)은 vague review(모호한 검토)가 아니다. 아래 중 하나 이상을 구체적으로 적는다.

- `preserved clue(보존 단서)`
- `negative memory(부정 기억)`
- `reusable artifact(재사용 산출물)`
- `do-not-repeat note(반복 금지 메모)`
- `blocked retry condition(차단 재시도 조건)`

효과(effect, 효과)는 archive amnesia(보관소 망각)를 막되, 과거 결과를 운영 권위(operating authority, 운영 권위)로 세탁하지 않는 것이다.

## Runtime Economics Anchor(런타임 경제성 고정점)

F64-F67(전선64-67)의 교훈은 Frontier stage(전선 단계)의 기본 운영 기억으로 둔다.

- F64(전선64): proxy parity(프록시 동등성), ONNX handoff(온엑스 인계), local handoff quality(로컬 인계 품질)는 MT5 economics(MT5 경제성)를 보장하지 않는다.
- F65(전선65): SL/TP unit semantics(손절/익절 단위 의미)와 broker point mapping(브로커 포인트 매핑)이 틀리면 좋은 표면도 런타임에서 다른 의미가 된다.
- F66(전선66): feature/signal count parity(피처/신호 수 동등성)는 PnL/DD/density(손익/손실폭/밀도) 동등성이 아니다.
- F67(전선67): 이후 작업은 runtime-native lifecycle/cost/DD/order intent economics(런타임 네이티브 생명주기/비용/손실폭/주문 의도 경제성)를 우선한다.

효과(effect, 효과)는 Frontier(전선)가 좁은 repair(수리)나 parity-only economics(동등성 단독 경제성)로 되돌아가지 않고, 실제 MT5 runtime probe(MT5 런타임 탐침)가 필요한 주장을 낮춰 말하게 하는 것이다.

## Extra Stage Due Rule(추가 단계 도래 규칙)

Frontier Extra Stage(전선 추가 단계)는 50개 frontier closeout(전선 마감)마다 여는 heavy finite runtime-learning campaign(무겁지만 유한한 런타임 학습 캠페인)이다. 목표는 retrospective(회고)가 아니라, 이전 50개 frontier hypothesis/failure/negative memory/preserved clue/reusable artifact/do-not-repeat/reopen condition(가설/실패/부정 기억/보존 단서/재사용 산출물/반복 금지/재개 조건)을 ingredient(재료)로 바꿔 공격적 mix(혼합)를 실제 MT5 runtime(런타임)까지 밀어보는 것이다.

Due check(도래 점검)는 next frontier open(다음 전선 개방) 전에 실행한다. broad goal(넓은 목표)처럼 stage number(단계 번호)를 직접 말하지 않는 요청도, 새 frontier stage(전선 단계)를 열기 전에 `docs/registers/frontier_extra_stage_register.yaml`와 closeout receipts(마감 영수증)를 먼저 본다.

Trigger(트리거)는 다음이다.

- F50 closeout(전선50 마감) 뒤 E01(추가01)이 due(도래)다.
- F100 closeout(전선100 마감) 뒤 E02(추가02)가 due(도래)다.
- F150/F200...(전선150/200...)도 같은 규칙을 쓴다.
- 과거 due(도래)가 아직 등록되지 않았으면 backfill execution(소급 실행)으로 같은 E-number(추가 번호)를 연다.

Folder rule(폴더 규칙)은 기존 `stages/*` 구조를 유지한다.

```text
stages/stage_frontier_extra_E01__f001_f050_hypothesis_mixing_runtime_learning/
  00_spec/
  01_inputs/
  02_runs/
  03_reviews/
  04_selected/
```

E01(추가01)은 F01-F50(전선01-50)을 material window(재료 구간)로 쓰고, closeout(마감) 뒤 resume target(재개 대상)으로 원래 next frontier(다음 전선)를 남긴다. 현재 backfill case(소급 사례)에서는 F80 closed(F80 마감) 뒤 E01을 닫고 F81(전선81)로 돌아간다.

Ingredient card(재료 카드)는 최소한 source frontier(원천 전선), hypothesis(가설), artifact path/hash(산출물 경로/해시), salvage value(회수 가치), do-not-repeat(반복 금지), tier scope(티어 범위), claim boundary(주장 경계)를 가진다. 빠진 자료는 missing_material/blocked/out_of_scope_by_claim(자료 누락/차단/주장 범위 밖)으로 적고 빈칸으로 숨기지 않는다.

Ingredient card receipt(재료 카드 영수증)는 selection eligibility(선정 자격)와 selection lane candidates(선정 선로 후보)까지 가진다. Mix queue receipt(혼합 대기열 영수증)는 source card ids(원천 카드 ID), axis tags(축 태그), selection lanes(선정 선로), novelty delta(신규성 차이), near-duplicate cluster id(근접 중복 군집 ID), sample method(표본 방식), selected-for-runtime flag(런타임 선택 여부), selection reason(선정 사유), risk notes(위험 기록), claim boundary(주장 경계)를 가진다. 효과(effect, 효과)는 card selection(카드 선정)과 combination selection(조합 선정)을 “나중에 설명”으로 남기지 않고, runtime attempt(런타임 시도)와 연결되는 앞단 근거로 고정하는 것이다.

Mix rule(혼합 규칙)은 소심한 repair(수리)가 아니다. Feature set/label/model family/trade shape/risk logic/regime split(피처 묶음/라벨/모델 계열/거래 형태/위험 로직/장세 분할)을 넓게 섞고, center/low/high/extreme/absurd-but-legal boundary(중앙/저/고/극단/말도 안 되지만 합법 경계)를 포함한다. 같은 threshold/filter/parameter(임계값/필터/파라미터)만 바꾸는 반복은 금지한다.

### Progressive Mix Depth Contract(점증 혼합 깊이 계약)

E02(추가02)부터 Frontier Extra Stage(전선 추가 단계)는 combinatorial explosion(조합 폭발)을 만들지 않는다. 50!(팩토리얼) exhaustive mix(전체 혼합 탐색)는 금지하고, depth-sampled runtime learning(깊이 표본 런타임 학습)으로 운영한다.

기본 depth sequence(깊이 순서)는 2-mix -> 3-mix -> 4-mix(2개 혼합 -> 3개 혼합 -> 4개 혼합)다. 5-mix(5개 혼합)는 기본 금지이며, 별도 explicit packet(명시 작업 묶음)과 새 근거가 없으면 열지 않는다. 효과(effect, 효과)는 “더 많이 섞으면 나아질 것”이라는 performance chase(성과 추격)를 막고, 어떤 깊이에서 어떤 보완성이 생겼는지 attribution(귀속)을 남기는 것이다.

기본 cap(상한)은 아래와 같다.

| depth(깊이) | queue cap(대기열 상한) | materialized mix cap(물질화 혼합 상한) | MT5 attempt cap(MT5 시도 상한) |
| --- | ---: | ---: | ---: |
| 2-mix(2개 혼합) | 60 | 6 | 12 |
| 3-mix(3개 혼합) | 36 | 4 | 8 |
| 4-mix(4개 혼합) | 12 | 2 | 4 |

전체 MT5 attempt(시도)는 기본 24회다. invalid/block recovery(무효/차단 복구)를 포함해도 30회 hard cap(절대 상한)을 넘지 않는다. 이 cap(상한)을 늘리려면 work packet(작업 묶음)에 explicit cost/evidence reason(명시 비용/근거 사유)과 stop condition(중단 조건)을 남긴다.

2-mix open gate(2개 혼합 개방 게이트)는 ingredient card digest(재료 카드 요약), axis tags(축 태그), candidate cap(후보 상한), sampling method(표본 방식)를 먼저 고정한다. 2-mix close gate(2개 혼합 마감 게이트)는 selected attempt rows(선정 시도 행), untested manifest rows(미시험 목록 행), failure/gap cause(실패/간극 원인)를 남긴다. 3-mix(3개 혼합)는 최소 2개 이상의 independent cluster(독립 군집)가 diversity/risk/reproducibility/materialization(다양성/위험/재현성/물질화)을 통과할 때만 연다.

3-mix(3개 혼합)는 모든 triple(세 개 조합)을 만들지 않는다. 통과한 2-mix parent(부모 2개 혼합)에 새 complementary axis(보완 축) 하나만 붙인다. 3-mix close gate(3개 혼합 마감 게이트)는 parent 대비 additive/dilutive/blocked(가산/희석/차단)를 판정한다. 4-mix(4개 혼합)는 3-mix survivor(생존 혼합)가 여러 축에서 보완성을 보일 때만 synthesis stress probe(종합 압박 탐침)로 연다.

selection lane(선정 선로)은 PF(수익 팩터), DD resilience(손실폭 회복력), density/materiality(밀도/물질성), runtime materialization(런타임 물질화), negative-memory repair(부정 기억 수리)를 포함한다. `top_forward_pf(상위 전진 수익 팩터)`는 전체 MT5 후보의 25%를 넘을 수 없다. near-duplicate cluster(근접 중복 군집)는 한 depth(깊이) 안에서 하나만 고른다.

다음 depth(깊이)를 열면 안 되는 조건은 아래와 같다.

- survivor(생존 후보)가 `top_forward_pf(상위 전진 수익 팩터)`만으로 뽑혔다.
- OOS(표본외)에서 PF(수익 팩터)가 유지돼도 DD collapse(손실폭 붕괴)가 있다.
- validation/OOS split(검증/표본외 분할)이 모호하거나 OOS(표본외)가 선정 과정에 이미 쓰였다.
- 후보가 같은 feature family/label/session/trade shape/substrate(피처 계열/라벨/세션/거래 형태/바탕)에 몰렸다.
- 실패 원인(failure cause, 실패 원인)을 기록하지 않고 다음 depth(깊이)로 넘어가려 한다.

각 depth receipt(깊이 영수증)는 최소한 `depth_id(깊이 ID)`, `candidate_possible_count(가능 후보 수)`, `candidate_queued_count(대기열 후보 수)`, `candidate_cap(후보 상한)`, `sample_method(표본 방식)`, `selected_for_runtime_count(런타임 선택 수)`, `materialized_count(물질화 수)`, `runtime_completed_count(런타임 완료 수)`, `selection_lane_counts(선정 선로별 수)`, `top_forward_pf_share(상위 전진 수익 팩터 비율)`, `runtime_substrate_count(런타임 바탕 수)`, `single_substrate_warning(단일 바탕 경고)`, `full_mix_materialized=false(전체 혼합 물질화 아님)`, `depth_decision(깊이 결정)`, `claim_effect(주장 효과)`, `claim_boundary(주장 경계)`를 가진다. Depth receipt(깊이 영수증)는 ingredient card receipts(재료 카드 영수증), mix queue receipts(혼합 대기열 영수증), materialized attempt receipts(물질화 시도 영수증)와 같은 `mix_id/source_card_ids(혼합 ID/원천 카드 ID)`로 연결돼야 한다.

Materialized attempt(물질화 시도)는 dataset/feature_set/label/split identity(데이터셋/피처 묶음/라벨/분할 정체성), source identities(원천 정체성), parser/runtime contract version(파서/런타임 계약 버전), runtime substrate id(런타임 바탕 ID), compile_status/tester_status/runtime_status/report_status(컴파일/테스터/런타임/보고서 상태), ONNX path/hash(온엑스 경로/해시), EA source/binary hash(EA 원천/실행파일 해시), set/ini hash(설정 해시), feature_order_hash(피처 순서 해시), tester identity(테스터 정체성), telemetry/report/trade-list/snapshot/log path/hash(텔레메트리/보고서/거래목록/스냅샷/로그 경로와 해시), trade count/PF/DD/gap cause(거래 수/수익 팩터/손실폭/간극 원인), claim_effect/claim_boundary(주장 효과/주장 경계)를 남긴다. compile-only(컴파일 전용)는 runtime evidence(런타임 근거)가 아니다.

Extra Stage(추가 단계)가 한 runtime substrate(런타임 바탕)만 쓰면 `single_substrate_warning(단일 바탕 경고)`를 남긴다. 이 경우 runtime learning record(런타임 학습 기록)는 가능하지만 broad materialization claim(넓은 물질화 주장)은 금지한다.

Closeout(마감) 전에는 `frontier_extra_mix_depth_lint(전선 추가 혼합 깊이 점검)`로 ingredient card/mix queue/depth/attempt receipts(재료 카드/혼합 대기열/깊이/시도 영수증)를 검사한다. cap 초과, PF-only selection(PF 단독 선정), source card mismatch(원천 카드 불일치), unknown mix id(알 수 없는 혼합 ID), compile-only/proxy-only runtime evidence(컴파일 단독/프록시 단독 런타임 근거), single substrate warning missing(단일 바탕 경고 누락)은 blocked(차단) 또는 lowered claim boundary(낮춘 주장 경계)로 닫는다.

Runtime rule(런타임 규칙)은 MT5(메타트레이더5)를 final check(최종 확인)가 아니라 learning device(학습 장치)로 둔다. MT5 failure(MT5 실패), zero-trade(무거래), mismatch(불일치), crash/block(충돌/차단), PF/DD collapse(수익 팩터/손실폭 붕괴), density death(밀도 사망)는 negative evidence(부정 근거)로 기록한다. compile(컴파일)은 runtime evidence(런타임 근거)를 대체하지 않는다.

Closeout boundary(마감 경계)는 runtime learning record(런타임 학습 기록)다. Extra stage(추가 단계)는 completion(완성), selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성), git push as validation(깃 원격 반영을 검증으로 간주)을 만들지 않는다.

## Repair Rule(수리 규칙)

Repair work(수리 작업)는 기본적으로 같은 frontier stage(전선 단계) 안의 work packet(작업 묶음)으로 처리한다.

Repair packet(수리 작업 묶음)은 최소한 아래 항목을 적는다.

- `broken_artifact(고장 산출물)`: 무엇이 깨졌거나 불충분한지.
- `repair_boundary(수리 경계)`: 어디까지 고치고 어디부터는 새 전선으로 넘기는지.
- `novelty_check(신규성 점검)`: 단순 반복인지, 새 원천/라벨/런타임/검증 변화가 있는지.
- `exit_or_escalate(종료 또는 격상)`: 같은 frontier stage(전선 단계) 안에서 닫을지, 새 frontier stage(전선 단계)로 격상할지.

새 frontier stage(전선 단계)를 여는 조건은 다음 중 하나다.

- source(원천), label(라벨), runtime representation(런타임 표현), validation philosophy(검증 철학)가 바뀐다.
- 기존 frontier stage(전선 단계)의 exit rule(종료 규칙)이 발동했고, 다음 질문(question, 질문)이 같은 surface repair(표면 수리)를 이어받지 않는다.
- 같은 broad topic(넓은 주제)을 다시 열되 material novelty delta(실질 신규성 차이)를 기록한다.

기존 repair chain(수리 연쇄)이 novelty delta(신규성 차이) 없이 반복되는 것은 새 frontier stage(전선 단계)를 여는 조건이 아니다. 이 경우 같은 stage(단계)의 repair packet(수리 묶음)으로 닫거나, negative/invalid/blocked/out_of_scope(부정/무효/차단/주장 범위 밖) 처분을 남긴다.

효과(effect, 효과)는 모든 작은 수리(repair, 수리)를 새 단계로 부풀리지 않고, 동시에 끝없는 repair loop(수리 반복)를 막는 것이다.

## Five-Frontier Topic Rotation Guard(5전선 주제 회전 보호장치)

이 guard(보호장치)는 retrospective(회고)가 아니라 frontier open discipline(전선 개방 규율)이다. 새 canonical frontier stage(정식 전선 단계)를 열기 전 `frontier_topic_rotation_check(전선 주제 회전 점검)`를 기록한다. 효과(effect, 효과)는 탐색(exploration, 탐색)을 막지 않고, 다음 단계(next stage, 다음 단계)가 같은 수리나 같은 표면의 이름 바꾸기로 열리는 것을 막는 것이다.

점검 범위(scope, 범위)는 직전 frontier closeout(전선 마감)과 최근 5개 closed canonical frontier stages(마감된 정식 전선 단계)다. 5개보다 적으면 가능한 범위만 쓰되, 누락을 `missing_required(필수 누락)`, `blocked(차단)`, 또는 `out_of_scope_by_claim(주장 범위 밖)`로 표시한다. 이 규칙은 retired five-stage Grok retrospective(퇴역 5단계 그록 회고)를 되살리지 않고, Grok call(그록 호출), external review(외부 검토), completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위)를 만들지 않는다.

다음 frontier open(전선 개방)은 아래 형태로 열 수 없다.

- continuation repair(연속 수리)
- near-duplicate hypothesis(근접 중복 가설)
- threshold/filter/session/routing/parameter-only tweak(임계값/필터/세션/라우팅/파라미터만 미세조정)
- same artifact surface repair(동일 산출물 표면 수리)
- renamed repair(이름만 바꾼 수리)
- repair disguised as a new hypothesis(새 가설로 위장한 수리)

Repair disposition(수리 처분)은 같은 active frontier stage(활성 전선 단계) 안에서 닫는다. 수리 묶음(repair packet, 수리 묶음)은 `broken_artifact(고장 산출물)`, `repair_boundary(수리 경계)`, `attempted_fix_or_reason_not_runnable(시도한 수정 또는 실행 불가 사유)`, `result_judgment(결과 판정)`, `remaining_defect(남은 결함)`, `do_not_repeat_boundary(반복 금지 경계)`, `final_disposition(최종 처분)`을 남긴다. `final_disposition(최종 처분)`은 `fixed(수정됨)`, `negative_memory(부정 기억)`, `invalid_setup(무효 설정)`, `blocked_retry_condition(차단 재시도 조건)`, `out_of_scope_by_claim(주장 범위 밖)` 중 하나일 수 있다.

Blocked(차단)는 next frontier stage(다음 전선 단계)가 같은 수리를 상속해도 된다는 허가가 아니다. 차단이면 현재 stage(단계)를 차단으로 닫거나, 필요한 사용자 행동(user action, 사용자 행동) 또는 외부 조건(external condition, 외부 조건)이 충족될 때 같은 stage repair packet(동일 단계 수리 묶음)으로 재진입한다. 다음 frontier open(전선 개방)을 같은 고장 표면의 후속 수리로 만들 수 없다.

같은 broad topic(넓은 주제)은 나중에 다시 등장할 수 있다. 금지는 topic ban(주제 금지)이 아니라 adjacent same-axis continuation(인접 동일 축 연속) 금지다. 인접한 같은 broad topic(넓은 주제)을 다시 열려면 최소 하나의 primary axis(주요 축), 또는 두 개 이상의 supporting axes(보조 축)가 실제로 달라져야 한다. 인정되는 material novelty delta(실질 신규성 차이)는 source/data representation(원천/데이터 표현), label/target(라벨/목표), runtime representation(런타임 표현), validation philosophy(검증 철학), model family/objective(모델 계열/목적함수), trade shape/risk logic/regime split(거래 형태/위험 로직/장세 분할)이다.

5개 frontier stage(전선 단계)를 한 block(블록)으로 계획할 때는 dominant research mechanism(지배 연구 메커니즘)과 non-overlapping hypothesis axes(서로 겹치지 않는 가설 축)를 적는다. 계획하지 못한 경우에도 각 frontier open(전선 개방)은 같은 block(블록) 안의 앞선 stage(단계)들과 비교해 novelty delta(신규성 차이)를 기록한다.

`frontier_topic_rotation_check(전선 주제 회전 점검)`가 실패하면 현재 proposed next-open shape(제안된 다음 개방 형태)로는 새 frontier stage(전선 단계)를 열지 않는다. 같은 active stage(활성 단계)의 repair packet(수리 묶음)으로 남기거나, material novelty delta(실질 신규성 차이)가 있는 새 질문(question, 질문)으로 다시 제안한다. 이 실패는 broad topic(넓은 주제)의 future reuse(미래 재사용)를 금지하지 않는다.

## Decision Weight(결정 무게)

Frontier stage(전선 단계)는 run count(실행 수)가 아니라 decision weight(결정 무게)로 닫는다.

Closeout(마감)은 아래 중 하나 이상을 남겨야 한다.

- `negative memory(부정 기억)`
- `preserved clue(보존 단서)`
- `reference surface(참고 표면)`
- `seed surface(씨앗 표면)`
- `invalid setup(무효 설정)`
- `blocked retry condition(차단 재시도 조건)`
- `next frontier proposal(다음 전선 제안)`

Decision-weight checklist(결정 무게 점검표)는 아래 질문으로 확인한다.

- frontier thesis(전선 가설)가 resolved/negative/blocked(해결/부정/차단) 중 하나로 닫혔는가?
- novelty delta(신규성 차이)가 실제 실행이나 점검에서 시험됐는가?
- negative memory(부정 기억)나 preserved clue(보존 단서)가 구체 경로와 한계와 함께 남았는가?
- 외부 검증(external verification, 외부 검증)이 필요한 claim(주장)은 시도했거나 out_of_scope_by_claim(주장 범위 밖)으로 낮췄는가?
- repair-to-exploration ratio(수리 대비 탐색 비중)가 반복 루프(loop, 반복)를 숨기지 않는가?

## Five-Stage Retrospective Archive(5단계 중간 검토 보관)

Five-stage Grok retrospective(5단계 그록 중간 검토)는 retired historical archive rule(퇴역 역사 보관 규칙)로 보존한다. 모든 새 frontier operating path(전선 운영 경로)에서 active trigger(활성 트리거), Grok call(그록 호출), Grok receipt(그록 영수증), next-open block(다음 개방 차단)을 만들지 않는다.

효과(effect, 효과)는 기존 기록을 지우지 않으면서도 새 대화/cold start(냉시작)에서 Grok succession(그록 승계)처럼 동작하지 않게 하는 것이다.

Historical trigger(역사 트리거)는 아래와 같았다.

Trigger(트리거)는 두 겹이다.

- primary trigger(주 트리거): closing frontier number(마감 전선 번호)가 5의 배수다.
- fallback trigger(대체 트리거): 번호가 건너뛰거나 비연속(non-contiguous, 비연속)일 때 `docs/registers/five_stage_retrospective_register.yaml`의 `closed_frontier_ids_since_last_retrospective`가 5개다.

Scope resolver(범위 결정자)는 숫자 `NN-4..NN`만 쓰지 않는다. 실제 closeout receipt(마감 영수증)가 있는 최근 5개 canonical frontier stage id(정식 전선 단계 ID)를 쓴다. missing stage(누락 단계)는 빈칸이 아니라 `missing_required(필수 누락)`, `blocked(차단)`, 또는 `out_of_scope_by_claim(주장 범위 밖)`로 남긴다. 5개보다 적으면 retrospective completion(중간 검토 완료)을 주장하지 않고 `incomplete_block(불완전 블록)`으로 닫는다.

Required evidence row(필수 근거 행)는 아래 field(필드)를 가진다.

```text
stage_id | hypothesis | proxy_kpi | mt5_runtime_probe_kpi | proxy_runtime_gap_cause | closeout_label | preserved_clue | negative_memory | systemic_repeat | next_action
```

Block-level synthesis(블록 수준 종합)는 `repeated_systemic_issues(반복 시스템성 문제)`, `repair_priority_delta(수리 우선순위 변화)`, `direction_delta(방향 변화)`, `covered_stage_ids(검토된 단계 ID)`, `retrospective_packet_id(중간 검토 묶음 ID)`를 남긴다.

Report header(보고서 머리말)는 항상 아래 claim boundary(주장 경계)를 포함한다.

```text
ALLOWED(허용): direction_delta, repair_priority_delta
FORBIDDEN(금지): completion, baseline, promotion, runtime_authority, live_readiness, goal_achieve
```

Next frontier open block(다음 전선 개방 차단)은 이 archive rule(보관 규칙)에서 발동하지 않는다. 새 대체 회고가 도입되기 전까지는 `docs/registers/five_stage_retrospective_register.yaml`의 보관 상태와 Codex Task Force review receipt(코덱스 태스크포스 검토 영수증)를 함께 보고, gate(게이트), threshold(임계값), claim boundary(주장 경계)를 완화하지 않는다.

## Forbidden Imports(금지 반입)

Frontier stage(전선 단계)는 아래를 prior stage(이전 단계)에서 가져올 수 없다.

- selected baseline(선택 기준선)
- operating reference(운영 기준)
- promotion candidate(승격 후보)
- operating promotion(운영 승격)
- runtime authority(런타임 권위)
- live readiness(실거래 준비)
- Goal Achieve(목표 달성)

이 항목은 별도 promotion/operating packet(승격/운영 작업 묶음)이 없으면 주장하지 않는다.

## Tier Rule(티어 규칙)

Stage10(10단계) 이후의 Tier A/B paired record(티어 A/B 쌍 기록) 규칙은 frontier stage(전선 단계) 안에서도 유지한다.

Tier B(티어 B)나 combined record(합산 기록)를 만들 수 없으면 빈칸으로 두지 않는다. `missing_required(필수 누락)`, `blocked(차단)`, 또는 `out_of_scope_by_claim(주장 범위 밖)`로 적는다.

## First Frontier(첫 전선)

첫 frontier stage(전선 단계)는 다음으로 연다.

`stage_frontier_01__archive_synthesis_and_new_axis_lock`

이 frontier stage(전선 단계)의 목적은 Stage12~364(12~364단계)를 campaign map(캠페인 지도)으로 압축하고, 새 독립 실험(independent experiment, 독립 실험)을 열기 전에 archive interface(보관소 접점), 반복 금지(do-not-repeat, 반복 금지), 신규성 조건(novelty condition, 신규성 조건)을 고정하는 것이다.
