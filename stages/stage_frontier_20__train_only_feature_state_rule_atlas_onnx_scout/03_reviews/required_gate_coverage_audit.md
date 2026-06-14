# Frontier20B Gate Coverage Audit(전선20B 게이트 커버리지 감사)

Updated(갱신): 2026-06-14T05:50:31Z

- train_only_leakage_guard(학습 전용 누수 방지): condition quantiles, side, and rank(조건 분위수/방향/순위)는 train split(학습 분할)에서만 계산했습니다.
- rule_atlas_lock_gate(규칙 지도 잠금 게이트): existing 58 features, fixed q-grid, max depth 2(기존 58 피처/고정 분위수 격자/최대 깊이 2)를 지켰습니다.
- tier_paired_record_gate(티어 쌍 기록 게이트): Tier A separate(티어 A 분리) 지표를 기록하고, Tier B/Tier A+B(티어 B/합산)는 장부에 missing/out-of-scope 행으로 기록합니다.
- runtime_probe_obligation_gate(런타임 탐침 의무 게이트): handoff candidates(인계 후보) `0`개; status(상태) `out_of_scope_by_claim_proxy_no_mt5(프록시 주장 범위라 MT5 없음)`.
- final_claim_guard(최종 주장 보호): completion/baseline/promotion/runtime/live/Goal(완성/기준선/승격/런타임/실거래/목표) 주장 없음.
