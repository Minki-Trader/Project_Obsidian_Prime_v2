# Stage267 Run267CR Shared Weakness Breakout Follow-up Materialization(267단계 267CR 공유 약점 돌파 후속 물질화)

## Summary(요약)

Run267CR(267CR 실행)은 run267CQ(267CQ 실행)의 follow-up/prune design(후속/가지치기 설계)을 MT5(MetaTrader 5, 메타트레이더5) 실행 대기 입력으로 바꿨다.

Effect(효과): variants(변형) `7`개, attempts(시도) `14`개, held queue(보류 대기열) `2`개, control pressure receipts(대조 압박 영수증) `2`개, guardrail receipts(가드레일 영수증) `2`개를 만들었다.

## Why It Still Takes Time(왜 아직 오래 걸리는가)

Baseline candidate(기준 후보)는 운영 기준선이 아니라 R&D racing research candidate(연구개발 경주용 연구 후보)다. 그래서 숫자 1등을 바로 고르지 않고, weak slice(약한 구간), balance/equity curve(잔액/평가금 곡선), trade quality(거래 품질), similar replacement(유사 대체), feature ablation(피처 제거), Adapter handoff(어댑터 인계)를 같이 본다.

Effect(효과): 좋아 보이는 후보를 성급히 ONNX(오닉스) 후보로 올리지 않고, “어디서 깨지는지”를 먼저 드러낸다.

## Materialized Work(물질화한 작업)

- `run267cr_q01_pool_monday_state_phase_replacement`: five candidates(후보 5개)를 state phase replacement(상태 국면 대체) feature(피처)로 물질화했다.
- `run267cr_q03_aih_aggressive_shock_supply_expansion`: `s264_aih`를 aggressive supply expansion(공격형 공급 확장) 변형으로 물질화했다.
- `run267cr_q04_stc_redzone_stress_blast`: `s258_stc`를 one-shot red-zone stress(단발 고위험 압박) 변형으로 물질화했다.
- `run267cr_q02_lc_aia_anchor_cross_period_pressure`: adjacent-period feature frames(인접 기간 피처 프레임)가 필요해 보류했다.
- `run267cr_q05_lih_validation_guardrail_trace`: `s262_lih`는 q01 안에서 validation-heavy guardrail(검증 중심 가드레일)로 연결했다.
- `run267cr_q06_buy_side_similar_replacement_probe`: q03에 일부 흡수하고 standalone probe(독립 탐침)는 보류했다.

## Boundary(경계)

- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Next Action(다음 행동)

`run267CS_execute_shared_weakness_breakout_followup_mt5_batch`
