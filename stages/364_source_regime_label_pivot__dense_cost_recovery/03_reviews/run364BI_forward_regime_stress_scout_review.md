# run364BI forward/regime stress scout review(364BI 전진/국면 스트레스 탐색 검토)

## Scope(범위)
- Parent(부모): `run364BH_train_density_restore_forward_regime_stress_scout_without_db_v1`
- Selected candidate(선택 후보): `bh02_long_h19_margin_opp_0020`
- New MT5 execution(새 MT5 실행): not run(미실행)
- Operating claim(운영 주장): not claimed(주장 안 함)

## Current Truth(현재 진실)
BH 후보는 proxy(프록시) 기준으로 net profit(순수익) `938.59`, profit factor(수익 팩터) `1.3732279833`, trades(거래수) `1003`, density(밀도) `3.012012012`를 냈다. 효과는 작은 h19 long margin guard(19시 롱 마진 가드)가 수익 구조를 개선할 수 있다는 clue(단서)를 살린 것이다.

하지만 parameter-only package(파라미터만 패키지)는 불가하다. 후보는 `p_long - p_short < 0.002`를 hour 19 long(19시 롱)에만 적용하지만, 현재 EA는 global max-other entry margin floor(전역 최대 타방 진입 마진 하한)와 March-specific filter(3월 전용 필터)만 가진다.

## Runtime Gap(런타임 차이)
| gap_id | research_semantic | runtime_semantic | exact_match | usability |
| --- | --- | --- | --- | --- |
| hour_scope_gap | entry_hour == 19 and side == long only(진입 시간이 19이고 롱만) | global entry margin floor or March-only filter(전역 진입 마진 하한 또는 3월 전용 필터) | False | requires_code_support_before_package(패키지 전 코드 지원 필요) |
| margin_basis_gap | p_long - p_short < 0.002 blocks long(롱 확률-숏 확률이 0.002 미만이면 롱 차단) | p_long - max(p_flat, p_short) with InpEntryMarginFloor(전역 진입 마진 하한은 롱 확률-최대 타방 확률) | False | cannot_be_parameter_only_runtime_probe(파라미터만으로 런타임 탐침 불가) |
| runtime_claim_gap | closed trade proxy replay(종료 거래 프록시 재생) | Strategy Tester tick execution(전략 테스터 틱 실행) | False | screening_positive_only(선별 긍정 근거 전용) |

## Support Audit(지원 감사)
| capability | present | usable_for_selected_candidate | reason |
| --- | --- | --- | --- |
| global_entry_margin_floor(전역 진입 마진 하한) | True | False | 전역(global, 전역)이고 max-other margin(최대 타방 마진)을 쓰므로 h19 long opposite margin(19시 롱 반대 마진)과 의미가 다르다. |
| march_specific_time_margin_filter(3월 전용 시간/마진 필터) | True | False | 월(month, 월)이 3월로 고정된 특수 필터라 h19 long guard(19시 롱 가드)를 표현하지 못한다. |
| generic_hour_side_probability_guard(일반 시간/방향/확률 가드) | False | False | 현재 입력(input, 입력)에는 임의 hour(시간), side(방향), margin basis(마진 기준)를 받는 범용 가드가 없다. |
| opposite_probability_margin_basis(반대 방향 확률 마진 기준) | False | False | EA의 SignalSideMargin(신호 방향 마진)은 selected - max(flat, opposite)이고 BH 후보는 selected - opposite이다. |

## Package Decision(패키지 결정)
| variant_id | proxy_positive | runtime_exact_support | package_ready_parameter_only | package_readiness |
| --- | --- | --- | --- | --- |
| bh02_long_h19_margin_opp_0020 | True | False | False | not_ready_requires_runtime_guard_support(미준비, 런타임 가드 지원 필요) |

## Short Source(숏 원천)
| action_id | current_short_share | minimum_added_shorts_needed_if_no_long_removal | next_action |
| --- | --- | --- | --- |
| new_short_source_required | 0.0987038883 | 25 | explore_new_short_source_after_runtime_guard_support(런타임 가드 지원 후 새 숏 원천 탐색) |

## Next Queue(다음 대기열)
| queue_rank | queue_id | task | success_criteria |
| --- | --- | --- | --- |
| 1 | bj01_add_generic_hour_side_margin_guard | add EA inputs for enabled/side/hour_start/hour_end/margin_basis/min_margin(EA 입력에 사용 여부/방향/시작시/끝시/마진 기준/최소 마진 추가) | can express hour 19 long p_long-p_short < 0.002 as flat(19시 롱 p_long-p_short < 0.002를 flat으로 표현) |
| 2 | bj02_package_exact_candidate_after_compile | package exact h19 opposite-margin candidate after compile check(컴파일 확인 후 h19 반대마진 후보를 정확 패키징) | set/config/semantic audit all name the same guard(set/config/의미 감사가 같은 가드를 지칭) |
| 3 | bj03_execute_or_block_narrow_mt5_probe | attempt the narrow Strategy Tester probe or record exact blocker(좁은 전략 테스터 탐침을 시도하거나 정확 차단 사유 기록) | tester output exists or blocker has command/log/next condition(테스터 출력 존재 또는 명령/로그/다음 조건이 있는 차단 기록) |

## Gates(게이트)
| gate | status | effect |
| --- | --- | --- |
| kpi_contract_audit | passed | KPI 계약(KPI contract, KPI 계약)이 후보 숫자를 모두 가진다. |
| row_grain_audit | passed | 행 단위(row grain, 행 단위)가 후보/블록/수리별로 분리됐다. |
| source_authority_audit | passed | 원천 권위(source authority, 원천 권위)가 프록시와 런타임 소스로 분리됐다. |
| runtime_semantic_gap_audit | passed | 현재 EA 파라미터로 정확 표현 불가함을 기록했다. |
| required_gate_coverage_audit | passed | 필수 게이트(required gates, 필수 게이트)가 closeout(종료 기록)에 연결됐다. |
| final_claim_guard | passed | 운영 승격/런타임 권위/목표 달성 주장을 금지했다. |
