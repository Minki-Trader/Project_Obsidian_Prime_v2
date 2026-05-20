# Stage267 Run267B Input Readiness Report(267단계 267B 입력 준비 보고)

- run(실행): `run267B_stage267_extended_period_ablation_probe_v1`
- status(상태): `input_manifest_materialized_no_execution_yet`
- judgment(판정): `not_yet_evaluated`
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`

## What Changed(바뀐 것)

Action(행동): run267B(267B 실행)의 manifest(목록), candidate source feature manifest(후보 원천 피처 목록), extended period plan(확장 기간 계획), feature ablation map(피처 제거 지도), similar replacement map(유사 대체 지도), equity report manifest(평가금 보고서 목록), prior research utilization audit(이전 연구 활용 감사)을 만들었다.

Effect(효과): 다음 실행은 후보를 바로 고르지 않고, 다섯 후보를 같은 조건에서 더 넓게 깨뜨려 보는 방향으로 시작할 수 있다.

## Important Findings(중요 확인)

- 후보별 validation/OOS(검증/표본외) feature CSV(피처 CSV)는 모두 존재한다.
- 각 후보 feature CSV(피처 CSV)는 4 columns(4개 열)이다: time(시간), Stage56 context signal(56단계 문맥 신호), source feature rank bucket(원천 피처 순위 구간), candidate source gate(후보 원천 게이트).
- 따라서 현재 후보 파일만으로는 사용자가 요구한 full feature/category ablation(전체 피처/범주 제거)을 충분히 할 수 없다.
- Full ablation/replacement(전체 제거/대체)는 원래 58-feature contract(58개 피처 계약)에서 재물질화(rematerialization, 재물질화)가 필요하다.
- 2024년 구간은 training-era historical stress(학습 기간 과거 압박)다. OOS(out-of-sample, 표본외)라고 부르면 안 된다.
- MT5 report image(MT5 보고서 이미지)는 존재한다. Windows(윈도우) 로컬 접근은 일부 경로가 길어서 long-path prefix(긴 경로 접두사)가 필요할 수 있다.

## Files(파일)

- `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267B/run_manifest.json`
- `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267B/source_feature_manifest.csv`
- `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267B/extended_period_probe_plan.csv`
- `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267B/feature_ablation_map.csv`
- `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267B/similar_feature_replacement_map.csv`
- `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267B/equity_report_manifest.csv`
- `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_prior_research_utilization_audit.md`

## Next Execution(다음 실행)

Next action(다음 행동): run267B(267B 실행)를 실제 실행 단계로 넘길 때는 먼저 2024 historical stress(2024 과거 압박) 물질화, full feature/category ablation(전체 피처/범주 제거), similar replacement(유사 대체), equity full/zoom visual grading(평가금 전체/확대 시각 판정)을 같은 후보군에 적용한다.

Effect(효과): 특정 월, 특정 feature(피처), 특정 threshold(임계값), 특정 graph section(그래프 구간)에만 맞춘 미세 수리 루프를 피한다.
