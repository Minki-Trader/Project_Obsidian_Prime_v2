# run344I s07 Forward/Cost/Stability Review(344I s07 전진/비용/안정성 검토)

## Summary(요약)

- run_id(실행 ID): `run344I_review_s07_forward_cost_stability_validation_mt5_probe_without_db_v1`
- status(상태): `completed_stage344I_s07_forward_cost_stability_validation_reviewed_positive_moderate_cost_no_selection`
- judgment(판정): `s07_survives_moderate_cost_overlay_and_exact_runtime_parity_heavy_cost_and_session_pnl_still_unresolved_no_operating_claim`
- MT5 parity(MT5 동등성): `17481/17481`, mismatch(불일치) `0`
- s07 base net profit(s07 기본 순수익): `186.67`
- s07 moderate adjusted net(s07 중간 비용 조정 순수익): `134.67`
- s07 moderate recovery(s07 중간 비용 회복 계수): `1.507894`
- s07 heavy survival(s07 강한 비용 생존): `False`
- next_run(다음 실행): `run344J_design_s07_deal_level_cost_session_forward_replay_validation_without_db_v1`

## Action(행동)

run344H MT5 runtime probe(MT5 런타임 탐침)를 비용 오버레이(cost overlay, 비용 오버레이), comparator review(대조 검토), session/regime signal stability(세션/국면 신호 안정성)로 재판독했다.

## Effect(효과)

s07은 중간 비용(moderate cost, 중간 비용)에서도 s05/s01보다 순수익과 회복 계수가 높다. 다만 강한 비용(heavy cost, 강한 비용)에서는 회복 계수 하한을 깨고, 세션/국면은 아직 PnL attribution(손익 귀속)이 아니라 signal/fill attribution(신호/체결 귀속)이다.

## Boundary(경계)

이 run(실행)은 review(검토)다. candidate selection(후보 선정), forward pass(전진 통과), live readiness(실거래 준비), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.
