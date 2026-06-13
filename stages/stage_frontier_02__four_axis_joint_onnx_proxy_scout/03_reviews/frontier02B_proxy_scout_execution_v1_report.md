# frontier02B Proxy Scout Report(전선02B 프록시 탐색 보고)

- run_id(실행 ID): `frontier02B_proxy_scout_execution_v1`
- status(상태): `completed_proxy_scout_no_authority(프록시 탐색 완료, 권위 없음)`
- metric_rows(측정 행): `3726`
- candidate_rows(후보 표면 행): `1242`
- scout_clue_rows(탐색 단서 행): `253`

## Boundary(경계)

이번 실행(run, 실행)은 cheap proxy replay(저비용 프록시 재생)입니다. ONNX model training(온엑스 모델 학습), WFO(워크포워드 최적화), MT5 runtime validation(MT5 런타임 검증), baseline selection(기준선 선택), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 주장하지 않습니다.

## Best Validation Rank(검증 순위 1위)

- candidate_id(후보 ID): `trend_follow_joint__all_cash__both__q70__cd6`
- surface/filter/side(표면/필터/방향): `trend_follow_joint` / `all_cash` / `both`
- validation score(검증 점수): `1.27647`
- validation net/PF/density/DD(검증 순수익/수익 팩터/밀도/손실폭): `0.25549` / `1.26986` / `3.39891` / `6.80087%`
- OOS net/PF/density/DD(표본외 순수익/수익 팩터/밀도/손실폭): `0.12953` / `1.17749` / `4.22901` / `8.9434%`
- joint_pass_count(동시 통과 수): validation(검증) `1`, OOS(표본외) `1`

## Read(판독)

Scout clue(탐색 단서)는 있습니다. 다만 proxy-only(프록시 전용)라서 다음 행동(action, 행동)은 seed surface(씨앗 표면)를 학습 가능한 ONNX-ready surface(온엑스 준비 표면)로 바꾸는 것입니다.

## Artifacts(산출물)

- candidate_surface_metrics: `stages/stage_frontier_02__four_axis_joint_onnx_proxy_scout/02_runs/frontier02B_proxy_scout_execution_v1/candidate_surface_metrics.csv` sha256(해시) `231e74ef172597a4c90b419400f86746286e97e6c77d1acd24f839ba6b7f5433`
- candidate_surface_summary: `stages/stage_frontier_02__four_axis_joint_onnx_proxy_scout/02_runs/frontier02B_proxy_scout_execution_v1/candidate_surface_summary.csv` sha256(해시) `1b4a2b3f74dc8b1aacf15cbbec0541adde3a610222a711c3bd6b0bcfedd8163f`
- top_seed_surfaces: `stages/stage_frontier_02__four_axis_joint_onnx_proxy_scout/02_runs/frontier02B_proxy_scout_execution_v1/top_seed_surfaces.csv` sha256(해시) `b976e425c4d70ee539cd9f83d016f28232878b1a6a70050f2ef31b7f82ebce36`
- input_integrity_audit: `stages/stage_frontier_02__four_axis_joint_onnx_proxy_scout/02_runs/frontier02B_proxy_scout_execution_v1/input_integrity_audit.json` sha256(해시) `c4d96ed1e52f14aae71c1c8a73c310054d9e65fa9c28944e80a332c8a3d309ec`
- score_contract: `stages/stage_frontier_02__four_axis_joint_onnx_proxy_scout/02_runs/frontier02B_proxy_scout_execution_v1/score_contract.json` sha256(해시) `a55884f798688d110a3bda5f79dbdaf995b07380286e4cdf151cb82c7dcaf5a8`

## Gate Boundary(게이트 경계)

- Tier A separate(Tier A 분리): materialized(물질화)
- Tier B separate(Tier B 분리): 이번 proxy run(프록시 실행)에서는 partial-context Tier B artifact(부분 문맥 Tier B 산출물)를 만들지 않았으므로 `missing_required(필수 누락)`입니다.
- Tier A+B combined(Tier A+B 합산): routed Tier B fallback(라우팅 Tier B 대체)을 실행하지 않았으므로 `out_of_scope_by_claim(주장 범위 밖)`입니다.
- Grok pre-expensive review(비싼 검증 전 그록 검토): 이번 cheap proxy replay(저비용 프록시 재생)에는 not required(필요 없음)입니다. WFO/MT5(워크포워드/MT5) 전에는 required(필요)입니다.
