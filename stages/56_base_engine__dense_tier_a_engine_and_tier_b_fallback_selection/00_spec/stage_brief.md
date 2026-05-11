# Stage56 Dense Tier A Engine And Tier B Fallback Selection(56단계 두꺼운 Tier A 엔진과 Tier B 대체 선택)

- stage_id(단계 ID): `56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection`
- idea_id(아이디어 ID): `IDEA-ST56-DENSE-BASE-ENGINE-RESEARCH-BASELINE`
- opening_run_id(개방 실행 ID): `run50A_existing_model_density_audit_v1`
- packet_id(작업 묶음 ID): `stage56_open_dense_base_engine_selection_v1`
- decision_path(결정 경로): `docs/decisions/2026-05-11_stage56_dense_base_engine_open.md`

## Purpose(목적)

Stage56(56단계)의 목적은 수익률만 좋아 보이는 얇은 후보(thin candidate, 얇은 후보)를 더 찾는 것이 아니다.

v2에서 앞으로 계속 키울 수 있는 `research baseline(연구 기준선)` base engine(기본 엔진)을 고른다.

## Core Question(핵심 질문)

Tier A(티어 A) 기본 엔진이 실제 MT5 closed trades(닫힌 거래)를 충분히 만들고, Tier B(티어 B)가 Tier A(티어 A)의 빈 구간에서 의미 있게 보조하는가?

## Lanes(레인)

1. Tier A dense engine lane(Tier A 두꺼운 엔진 레인)
2. Tier B fallback engine lane(Tier B 대체 엔진 레인)
3. A-primary / B-fallback routed integration lane(A 우선 / B 대체 라우팅 통합 레인)

## Guardrails(가드레일)

- permission filter(허용 필터), side filter(방향 필터), cost-aware filter(비용 인식 필터)는 초기 선발전에 붙이지 않는다.
- Python raw signal(파이썬 원천 신호)은 참고 자료이고, 최종 판단은 MT5 closed trades(닫힌 거래) 기준이다.
- Tier B(티어 B)는 add-on entry(추가 진입) 엔진이 아니라 fallback insurance(대체 보험)이다.
- market state(시장 상태)는 처음에는 hard filter(강제 필터)가 아니라 attribution table(귀속 표)로만 쓴다.

## Claim Boundary(주장 경계)

Stage56(56단계)은 `research_baseline_selection_only(연구 기준선 선택 전용)`이다.

live readiness(실거래 준비), runtime authority(런타임 권위), operating promotion(운영 승격), production baseline(운영 기준선), operating reference(운영 참조)는 만들지 않는다.
