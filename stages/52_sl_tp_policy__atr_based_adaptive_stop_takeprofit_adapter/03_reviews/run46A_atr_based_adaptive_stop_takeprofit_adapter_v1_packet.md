# Stage52 Run Packet(52단계 실행 패킷)

- judgment(판정): `reviewed_completed_negative_memory_runtime_probe_only`
- best_validation_candidate(최상 검증 후보): `atr01_sl1p0_tp1p5` net(순손익)=`-38.6` pf(수익 팩터)=`0.530071` trades(거래수)=`318`
- best_oos_candidate(최상 표본외 후보): `atr01_sl1p0_tp1p5` net(순손익)=`-12.73` pf(수익 팩터)=`0.796483` trades(거래수)=`269`
- adapter_candidate_gate(어댑터 후보 게이트): `failed` reasons(이유)=`['validation_net_profit_not_positive', 'oos_net_profit_not_positive', 'validation_pf_lt_1p10', 'oos_pf_lt_1p10', 'trade_count_or_concentration_gate_failed', 'concentration_gate_failed', 'cost_0p5_sensitivity_failed']`
- practical_tradability_gate(실전 거래 가능성 게이트): `failed`
- trade_count_coverage_gate(거래수 커버리지 게이트): `failed` reasons(이유)=`['single_trade_share_gt_25pct', 'day_share_gt_35pct', 'week_share_gt_50pct', 'month_share_gt_65pct']`
- concentration_audit(집중도 감사): `failed_concentrated`
- MT5 attempts(MT5 시도): `40`
- MT5 status(MT5 상태): `completed`
- boundary(주장 경계): `stage52_atr_sltp_runtime_probe_only_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_operating_reference`

Stage52(52단계)는 mandatory ATR SL/TP(필수 ATR 손절/익절) stage requirement(단계 요구)를 실행 대상으로 삼았다. Adapter-complete(어댑터 완료) 여부는 모든 gate(게이트)가 passed(통과)일 때만 열린다.
