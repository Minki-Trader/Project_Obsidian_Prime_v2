﻿# Decision: Stage 337IB Runtime Probe Package

- date: `2026-06-01`
- run_id: `run337IB_materialize_proxy_positive_offensive_pivot_runtime_probe_package_without_db_v1`
- decision: `stage337IB_open_run337IC_execute_proxy_positive_offensive_pivot_mt5_runtime_probe`
- judgment: `runtime_probe_package_ready_for_mt5_attempt_proxy_diff_required_no_selection`
- next_run_id: `run337IC_execute_proxy_positive_offensive_pivot_mt5_runtime_probe_without_db_v1`

## Reason

IA review(검토)는 proxy-positive(프록시 양수) ONNX candidates(ONNX 후보)를 확인했고, proxy expected value(프록시 예상값)는 MT5 runtime probe(MT5 런타임 탐침)와 비교해야 한다.

## Effect

IB package(패키지)는 feature matrix(피처 행렬), ONNX handoff(ONNX 인계), expected tape(예상 테이프), tester set/ini(테스터 설정)를 고정해 IC 실행 시도를 가능하게 한다.

## Boundary

`research_development_runtime_probe_package_only_no_mt5_execution_in_IB_no_candidate_selection_no_forward_no_runtime_authority_no_operating_or_goal_claim`
