# Frontier41 Stage Open Grok Review(전선41 단계 개방 그록 검토)

You are Grok(Grok, 그록) acting only as an external second opinion(외부 2차 의견). Do not claim operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), selected baseline(선택 기준선), or Goal Achieve(목표 달성).

Do not inspect files, call tools, or request more repository context(파일/도구/추가 저장소 문맥을 사용하지 말 것). Answer only from the bounded evidence(제한 근거) below.

## Current Truth(현재 진실)

- Workspace(작업공간): Project Obsidian Prime v2, FPMarkets `US100` `M5`.
- Latest closed stage(최근 닫힌 단계): `stage_frontier_40__short_pf_edge_non_score_source_pivot_after_regime_gate_negative`.
- F40 result(F40 결과): `preserved_clue_negative_memory`.
- F40 best scout(F40 최상 탐색): `f40b_0001`, rule `vix_zscore_20 >= q75 & ppo_hist_12_26_9 <= q25`.
- F40 validation/OOS PF-density-DD(F40 검증/표본외 수익 팩터-밀도-손실폭): `1.154 / 7.262 / 11.867` and `1.158 / 7.985 / 13.517`.
- F40 seed/runtime rows(F40 씨앗/런타임 행): `0 / 0`.
- F40 runtime probe status(F40 런타임 탐침 상태): `runtime_probe_ineligible_no_seed_or_runtime_candidate_after_f40_proxy_repair`.
- Forbidden import(금지 반입): no winner/baseline/promotion/runtime authority/live readiness(승자/기준선/승격/런타임 권위/실거래 준비 없음) from prior stages.

## Proposed Frontier41 Direction(제안 전선41 방향)

Hypothesis(가설): The F40 short-side raw feature pocket may have enough entry density(진입 밀도) but a poor exit shape(청산 형태). If we freeze entry source(진입 원천) to F40 scout rows and vary only executable exit shapes(실행 가능한 청산 형태), train-only exit shape selection(학습 전용 청산 형태 선택) may improve validation/OOS PF/DD(검증/표본외 수익 팩터/손실폭) without repeating raw feature threshold mining(원천 피처 임계값 채굴 반복).

## Planned Proxy(예정 프록시)

- Entry source(진입 원천): frozen F40 scout-derived short pockets only, starting with top F40 rows. No new raw feature threshold search(새 원천 피처 임계값 탐색 없음).
- Exit source(청산 원천): path-native raw OHLC first-hit replay(경로 기반 원천 OHLC 선터치 재생).
- Exit variants(청산 변형):
  - fixed hold bars(고정 보유 봉 수): `4, 6, 8, 12, 18`.
  - stop/take train quantiles(손절/익절 학습 분위수) from selected train entries only.
  - conservative first-hit tie-break(동시 터치 시 보수적 손절 우선).
  - optional time-stop after `N` bars(선터치 없으면 N봉 뒤 청산).
- Selection freeze(선택 고정): entry pockets and exit thresholds are selected on train split only. Validation/OOS are read-only(검증/표본외 읽기 전용).
- Comparison(비교): density-matched A comparison(밀도 맞춤 A 비교) and F40 fixed-exit reference(고정 청산 참조) where available.

## Success Boundary(성공 경계)

Scout clue(탐색 단서): validation and OOS both PF >= `1.03`, density `4-12/day`, DD <= `18%`, and non-negative lift vs density-matched A(밀도 맞춤 A 대비 비음수 상승).

Seed surface(씨앗 표면): validation and OOS both PF >= `1.20`, density `5-10/day`, DD <= `12%`.

Runtime candidate(런타임 후보): validation and OOS both PF >= `1.50`, density `5-10/day`, DD <= `10%`, and executable first-hit/time-stop representation(실행 가능한 선터치/시간 청산 표현).

If runtime candidate appears, Codex stops before expensive WFO/MT5(비싼 WFO/MT5 전 중지) and asks Grok for pre-expensive review(비싼 실행 전 검토).

## Claim Boundary(주장 경계)

This is proxy-only(프록시 전용) until seed/runtime rows exist and later validation closes. No completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).

## Review Question(검토 질문)

Is this F41 direction novel and bounded enough after F40? Please answer with:

1. `verdict`: accepted / rejected / needs_local_verification(수용/거절/로컬 검증 필요)
2. `novelty_ok`: yes/no and why
3. `leakage_guard_ok`: yes/no/needs_local_verification
4. `runtime_claim_boundary_ok`: yes/no
5. `mandatory_guardrail`: one or two guardrails Codex must implement before trusting the proxy
6. `do_not_repeat`: what would make this stage a repeat of F40/F31/F32/F33 instead of a new hypothesis
