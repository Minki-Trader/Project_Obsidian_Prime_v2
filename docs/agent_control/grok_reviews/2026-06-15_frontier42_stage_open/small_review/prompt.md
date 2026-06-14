# Frontier42 stage-open Grok review(그록 단계 개방 검토)

Role(역할): external second opinion(외부 2차 의견) only.

Do not claim operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), selected baseline(선택 기준선), or Goal Achieve(목표 달성).
Do not inspect files, call tools, or request more repository context(파일/도구/추가 저장소 문맥을 사용하지 말 것). Answer only from bounded evidence(제한 근거) below.

## Current truth(현재 진실)

- F41 closed as `preserved_clue_negative_memory`.
- F41 found 94 scout clues(탐색 단서) but 0 seed surfaces(씨앗 표면) and 0 runtime probe candidates(런타임 탐침 후보).
- Best F41 observed row: `f40b_0013_initial_exit_family_hold04_s18_t86`, forward min PF(전진 최소 수익 팩터) 1.080, density(거래 밀도) 7.18~7.43/day, max DD(최대 손실폭) 6.04, same-entry lock(동일 진입 잠금) true.
- F41 negative memory(부정 기억): exit shape(청산 형태) alone did not get close enough to final target(최종 목표).
- F41 preserved clue(보존 단서): exit shape can compress DD(손실폭), but train-positive track(학습 양수 경로) must be kept so score-only DD compression does not dominate.

## Proposed Frontier42 direction(제안 방향)

Open `stage_frontier_42__short_pf_edge_timing_source_pivot_after_f41_exit_shape_negative`.

Hypothesis(가설): F40/F41 short raw pockets(숏 원천 포켓)의 weak PF(약한 수익 팩터)는 time-of-session contamination(세션 시간 오염)일 수 있다. Entry-known timing gates(진입 시점에 아는 타이밍 제한), especially `minutes_from_cash_open`, first/last 30m flags(첫/마지막 30분 플래그), broad session buckets(넓은 세션 구간), and optionally broker-clock hour/day-of-week diagnostics(브로커 시계 시간/요일 진단), may isolate a train-positive(학습 양수), forward-stable(전진 안정) short source without new feature-threshold mining(새 피처 임계값 채굴).

## Planned proxy(계획 프록시)

- Use frozen 58-feature model input dataset(58 피처 모델 입력 데이터셋): 46,650 rows(행), train 29,222 / validation 9,844 / oos 7,584.
- Use F40/F41 entry sources only as reference clues(참조 단서): the 12 frozen short entry masks from F41 entry manifest(진입 고정 목록). No winner/baseline/promotion inheritance(승자/기준선/승격 상속 없음).
- Change only timing gates(타이밍 제한): broad NY session buckets based on `minutes_from_cash_open`, first/last 30m flags, and a capped diagnostic broker-hour/day-of-week family.
- Keep exit representation finite and executable(실행 가능): fixed hold 4/6/8/12 plus train-only MFE/MAE quantile stop/take, conservative stop-first path replay(보수적 stop-first 경로 재현).
- Require train-positive lane(학습 양수 경로) tracking separately from best forward score(최상 전진 점수).

## Success criteria(성공 기준)

- Scout clue(탐색 단서): validation and oos PF >= 1.05, density 4~12/day, DD <= 18, timing gate executable, no same-entry/source mutation.
- Seed surface(씨앗 표면): train PF >= 1.03 and validation/oos PF >= 1.20, density 5~10/day, DD <= 12.
- Runtime probe candidate(런타임 탐침 후보): train PF >= 1.05 and validation/oos PF >= 1.50, density 5~10/day, DD <= 10, expressible as timing + finite exit rules.
- If runtime candidate appears, stop before expensive WFO/MT5 and run pre-expensive Grok(비싼 검증 전 그록) first.

## Claim boundary(주장 경계)

This stage may report scout clue(탐색 단서), seed surface(씨앗 표면), runtime probe observation(런타임 탐침 관찰), or completion candidate(완성 후보) only if evidence supports it.

It may not claim completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), or Goal Achieve(목표 달성).

## Review question(검토 질문)

Is this Frontier42 timing-source pivot(타이밍 원천 전환) novel enough and properly bounded after F41, or is it just another disguised repair loop(위장 수리 반복)?

Return only:
1. verdict: accepted, rejected, or needs_local_verification(수용/거절/로컬 검증 필요)
2. novelty_ok: yes/no(예/아니오)
3. leakage_guard_ok: yes/no/needs_local_verification(예/아니오/로컬 검증 필요)
4. runtime_claim_boundary_ok: yes/no(예/아니오)
5. mandatory guardrails(필수 보호선), max 3
6. do-not-repeat note(반복 금지 메모), max 3
