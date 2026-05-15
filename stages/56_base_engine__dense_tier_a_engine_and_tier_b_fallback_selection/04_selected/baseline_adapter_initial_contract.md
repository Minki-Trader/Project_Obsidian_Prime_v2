# BaselineAdapter Initial Contract(기준선 어댑터 초기 계약)

- adapter_id(어댑터 ID): `baseline_adapter_v0_stage56_run50BR_v64`
- development_anchor(개발 기준점): `v64_v47_ctxgap14_refill_etfw_h2_no_b`
- selected_research_baseline(선택 연구 기준선): `none`
- routing(라우팅): Tier A primary(Tier A 우선), Tier B disabled(Tier B 비활성)
- risk(위험): model confidence(모델 신뢰도) 기반 risk_per_trade(거래당 위험), cap(상한) `5%`, floor lot(최소 랏) `0.01`
- ATR bracket(ATR 브래킷): ATR(14), SL(손절) `1.5x`, TP(익절) `2.0x`
- MT5 run(MT5 실행): `run50BT_stage56_baseline_adapter_v64_mt5_v1`

Effect(효과): contract(계약)이 더 이상 handoff-only(인계 전용)가 아니라 실제 adapter MT5 validation/OOS(어댑터 MT5 검증/표본외) 경로를 가리킨다.
