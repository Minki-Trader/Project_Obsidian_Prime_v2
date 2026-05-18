# Stage171 Segment/Equity Curve Audit(171단계 구간/자산 곡선 감사)

- stage(단계): `171_adapter_research__segment_stability_equity_curve_audit`
- run(실행): `run171A_stage171_segment_stability_equity_curve_audit_v1`
- source_stage(원천 단계): `170_adapter_research__stage169_net_density_followup_review`
- source_closeout_commit(원천 종료 커밋): `9e82e985bdd235efe4e04c9a36cde4368495e19e`
- source_hash_record_commit(원천 해시 기록 커밋): `802fd1d18fe2d776866723556d63c409725f7c62`
- external_verification_status(외부 검증 상태): `review_only_source_stage169_mt5_reports_completed`
- decision(판정): `open_stage172_validation_drawdown_concentration_repair_candidate_not_final`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Bounded Question(경계 질문)

Does `s169_short_pre_risk0350_h3_cd5_sht54_lng52` survive segment stability(구간 안정성), equity curve(자산 곡선), balance curve(잔고 곡선), concentration(집중도), drawdown recovery(낙폭 회복), and MFE/MAE behavior(MFE/MAE 동작) audit as a research candidate(연구 후보)?

## Answer(답)

No(아니오). KPI(핵심 성과 지표)는 34D(34D)에 매우 가까워졌지만, research-grade candidate(연구급 후보)로 바로 넘기기에는 validation drawdown(검증 낙폭), validation early/mid PF(검증 초반/중반 수익요인), late concentration(후반 집중)이 약하다.

Effect(효과): Stage172(172단계)는 open-ended tuning(개방형 튜닝)이 아니라 validation DD/concentration repair(검증 낙폭/집중도 수리)만 좁게 다룬다.

## Balance Curve Summary(잔고 곡선 요약)

| split(분할) | net_profit(순손익) | profit_factor(수익요인) | max_drawdown_amount(최대 낙폭 금액) | max_drawdown_percent(최대 낙폭률) | report_balance_drawdown_relative(보고서 잔고 상대 낙폭) | report_equity_drawdown_relative(보고서 자산 상대 낙폭) | late_net_share(후반 순손익 비중) | validation_weak_segments(검증 약한 구간) | split_quality_flag(분할 품질 표식) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| validation_is | 983.96 | 1.611235 | 135.28 | 14.301 | 14.30% (135.28) | 14.98% (142.64) | 0.5508 | early;mid | validation_dd_above_34d(검증 낙폭 34D 초과);late_concentration_above_50pct(후반 집중 50% 초과);validation_early_mid_pf_below_34d(검증 초중반 수익요인 34D 미만) |
| oos | 835.78 | 1.8221 | 95.71 | 10.0007 | 10.54% (58.01) | 13.07% (73.07) | 0.5078 |  | late_concentration_above_50pct(후반 집중 50% 초과) |

## Drawdown Recovery(낙폭 회복)

| split(분할) | max_drawdown_amount(최대 낙폭 금액) | max_drawdown_percent(최대 낙폭률) | drawdown_peak_time(낙폭 고점 시간) | drawdown_trough_time(낙폭 저점 시간) | recovered(회복 여부) | recovery_time(회복 시간) | recovery_trades(회복 거래 수) | max_underwater_trades(최장 수중 거래 수) | drawdown_flag(낙폭 표식) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| validation_is | 135.28 | 14.301 | 2025.04.25 16:50:00 | 2025.05.05 17:35:00 | True | 2025.05.15 16:50:00 | 10 | 26 | dd_above_34d(34D 초과 낙폭) |
| oos | 95.71 | 10.0007 | 2026.02.17 21:35:00 | 2026.02.24 16:38:52 | True | 2026.03.06 22:27:57 | 14 | 24 | dd_measurement_only(낙폭 측정 전용) |

## Concentration(집중도)

| split(분할) | top1_winner_share_of_net(최대 승리 순손익 비중) | top3_winner_share_of_net(상위 3승 순손익 비중) | top5_winner_share_of_net(상위 5승 순손익 비중) | worst_loss_share_of_net_abs(최대 손실 순손익 비중) | last_quarter_net_share(마지막 25% 순손익 비중) |
| --- | --- | --- | --- | --- | --- |
| validation_is | 0.0774 | 0.2278 | 0.372 | 0.0495 | 0.4681 |
| oos | 0.105 | 0.2603 | 0.3823 | 0.0456 | 0.47 |

## Decision Basis(판정 근거)

- action(행동): MT5 report(메타트레이더5 보고서)의 closed deals(청산 거래)에서 balance curve(잔고 곡선)를 재구성했다. effect(효과): final net(최종 순손익)만 보지 않고 peak-to-trough drawdown(고점-저점 낙폭)과 recovery(회복)를 확인했다.
- action(행동): Stage170 segment review(170단계 구간 검토)를 결합했다. effect(효과): validation early/mid PF(검증 초반/중반 수익요인) 약점과 late contribution(후반 기여)을 그대로 보존했다.
- action(행동): Stage169 trade audit(169단계 거래 감사)의 cost stress/MFE/re-entry(비용 압박/MFE/재진입)를 같이 읽었다. effect(효과): OOS(표본외)가 강한 부분은 보존하되, 약한 validation(검증)을 다음 repair(수리) 질문으로 넘긴다.

## Route Decision(경로 판정)

1. primary(주): `stage172_validation_drawdown_concentration_repair`.
2. guardrail(보호 기준): `preserve_oos_strength_and_risk_atr_telemetry`.
3. failure_memory(실패 기억): `keep_long_restore_as_failure_memory`.

Audit judgment(감사 판정): `segment_equity_audit_failed_repair_required_not_final`.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료).
