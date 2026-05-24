# run292C Anti-Direction Meta Trade Sim Review(292C 반대방향 메타 거래 시뮬레이터 검토)

- status(상태): `completed_anti_direction_meta_trade_sim_review_no_candidate_stage293_opened`
- judgment(판정): `anti_direction_meta_trade_sim_runtime_probe_negative_no_adapter_no_onnx`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(ONNX 준비): `not_started`
- next_action(다음 행동): `run293A_design_profit_scale_density_calibration_rebuild_packet`
- next_stage(다음 단계): `293_onnx_candidate_campaign__profit_scale_density_calibration_rebuild`

Effect(효과): MT5 actual routed total(MT5 실제 라우팅 전체)을 최소 거래수, 일 4-10거래, 순수익 규모, PF(수익 팩터), 회복, 기대값, 확대 곡선 포켓 조건으로 판정한다.

| package(패키지) | val net(검증 순수익) | val PF(검증 수익 팩터) | val/day(검증 일거래) | OOS net(표본외 순수익) | OOS PF(표본외 수익 팩터) | OOS/day(표본외 일거래) | gate(게이트) |
|---|---:|---:|---:|---:|---:|---:|---|
| cp292A_anti_direction_lgbm_meta_hold6_surface | 60.45 | 1.42 | 0.39 | 81.48 | 2.28 | 0.52 | valid_negative_no_candidate |
| cp292B_trade_sim_xgb_inverse_hold8_surface | -490.99 | 0.74 | 2.83 | -168.22 | 0.93 | 6.50 | valid_negative_no_candidate |
| cp292C_density_profit_two_head_histgb_hold5_surface | -202.34 | 0.88 | 5.93 | 165.37 | 1.12 | 7.50 | valid_negative_no_candidate |
| cp292D_contrarian_session_extratrees_hold4_surface | 41.17 | 1.04 | 3.98 | -50.77 | 0.95 | 4.66 | valid_negative_no_candidate |
| cp292E_curve_guarded_lgbm_hold10_surface | -355.47 | 0.89 | 7.88 | -494.21 | 0.79 | 6.89 | valid_negative_no_candidate |
| cp292F_aggressive_tail_xgb_meta_hold6_surface | -113.00 | 0.59 | 0.36 | 42.52 | 1.39 | 0.40 | valid_negative_no_candidate |

Claim boundary(주장 경계): 이 결과는 연구/개발 판정이다. 운영 승격, 런타임 권위, 배포, production baseline(운영 기준선)은 주장하지 않는다.
