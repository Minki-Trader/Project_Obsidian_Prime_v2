Frontier31 stage-open review(전선31 단계 개방 검토) 요청입니다.

## Current truth(현재 진실)

- Current completed stage(현재 완료 단계): `stage_frontier_30__train_density_preserving_selector_before_loss_veto_or_exit_shape_pivot_onnx_scout`
- Current completed run(현재 완료 실행): `frontier30D_stage_closeout_density_preserving_preselector_v1`
- F30 closeout status(F30 마감 상태): `closed_preserved_clue_negative_memory_density_preselector_scout_only_no_handoff`
- F30 judgment(F30 판정): `preserved_clue_negative_memory(보존 단서+부정 기억)`
- Runtime authority(런타임 권위): not_claimed(주장 없음)
- Operating promotion(운영 승격): not_claimed(주장 없음)
- Goal Achieve(목표 달성): not_claimed(주장 없음)

## Bounded evidence(제한 근거)

F30B train-only density-preserving preselector(학습 전용 밀도 보존 사전 선택기) proxy(프록시)는 F28/F29 reference surface(참조 표면)를 상속 없이 읽었습니다.

- Source/preselected/candidate rows(원천/사전 선택/후보 행): `234` / `160` / `245`
- Density/scout/seed/handoff rows(밀도/탐색/씨앗/인계 행): `188` / `5` / `0` / `0`
- Scout split(탐색 분해): source no-veto branch(원천 무차단 분기) `5`, veto branch(차단 분기) `0`
- Best read-only forward candidate(최상 읽기 전용 전진 후보): `f30b_0214` from `f28b_0079`
- Best validation PF/density/DD(검증 수익 팩터/밀도/손실폭): `1.310` / `5.962/day` / `17.839%`
- Best OOS PF/density/DD(표본외 수익 팩터/밀도/손실폭): `1.151` / `6.687/day` / `13.416%`
- F30C diagnosis(전선30C 진단): near_seed_pf_band(씨앗 근접 PF 구간) `3`, scout_pf_blocked_seed(탐색 PF 부족 씨앗 차단) `5`, valid_train_density_repair_opportunity_rows(유효 학습 밀도 수리 기회 행) `0`
- Runtime probe status(런타임 탐침 상태): `runtime_probe_out_of_scope_by_claim_scout_only_no_handoff`
- ONNX blocker(온엑스 차단 사유): `onnx_branch_unattempted_no_handoff_candidate_after_f30c_repair_decision`

F30D preserved clue(보존 단서): `f30_density_preselector_recovered_five_train_selected_source_scouts_but_no_seed_handoff_reference_only(전선30 밀도 사전 선택기는 학습 선택 원천 탐색 5개를 회복했지만 씨앗/인계가 없어 참조 전용 보존)`

F30D negative memory(부정 기억): `under_f30_locked_density_preselector_veto_branch_scout_zero_and_pf_lift_missing(전선30 잠금 밀도 사전 선택기 아래 차단 분기 탐색은 0개이고 수익 팩터 상승이 부족함)`

## Proposed Frontier31 direction(제안 전선31 방향)

Codex(코덱스)는 F31을 새 hypothesis lifecycle(가설 생명주기)로 열려고 합니다.

- Proposed stage id(제안 단계 ID): `stage_frontier_31__exit_shape_pivot_for_density_preserved_source_scout_pf_lift_onnx_scout`
- Proposed run id(제안 실행 ID): `frontier31A_stage_open_exit_shape_pivot_for_density_preserved_source_scout_pf_lift_hypothesis_design_v1`
- Active changed variable(활성 변경 변수): `train_only_return_space_exit_shape_transform_for_density_preserved_source_scouts`
- Fixed surface(고정 표면): F30B의 5개 source no-veto scout rows(원천 무차단 탐색 행), mask(마스크)와 entry rule(진입 규칙)은 고정
- Data limitation(데이터 한계): current dataset(현재 데이터셋)은 `future_log_return_12`만 있고 intrabar high/low, MFE/MAE(봉내 고가/저가, 최대유리/불리 이동)가 없습니다.

Hypothesis(가설): F30의 5개 density-preserved source scouts(밀도 보존 원천 탐색)는 density(밀도)와 smoothness(매끄러움)는 가까웠지만 PF(수익 팩터)와 DD(손실폭)가 seed/handoff(씨앗/인계)를 막았습니다. F31은 entry mask(진입 마스크)를 고정하고, train-only(학습 전용)으로 고른 return-space exit-shape transform(수익률 공간 청산 형태 변환)을 validation/OOS(검증/표본외)에 read-only(읽기 전용)로 적용해 PF lift(PF 상승)와 DD reduction(DD 감소)이 가능한지 봅니다.

Selection boundary(선택 경계):

- Selection(선택)은 train split(학습 구간) PnL distribution(손익 분포)만 사용합니다.
- Validation/OOS(검증/표본외)는 read-only diagnostics(읽기 전용 진단)만 합니다.
- F30 candidate identity(후보 정체성)는 reference-only(참조 전용)이며 winner/baseline/promotion/runtime authority/live readiness(승자/기준선/승격/런타임 권위/실거래 준비)를 상속하지 않습니다.
- F31B may speak only to scout clue/seed surface/handoff candidate(탐색 단서/씨앗 표면/인계 후보) in return-space proxy boundary(수익률 공간 프록시 경계)입니다.
- MT5/ONNX/WFO(MT5/온엑스/워크포워드 최적화)는 executable exit representation(실행 가능한 청산 표현), handoff candidate rows(인계 후보 행) `> 0`, 그리고 pre-expensive Grok review(비싼 실행 전 그록 검토)가 모두 있을 때만 실행합니다.

Failure/invalid boundary(실패/무효 경계):

- If F31 selects stop/take parameters by validation/OOS metrics(F31이 검증/표본외 수치로 손절/익절 파라미터를 고르면), invalid setup(무효 설정)입니다.
- If F31 claims MT5 executable behavior from return-space clipping alone(F31이 수익률 클리핑만으로 MT5 실행 가능성을 주장하면), invalid setup(무효 설정) 또는 claim overreach(주장 과장)입니다.
- If F31 changes entry masks or re-ranks source scouts by forward metrics(F31이 진입 마스크를 바꾸거나 전진 수치로 원천 탐색을 재순위화하면), invalid setup(무효 설정)입니다.
- If no seed/handoff appears or only unrealistic tight clipping works(씨앗/인계가 없거나 비현실적으로 강한 클리핑만 통하면), close as preserved clue/negative memory(보존 단서/부정 기억) or invalid setup(무효 설정) depending on diagnostics(진단)에 따라 닫습니다.

## Review questions(검토 질문)

Please answer in this exact shape(아래 형식으로 답해주세요):

- verdict: accepted / rejected / needs_local_verification(수용 / 거절 / 로컬 검증 필요)
- novelty_ok: yes/no(예/아니오)
- leakage_risk: low/medium/high(낮음/중간/높음)
- frontier_boundary_ok: yes/no(예/아니오)
- hypothesis_scope_ok: yes/no(예/아니오)
- runtime_claim_boundary_ok: yes/no(예/아니오)
- must_watch: concise bullets(짧은 항목)
- advice_classification: accepted/rejected/needs_local_verification bullets(수용/거절/로컬 검증 필요 항목)

Specific checks(구체 확인):

1. Is it valid to open F31 as a new frontier stage(전선 단계) focused only on exit-shape pivot(청산 형태 전환), after F30 explicitly kept exit-shape as reference fallback only(참조 대체 전용)?
2. Is return-space exit-shape proxy(수익률 공간 청산 형태 프록시) useful enough for exploration if it explicitly does not claim MT5 executability(MT5 실행 가능성)?
3. Is leakage risk(누수 위험) low if exit parameters are selected only from train split(학습 구간) and validation/OOS(검증/표본외) are read-only(읽기 전용)?
4. What must Codex(코덱스) watch before F31B proxy(프록시) and before any expensive MT5/ONNX/WFO(MT5/온엑스/워크포워드 최적화)?
