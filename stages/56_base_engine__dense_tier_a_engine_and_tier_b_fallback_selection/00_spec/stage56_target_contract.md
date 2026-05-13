# Stage56 Target Contract(56단계 목표 계약)

- stage_id(단계 ID): `56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection`
- contract_id(계약 ID): `stage56_target_contract_v2_reopen_goal`
- claim_boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion`
- stage_mode(단계 모드): `active_in_progress_until_selected_research_baseline`

## Reopen Rule(재개 규칙)

Stage56(56단계)은 selected_research_baseline(선택 연구 기준선)을 찾을 때까지 열린 optimization campaign(최적화 캠페인)이다.

효과(effect, 효과): stronger candidate(강화 후보), completed candidate batch(완료 후보 묶음), failed hypothesis family(실패 가설군), progress log(진행 기록), closeout-like packet(종료 유사 묶음)은 Stage56(56단계)을 닫지 못한다.

## Density Target(거래 밀도 목표)

- preferred target(선호 목표): 실제 MT5 closed trades(닫힌 거래) 일 평균 `5~10`건
- minimum review target(최소 검토 목표): 실제 MT5 closed trades(닫힌 거래) 일 평균 `3`건 이상
- failure density(실패 밀도): validation(검증) 또는 OOS(표본외)에서 일 평균 `1~2`건 이하로 유지

## Quality Target(품질 목표)

- strong pass(강한 통과): validation(검증)과 OOS(표본외)가 모두 양수이고 profit factor(수익 팩터)가 `1.10~1.20` 이상
- weak pass(약한 통과): validation(검증)과 OOS(표본외)가 모두 양수이고 profit factor(수익 팩터)가 `1.05` 이상
- drawdown rule(손실폭 규칙): max drawdown(최대 손실폭)이 거래 수 증가보다 빠르게 폭발하면 selected_research_baseline(선택 연구 기준선)으로 선언하지 않는다. Stage56(56단계)은 open(열림) 상태로 유지하고 progress evidence(진행 근거)와 next hypothesis branch(다음 가설 가지)를 기록한다.

## Tier B Fallback Rule(Tier B 대체 규칙)

Tier B(티어 B)는 다음 조건을 모두 만족할 때만 routed entry(라우팅 진입)가 된다.

- Tier A(티어 A)가 신호를 내지 않는다.
- 현재 position(포지션)이 없다.
- Tier B(티어 B)가 flat(무진입)이 아닌 신호를 낸다.
- MT5 execution rule(MT5 실행 규칙)이 skip(스킵)하지 않는다.

효과(effect, 효과)는 Tier B(티어 B) 단독 수익을 routed value(라우팅 가치)로 오해하지 않게 하는 것이다.

## Terminal Result(종료 결과)

- `selected_research_baseline(선택 연구 기준선)`

Stage56(56단계)의 유일한 terminal condition(종료 조건)은 selected_research_baseline(선택 연구 기준선)이다.

## Selected Research Baseline Criteria(선택 연구 기준선 조건)

selected_research_baseline(선택 연구 기준선)은 아래 조건을 모두 만족할 때만 선언한다.

- actual routed MT5 validation trades/day(실제 라우팅 MT5 검증 일 거래 수) >= `5.0`
- actual routed MT5 OOS trades/day(실제 라우팅 MT5 표본외 일 거래 수) >= `5.0`
- validation net(검증 순손익) > `0`
- OOS net(표본외 순손익) > `0`
- validation PF(검증 수익 팩터) >= `1.10`
- OOS PF(표본외 수익 팩터) >= `1.10`
- cost-stressed expectancy(비용 압박 기대값)가 양수로 유지된다.
- MFE capture(최대 유리 이동 포착)가 `d390h10` reference(참고)보다 materially worse(실질 악화)하지 않다.
- density increase(밀도 증가)가 same-move(동일 이동) 또는 same-direction split re-entry(동방향 분할 재진입)에서 주로 오지 않는다.
- Tier B fallback-only OOS(Tier B 대체 전용 표본외)가 non-negative(비음수)이거나, Tier B(티어 B)가 근거와 함께 명시적으로 disabled(비활성화)된다.
- actual routed result(실제 라우팅 결과)는 one MT5 tester account path(단일 MT5 테스터 계좌 경로)에서 생산되고 synthetic aggregation(합성 집계)이 아니다.
- validation/OOS MT5 reports(검증/표본외 MT5 보고서)가 `summary.json`과 CSV(쉼표 구분 파일)로 파싱된다.
- ledger rows(장부 행)와 artifact hashes(산출물 해시)가 갱신된다.

## Non-Terminal Outcomes(비종료 결과)

다음 outcome(결과)은 Stage56(56단계)을 닫지 않는다.

- `exhaustion(소진)`
- `no_dense_engine_found(두꺼운 엔진 없음)`
- `stronger_baseline_candidate_only(강화 기준선 후보 전용)`
- `baseline_candidate_only(기준선 후보 전용)`
- `density_frontier_only(밀도 경계 전용)`
- `quality_frontier_only(품질 경계 전용)`

## Invalid Conditions(무효 조건)

- split boundary(분할 경계)가 불명확하다.
- MT5 report(메타트레이더5 보고서)와 ledger row(장부 행)가 연결되지 않는다.
- Python signal count(파이썬 신호 수)만 있고 MT5 closed trades(닫힌 거래)가 없다.
- Tier A/B routed total(Tier A/B 라우팅 전체)을 synthetic sum(합성 합산)으로 만든다.
