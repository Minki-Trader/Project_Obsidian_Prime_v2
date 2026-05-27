# Stage337AE Completed-Day Forward Attribution Cost Stress(337AE 완성일 전진 귀속/비용 압박)

- run_id(실행 ID): `run337AE_completed_day_forward_attribution_cost_stress_v1`
- status(상태): `completed_stage337AE_completed_day_attribution_cost_stress_fragile_no_forward_decision`
- judgment(판정): `completed_day_slice_runtime_parity_holds_but_cost_buffer_recovery_and_curve_pockets_are_fragile`
- decision(결정): `stage337AE_open_run337AF_failure_memory_and_no_overfit_rebuild_queue_no_selection`
- completed_day_net(완성일 순수익): `99.9`
- completed_day_pf(완성일 수익 팩터): `1.1343066871`
- completed_day_closed_trade_dd(완성일 마감 거래 손실폭): `95.53`
- completed_day_mt5_equity_dd(완성일 MT5 평가금 손실폭): `112.86`
- completed_day_mt5_recovery(완성일 MT5 회복 계수): `0.89`
- one_point_stress_pf(1포인트 압박 수익 팩터): `1.08630090555`
- five_point_stress_net(5포인트 압박 순수익): `-72.1175977083`
- parser_errors(파서 오류): `0`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Read(판독)

run337AD(337AD 실행)의 completed-day broker slice(완성일 브로커 구간)는 MT5(메타트레이더5) 거래 보고서 기준으로 순수익은 양수지만 PF(수익 팩터)와 recovery(회복)가 얇다. 1포인트 추가 비용에서 PF가 약해지고 5포인트 압박에서는 순수익이 깨진다.

효과: 이 결과는 후보를 수정하지 않고도 cost buffer(비용 버퍼), curve pocket(곡선 포켓), direction mix(방향 혼합)의 약점을 다음 실패 기억/재구성 큐로 넘긴다. 최신 현재일 전체 forward(전진) 판정은 full current-day control(현재일 전체 대조군) 공백 때문에 아직 닫지 않는다.

## Curve Pockets(곡선 포켓)

| pocket(포켓) | bucket(구간) | net(순수익) | PF(수익 팩터) | trades(거래 수) | read(판독) |
|---|---|---:|---:|---:|---|
| `worst_rolling_50_trades` | `2026-05-14 08:00:00` | `-75.83` | `` | `50` | `negative_rolling_pocket` |
| `worst_rolling_20_trades` | `2026-05-18 09:20:00` | `-72.06` | `` | `20` | `negative_rolling_pocket` |
| `worst_chron_segment` | `chron_late` | `-11.45` | `0.965924647342` | `114` | `negative_slice` |

## Artifacts(산출물)

- frozen forward MT5 report(고정 전진 MT5 보고): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/03_reviews/run337AE_completed_day_forward_attribution_cost_stress.md`
- regime attribution report(국면 귀속 보고): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337AE/regime_attribution_report.csv`
- D/B attribution report(D/B 귀속 보고): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337AE/db_attribution_report.csv`
- lot-normalized report(랏 정규화 보고): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337AE/lot_normalized_report.csv`
- cost stress report(비용 압박 보고): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337AE/cost_stress_report.csv`
- curve pocket report(곡선 포켓 보고): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337AE/curve_pocket_report.csv`
- final forward decision report(최종 전진 결정 보고): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337AE/final_forward_decision_report.json`

## Attribution Boundary(귀속 경계)

- D/B attribution(D/B 귀속): `not_available_in_run337AD_u42_artifacts`
- economic external fields(경제 외부 필드): `0/3` available(사용 가능)
- no retune(재튜닝 없음): `true`
- no threshold change(임계값 변경 없음): `true`
- no lot optimization(랏 최적화 없음): `true`
