Role(역할): external second opinion(외부 2차 의견) for Project Obsidian Prime v2(프로젝트 옵시디언 프라임 v2).

Task(과업): Review proposed Stage Frontier23(전선23 단계) closeout only. Do not create operating promotion(운영 승격), runtime authority(런타임 권위), selected baseline(선택 기준선), live readiness(실거래 준비), or Goal Achieve(목표 달성).

Current truth(현재 진실):
- Stage(단계): stage_frontier_23__payoff_asymmetry_pf_source_onnx_scout.
- Hypothesis(가설): Train-only payoff asymmetry(훈련 전용 보상 비대칭) states might reveal PF source(PF 원천, 수익 팩터 원천) without inheriting F22 shock lifecycle(전선22 충격 생명주기).
- Reference boundary(참조 경계): Stage12~364(12~364단계) and F22(전선22)는 reference only(참조 전용), not inheritance(상속 아님).
- Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 all not_claimed(모두 주장 없음).

F23A stage open(전선23A 단계 개방):
- Prior Grok review(이전 그록 검토): accepted_with_adjustments(조정 수용).
- Accepted locks(수용 잠금): exact train-only payoff asymmetry metrics(정확한 훈련 전용 보상 비대칭 지표), pre-scout sanity gate(사전 탐색 sanity 게이트), novelty guard(신규성 보호), no lifecycle repair until seed(씨앗 전 생명주기 수리 금지), validation/OOS PF >= 1.20 seed rule(검증/표본외 PF 1.20 이상 씨앗 규칙), no ONNX/model training until handoff candidate(인계 후보 전 ONNX/모델 학습 금지).

F23B proxy scout(전선23B 프록시 탐색):
- Dataset(데이터셋): data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet.
- Feature hash(피처 해시): fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2.
- Condition pool rows(조건 풀 행): 640.
- Pre-scout sanity(사전 탐색 sanity): pass true(통과 true), pass rows(통과 행) 78.
- Candidate rows(후보 행): 360.
- Scout clue rows(탐색 단서 행): 23.
- Seed surface rows(씨앗 표면 행): 0.
- Handoff candidate rows(인계 후보 행): 0.
- Best F23B candidate(최상 전선23B 후보): f23b_0333, long(롱), bb_position_20|vortex_indicator.
  - Validation PF/density/DD(검증 수익 팩터/빈도/손실폭): 1.278353 / 7.601093 / 19.109471.
  - OOS PF/density/DD(표본외 수익 팩터/빈도/손실폭): 1.078655 / 8.251908 / 15.439481.
  - scout clue true(탐색 단서 true), seed false(씨앗 false), handoff false(인계 false).

F23C capped repair(전선23C 상한 수리):
- Repair type(수리 유형): entry-known include/veto filters(진입 시점에 알 수 있는 포함/제외 필터) only; no lifecycle repair(생명주기 수리 없음), no ONNX(온엑스 없음), no MT5 runtime probe(MT5 런타임 탐침 없음) because no handoff candidate(인계 후보 없음).
- Source candidates(원천 후보): 16.
- Repair candidates(수리 후보): 240.
- Scout clue rows(탐색 단서 행): 77.
- Seed surface rows(씨앗 표면 행): 0.
- Handoff candidate rows(인계 후보 행): 0.
- Best repair(최상 수리): f23c_0123, from f23b_0333, include close_ema20_ratio.
  - Validation PF/density/DD(검증 수익 팩터/빈도/손실폭): 1.279658 / 7.573770 / 19.109471.
  - OOS PF/density/DD(표본외 수익 팩터/빈도/손실폭): 1.083882 / 8.175573 / 15.316055.
  - scout clue true(탐색 단서 true), seed false(씨앗 false), handoff false(인계 false).
- Near clue 1(근접 단서 1): f23c_0071, include vix_zscore_20.
  - Validation PF/density/DD(검증 수익 팩터/빈도/손실폭): 1.591626 / 3.896175 / 14.495437.
  - OOS PF/density/DD(표본외 수익 팩터/빈도/손실폭): 1.233024 / 4.068702 / 12.369277.
  - Reason not seed(씨앗 아님 이유): density(빈도) below 5/day(일 5회 미만) and DD(손실폭) still above 10%.
- Near clue 2(근접 단서 2): f23c_0233, veto usdx_zscore_20.
  - Validation PF/density/DD(검증 수익 팩터/빈도/손실폭): 1.327421 / 7.087432 / 29.550275.
  - OOS PF/density/DD(표본외 수익 팩터/빈도/손실폭): 1.273170 / 6.862595 / 12.376196.
  - Reason not seed(씨앗 아님 이유): validation DD(검증 손실폭) is too high.

Proposed Codex closeout(코덱스 제안 마감):
- Close type(마감 유형): preserved clue + negative memory(보존 단서 + 부정 기억).
- Preserved clue(보존 단서): payoff asymmetry sanity gate and entry-known filters can expose PF-positive pockets(PF 양수 구간), including low-density stronger PF rows and density-aligned weak PF rows; useful as reference only(참조 전용) for next frontier(다음 전선).
- Negative memory(부정 기억): payoff asymmetry plus capped entry filters did not jointly satisfy PF/density/DD seed or handoff(수익 팩터/빈도/손실폭 씨앗 또는 인계 동시 충족 실패).
- Runtime probe status(런타임 탐침 상태): runtime_probe_ineligible_no_handoff_candidate_after_f23_capped_repair(전선23 상한 수리 뒤 인계 후보가 없어 런타임 탐침 부적격).
- ONNX status(온엑스 상태): onnx_branch_unattempted_no_handoff_candidate_after_f23_capped_repair(전선23 상한 수리 뒤 인계 후보가 없어 ONNX 분기 미개시).
- Next proposed run(다음 제안 실행): frontier24A_stage_open_density_bridge_payoff_pockets_hypothesis_design_v1, focused on density bridge(빈도 연결) for PF-positive payoff pockets(PF 양수 보상 구간) while preserving DD guard(손실폭 보호).

Review questions(검토 질문):
1. Is the proposed closeout judgment(마감 판정) too strong, too weak, or correctly bounded?
2. Should any clue(단서) or negative memory(부정 기억) be reworded before local closeout(로컬 마감)?
3. Is the runtime probe ineligible(런타임 탐침 부적격) boundary valid given zero handoff candidates(인계 후보 0)?
4. Should the next frontier(다음 전선) focus on density bridge(빈도 연결), DD normalization(손실폭 정규화), or something else based only on this bounded evidence(제한 근거)?

Return(반환): accepted(수용), rejected(거절), or needs_local_verification(로컬 검증 필요), with concise critique(간결한 비판).
