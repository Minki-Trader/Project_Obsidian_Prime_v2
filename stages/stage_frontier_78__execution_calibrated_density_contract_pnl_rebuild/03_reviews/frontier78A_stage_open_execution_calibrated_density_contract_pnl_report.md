# Frontier78A Stage Open Report(F78A 단계 개방 보고서)

Updated(갱신): 2026-06-17T08:29:49Z

- run id(실행 ID): `frontier78A_stage_open_execution_calibrated_density_contract_pnl_v1`
- stage id(단계 ID): `stage_frontier_78__execution_calibrated_density_contract_pnl_rebuild`
- status(상태): `stage_open_execution_calibrated_design_completed_no_authority`
- judgment(판정): `execution_calibrated_density_contract_pnl_stage_open_design_only_no_authority`
- Grok advice(Grok 조언): `accepted_with_conditions(조건부 수용)`
- final Codex direction(최종 Codex 방향): `open_f78_with_conditions_recorded(조건 기록 후 F78 개방)`
- forbidden claim hits(금지 주장 감지): `none(없음)`
- next action(다음 행동): `frontier78B_execution_calibrated_density_contract_pnl_proxy_scout_v1`
- claim boundary(주장 경계): `stage_open_design_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`

## Hypothesis(가설)

Execution-calibrated labels(실행 보정 라벨)이 broker contract P/L(브로커 계약 손익), final-review calendar density(최종 검토 달력 밀도), fill semantics(체결 의미), lifecycle occupancy(생명주기 점유), and risk penalty(위험 벌점)를 proxy stage(프록시 단계)부터 내장하면 F77의 money/density gap(금액/밀도 간극)을 줄일 수 있는지 본다.

## Prior Evidence Boundary(이전 근거 경계)

- F77 closeout(마감): `preserved_clue(보존 단서)`
- F77 status(상태): `closed_preserved_clue_no_authority`
- preserved clue(보존 단서): ['point-unit repair(포인트 단위 수리): TP18/SL12 price units(가격 단위) -> TP1800/SL1200 broker points(브로커 포인트).', 'ONNX/EA signal parity path(ONNX/EA 신호 동등성 경로) with selected-entry veto tape(선택 진입 거부 테이프).', 'runtime bridge mechanics(런타임 연결 메커니즘) can fill after point repair(포인트 수리 후 체결 가능).']
- negative memory(부정 기억): ['F77B meaningful signal(의미 신호) 0, final-like reference(완성 유사 참조) 0.', 'F77F OOS runtime(표본외 런타임) net/PF/DD/tpd(순수익/수익 팩터/손실폭/일 거래 수) 4.48/1.23/1.41/0.1487.', 'proxy money(프록시 금액) was not broker contract calibrated(브로커 계약 보정 안 됨).', 'proxy density denominator(프록시 밀도 분모) used active dates(활성 날짜), not calendar days(달력일).']

## Data Identity(데이터 정체성)

- dataset(데이터셋): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet` sha256 `c30eb033f104f0b1682964b546593e8b18125760c37ce2b945f7ab0f447ae38f`
- rows/columns(행/열): `46650/69`
- split counts(분할 수): `{'train': 29222, 'validation': 9844, 'oos': 7584}`
- raw bars(원천 봉): `data/raw/mt5_bars/m5/US100/bars_us100_m5_mt5api_raw.csv` sha256 `2ab1cb8214182ff9063a64c10ce4ac6a142a8bf660e2476a60842d3452c6d784`
- feature count(피처 수): `58`

## Retrospective Gate(회고 게이트)

- status(상태): `not_due_after_f77_closeout_2_of_5`
- closeouts since last(이전 회고 이후 마감 수): `2`
- effect(효과): five-stage retrospective(5단계 회고)는 not_due(아직 아님)이므로 F78 open(개방)을 막지 않는다.

## Grok Stage-Open Review(Grok 단계 개방 검토)

- packet(묶음): `docs/agent_control/grok_reviews/2026-06-17_f78a_stage_open_execution_calibrated_density_contract_pnl`
- prompt(프롬프트): `docs/agent_control/grok_reviews/2026-06-17_f78a_stage_open_execution_calibrated_density_contract_pnl/prompts/f78a_stage_open_execution_calibrated_density_contract_pnl_prompt.md` sha256 `82044cc800995f1c674688012712c46cde1a2b2efd074854500d938367bd2934`
- output(출력): `docs/agent_control/grok_reviews/2026-06-17_f78a_stage_open_execution_calibrated_density_contract_pnl/clean_output.md` sha256 `c816ffcbd3a6194f1f3b0e60216b91b5ffcd0267cb16c7b9bb7d36d23dd5ac01`
- metadata(메타데이터): `docs/agent_control/grok_reviews/2026-06-17_f78a_stage_open_execution_calibrated_density_contract_pnl/metadata.json` sha256 `156f5dce2e1b7cdd36ae5a8c98d5bb1b2097e6c095ec30da586561d0a0502537`

This report does not create completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
