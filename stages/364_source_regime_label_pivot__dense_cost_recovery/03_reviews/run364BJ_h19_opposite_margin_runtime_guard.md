# run364BJ h19 opposite-margin runtime guard(364BJ 19시 반대마진 런타임 가드)

## Scope(범위)
- Parent(부모): `run364BI_review_density_restore_forward_regime_stress_scout_without_db_v1`
- Candidate(후보): `bh02_long_h19_margin_opp_0020`
- New model training(새 모델 학습): not run(미실행)
- MT5 execution(메타트레이더5 실행): `attempted`
- Operating claim(운영 주장): not claimed(주장 안 함)

## Result(결과)
EA(`Expert Advisor`, 전문가 자문)에 generic time-margin guard(범용 시간-마진 가드)를 추가하고, BJ `.set/.ini` package(설정/INI 패키지)를 만들었다. 효과는 BH proxy rule(BH 프록시 규칙) `hour 19 long p_long-p_short < 0.002`를 MT5에서 같은 의미로 켤 수 있게 한 것이다.

Compile status(컴파일 상태): `completed`. Portable sync(포터블 동기화): `True`.

Runtime output status(런타임 출력 상태): `completed`. Strategy report status(전략 보고서 상태): `completed`.

## Support Audit(지원 감사)
| check_id | present | status | effect |
| --- | --- | --- | --- |
| input_enabled | True | passed | EA가 h19 opposite-margin guard(19시 반대마진 가드)를 같은 의미로 표현할 수 있는지 확인한다. |
| input_side | True | passed | EA가 h19 opposite-margin guard(19시 반대마진 가드)를 같은 의미로 표현할 수 있는지 확인한다. |
| input_hour_start | True | passed | EA가 h19 opposite-margin guard(19시 반대마진 가드)를 같은 의미로 표현할 수 있는지 확인한다. |
| input_hour_end | True | passed | EA가 h19 opposite-margin guard(19시 반대마진 가드)를 같은 의미로 표현할 수 있는지 확인한다. |
| input_basis | True | passed | EA가 h19 opposite-margin guard(19시 반대마진 가드)를 같은 의미로 표현할 수 있는지 확인한다. |
| input_min_margin | True | passed | EA가 h19 opposite-margin guard(19시 반대마진 가드)를 같은 의미로 표현할 수 있는지 확인한다. |
| opposite_basis_logic | True | passed | EA가 h19 opposite-margin guard(19시 반대마진 가드)를 같은 의미로 표현할 수 있는지 확인한다. |
| guard_reason | True | passed | EA가 h19 opposite-margin guard(19시 반대마진 가드)를 같은 의미로 표현할 수 있는지 확인한다. |
| contract_documented | True | passed | EA가 h19 opposite-margin guard(19시 반대마진 가드)를 같은 의미로 표현할 수 있는지 확인한다. |

## Proxy vs MT5(프록시 대 MT5)
| proxy_net_profit | proxy_profit_factor | proxy_trade_count | mt5_net_profit | mt5_profit_factor | mt5_trade_count | usability |
| --- | --- | --- | --- | --- | --- | --- |
| 938.59 | 1.3732279833 | 1003 | 959.64 | 1.38 | 1006 | mt5_kpi_review_ready(테스터 KPI 검토 준비) |

## Gates(게이트)
| gate | status | effect |
| --- | --- | --- |
| code_surface_audit | passed | EA 입력과 계약 문서가 새 guard(가드)를 포함한다. |
| metaeditor_compile_gate | passed | MetaEditor compile(메타에디터 컴파일)이 통과해야 런타임 패키지를 주장할 수 있다. |
| portable_sync_gate | passed | compiled EX5(컴파일된 EX5)를 portable tester(포터블 테스터)에 동기화한다. |
| tester_identity_gate | passed | US100 M5 real ticks(실제 틱), deposit 500(예치금 500), leverage 100(레버리지 100)을 고정한다. |
| runtime_execution_attempt_gate | passed | MT5 Strategy Tester(전략 테스터) 실행을 시도하거나 차단 로그를 남긴다. |
| runtime_evidence_gate | passed | runtime telemetry/summary(런타임 기록/요약)가 있어야 완료 증거가 된다. |
| strategy_report_gate | passed | 전략 테스터 보고서가 있어야 MT5 KPI를 읽는다. |
| proxy_mt5_diff_gate | passed | proxy expected value(프록시 예상값)와 MT5 출력 차이 기록을 만든다. |
| final_claim_guard | passed | runtime authority(런타임 권위)와 operating promotion(운영 승격)을 금지한다. |
| required_gate_coverage_audit | passed | 필수 게이트(required gates, 필수 게이트)를 closeout(종료 기록)에 연결한다. |
