# Frontier43 stage-open Grok review(그록 단계 개방 검토)

Role(역할): external second opinion(외부 2차 의견) only.

Do not claim operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), selected baseline(선택 기준선), or Goal Achieve(목표 달성).
Do not inspect files, call tools, or request more repository context(파일/도구/추가 저장소 문맥을 사용하지 말 것). Answer only from bounded evidence(제한 근거) below.

Codex current truth(현재 진실):
- latest closed stage(최근 종료 단계): `stage_frontier_42__short_pf_edge_timing_source_pivot_after_f41_exit_shape_negative`
- closeout_class(마감 분류): `preserved_clue_negative_memory`
- runtime_probe_status(런타임 탐침 상태): `runtime_probe_ineligible_no_seed_or_runtime_candidate_after_f42_timing_proxy`
- F42 scout/seed/runtime(탐색/씨앗/런타임): `3/0/0`
- best F42 row(최상 F42 행): `f40b_0010_session_morning_5_120_session_morning_5_120_hold12_s18_t86`
- best F42 forward_min_pf(전진 최소 수익 팩터): `1.0552581638705354`
- best F42 forward density(전진 일 거래 수): `4.147540983606557` to `4.442748091603053`
- best F42 forward_max_dd(전진 최대 손실폭): `7.518263157657257`
- claim boundary(주장 경계): no completion/baseline/promotion/runtime authority/live readiness(완성/기준선/승격/런타임 권위/실거래 준비 없음)

Codex proposed Frontier43 direction(제안 방향):
- stage_id(단계 ID): `stage_frontier_43__short_pf_edge_trade_shape_source_pivot_after_f42_timing_negative`
- hypothesis(가설): If weak short PF(숏 수익 팩터) is mainly a trade-shape problem(거래 형태 문제), then entry-known feature conditions(진입 시점에 아는 피처 조건) selected by train-only path/trade-shape diagnostics(학습 전용 경로/거래 형태 진단) can find a source that improves PF/DD/density(수익 팩터/손실폭/밀도) without inheriting F42 timing gates(타이밍 제한).
- novelty_delta(신규성 차이): F40 raw feature pockets(원천 피처 포켓)는 PF-forward selection(전진 수익 팩터 선택)에 가까웠고, F41 exit shape(청산 형태), F42 timing(타이밍)은 source masks(원천 마스크)를 mostly fixed(대체로 고정)했다. F43 changes source selection criterion(원천 선택 기준) to train-only trade shape(학습 전용 거래 형태): payoff ratio(손익비), adverse excursion(불리 이동), stop/take balance(손절/익절 균형), loss streak(연속 손실), underwater ratio(손실 체류 비율), holding profile(보유 형태).
- comparison_baseline(비교 기준): F42 best observed scout row(최상 관찰 탐색 행) as reference-only(참조 전용), not baseline/winner(기준선/승자 아님).
- control_variables(고정 변수): US100 M5, frozen 58 feature order hash(고정 58개 피처 순서 해시), train/validation/OOS split(학습/검증/표본외 분할), short-only side(숏 전용), closed-bar features(닫힌 봉 피처), train-only thresholds(학습 전용 임계값).
- changed_variables(변경 변수): source ranking/composition(원천 순위/구성) from train-only trade-shape metrics(학습 전용 거래 형태 지표). Timing gates(타이밍 제한) are not the primary lever(주 레버 아님).
- proxy plan(프록시 계획): build single/pair entry-known feature conditions(단일/쌍 피처 조건), exclude pure session-clock conditions(순수 세션 시계 조건 제외), rank by train-only trade-shape quality(학습 전용 거래 형태 품질), then evaluate validation/OOS read-only(검증/표본외 읽기 전용) with finite fixed-hold and train-quantile bracket exits(유한 고정 보유와 학습 분위수 브래킷 청산).
- capped repair(상한 수리): If no seed/runtime candidate(씨앗/런타임 후보 없음), run one bounded trade-shape profile diagnostic(상한 거래 형태 프로필 진단) on top source rows only. No unbounded feature mining(무제한 피처 채굴 없음), no timing-gate expansion(타이밍 제한 확장 없음), no F42 best row inheritance(F42 최상 행 상속 없음).

Success criteria(성공 기준):
- scout clue(탐색 단서): train-positive shape lane(학습 양수 형태 경로) and forward_min_pf >= 1.05, forward density 4~12/day, forward_max_dd <= 18%.
- seed surface(씨앗 표면): forward_min_pf >= 1.20, density 5~10/day, forward_max_dd <= 12%.
- runtime probe candidate(런타임 탐침 후보): seed plus forward_min_pf >= 1.50, density 5~10/day, forward_max_dd <= 10%, executable entry-known source(실행 가능한 진입시점 원천).
- final target gates(최종 목표 게이트)는 final completion review(최종 완성 검토)에서만 hard gate(강제 게이트)다.

Invalid conditions(무효 조건):
- validation/OOS outcome(검증/표본외 결과)을 source selection(원천 선택)에 사용함.
- F42 timing gate(타이밍 제한)를 winner/baseline(승자/기준선)처럼 상속함.
- session-clock filtering(세션 시계 필터링)이 primary lever(주 레버)가 됨.
- runtime/ONNX authority(런타임/온엑스 권위)를 proxy-only(프록시 전용) 결과로 주장함.

Question(질문):
Is this F43 direction honest and novel enough under reference-not-inheritance(참조이지 상속 아님) and the F42 negative memory(부정 기억)? Give one required guardrail(필수 보호선), one do-not-repeat warning(반복 금지 경고), and whether the proposed claim boundary(주장 경계) is acceptable.

Return only:
1. verdict: accepted, rejected, or needs_local_verification(수용/거절/로컬 검증 필요)
2. required_guardrail(필수 보호선)
3. do_not_repeat(반복 금지)
4. claim_boundary_ok: yes/no(예/아니오)
