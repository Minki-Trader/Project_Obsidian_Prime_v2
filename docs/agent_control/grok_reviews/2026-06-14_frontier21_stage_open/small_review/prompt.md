# Frontier21 Stage Open Review(전선21 단계 개방 검토)

You are Grok(그록), external second opinion(외부 2차 의견). Review only this bounded snapshot(제한 스냅샷). Do not claim baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), or Goal Achieve(목표 달성).

## Current Truth(현재 진실)

- Frontier20(전선20)은 `preserved_clue + negative_memory(보존 단서 + 부정 기억)`로 닫혔다.
- Preserved clue(보존 단서): `low_vix_momentum_price_position_long_feature_state_surface_density_aligned_pf12_seed(낮은 VIX 모멘텀/가격 위치 롱 피처 상태 표면은 빈도 정렬 PF 약 1.2 씨앗 표면)`.
- Best F20 seed(전선20 최선 씨앗): `vix_zscore_20 <= q30 & close_ema50_ratio >= q70`, long(롱), validation PF/density/DD(검증 수익 팩터/빈도/손실폭) `1.32666 / 8.57923/day / 31.7443%`, OOS PF/density/DD(표본외 수익 팩터/빈도/손실폭) `1.22065 / 9.9084/day / 20.7766%`.
- Negative memory(부정 기억): train-only depth-2 rule atlas(학습 전용 깊이2 규칙 지도) alone(단독)은 DD(손실폭)를 줄이거나 runtime handoff(런타임 인계)를 만들지 못했다.
- Runtime probe(런타임 탐침)는 F20 locks(F20 잠금) 아래 handoff candidate(인계 후보)가 없어 ineligible(부적격)였다.

## Proposed Frontier21 Direction(제안 전선21 방향)

Open `stage_frontier_21__f20_seed_lifecycle_dd_containment_onnx_scout(전선21 F20 씨앗 생명주기 손실폭 억제 ONNX 탐색)`.

Hypothesis(가설): Use the F20 low-VIX momentum/price-position long entry surface(F20 낮은 VIX 모멘텀/가격 위치 롱 진입 표면) only as a reference clue(참조 단서), then test a new runtime-representable lifecycle/risk mechanism(런타임 표현 가능한 생명주기/위험 메커니즘): next-bar-open entry(다음 봉 시가 진입), ATR stop/take-profit(ATR 손절/익절), max-hold bars(최대 보유 봉), re-entry cooldown(재진입 쿨다운), and optional early-adverse-exit(초기 불리 이동 청산). The aim is to reduce DD(손실폭) toward under 10% while preserving 5~10 trades/day(일 5~10회 거래) and improving PF(수익 팩터), without calling it completion(완성).

Novelty delta(신규성 차이):

- Different from F20(전선20과 다름): not another train-only rule atlas rerank(학습 전용 규칙 지도 재순위 반복 아님); entry surface(진입 표면)는 fixed reference clue(고정 참조 단서)이고 changed variable(변경 변수)은 lifecycle/risk rule stack(생명주기/위험 규칙 묶음)이다.
- Different from F18(전선18과 다름): not a new model/backbone lifecycle sweep(새 모델/백본 생명주기 훑기 아님); it uses a specific F20 seed entry surface(특정 F20 씨앗 진입 표면) and asks whether risk mechanics(위험 메커니즘)가 DD-heavy seed(손실폭 큰 씨앗)를 구조적으로 정화할 수 있는지 본다.
- Different from F17(전선17과 다름): not a loss-cluster firewall(손실 군집 방화벽) alone(단독); it is bar-level trade lifecycle simulation(봉 단위 거래 생명주기 시뮬레이션) with explicit stop/take/hold/cooldown(손절/익절/보유/쿨다운).

## Success Criteria(성공 기준)

- Scout clue(탐색 단서): validation/OOS(검증/표본외) both positive(둘 다 양수), density(빈도) near 5~10/day(일 5~10회 근처), and DD(손실폭) clearly lower than F20 seed.
- Seed surface(씨앗 표면): validation/OOS PF(검증/표본외 수익 팩터) at least around 1.2, density(빈도) 5~10/day(일 5~10회), DD(손실폭) materially below F20, and no single split collapse(단일 분할 붕괴 없음).
- Handoff candidate(인계 후보): only if validation/OOS density(검증/표본외 빈도) 5~10/day, PF(수익 팩터) >= 1.5, DD(손실폭) <= 15%, and smoothness(매끄러움) improves. If this appears, Codex(코덱스) must ask for pre-expensive Grok review(비싼 실행 전 그록 검토) before MT5(runtime) work.

## Claim Boundary(주장 경계)

Allowed words(허용 표현): scout clue(탐색 단서), seed surface(씨앗 표면), runtime probe observation(런타임 탐침 관찰), preserved clue(보존 단서), negative memory(부정 기억), invalid setup(무효 설정), blocked(차단).

Forbidden words(금지 표현): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성).

## Review Question(검토 질문)

Is this a valid new frontier hypothesis(유효한 새 전선 가설) and not a forbidden repetition(금지 반복)? Answer with:

- Decision(결정): accept(수용), adjust(조정), or reject(거절)
- Main risk(주요 위험)
- Required adjustment(필수 조정)
- Stop condition(중단 조건)
- Claim boundary reminder(주장 경계 알림)
