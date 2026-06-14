You are Grok(그록), an external second opinion(외부 2차 의견) for Project Obsidian Prime v2(프로젝트 옵시디언 프라임 v2).

Review size(검토 크기): small(소규모).

Current truth(현재 진실):
- Frontier36(전선36) closed as preserved clue + negative memory(보존 단서 + 부정 기억).
- F36 proxy(프록시): 320 candidates(후보), 73 scout clues(탐색 단서), 3 near-seed(근접 씨앗), 0 seed(씨앗), 0 runtime(런타임). Best validation/OOS PF-DD(검증/표본외 수익 팩터-손실폭): 1.132/9.903 and 1.243/8.218.
- F36 repair(수리): 320 candidates(후보), 132 scout clues(탐색 단서), 1 near-seed(근접 씨앗), 0 seed(씨앗), 0 runtime(런타임). Best validation/OOS PF-DD(검증/표본외 수익 팩터-손실폭): 1.123/9.191 and 1.138/7.706.
- F36 closeout Grok(마감 그록): accepted closeout class and runtime boundary(마감 분류와 런타임 경계 수용).

Codex proposed Frontier37 direction(코덱스 제안 전선37 방향):
- stage_id(단계 ID): stage_frontier_37__short_pf_edge_label_family_pivot_after_source_utility_scout
- hypothesis(가설): F36 found enough short scout surface(숏 탐색 표면), but PF(수익 팩터) stayed too weak. Instead of adding another single-feature filter layer(단일 피처 필터 적층), test a label-family pivot(라벨 계열 전환): train-only payoff-dominance labels(학습 전용 수익 우위 라벨) that score short entries by MFE/MAE separation(최대 유리/불리 이동 분리), stop/take asymmetry(손절/익절 비대칭), ambiguity rate(동시 타격 모호성), and PF/density/DD balance(수익 팩터/거래 빈도/손실폭 균형).
- comparison baseline(비교 기준): F36 best read-only candidate(읽기 전용 후보) and F36 negative memory(부정 기억), not inherited baseline(상속 기준선 아님).
- controls(고정 변수): US100 M5, same frozen train/validation/OOS split(동일 고정 학습/검증/표본외 분할), same feature order hash(동일 피처 순서 해시), same raw open-to-open path replay(동일 원천 시가-시가 경로 재생), validation/OOS read-only(검증/표본외 읽기 전용).
- changed variable(변경 변수): label family and train ranking objective(라벨 계열과 학습 순위 목적함수), not source-filter layering(원천 필터 적층 아님).
- success criteria(성공 기준): produce scout clue(탐색 단서), seed surface(씨앗 표면), or runtime probe candidate(런타임 탐침 후보) by improving forward PF while keeping density near 5-10/day(일 5~10회) and DD under scout caps(탐색 손실폭 상한).
- claim boundary(주장 경계): no completion(완성 없음), no baseline(기준선 없음), no promotion(승격 없음), no runtime authority(런타임 권위 없음), no live readiness(실거래 준비 없음), no Goal Achieve(목표 달성 없음).

Question(질문): Is this a valid next frontier stage(전선 단계) with enough novelty(신규성) and a correct runtime boundary(런타임 경계)?

Please answer exactly(정확히 답하세요):
verdict(판정): accepted(수용) / rejected(거절) / needs_local_verification(로컬 검증 필요)
novelty_ok(신규성 적절): yes/no
main_leakage_or_overfit_risk(주요 누수 또는 과최적화 위험): one sentence(한 문장)
must_not_repeat(반복 금지): one sentence(한 문장)
runtime_claim_boundary_ok(런타임 주장 경계 적절): yes/no
