# Stage269 Input References(269단계 입력 참조)

## Source Inputs(원천 입력)

- Stage268 triage report(268단계 분리 보고): `stages/268_onnx_candidate_campaign__stage267_lineage_triage/03_reviews/stage268_run268A_stage267_profile_lineage_triage_report.md`
- Stage268 triage matrix(268단계 분리 행렬): `stages/268_onnx_candidate_campaign__stage267_lineage_triage/03_reviews/stage268_run268A_stage267_profile_lineage_triage_matrix.csv`
- Stage267 closeout(267단계 종료): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_closeout_onnx_campaign_handoff.md`
- run267ET KPI summary(267ET 핵심 성과 지표 요약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267ET/runtime_gap_aware_tenth_followup_or_prune_mt5_execution/kpi_summary.csv`
- run267ET backtest forensics(267ET 백테스트 포렌식): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267ET/runtime_gap_aware_tenth_followup_or_prune_mt5_execution/backtest_forensics.csv`

## Allowed Starting Clues(허용 시작 단서)

- `s258_stc_aggressive_nonfilter_reentry`: upside clue(상방 단서) only, not candidate(후보 아님).
- `s262_lih_validation_identity_receipt` and `s264_aia_validation_identity_receipt`: identity-collapse clue(정체성 붕괴 단서) only.
- blocked handoff prechecks(차단된 인계 사전검사): runtime handoff gap(런타임 인계 공백) only.

## Forbidden Carryover(금지 계승)

- Stage267(267단계) baseline pool(기준 후보군)을 그대로 selected candidate(선택 후보)로 부르지 않는다.
- Stage267(267단계) alias(별칭)를 candidate package(후보 패키지) 이름으로 고정하지 않는다.
- 2026.04 shared-state pivot(공유 상태 전환) 실패 표면을 같은 방식으로 반복하지 않는다.
