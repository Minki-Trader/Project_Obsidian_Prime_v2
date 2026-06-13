You are Grok(Grok, 그록), external second opinion(외부 2차 의견) only. Review this bounded Project Obsidian Prime v2 Frontier07 stage closeout(전선07 단계 마감) proposal.

Current truth(현재 진실):
- Stage(단계): `stage_frontier_07__adverse_excursion_risk_shaped_labeling` adverse excursion risk-shaped labeling(불리한 이동 위험 형성 라벨링).
- Frontier07A(전선07A) opened after Grok review(그록 검토 후 개방). No completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) claimed.
- Frontier07B(전선07B) built 4 label families x 3 variants(라벨군 4개 x 변형 3개), fixed feature_set_v2(고정 피처 세트 v2), same small ONNX-exportable model family(같은 작은 온엑스 내보내기 가능 모델군), argmax-only(최대확률 전용). Result(결과): strict scout clue rows(엄격 탐색 단서 행) 0, preserved clue rows(보존 단서 행) 21. Best(최상위): validation PF/density/DD(검증 수익 팩터/밀도/손실폭) 1.06855 / 3.10929/day / 53.129%, OOS PF/density/DD(표본밖 수익 팩터/밀도/손실폭) 1.70687 / 1.36641/day / 13.0888%, ONNX parity(온엑스 동등성) true.
- Frontier07C(전선07C) ran capped repair(상한 있는 수리): top 4 preserved variants(보존 변형 상위 4개) x 4 class-prior directional weights(방향 클래스 사전분포 가중치). Result(결과): strict scout clue rows(엄격 탐색 단서 행) 0, preserved clue rows(보존 단서 행) 16. Best repair(최상위 수리): validation PF/density/DD(검증 수익 팩터/밀도/손실폭) 1.03874 / 5.71038/day / 58.8505%, OOS PF/density/DD(표본밖 수익 팩터/밀도/손실폭) 1.17777 / 4.12214/day / 13.1215%, ONNX parity(온엑스 동등성) true.

Codex proposed closeout(코덱스 제안 마감):
- Close Frontier07(전선07) as preserved_clue_with_negative_memory_no_authority(보존 단서 + 부정 기억, 권위 없음).
- Preserved clue(보존 단서): adverse-excursion risk labels can materially reduce OOS DD(표본밖 손실폭) and improve OOS PF(표본밖 수익 팩터), especially time-to-adverse penalty(불리 이동까지 시간 벌점) and side-asymmetric caps(방향 비대칭 상한).
- Negative memory(부정 기억): the clue did not satisfy simultaneous four axes(네 축 동시 충족). Validation DD(검증 손실폭) stayed very high, PF(수익 팩터) stayed below scout floor(탐색 하한), and density(밀도) either undershot or overshot. The capped class-prior repair(상한 클래스 사전분포 수리) improved density but still did not create strict clue(엄격 단서).
- No WFO/MT5(워크포워드/메타트레이더5 없음), because strict scout clue rows(엄격 탐색 단서 행) are 0.
- Next frontier(다음 전선)는 new hypothesis(새 가설)로 open(개방)해야 하며, not inherit winner/baseline/promotion/runtime authority/live readiness(승자/기준선/승격/런타임 권위/실거래 준비 상속 없음).

Bounded evidence(제한 근거):
- F07A report(전선07A 보고서): `stages/stage_frontier_07__adverse_excursion_risk_shaped_labeling/03_reviews/frontier07A_stage_open_adverse_excursion_risk_shaped_labeling_v1_report.md` sha256 `9defbf54947c0c83685767a03693eb9c72cf8cf068a409c5148bf3c9e1882a0d`
- F07B report(전선07B 보고서): `stages/stage_frontier_07__adverse_excursion_risk_shaped_labeling/03_reviews/frontier07B_adverse_excursion_risk_label_proxy_scout_v1_report.md` sha256 `6010f1f8262310d169bf69bf81b6dc75c8396788f89f91c698dff09a005736ad`
- F07B candidate summary(전선07B 후보 요약): `stages/stage_frontier_07__adverse_excursion_risk_shaped_labeling/02_runs/frontier07B_adverse_excursion_risk_label_proxy_scout_v1/candidate_summary.csv` sha256 `2f89725f4d3da035a8735ec830d3c47b2a29b17985f82801bb9eff1f49f071ac`
- F07B ONNX parity(전선07B 온엑스 동등성): `stages/stage_frontier_07__adverse_excursion_risk_shaped_labeling/02_runs/frontier07B_adverse_excursion_risk_label_proxy_scout_v1/onnx_parity.csv` sha256 `cc979fac34d7031dfa829d1e8c71bf224cb74254cfabddbb7daea89ab03704d6`
- F07C report(전선07C 보고서): `stages/stage_frontier_07__adverse_excursion_risk_shaped_labeling/03_reviews/frontier07C_class_prior_density_bridge_repair_v1_report.md` sha256 `f79659aa22eb0402d05ec57db07e9c54f38172491eb97f1b310a7b79a57cbf58`
- F07C repair summary(전선07C 수리 요약): `stages/stage_frontier_07__adverse_excursion_risk_shaped_labeling/02_runs/frontier07C_class_prior_density_bridge_repair_v1/repair_candidate_summary.csv` sha256 `96b9213fe170b8460203c2fcd4d60e9199b2842869ab650ab02197c66cd9efb1`
- F07C ONNX parity(전선07C 온엑스 동등성): `stages/stage_frontier_07__adverse_excursion_risk_shaped_labeling/02_runs/frontier07C_class_prior_density_bridge_repair_v1/onnx_parity.csv` sha256 `0984aeba6825ed2e40a0e2b27a35bde73d68f768a3371c9c921fb081d0e9c553`

Focused question(집중 질문):
Should Codex(Codex, 코덱스) close Frontier07(전선07) as preserved_clue_with_negative_memory_no_authority(보존 단서 + 부정 기억, 권위 없음), run another repair(추가 수리), or mark invalid/blocked(무효/차단)?

Please answer in this structure:
1. Recommendation(권고): close_preserved_clue_negative_memory(보존 단서+부정 기억 마감) / repair_once_more(한 번 더 수리) / invalid_or_blocked(무효 또는 차단)
2. Reasoning(근거)
3. Required closeout wording(필수 마감 표현)
4. Do-not-claim boundary(주장 금지 경계)
