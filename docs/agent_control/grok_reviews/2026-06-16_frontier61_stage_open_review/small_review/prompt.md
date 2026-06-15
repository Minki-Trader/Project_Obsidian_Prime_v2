# Frontier61 Stage Open Review(전선61 단계 개방 검토)

Current truth(현재 진실):
- Current closed stage(현재 닫힌 단계): `stage_frontier_60__long_axis_friction_escape_or_negative_memory`.
- F60 judgment(전선60 판정): `negative_memory_long_axis_friction_escape_failed_pf`.
- F60 MT5 runtime probe(MT5 런타임 탐침): validation_is PF=0.41, DD=14.89%, trades=661, density/day=3.61; OOS PF=0.51, DD=8.48%, trades=494, density/day=3.77.
- Prior memory(이전 기억): F53-F58 short-axis(숏 축) PF sources did not transfer to MT5; F59-F60 long-axis(롱 축) repair also failed PF.
- Runtime probe backfill(런타임 탐침 소급): F01-F60 has `still_missing=0`; no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) claimed.

Proposed new stage(제안 새 단계):
- Stage id(단계 ID): `stage_frontier_61__non_long_axis_pf_source_after_friction_memory`.
- Run id(실행 ID): `frontier61A_stage_open_non_long_axis_pf_source_after_friction_memory_v1`.
- Work family(작업군): `runtime_backtest`.
- Primary skill(주 스킬): `obsidian-runtime-parity`.

Hypothesis(가설):
- Instead of repairing short-only(숏 전용) or long-only(롱 전용) direction scores, train a 3-class side-allocation model(3분류 방향 배분 모델) that predicts short/flat/long(숏/무거래/롱) from the same US100 M5 feature contract(피처 계약).
- The label(라벨) compares executable long and short path outcomes under the same ATR SL/TP/max-hold envelope(ATR 손절/익절/최대보유 봉투), then chooses the better side only if it beats flat and has enough margin(마진).

Novelty delta(신규성 차이):
- F53-F58: mostly short source(숏 원천) repair.
- F59-F60: long source/admission cadence(롱 원천/진입 리듬) repair.
- F61: side allocation(방향 배분) is the model target itself; no inherited winner/baseline/promotion/runtime authority(승자/기준선/승격/런타임 권위 상속 없음).

Bounded execution plan(제한 실행 계획):
- Create one broad but capped proxy grid(넓지만 상한 있는 프록시 격자): a small set of margin/threshold combinations, then freeze one runtime probe candidate(런타임 탐침 후보 1개).
- Run mandatory MT5 runtime probe(MT5 런타임 탐침 필수 실행) for validation_is and OOS.
- Record proxy-runtime gap(프록시-런타임 차이), Tier A rows(티어 A 행), Tier B/combined status(티어 B/합산 상태), artifact hashes(산출물 해시), and closeout judgment(마감 판정).

Do-not-repeat(반복 금지):
- Do not extend F61 into many tiny side-threshold repairs.
- Do not treat proxy PF(프록시 PF) as runtime authority(런타임 권위).
- Do not inherit F59/F60 as baseline(기준선) or promotion(승격).

Claim boundary(주장 경계):
- During work: scout clue(탐색 단서), seed surface(씨앗 표면), runtime probe observation(런타임 탐침 관찰), or completion candidate(완성 후보) only.
- Forbidden now(현재 금지): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성).

Question(질문):
Is this F61 opening direction accepted/rejected/needs_local_verification(수용/거절/로컬 검증 필요) for an exploration-only runtime probe stage? Answer only from this snapshot(스냅샷) and list concrete risks or required local checks before implementation.
