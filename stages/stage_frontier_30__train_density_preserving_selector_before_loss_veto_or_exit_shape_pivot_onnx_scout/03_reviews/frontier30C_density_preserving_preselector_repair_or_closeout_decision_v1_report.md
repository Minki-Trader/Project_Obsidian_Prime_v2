# Frontier30C Repair Or Closeout Decision Report(전선30C 수리 또는 마감 결정 보고서)

Updated(갱신): 2026-06-14T12:21:24Z

Status(상태): `density_preserving_preselector_repair_rejected_scout_only_no_seed_no_handoff_no_authority`

Judgment(판정): `repair_rejected_frozen_contract_no_valid_train_only_pf_lift_opportunity`

Action(행동): F30B density-preserving preselector(전선30B 밀도 보존 사전 선택기) 결과를 repair audit(수리 감사)로 분해했습니다.

Effect(효과): scout clue(탐색 단서)는 `5`개였지만 모두 source no-veto branch(원천 무차단 분기)에 있고, seed/handoff(씨앗/인계)는 `0/0`개라서 F30 잠금 안의 수리는 거절했습니다.

Diagnosis(진단):

- candidate_rows(후보 행): `245`
- density_bridge_rows(밀도 충족 행): `188`
- dual_positive_rows(양수 행): `114`
- scout_clue_rows(탐색 단서 행): `5`
- seed_surface_rows(씨앗 표면 행): `0`
- handoff_candidate_rows(인계 후보 행): `0`
- near_seed_pf_band_rows(씨앗 근접 PF 구간 행): `3`
- scout_pf_blocked_seed_rows(탐색 중 PF 부족 씨앗 차단 행): `5`
- source_branch_scout_only_rows(원천 분기 전용 탐색 행): `5`
- veto_branch_scout_rows(차단 분기 탐색 행): `0`
- valid_train_density_repair_opportunity_rows(유효 학습 밀도 수리 기회 행): `0`

Preserved clue(보존 단서): `f30_density_preselector_recovered_five_train_selected_source_scouts_but_no_seed_handoff_reference_only(전선30 밀도 사전 선택기는 학습 선택 원천 탐색 5개를 회복했지만 씨앗/인계가 없어 참조 전용 보존)`

Negative memory(부정 기억): `under_f30_locked_density_preselector_veto_branch_scout_zero_and_pf_lift_missing(전선30 잠금 밀도 사전 선택기 아래 차단 분기 탐색은 0개이고 수익 팩터 상승이 부족함)`

Runtime probe status(런타임 탐침 상태): `runtime_probe_out_of_scope_by_claim_scout_only_no_handoff`

ONNX status(ONNX 상태): `onnx_branch_unattempted_no_handoff_candidate_after_f30c_repair_decision`

Next action(다음 행동): `frontier30D_stage_closeout_density_preserving_preselector_v1`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 not_claimed(주장 없음)입니다.
