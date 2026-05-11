# Stage56 Dense Base Engine Open Decision(56단계 두꺼운 기본 엔진 개방 결정)

- decision_id(결정 ID): `2026-05-11_stage56_dense_base_engine_open`
- stage_id(단계 ID): `56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection`
- opening_run_id(개방 실행 ID): `run50A_existing_model_density_audit_v1`
- branch(브랜치): `codex/stage56-dense-base-engine-selection`
- source_inputs(원천 입력): Stage56 design summaries(Stage56 설계 요약), Stage55 reviewed runtime probe(55단계 검토된 런타임 탐침) evidence(근거)

## Decision(결정)

Stage56(56단계)을 `research baseline(연구 기준선)` 선택 단계로 연다.

핵심 질문(core question, 핵심 질문)은 다음이다.

`Tier A(티어 A) 기본 엔진이 실제 MT5 closed trades(닫힌 거래)를 충분히 만들고, Tier B(티어 B)가 빈 구간에서 의미 있게 보조하는가?`

## Claim Boundary(주장 경계)

허용되는 주장(allowed claims, 허용 주장):

- `dense_engine_candidate(두꺼운 엔진 후보)`
- `selected_research_baseline(선택 연구 기준선)`
- `selected_shadow_candidate(선택 그림자 후보)`
- `tier_b_fallback_usefulness(Tier B 대체 유용성)`
- `no_dense_engine_found(두꺼운 엔진 없음)`

금지되는 주장(forbidden claims, 금지 주장):

- `live_readiness(실거래 준비)`
- `runtime_authority(런타임 권위)`
- `operating_promotion(운영 승격)`
- `production_baseline(운영 기준선)`
- `operating_reference(운영 참조)`

`baseline(기준선)`이라는 말을 쓰면 반드시 `research baseline(연구 기준선)`으로 제한한다.

## Effect(효과)

Stage52~55(52~55단계)의 filter/adapter(필터/어댑터) 후보를 바로 운영 후보로 올리지 않고, 먼저 LogReg(로지스틱 회귀), QDA(이차 판별 분석), CatBoost(캣부스트) 같은 base engine(기본 엔진)의 실제 거래 밀도(trade density, 거래 밀도)를 다시 본다.
