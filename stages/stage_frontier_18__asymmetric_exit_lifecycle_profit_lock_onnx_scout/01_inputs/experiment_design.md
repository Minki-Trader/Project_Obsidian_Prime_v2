# Frontier18 Experiment Design(전선18 실험 설계)

- primary_family(주 작업군): `experiment_design(실험 설계)`
- primary_skill(주 스킬): `obsidian-experiment-design`
- support_skills(보조 스킬): `obsidian-data-integrity`, `obsidian-model-validation`, `obsidian-grok-collaboration`
- required_gates(필수 게이트): `work_packet_schema_lint`, `external_review_packet`, `lifecycle_profile_lock_gate`, `required_gate_coverage_audit`, `final_claim_guard`

hypothesis(가설): Asymmetric exit lifecycle(비대칭 청산 생명주기) and profit-lock policy(수익 잠금 정책) can improve PF/DD/smoothness(수익 팩터/손실폭/매끄러움) for moderate ONNX entry signals(중간 품질 ONNX 진입 신호) without reusing F17 loss-cluster firewall alpha(전선17 손실 군집 방화벽 알파).

decision_use(결정 용도): Open a bounded proxy scout(제한된 프록시 탐색) for lifecycle profiles(생명주기 프로필), not a completion or runtime authority claim(완성 또는 런타임 권위 주장 아님).

comparison_baseline(비교 기준): F17B proxy and F17C MT5 runtime observation(전선17B 프록시와 전선17C MT5 런타임 관찰), reference only(참조 전용).

control_variables(통제 변수): US100 M5 FPMarkets data contract(US100 5분봉 FPMarkets 데이터 계약), closed-bar inference(닫힌 봉 추론), 58-feature order contract(58개 피처 순서 계약), one concurrent position max(동시 포지션 1개), fixed 0.1 lot for scout runtime probe(탐색 런타임 탐침 고정 0.1랏)

changed_variables(변경 변수): max hold bars(최대 보유 봉), flat/opposite exit behavior(중립/반대 신호 청산 동작), ATR stop/take-profit bracket(ATR 손절/익절 괄호), entry-known exit-risk overlay when available(가능하면 진입 시점에 아는 청산 위험 덧씌움)

sample_scope(표본 범위): Tier A full-context sample first(티어 A 전체 문맥 표본 우선), Tier B and combined records explicit if missing(티어 B와 합산은 누락 시 명시).

success_criteria(성공 기준): {"scout_clue": "validation/OOS PF moves toward 2+, density stays near 5~10/day, DD improves toward 10~15%, and smoothness improves(검증/표본외 수익 팩터 2+ 방향, 일 5~10회 근처, 손실폭 10~15% 방향, 매끄러움 개선).", "seed_surface": "a lifecycle profile reduces proxy or MT5 DD/smoothness damage without density below 3/day(생명주기 프로필이 밀도 3/day 미만 붕괴 없이 프록시 또는 MT5 손실폭/매끄러움 손상을 줄임).", "runtime_probe_obligation": "one narrow MT5 runtime probe before closeout or exact blocked reason(마감 전 좁은 MT5 런타임 탐침 1회 또는 정확한 차단 사유)."}

failure_criteria(실패 기준): global exit repair damages net/PF/expectancy like Stage344(전역 청산 수리가 344단계처럼 순수익/수익 팩터/기대값 훼손), lifecycle-aware proxy clears parity but cost/direction failure remains like Stage337(생명주기 인식 프록시가 동등성은 맞지만 337단계처럼 비용/방향 실패 유지), density/PF/DD tradeoff repeats F17 MT5 collapse(빈도/수익 팩터/손실폭 상충이 전선17 MT5 붕괴 반복)

invalid_conditions(무효 조건): validation/OOS lifecycle retuning(검증/표본외 생명주기 재조정), F17 loss-cluster firewall alpha reused as main hypothesis(전선17 손실 군집 방화벽 알파를 주 가설로 재사용), current-bar or future outcome leakage(현재봉 또는 미래 결과 누수)

stop_conditions(중단 조건): strict scout clue or seed surface found, then pre-expensive Grok review before MT5(WFO/MT5 전 그록 검토), no seed after pre-registered profiles, then repair/closeout decision(사전 등록 프로필 후 씨앗 없음이면 수리/마감 결정), runtime claim would be needed, then MT5 probe attempted or exact blocked reason recorded(런타임 주장이 필요하면 MT5 탐침 시도 또는 정확한 차단 기록)

evidence_plan(근거 계획): stage open summary and manifests(단계 개방 요약과 목록), proxy profile metrics by split(분할별 프록시 프로필 지표), Tier A/B/combined ledger rows(티어 A/B/합산 장부 행), ONNX parity when a model artifact is created(모델 산출물 생성 시 ONNX 동등성), MT5 runtime probe report before closeout(마감 전 MT5 런타임 탐침 보고서)
