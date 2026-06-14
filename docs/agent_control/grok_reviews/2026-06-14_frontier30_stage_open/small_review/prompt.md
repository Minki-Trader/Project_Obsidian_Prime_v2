Frontier30 stage-open review(전선30 단계 개방 검토) 요청입니다.

## Current truth(현재 진실)

- Current stage(현재 단계): `stage_frontier_29__train_only_loss_concentration_veto_for_pf_dd_balance_onnx_scout`
- Current run(현재 실행): `frontier29D_stage_closeout_loss_concentration_veto_v1`
- F29 closeout status(F29 마감 상태): `closed_preserved_clue_negative_memory_loss_concentration_veto_scout_zero_no_handoff`
- F29 judgment(F29 판정): `preserved_clue_negative_memory(보존 단서+부정 기억)`
- Runtime authority(런타임 권위): not_claimed(주장 없음)
- Operating promotion(운영 승격): not_claimed(주장 없음)
- Goal Achieve(목표 달성): not_claimed(주장 없음)

## Bounded evidence(제한 근거)

F29B train-only loss concentration veto(학습 전용 손실 집중 차단) proxy(프록시)는 F28 reference union surface(F28 참조 합집합 표면) `234`개에 veto(차단)를 적용했습니다.

- Screened/selected rows(선별/선택 행): `36108` / `1438`
- Density/scout/seed/handoff rows(밀도/탐색/씨앗/인계 행): `287` / `0` / `0` / `0`
- Best read-only forward candidate(최상 읽기 전용 전진 후보): `f29b_0274` from `f28b_0197`
- Best validation PF/density/DD(최상 검증 수익 팩터/밀도/손실폭): `1.073` / `4.781/day` / `11.821%`
- Best OOS PF/density/DD(최상 표본외 수익 팩터/밀도/손실폭): `1.207` / `5.084/day` / `12.748%`

F29C repair audit(수리 감사)는 다음처럼 닫혔습니다.

- selected_veto_rows(선택 차단 행): `1438`
- density_bridge_rows(밀도 충족 행): `287`
- density_dual_positive_rows(밀도+양수 행): `14`
- near_scout_rows(탐색 근접 행): `9`
- pf_ready_density_rows(PF 준비+밀도 행): `0`
- dd_ready_pf_blocked_rows(DD 준비+PF 차단 행): `7`
- would_require_posthoc_contract_edit_rows(사후 계약 변경 필요 행): `11`
- valid_train_loss_repair_opportunity_rows(유효 학습 손실 수리 기회 행): `0`

F29D closeout(마감)은 다음을 보존했습니다.

- Preserved clue(보존 단서): `f29_loss_concentration_veto_created_density_bridge_and_dual_positive_fragments_but_no_scout_rows_reference_only(전선29 손실 집중 차단은 밀도 충족과 양수 조각을 만들었지만 탐색 행은 0개라 참조 전용 보존)`
- Negative memory(부정 기억): `under_f29_locked_train_loss_veto_contract_scout_seed_and_handoff_remained_zero(전선29 잠금 학습 손실 차단 계약 아래 탐색/씨앗/인계가 모두 0개로 남음)`
- Runtime probe blocker(런타임 탐침 차단 사유): `runtime_probe_ineligible_no_handoff_candidate_after_f29c_repair_decision`
- ONNX blocker(온엑스 차단 사유): `onnx_branch_unattempted_no_handoff_candidate_after_f29c_repair_decision`
- Next clue(다음 단서): `train_density_preserving_selector_before_loss_veto_or_exit_shape_pivot_reference_only(손실 차단 전 학습 밀도 보존 선택기 또는 청산 형태 전환을 참조 전용 다음 단서로 보존)`

## Proposed Frontier30 direction(제안 전선30 방향)

Codex(코덱스)는 F30을 새 hypothesis lifecycle(가설 생명주기)로 열려고 합니다.

- Proposed stage id(제안 단계 ID): `stage_frontier_30__train_density_preserving_selector_before_loss_veto_or_exit_shape_pivot_onnx_scout`
- Proposed run id(제안 실행 ID): `frontier30A_stage_open_train_density_preserving_selector_or_exit_shape_pivot_hypothesis_design_v1`
- Active changed variable(활성 변경 변수): `train_density_preserving_preselector_before_loss_veto`
- Deferred fallback clue(지연 대체 단서): `exit_shape_pivot_reference_only_not_active_changed_variable(청산 형태 전환은 참조 전용이며 활성 변경 변수가 아님)`

Hypothesis(가설): F29의 loss veto(손실 차단)는 forward density(전진 밀도)를 너무 얇게 만들었습니다. F30은 loss veto(손실 차단)를 적용하기 전에 train-only density-preserving preselector(학습 전용 밀도 보존 사전 선택기)로 source union(원천 합집합)을 거르거나 점수화하면, validation/OOS(검증/표본외)에서는 읽기 전용으로 5~10/day 밀도를 유지하면서 PF/DD(수익 팩터/손실폭) 균형이 좋아질 수 있는지 봅니다.

Selection boundary(선택 경계):

- Selection(선택)은 train split(학습 구간)만 사용합니다.
- Validation/OOS(검증/표본외)는 read-only diagnostics(읽기 전용 진단)만 합니다.
- F28/F29 rows(행)는 reference-only(참조 전용)이며 winner/baseline/promotion/runtime authority/live readiness(승자/기준선/승격/런타임 권위/실거래 준비)를 상속하지 않습니다.
- F30B는 scout clue/seed surface/handoff candidate(탐색 단서/씨앗 표면/인계 후보)까지만 말할 수 있습니다.
- MT5/ONNX/WFO(MT5/온엑스/워크포워드 최적화)는 handoff candidate rows(인계 후보 행) `> 0`이고 pre-expensive Grok review(비싼 실행 전 그록 검토)가 통과할 때만 실행합니다.

Failure/invalid boundary(실패/무효 경계):

- If F30 re-ranks by validation/OOS PF, DD, or density(F30이 검증/표본외 수익 팩터, 손실폭, 밀도로 재순위화하면), invalid setup(무효 설정)입니다.
- If F30 merely relaxes F29 thresholds(F30이 F29 임계값만 완화하면), negative memory(부정 기억) 또는 invalid setup(무효 설정)입니다.
- If F30 mixes exit-shape pivot(청산 형태 전환) into the same active proxy(활성 프록시), scope failure(범위 실패)로 봅니다.
- If no scout/seed/handoff(탐색/씨앗/인계)가 appears(나오지 않으면), close as preserved clue/negative memory(보존 단서/부정 기억) or blocked(차단) depending on diagnostics(진단)에 따라 닫습니다.

## Review questions(검토 질문)

Please answer in this exact shape(아래 형식으로 답해주세요):

- verdict: accepted / rejected / needs_local_verification(수용 / 거절 / 로컬 검증 필요)
- novelty_ok: yes/no(예/아니오)
- leakage_risk: low/medium/high(낮음/중간/높음)
- frontier_boundary_ok: yes/no(예/아니오)
- hypothesis_scope_ok: yes/no(예/아니오)
- must_watch: concise bullets(짧은 항목)
- advice_classification: accepted/rejected/needs_local_verification bullets(수용/거절/로컬 검증 필요 항목)

Specific checks(구체 확인):

1. Is it valid to narrow the stage id(단계 ID)의 `or_exit_shape_pivot` clue(단서)를 active F30 hypothesis(활성 F30 가설)에서는 density-preserving preselector(밀도 보존 사전 선택기)로 잠그고, exit-shape pivot(청산 형태 전환)은 reference fallback only(참조 대체 전용)로 두는가?
2. Is the novelty(신규성) sufficient relative to F29 loss veto(손실 차단), or is this just F29 repair(수리)?
3. Is leakage risk(누수 위험) low if all selection(선택) stays train-only(학습 전용) and validation/OOS(검증/표본외) stays read-only(읽기 전용)?
4. What must Codex(코덱스) watch before opening F30B proxy(프록시)?
