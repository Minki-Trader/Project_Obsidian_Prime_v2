# Stage52 ATR SL/TP Adapter(52단계 ATR 손절/익절 어댑터)

- idea_id(아이디어 ID): `IDEA-ST52-ATR-BASED-ADAPTIVE-STOP-TAKEPROFIT-ADAPTER`
- run_id(실행 ID): `run46A_atr_based_adaptive_stop_takeprofit_adapter_v1`
- packet_id(패킷 ID): `stage52_run46A_atr_based_adaptive_stop_takeprofit_adapter_v1`
- adapter_hypothesis(어댑터 가설): ATR-based SL/TP(ATR 기반 손절/익절)가 Stage51(51단계) `fw02_block_di_short_mild` entry stream(진입 흐름)에 붙으면 validation/OOS(검증/표본외) 양쪽에서 실제 risk adapter(위험 어댑터)로 버틸 수 있는지 확인한다.
- core_question(핵심 질문): SL/TP distance(손절/익절 거리)를 ATR(평균 진폭)로 정하면 WFO(워크포워드), cost(비용), concentration(집중도), trade-count density(거래 밀도)를 통과하는가?
- allowed_mechanisms(허용 메커니즘): MT5 iATR(메타트레이더5 iATR), fixed lot(고정 랏), Stage51 firewall signal(Stage51 방화벽 신호), `.set` parameterized SL/TP(`.set` 파라미터 손절/익절).
- forbidden_mechanisms(금지 메커니즘): future leakage(미래 누수), post-trade selection(사후 거래 선택), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비).
- expected_mt5_evidence(예상 MT5 근거): `.set`, `.ini`, Strategy Tester HTML(전략 테스터 HTML), telemetry(텔레메트리), imported KPI(가져온 핵심성과지표) rows(행).
- boundary(주장 경계): `stage52_atr_sltp_runtime_probe_only_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_operating_reference`
