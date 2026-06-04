# run364BU late-year session gate MT5 precheck(364BU 연말 세션 게이트 MT5 사전점검)

## Scope(범위)
- Parent(부모): `run364BT_review_late_year_short_share_stress_repair_scout_without_db_v1`
- Candidate(후보): `bs02_late_year_parent_session_suppress__moy12__h21__side_long`
- New model training(새 모델 학습): `not_run(미실행)`
- Exact MT5 execution(정확 MT5 실행): `not_run`
- Operating claim(운영 주장): `not_claimed(주장 없음)`

## Result(결과)
Calendar block(달력 차단)은 EA(`Expert Advisor`, 전문가 자문)와 input contract(입력 계약)에 추가했고, MetaEditor compile(메타에디터 컴파일) 상태는 `completed`다. 효과(effect, 효과)는 `December h21 long suppression(12월 21시 롱 억제)`을 `.set` parameter(설정 파라미터)로 표현할 수 있게 한 것이다.

Exact MT5 precheck(정확 MT5 사전점검)는 실행하지 않았다. 이유(reason, 이유)는 BS proxy(BS 프록시)가 `synthetic short source(합성 숏 원천)` 47개를 필요로 하지만, 현재 EA runtime(EA 런타임)에 같은 숏 진입 원천을 내는 기능이 없기 때문이다. 효과(effect, 효과)는 proxy expected value(프록시 예상값)를 MT5 KPI(MT5 핵심 성과 지표)처럼 오해하지 않게 하는 것이다.

## Proxy KPI(프록시 KPI)
- net/PF/expectancy(순수익/수익 팩터/기대값): `1063.14` / `1.4220035161` / `1.0392346041`
- trades/density(거래수/밀도): `1023` / `3.0720720721`
- long/short(롱/숏): `898` / `125`
- suppressed parent trades/net(억제 부모 거래/순수익): `5` / `-15.29`

## Support Audit(지원 감사)
| check_id | present | status | effect |
| --- | --- | --- | --- |
| calendar_block_enabled_input | True | passed | calendar block(달력 차단) 사용 여부가 EA 입력으로 존재한다. |
| calendar_block_side_input | True | passed | long/short(롱/숏) 방향을 `.set`에서 지정할 수 있다. |
| calendar_block_month_input | True | passed | 12월 같은 month(월) 조건을 런타임에서 지정할 수 있다. |
| calendar_block_hour_inputs | True | passed | 21-22시 같은 half-open hour range(반개구간 시간 범위)를 지정할 수 있다. |
| calendar_block_reason | True | passed | 런타임 telemetry(기록)에 차단 이유가 남는다. |
| calendar_contract_documented | True | passed | 입력 계약(input contract, 입력 계약)에 새 의미가 기록됐다. |
| synthetic_short_source_insertion | False | blocked | BQ/BS synthetic short(합성 숏) 47개를 MT5 신호 원천으로 재현하는 런타임 기능은 없다. |
| exact_bs_proxy_semantic | False | blocked | BS proxy(프록시)는 synthetic short(합성 숏) 추가와 parent long(부모 롱) 억제를 함께 쓰므로 calendar block(달력 차단)만으로 exact MT5 precheck(정확 MT5 사전점검)가 아니다. |

## Proxy vs MT5(프록시 대 MT5)
| comparison_id | proxy_net_profit | mt5_net_profit | net_diff_proxy_minus_mt5 | proxy_trade_count | mt5_trade_count | usability |
| --- | --- | --- | --- | --- | --- | --- |
| bs_proxy_vs_bk_mt5_runtime_probe | 1063.14 | 959.64 | 103.5 | 1023 | 1006 | signal_sanity_only_not_runtime_authority(신호 점검 전용, 런타임 권위 아님) |
| bq_proxy_vs_bk_mt5_runtime_probe | 1047.85 | 959.64 | 88.21 | 1028 | 1006 | signal_sanity_only_not_runtime_authority(신호 점검 전용, 런타임 권위 아님) |
| exact_bs_mt5_precheck | 1063.14 |  |  | 1023 |  | blocked_until_runtime_signal_source_repair(런타임 신호 원천 수리 전까지 차단) |

## Blocker Recovery(차단 복구)
| blocker_id | status | recovery_action | next_condition |
| --- | --- | --- | --- |
| calendar_gate_missing_before_bu | repaired_if_compile_completed(컴파일 완료 시 수리됨) | added generic calendar block inputs to EA and contract(EA와 계약에 범용 달력 차단 입력 추가) | compile_status_completed(컴파일 완료 상태) |
| synthetic_short_source_runtime_missing | blocked(차단) | materialized exact blocker and BV repair queue(정확 차단 사유와 BV 수리 대기열 물질화) | runtime signal source package or model/rule bundle that emits the same short entries(같은 숏 진입을 내는 런타임 신호 원천 패키지 또는 모델/규칙 번들) |

## Gates(게이트)
| gate | status | effect |
| --- | --- | --- |
| input_lineage_gate | passed | BU 입력과 해시(hash, 해시)를 고정한다. |
| runtime_calendar_gate_support | passed | 12월 21시 long(롱) 억제를 런타임 파라미터로 표현한다. |
| metaeditor_compile_gate | passed | EA(전문가 자문) 변경이 컴파일되는지 좁게 확인한다. |
| tester_identity_handoff_gate | passed | MT5 tester(테스터) 정체성은 고정하되 실행 KPI는 주장하지 않는다. |
| exact_runtime_semantic_gate | blocked | synthetic short(합성 숏) 원천이 없어 정확 BS proxy(프록시)는 아직 런타임 의미가 닫히지 않았다. |
| mt5_execution_gate | blocked | 정확 의미 차이 때문에 Strategy Tester(전략 테스터)를 KPI 근거로 실행하지 않는다. |
| proxy_mt5_diff_gate | passed | proxy expected value(프록시 예상값)와 기존 MT5 KPI(MT5 핵심 성과 지표) 차이를 분리한다. |
| blocker_recovery_gate | passed | 차단 사유와 복구 조건을 정확히 남긴다. |
| final_claim_guard | passed | runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성)를 주장하지 않는다. |
| required_gate_coverage_audit | blocked | 필수 gate(게이트)의 통과/차단 상태를 closeout(종료 기록)에 연결한다. |

## Boundary(경계)
이 run(실행)은 runtime precheck(런타임 사전점검)와 blocker recovery(차단 복구)다. runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 `not_claimed(주장 없음)`이다.
