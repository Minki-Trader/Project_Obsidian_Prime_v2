
# F68 Stage Brief(F68 단계 개요)

Stage(단계): `stage_frontier_68__runtime_native_trade_lifecycle_economics_proxy_onnx_scout`

Opened(개방): 2026-06-17T00:00:00Z

## Hypothesis(가설)

Runtime-native trade lifecycle economics proxy(런타임 기반 거래 생명주기 경제성 프록시)를 먼저 만들면, count/feature parity(개수/피처 동등성)만 맞춘 F67보다 MT5 Runtime Probe(MT5 런타임 탐침)의 PF/DD/trade density(수익 팩터/손실폭/거래 빈도) 간극을 더 직접적으로 줄일 수 있다.

## Action And Effect(행동 및 효과)

Action(행동): F68을 new frontier hypothesis lifecycle(새 전선 가설 생명주기)로 열고, first run(첫 실행)을 `frontier68A_stage_open_lifecycle_economics_proxy_design_v1`로 둔다.

Effect(효과): F67의 preserved clue/negative memory(보존 단서/부정 기억)는 reference only(참조 전용)로 쓰고, winner/baseline/promotion/runtime authority(승자/기준선/승격/런타임 권위)는 상속하지 않는다.

## Comparison Baseline(비교 기준)

- F67D MT5 Runtime Probe(F67D MT5 런타임 탐침): PF(수익 팩터) `1.0`, DD(손실폭) `30.58%`, trades/day(일 거래 수) `1.3282`, signal/feature diff(신호/피처 차이) `0/0`.
- F67C aggregate runtime-native order intent(F67C 집계 런타임 기반 주문 의도): signal/trade ratio(신호/거래 비율) `0.3468`, deal minus order fill positive rows(딜-주문 체결 양수 행) `53/64`, nonzero swap rows(스왑 0 아님 행) `54/64`.

## Controls(통제)

- symbol/timeframe(심볼/시간프레임): FPMarkets `US100` `M5`.
- no inheritance(상속 없음): no winner, no baseline, no promotion, no runtime authority, no live readiness(승자/기준선/승격/런타임 권위/실거래 준비 없음).
- tier record(티어 기록): Tier A separate/Tier B separate/Tier A+B combined(티어 A 분리/티어 B 분리/티어 A+B 합산)는 실행 가능해지는 즉시 기록한다.
- mandatory probe(필수 탐침): F68에서 meaningful proxy signal(의미 있는 프록시 신호)이 생기면 MT5 Strategy Tester(전략 테스터) Runtime Probe(런타임 탐침)를 최소 1회 실행한다.

## Changed Variables(변경 변수)

- label target(라벨 목표): trade lifecycle economics(거래 생명주기 경제성), cost identity(비용 정체성), DD basis(손실폭 기준).
- score source(점수 원천): proxy score(프록시 점수) must include lifecycle/cost/DD terms(생명주기/비용/손실폭 항).
- model/export path(모델/내보내기 경로): ONNX(온엑스)는 scoring vehicle(점수화 수단)일 뿐, stage subject(단계 주제)는 lifecycle economics proxy(생명주기 경제성 프록시)다.

## Invalid Conditions(무효 조건)

- same parity-only repair(같은 동등성 단독 수리)를 반복하면 invalid setup(무효 설정)으로 닫는다.
- bridge feasibility(연결 가능성)가 확인되지 않으면 MT5 probe(MT5 탐침)를 강행하지 않고 bridge repair action(연결 수리 행동)을 먼저 기록한다.
- proxy(프록시)가 zero signal(영 신호)을 만들면 runtime materialization(런타임 물질화)은 blocked/invalid(차단/무효)로 낮춰 판정한다.

## Evidence Plan(근거 계획)

1. `frontier68A_stage_open_lifecycle_economics_proxy_design_v1`: lifecycle economics label design and bridge preflight(생명주기 경제성 라벨 설계 및 연결 사전확인).
2. F68B: proxy prototype and row-level audit(프록시 원형 및 행 단위 감사).
3. F68C: candidate scoring or ONNX scout export if useful(후보 점수화 또는 필요 시 ONNX 탐색 내보내기).
4. F68D: mandatory MT5 Runtime Probe(필수 MT5 런타임 탐침) once proxy signal is meaningful(프록시 신호가 의미 있을 때).
5. F68E: proxy/runtime gap analysis and repair/closeout decision(프록시/런타임 간극 분석 및 수리/마감 결정).

## Grok Stage Open Review(그록 단계 개방 검토)

- prompt_path(프롬프트 경로): `docs/agent_control/grok_reviews/2026-06-17_f68_stage_open_runtime_lifecycle_proxy/prompts/f68_stage_open_prompt.md`
- prompt_sha256(프롬프트 해시): `8227a1c990ed555bf4da535c11eecebba3503c2beb291f56e8058ffa7d969ff5`
- clean_output_path(정리 출력 경로): `docs/agent_control/grok_reviews/2026-06-17_f68_stage_open_runtime_lifecycle_proxy/outputs/clean_output.md`
- clean_output_sha256(정리 출력 해시): `d02b2d66c7504f328722f433924b73b76608799535f7ad7ba39ea39f5c73d8d0`
- advice_classification(조언 분류): `accepted_with_local_verification(로컬 검증 조건 수용)`
- accepted(수용): open F68 as new frontier(새 전선으로 F68 개방), keep ONNX as scoring vehicle(ONNX는 점수화 수단), sequence with bridge preflight(연결 사전확인 포함 순서).
- needs_local_verification(로컬 검증 필요): runtime row inventory(런타임 행 목록), bridge feasibility checklist(연결 가능성 체크리스트), five-stage retrospective gate(5단계 중간 검토 게이트).

## Local Verification(로컬 검증)

- runtime row inventory(런타임 행 목록): F67C row table(F67C 행 표) and F67D KPI record(F67D KPI 기록) exist(존재).
- bridge feasibility(연결 가능성): `not_yet_verified(아직 검증 안 됨)`; F68A must write checklist(F68A에서 체크리스트 작성 필요).
- five-stage retrospective(5단계 중간 검토): after F67 closeout(마감 후) `not_due_2_of_5(아직 아님, 2/5)`.

Claim boundary(주장 경계): scout clue/seed surface/runtime probe observation/completion candidate(탐색 단서/씨앗 표면/런타임 탐침 관찰/완성 후보)까지만 허용한다. completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 주장하지 않는다.
