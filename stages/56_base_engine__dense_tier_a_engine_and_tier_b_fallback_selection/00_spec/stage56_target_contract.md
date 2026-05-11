# Stage56 Target Contract(56단계 목표 계약)

- stage_id(단계 ID): `56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection`
- contract_id(계약 ID): `stage56_target_contract_v1`
- claim_boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion`

## Density Target(거래 밀도 목표)

- preferred target(선호 목표): 실제 MT5 closed trades(닫힌 거래) 일 평균 `5~10`건
- minimum review target(최소 검토 목표): 실제 MT5 closed trades(닫힌 거래) 일 평균 `3`건 이상
- failure density(실패 밀도): validation(검증) 또는 OOS(표본외)에서 일 평균 `1~2`건 이하로 유지

## Quality Target(품질 목표)

- strong pass(강한 통과): validation(검증)과 OOS(표본외)가 모두 양수이고 profit factor(수익 팩터)가 `1.10~1.20` 이상
- weak pass(약한 통과): validation(검증)과 OOS(표본외)가 모두 양수이고 profit factor(수익 팩터)가 `1.05` 이상
- drawdown rule(손실폭 규칙): max drawdown(최대 손실폭)이 거래 수 증가보다 빠르게 폭발하면 `baseline_candidate_only(기준선 후보 전용)` 또는 `no_dense_engine_found(두꺼운 엔진 없음)`로 낮춘다.

## Tier B Fallback Rule(Tier B 대체 규칙)

Tier B(티어 B)는 다음 조건을 모두 만족할 때만 routed entry(라우팅 진입)가 된다.

- Tier A(티어 A)가 신호를 내지 않는다.
- 현재 position(포지션)이 없다.
- Tier B(티어 B)가 flat(무진입)이 아닌 신호를 낸다.
- MT5 execution rule(MT5 실행 규칙)이 skip(스킵)하지 않는다.

효과(effect, 효과)는 Tier B(티어 B) 단독 수익을 routed value(라우팅 가치)로 오해하지 않게 하는 것이다.

## Allowed Results(허용 결과)

- `selected_research_baseline(선택 연구 기준선)`
- `baseline_candidate_only(기준선 후보 전용)`
- `no_dense_engine_found(두꺼운 엔진 없음)`

## Invalid Conditions(무효 조건)

- split boundary(분할 경계)가 불명확하다.
- MT5 report(메타트레이더5 보고서)와 ledger row(장부 행)가 연결되지 않는다.
- Python signal count(파이썬 신호 수)만 있고 MT5 closed trades(닫힌 거래)가 없다.
- Tier A/B routed total(Tier A/B 라우팅 전체)을 synthetic sum(합성 합산)으로 만든다.
