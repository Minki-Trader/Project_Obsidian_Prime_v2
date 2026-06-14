# Frontier46 stage-open Grok review(그록 단계 개방 검토)

Role(역할): external second opinion(외부 2차 의견) only.

Do not claim operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), selected baseline(선택 기준선), or Goal Achieve(목표 달성).
Do not inspect files, call tools, or request more repository context(파일/도구/추가 저장소 문맥을 사용하지 말 것). Answer only from bounded evidence(제한 근거) below.

Current truth(현재 진실):
- F45 closed as `negative_memory(부정 기억)`.
- F45 runtime probe status(런타임 탐침 상태): `runtime_probe_ineligible_no_scout_seed_or_runtime_candidate_after_f45_event_classifier_proxy`.
- F45 scout/seed/runtime counts(탐색/씨앗/런타임 수): `0/0/0`.
- F45 best train-ranked row(학습 순위 최상 행): `f45b_0001`, event `event_mfe65_mae35_loss_contained`, model `extratrees_cls_d5_leaf240`, train PF 1.17, validation PF 0.90, OOS PF 0.95, forward DD 12.39.
- F45 nonwinner forward observation(비승자 전진 관찰): `f45c_0077`, event `event_mfe65_mae35_loss_contained`, model `logreg_balanced_l2_c0p25`, forward min PF 1.003, density 6.16..8.67/day, forward DD 10.70. This is clue only(단서 전용), not winner/baseline/promotion(승자/기준선/승격 아님).

Codex proposed F46 direction(코덱스 제안 방향):
- stage_id(단계 ID): `stage_frontier_46__short_pf_edge_event_sequence_context_pivot_after_f45_event_classifier_memory`
- run_id(실행 ID): `frontier46A_stage_open_short_pf_edge_event_sequence_context_hypothesis_design_v1`
- hypothesis(가설): A short event sequence context model(숏 이벤트 순서 문맥 모델) can improve the weak F45 event surface by using only closed-bar, entry-known lagged context(닫힌 봉/진입시점에 아는 지연 문맥): prior event-score rolling mean/slope, high-score cooldown, and fully-known past outcome tape with an embargo at least equal to the path horizon.
- decision_use(결정 용도): scout clue(탐색 단서), seed surface(씨앗 표면), or runtime probe candidate(런타임 탐침 후보) classification only.
- novelty_delta(신규성 차이): F46 changes the source from same-bar event classifier score(동일 봉 이벤트 분류 점수) to sequence context(순서 문맥). It must not repeat F45 by only changing score quantiles or class weights.
- comparison_baseline(비교 기준): F45 is reference-only(참조 전용). It is not a baseline(기준선) or winner(승자).
- control_variables(고정 변수): US100 M5, frozen 58 feature order(고정 58개 피처 순서), train/validation/OOS chronological split(시간순 분할), short-only(숏 전용), first-hit SL/TP path proxy(첫 터치 손익절 경로 프록시), validation/OOS read-only(검증/표본외 읽기 전용).
- changed_variables(변경 변수): lagged sequence context feature construction(지연 순서 문맥 피처 구성), sequence-context model family(순서 문맥 모델 계열), train-only score/risk thresholds(학습 전용 점수/위험 임계값).

Proposed guardrails(제안 보호선):
- Train-split-only construction lock(학습 분할 전용 구성 잠금): sequence feature definitions, event labels, class weights, probability thresholds, SL/TP caps, candidate rank, and repair choices are selected from train split only.
- Past outcome tape(과거 결과 테이프)는 current row(현재 행)보다 at least horizon+1 bars older(최소 예측수평선+1봉 이전)인 fully known labels(완전히 알려진 라벨)만 쓴다.
- Validation/OOS(검증/표본외)는 read-only evaluation(읽기 전용 평가)이다.
- Runtime boundary(런타임 경계): if no runtime candidate appears, MT5 runtime probe(메타트레이더5 런타임 탐침)는 ineligible(부적격)로 기록한다. If runtime candidate appears, stop before expensive WFO/MT5 and run pre-expensive Grok review(비싼 검증 전 그록 검토)를 먼저 한다.

Success criteria(성공 기준):
- scout clue(탐색 단서): forward validation/OOS both positive(검증/표본외 둘 다 양수), forward min PF >= 1.05, density 4..12/day, forward max DD <= 18%.
- seed surface(씨앗 표면): forward min PF >= 1.20, density 5..10/day, forward max DD <= 12%.
- runtime probe candidate(런타임 탐침 후보): seed surface plus forward min PF >= 1.50 and forward max DD <= 10%.

Failure/invalid conditions(실패/무효 조건):
- negative memory(부정 기억): capped proxy+repair does not create scout/seed/runtime candidate.
- preserved clue(보존 단서): sequence context improves one or more axes but fails seed/runtime.
- invalid setup(무효 설정): validation/OOS leakage, using not-yet-known future outcome labels as current features, same F45 threshold-only repair, or claiming runtime/ONNX authority without external validation.

Question(질문):
Is this F46 stage-open design honest, novel enough after F45, and properly guarded against leakage and overclaiming?

Return only:
1. verdict: accepted, rejected, or needs_local_verification(수용/거절/로컬 검증 필요)
2. main_guardrail(주 보호선)
3. one do_not_repeat(반복 금지) warning
4. one concrete improvement(구체 개선) if needed
5. claim_boundary_ok: yes/no(예/아니오)
