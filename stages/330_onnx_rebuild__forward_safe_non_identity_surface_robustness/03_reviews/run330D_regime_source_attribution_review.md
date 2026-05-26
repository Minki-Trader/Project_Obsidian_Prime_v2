# Run330D Regime Source Attribution Review(330D 국면 원천 귀속 검토)

- run_id(실행 ID): `run330D_regime_attribution_v1`
- parent_run_id(부모 실행 ID): `run330C_forward_mt5_or_score_curve_review_v1`
- status(상태): `completed_regime_source_attribution_no_forward_decision`
- judgment(판정): `regime_source_attribution_completed_research_only_runtime_gap_remains`
- decision(결정): `stage330D_regime_source_pressure_runtime_probe_or_block_next`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- claim_boundary(주장 경계): `research_development_only_regime_source_attribution_no_forward_threshold_tuning_no_candidate_selection_no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve`

## Source View Read(원천 보기 판독)

| artifact(산출물) | judgment(판정) | raw net(원본 순손익) | cost +1 survives(비용 +1 생존) | worst curve(최악 곡선) | gap(간극) |
|---|---|---:|---|---:|---|
| c56_bal | multi_regime_fragility_review_required | 166.685 | True | -32.8 | raw_session_gap_within_review_band |
| c56_plain | multi_regime_fragility_review_required | 208.66 | True | -25.5 | raw_session_gap_within_review_band |
| m48_bal | raw_forward_density_pressure_blocks_forward_pass | 103.82 | False | -73.4 | raw_session_gap_high_pressure |
| m48_plain | raw_forward_density_pressure_blocks_forward_pass | 123.41 | False | -51.775 | raw_session_gap_high_pressure |
| u42_bal | raw_forward_density_pressure_blocks_forward_pass | 93.24 | False | -90.5 | raw_session_gap_high_pressure |
| u42_plain | raw_forward_density_pressure_blocks_forward_pass | 125.275 | False | -71.325 | raw_session_gap_high_pressure |

## Worst Regime Pockets(최악 국면 포켓)

| artifact(산출물) | view(보기) | axis(축) | bucket(구간) | worst net(최악 순손익) | judgment(판정) |
|---|---|---|---|---:|---|
| c56_bal | old_session_parity | rate | us10yr_low | -123.3 | loss_pocket_and_one_bucket_concentration |
| u42_bal | old_session_parity | direction | sell | -77.76 | loss_pocket_and_one_bucket_concentration |
| m48_bal | raw_forward | usd | neutral_usd | -74.16 | loss_pocket_and_one_bucket_concentration |
| u42_bal | raw_forward | direction | short | -72.97 | loss_pocket_and_one_bucket_concentration |
| u42_plain | raw_forward | direction | short | -68.1 | loss_pocket_and_one_bucket_concentration |
| u42_bal | old_session_parity | adx | adx_20_25 | -65.38 | loss_pocket_and_one_bucket_concentration |
| c56_bal | old_session_parity | direction | sell | -63.97 | loss_pocket_and_one_bucket_concentration |
| u42_bal | old_session_parity | volatility | vol_low | -58.73 | loss_pocket_and_one_bucket_concentration |
| m48_bal | raw_forward | month | 2026-04 | -56.86 | loss_pocket_and_one_bucket_concentration |
| u42_bal | old_session_parity | hour | 16 | -54.86 | loss_pocket_and_one_bucket_concentration |

## Read(판독)

- blocking source views(차단 원천 보기): `4`
- high fragility axes(고취약 축): `70`
- c56 watchlist not selection(c56 관찰 목록, 선택 아님): `2`
- direction loss pockets(방향 손실 포켓): `11`

Effect(효과): c56(코어56) 쪽은 watchlist(관찰 목록)에 남지만, m48/u42(raw-forward density pressure, 원본 전진 밀도 압력)와 raw-forward MT5 missing(원본 전진 MT5 누락)이 남아 Forward Passed(전진 통과)는 없다.

## Key Files(주요 파일)

- regime attribution(국면 귀속): `stages/330_onnx_rebuild__forward_safe_non_identity_surface_robustness/02_runs/run330D/regime_attribution_unified.csv`
- fragility matrix(취약성 행렬): `stages/330_onnx_rebuild__forward_safe_non_identity_surface_robustness/02_runs/run330D/regime_fragility_matrix.csv`
- source/view attribution(원천/보기 귀속): `stages/330_onnx_rebuild__forward_safe_non_identity_surface_robustness/02_runs/run330D/source_view_attribution_matrix.csv`
- directional fragility(방향 취약성): `stages/330_onnx_rebuild__forward_safe_non_identity_surface_robustness/02_runs/run330D/directional_fragility_report.csv`
- handoff gaps(인계 공백): `stages/330_onnx_rebuild__forward_safe_non_identity_surface_robustness/02_runs/run330D/handoff_gap_audit.csv`

## Next(다음)

`run330E_mt5_runtime_probe_or_block_v1`
