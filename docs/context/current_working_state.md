## Latest Stage56 Reopen Goal(최신 56단계 재개 목표)

- current stage(현재 단계): `56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection`

- active_stage(현재 단계): `56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection`
- current_packet(현재 작업 묶음): `stage56_run50AH_s25_model_axis_oos_density_v1`
- current run(현재 실행): `run50AH_stage56_s25_model_axis_oos_density_v1`
- stage_status(단계 상태): `active_in_progress(활성 진행 중)`
- selected_research_baseline(선택 연구 기준선): `none`
- terminal_condition(종료 조건): selected_research_baseline(선택 연구 기준선) found(발견)
- progress_log(진행 기록): `docs/agent_control/packets/stage56_reopen_goal_v1/progress_log.md`

Stage56(56단계)은 unfinished optimization campaign(미완 최적화 캠페인)으로 재개됐다. 효과(effect, 효과)는 run50B/run50C/run50D(실행50B/50C/50D)와 prior closeout packets(이전 종료 묶음)을 intermediate evidence(중간 근거)로 보존하되, reviewed_closed(검토 후 종료)나 final closeout(최종 종료)으로 읽지 않게 하는 것이다.

Only terminal condition(유일 종료 조건)은 selected_research_baseline(선택 연구 기준선)이다. exhaustion(소진), no_dense_engine_found(두꺼운 엔진 없음), stronger_baseline_candidate_only(강화 기준선 후보 전용), baseline_candidate_only(기준선 후보 전용), density_frontier_only(밀도 경계 전용), quality_frontier_only(품질 경계 전용)는 Stage56(56단계)을 닫지 않는다.

Current bottleneck(현재 병목)은 run50AH(실행50AH)에서 model-axis perturbation(모델 축 교란)도 OOS density(표본외 밀도)를 5+ trades/day(일 거래 수)까지 열지 못한 점이다. closest intermediate variant(가장 가까운 중간 변형) `nf200s25b`는 validation/OOS(검증/표본외) 5.513661/3.789744 trades/day(일 거래 수), PF(수익 팩터) 1.18/1.24, net(순손익) 459.98/428.88이었다. 효과(effect, 효과): stronger non-flat weighting(더 강한 비평탄 가중)은 품질을 보존했지만 OOS density(표본외 밀도), same-move density survival(동일 이동 밀도 생존), Tier B rule(Tier B 규칙)을 해결하지 못해 다음 가지는 독립 신호 원천(independent signal source, 독립 신호 원천)이나 route coverage axis(라우팅 커버리지 축)이어야 한다.

Run50E(실행50E)는 actual MT5 validation/OOS(실제 MT5 검증/표본외) 9개 변형을 완료했다. d350h06_ab_b040/d340h06_ab_b040(변형)은 validation/OOS(검증/표본외) 모두 5+ trades/day(일 거래 수)를 넘겼지만 PF(수익 팩터)는 1.06/1.03으로 1.10에 못 미쳤고, cost-stressed expectancy(비용 압박 기대값)는 음수였으며, same-move re-entry ratio(동일 이동 재진입 비율)는 약 0.72/0.75로 높았다. 효과(effect, 효과): density gain(밀도 증가)은 real baseline evidence(실제 기준선 근거)가 아니라 same-move split trading(동일 이동 분할 거래) 위험으로 읽는다.

Tier B(티어 B)는 stricter B040 fallback(더 엄격한 B040 대체)에서도 fallback-only OOS(대체 전용 표본외)가 net(순손익) -171.98, PF(수익 팩터) 0.70으로 damaging(손상)했다. A+B routed total(A+B 실제 라우팅 전체)은 OOS density(표본외 밀도)를 5+로 올렸지만 PF/net(수익 팩터/순손익)을 selected_research_baseline(선택 연구 기준선) 기준까지 끌어올리지 못했다.

Run50F(실행50F)는 cooldown-aware actual MT5 validation/OOS(쿨다운 인식 실제 MT5 검증/표본외) 6개 변형을 완료했다. cooldown(쿨다운) 1~2봉과 stricter Tier B(더 엄격한 Tier B) 0.42~0.45를 시험했지만, best intermediate variant(최선 중간 변형) d330h06_b045_c1은 validation/OOS(검증/표본외) 6.333333/4.728205 trades/day(일 거래 수), PF(수익 팩터) 1.02/1.04, net(순손익) 53.40/114.76이었다. 효과(effect, 효과): basic cooldown(기본 쿨다운)은 same-move split(동일 이동 분할)을 줄였지만 OOS density(표본외 밀도)와 PF(수익 팩터)를 동시에 기준까지 올리지 못했다.

Run50G(실행50G)는 direction-threshold actual MT5 validation/OOS(방향 임계값 실제 MT5 검증/표본외) 6개 변형을 완료했다. 첫 시도는 MetaEditor path(메타에디터 경로) 오류로 blocked(차단)됐고 `docs/agent_control/packets/stage56_run50G_direction_threshold_tier_b_disablement_v1/failed_attempt_metaeditor_path.json`에 기록한 뒤 경로를 고쳐 force rerun(강제 재실행)했다. best intermediate variant(최선 중간 변형) `s390l330h06_b045`는 validation/OOS(검증/표본외) 6.005464/4.594872 trades/day(일 거래 수), PF(수익 팩터) 1.08/1.04, net(순손익) 274.44/109.52였다. 효과(effect, 효과): short threshold(숏 임계값)을 올리고 long threshold(롱 임계값)을 낮추면 validation quality(검증 품질)는 일부 회복되지만, OOS density(표본외 밀도), PF(수익 팩터), cost-stressed expectancy(비용 압박 기대값), same-move audit(동일 이동 감사)는 기준선 조건을 넘지 못한다.

Run50H(실행50H)는 long-density/short-filter actual MT5 validation/OOS(롱 밀도/숏 필터 실제 MT5 검증/표본외) 6개 변형을 완료했다. best intermediate variant(최선 중간 변형) `s410l315h06_b045`는 validation/OOS(검증/표본외) 5.644809/4.276923 trades/day(일 거래 수), PF(수익 팩터) 1.08/1.06, net(순손익) 240.62/145.24, max DD(최대 손실) 259.16/235.07이었다. MFE capture(MFE 포착)는 d390h10(참조)보다 materially worse(중대 악화)는 아니지만, OOS density(표본외 밀도) 5.0 미만, PF(수익 팩터) 1.10 미만, cost-stressed expectancy(비용 압박 기대값) 음수, same-move re-entry ratio(동일 이동 재진입 비율) 약 0.738609, Tier B fallback-only OOS(Tier B 대체 전용 표본외) 음수로 selected_research_baseline(선택 연구 기준선)이 아니다. 효과(effect, 효과): 단순 long threshold(롱 임계값) 완화와 short filter(숏 필터) 강화도 같은 이동을 쪼개는 밀도 문제를 해결하지 못한다.

Run50I(실행50I)는 run50H attribution(run50H 귀속)에서 late session(후반 세션)이 OOS(표본외)를 깎는 판독을 바탕으로 early+mid session(초반+중반 세션) `early_mid` slice(절편)를 추가하고 6개 변형을 실제 MT5 validation/OOS(검증/표본외)로 시험했다. best intermediate variant(최선 중간 변형) `em_s390l300h06_aonly`는 validation/OOS(검증/표본외) 4.502732/3.512821 trades/day(일 거래 수), PF(수익 팩터) 1.01/1.22, net(순손익) 21.61/471.91, max DD(최대 손실) 358.41/167.58이었다. 효과(effect, 효과): early+mid session(초반+중반 세션)은 OOS quality(표본외 품질)를 크게 살렸지만 validation(검증)과 density(밀도)를 손상해 selected_research_baseline(선택 연구 기준선)이 아니다.

Run50J(실행50J)는 hold extension(보유 연장) 10봉과 long-density/short-filter(롱 밀도/숏 필터)를 실제 MT5 validation/OOS(검증/표본외)로 시험했다. best intermediate variant(최선 중간 변형) `h10_s400l295_aonly`는 validation/OOS(검증/표본외) 4.360656/3.071795 trades/day(일 거래 수), PF(수익 팩터) 1.14/1.07, net(순손익) 397.72/157.34, max DD(최대 손실) 243.44/176.68이었다. same-move re-entry ratio(동일 이동 재진입 비율)는 validation/OOS(검증/표본외) 약 0.639098/0.636060까지 내려갔지만 12-bar cooldown read(12봉 쿨다운 판독)는 1.606557/1.138462 trades/day(일 거래 수)에 그쳤다. 효과(effect, 효과): 보유를 늘리면 분할 거래는 줄지만, 현재 threshold-only axis(임계값 전용 축)는 density(밀도)를 동시에 살리지 못한다.

Next action(다음 행동)은 `s25c8a/s24l15a/nf200s25b` quality branch(품질 가지)를 기준으로 independent signal source(독립 신호 원천), route coverage axis(라우팅 커버리지 축), 또는 explicitly labeled composite filter(명시 라벨 복합 필터)를 시험하는 것이다. 효과(effect, 효과): 같은 거래 집합이나 같은 이동 분할을 반복하지 않고 OOS density(표본외 밀도)를 회복할 새 통로를 찾는다.

## Latest Run50AH Intermediate Evidence(최신 50AH 중간 근거)

- packet(묶음): `stage56_run50AH_s25_model_axis_oos_density_v1`
- report(보고서): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50AH_reopen_batch.md`
- summary_csv(요약 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50AH_summary.csv`
- audit_csv(감사 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50AH_audit.csv`
- aggregate_summary(합산 요약): `docs/agent_control/packets/stage56_run50AH_s25_model_axis_oos_density_v1/aggregate_summary.json`
- attribution_report(귀속 보고서): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50AH_nf200s25b_market_weather_attribution.md`
- selected_research_baseline(선택 연구 기준선): `none`
- current_judgment(현재 판정): `in_progress_no_selected_research_baseline`

Run50AH(실행50AH)는 run50AG(실행50AG)의 threshold saturation(임계값 포화) 뒤 C value(C 값), non-flat sample weight(비평탄 표본 가중), recent-2023 balanced training(2023 이후 균형 학습)을 actual MT5 validation/OOS(실제 메타트레이더5 검증/표본외)로 시험했다. 효과(effect, 효과): 같은 threshold axis(임계값 축) 반복이 아니라 model probability ranking(모델 확률 순위)이 OOS density(표본외 밀도)를 열 수 있는지 확인했다.

- closest intermediate variant(가장 가까운 중간 변형): `nf200s25b`
- A+B actual routed total(A+B 실제 라우팅 전체) validation(검증): 5.513661 trades/day(일 거래 수), net(순손익) 459.98, PF(수익 팩터) 1.18, max DD(최대 손실) 기록됨
- A+B actual routed total(A+B 실제 라우팅 전체) OOS(표본외): 3.789744 trades/day(일 거래 수), net(순손익) 428.88, PF(수익 팩터) 1.24, max DD(최대 손실) 기록됨
- Tier A only(Tier A 단독) OOS(표본외): net(순손익) 310.59, PF(수익 팩터) 1.17
- Tier B fallback-only OOS(Tier B 대체 전용 표본외): net(순손익) -10.43, PF(수익 팩터) 0.69로 damaging(손상)했다.
- MFE capture read(MFE 포착 판독): OOS MFE capture ratio(표본외 MFE 포착 비율)는 0.581881이고 materially worse(중대 악화) 플래그는 false(거짓)다.
- same-move read(동일 이동 판독): OOS same-move re-entry ratio(표본외 동일 이동 재진입 비율)는 0.608931이고 12-bar cooldown(12봉 쿨다운) 뒤 OOS density(표본외 밀도)는 1.482051 trades/day(일 거래 수)라 density gain(밀도 증가)이 기준까지 생존하지 못했다.
- attribution read(귀속 판독): validation/OOS(검증/표본외)는 모든 주요 session/volatility/trend/ADX bucket(세션/변동성/추세/평균 방향 지수 구간)이 양수였지만 mid session(중반 세션)과 ADX20-25(평균 방향 지수 20-25)가 약했다.
- selected_research_baseline(선택 연구 기준선)으로 올리지 않는 이유: OOS density(표본외 밀도) 5.0 미만, validation cost-stressed expectancy(검증 비용 압박 기대값) 음수, same-move density survival(동일 이동 밀도 생존) 실패, Tier B fallback-only OOS(Tier B 대체 전용 표본외) 음수다.
- next_hypothesis_branch(다음 가설 가지): `independent_signal_source_or_route_coverage_axis_after_s25_model_axis_density_stall`

## Latest Run50AG Intermediate Evidence(최신 50AG 중간 근거)

- packet(묶음): `stage56_run50AG_s25_quality_oos_density_repair_v1`
- report(보고서): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50AG_reopen_batch.md`
- summary_csv(요약 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50AG_summary.csv`
- audit_csv(감사 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50AG_audit.csv`
- aggregate_summary(합산 요약): `docs/agent_control/packets/stage56_run50AG_s25_quality_oos_density_repair_v1/aggregate_summary.json`
- attribution_report(귀속 보고서): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50AG_s24l15a_market_weather_attribution.md`
- selected_research_baseline(선택 연구 기준선): `none`
- current_judgment(현재 판정): `in_progress_no_selected_research_baseline`

Run50AG(실행50AG)는 run50AF(실행50AF)의 `s25c8a` quality branch(품질 가지)에서 short/long threshold(매도/매수 임계값)를 0.240/0.150, 0.220/0.140, 0.200/0.130까지 낮추고 cooldown(쿨다운) 6/8봉을 실제 MT5 validation/OOS(메타트레이더5 검증/표본외)로 시험했다. 효과(effect, 효과): OOS density(표본외 밀도)가 단순 임계값 완화로 더 열리는지 확인했다.

- closest intermediate variant(가장 가까운 중간 변형): `s24l15a`
- A+B actual routed total(A+B 실제 라우팅 전체) validation(검증): 5.349727 trades/day(일 거래 수), net(순손익) 466.64, PF(수익 팩터) 1.19, max DD(최대 손실) 255.14
- A+B actual routed total(A+B 실제 라우팅 전체) OOS(표본외): 3.646154 trades/day(일 거래 수), net(순손익) 417.57, PF(수익 팩터) 1.23, max DD(최대 손실) 159.26
- Tier A only(Tier A 단독) OOS(표본외): net(순손익) 417.57, PF(수익 팩터) 1.23
- Tier B fallback-only OOS(Tier B 대체 전용 표본외): net(순손익) -10.43, PF(수익 팩터) 0.69로 damaging(손상)했다.
- MFE capture read(MFE 포착 판독): OOS MFE capture ratio(표본외 MFE 포착 비율)는 0.588858로 d390h10 reference(d390h10 참조)보다 낮다.
- same-move read(동일 이동 판독): OOS same-move re-entry ratio(표본외 동일 이동 재진입 비율)는 0.594937이고 12-bar cooldown(12봉 쿨다운) 뒤 OOS density(표본외 밀도)는 1.476923 trades/day(일 거래 수)라 density gain(밀도 증가)이 기준까지 생존하지 못했다.
- attribution read(귀속 판독): run50AG(실행50AG)는 run50AF(실행50AF)의 s25c8a와 같은 거래 판독을 반복했다. validation(검증)은 전 세션/ADX 구간(세션/평균 방향 지수 구간)이 양수지만 OOS(표본외)는 buy vol_low(매수 저변동성) -42.92와 mid session(중반 세션) 약세가 남았다.
- selected_research_baseline(선택 연구 기준선)으로 올리지 않는 이유: OOS density(표본외 밀도) 5.0 미만, validation cost-stressed expectancy(검증 비용 압박 기대값) 음수, same-move density survival(동일 이동 밀도 생존) 실패, Tier B fallback-only OOS(Tier B 대체 전용 표본외) 음수다.
- next_hypothesis_branch(다음 가설 가지): `change_axis_after_s25_threshold_saturation_to_recover_oos_density_without_same_move_split`

## Latest Run50AF Intermediate Evidence(최신 50AF 중간 근거)

- packet(묶음): `stage56_run50AF_short_adx_repair_after_c08b_v1`
- report(보고서): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50AF_reopen_batch.md`
- summary_csv(요약 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50AF_summary.csv`
- audit_csv(감사 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50AF_audit.csv`
- aggregate_summary(합산 요약): `docs/agent_control/packets/stage56_run50AF_short_adx_repair_after_c08b_v1/aggregate_summary.json`
- attribution_report(귀속 보고서): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50AF_s25c8a_market_weather_attribution.md`
- selected_research_baseline(선택 연구 기준선): `none`
- current_judgment(현재 판정): `in_progress_no_selected_research_baseline`

Run50AF(실행50AF)는 `c08b` 이후 validation(검증)을 깎던 sell ADX20-25(매도 평균 방향 지수 20-25)를 차단하고 cooldown(쿨다운) 6/8봉, wider short ADX20-30(더 넓은 매도 평균 방향 지수 20-30), Tier A only/A+B routed comparison(Tier A 단독/A+B 실제 라우팅 비교)을 실제 MT5 validation/OOS(메타트레이더5 검증/표본외)로 시험했다. 효과(effect, 효과): ADX repair(평균 방향 지수 수리)가 품질과 밀도를 같이 회복하는지 확인했다.

- closest intermediate variant(가장 가까운 중간 변형): `s25c8a`
- A+B actual routed total(A+B 실제 라우팅 전체) validation(검증): 5.349727 trades/day(일 거래 수), net(순손익) 466.64, PF(수익 팩터) 1.19, max DD(최대 손실) 255.14
- A+B actual routed total(A+B 실제 라우팅 전체) OOS(표본외): 3.646154 trades/day(일 거래 수), net(순손익) 417.57, PF(수익 팩터) 1.23, max DD(최대 손실) 159.26
- Tier A only(Tier A 단독) OOS(표본외): net(순손익) 417.57, PF(수익 팩터) 1.23
- Tier B fallback-only OOS(Tier B 대체 전용 표본외): net(순손익) -10.43, PF(수익 팩터) 0.69로 damaging(손상)했다.
- MFE capture read(MFE 포착 판독): OOS MFE capture ratio(표본외 MFE 포착 비율)는 0.588858로 d390h10 reference(d390h10 참조)보다 낮다.
- same-move read(동일 이동 판독): OOS same-move re-entry ratio(표본외 동일 이동 재진입 비율)는 0.594937이고 12-bar cooldown(12봉 쿨다운) 뒤 OOS density(표본외 밀도)는 1.476923 trades/day(일 거래 수)라 density gain(밀도 증가)이 기준까지 생존하지 못했다.
- attribution read(귀속 판독): validation(검증)은 모든 session(세션)과 ADX bucket(평균 방향 지수 구간)이 양수로 바뀌었지만 OOS(표본외)는 buy vol_low(매수 저변동성) -42.92와 mid session(중반 세션) 약세가 남았다.
- selected_research_baseline(선택 연구 기준선)으로 올리지 않는 이유: OOS density(표본외 밀도) 5.0 미만, validation cost-stressed expectancy(검증 비용 압박 기대값) 음수, same-move density survival(동일 이동 밀도 생존) 실패, Tier B fallback-only OOS(Tier B 대체 전용 표본외) 음수다.
- next_hypothesis_branch(다음 가설 가지): `recover_oos_density_from_s25c8a_quality_branch_without_same_move_split_and_with_tier_b_disablement`

## Latest Run50AE Intermediate Evidence(최신 50AE 중간 근거)

- packet(묶음): `stage56_run50AE_vl_cooldown_density_v1`
- report(보고서): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50AE_reopen_batch.md`
- summary_csv(요약 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50AE_summary.csv`
- audit_csv(감사 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50AE_audit.csv`
- aggregate_summary(합산 요약): `docs/agent_control/packets/stage56_run50AE_vl_cooldown_density_v1/aggregate_summary.json`
- attribution_report(귀속 보고서): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50AE_c08b_market_weather_attribution.md`
- selected_research_baseline(선택 연구 기준선): `none`
- current_judgment(현재 판정): `in_progress_no_selected_research_baseline`

Run50AE(실행50AE)는 buy vol_low firewall(매수 저변동성 방화벽)을 유지하고 cooldown(쿨다운) 6/8/10봉 및 early_mid session(초반+중반 세션)을 실제 MT5 validation/OOS(메타트레이더5 검증/표본외)로 시험했다. 효과(effect, 효과): run50AD(실행50AD)의 희소성을 풀어도 same-move split(동일 이동 분할) 없이 밀도가 살아나는지 확인했다.

- closest intermediate variant(가장 가까운 중간 변형): `c08b`
- A+B actual routed total(A+B 실제 라우팅 전체) validation(검증): 4.322404 trades/day(일 거래 수), net(순손익) 118.68, PF(수익 팩터) 1.05, max DD(최대 손실) 217.41
- A+B actual routed total(A+B 실제 라우팅 전체) OOS(표본외): 3.153846 trades/day(일 거래 수), net(순손익) 330.59, PF(수익 팩터) 1.19, max DD(최대 손실) 133.17
- Tier A only(Tier A 단독) OOS(표본외): net(순손익) 288.55, PF(수익 팩터) 1.17
- Tier B fallback-only OOS(Tier B 대체 전용 표본외): net(순손익) 4.41, PF(수익 팩터) 1.24지만 validation(검증)은 net(순손익) -495.18, PF(수익 팩터) 0.01로 damaging(손상)했다.
- MFE capture read(MFE 포착 판독): OOS MFE capture ratio(표본외 MFE 포착 비율)는 0.598210으로 d390h10 reference(d390h10 참조)보다 낮지만 OOS PF/net(표본외 수익 팩터/순손익)은 살아 있다.
- same-move read(동일 이동 판독): OOS same-move re-entry ratio(표본외 동일 이동 재진입 비율)는 0.539837이고 12-bar cooldown(12봉 쿨다운) 뒤 OOS density(표본외 밀도)는 1.451282 trades/day(일 거래 수)라 density gain(밀도 증가)이 생존하지 못했다.
- attribution read(귀속 판독): validation(검증)은 late session(후반 세션) -30.59, vol_low(저변동성) -73.66, ADX 20-25(평균 방향 지수 20-25) -87.83이 약했고 OOS(표본외)는 late/early session(후반/초반 세션), vol_low(저변동성), range_or_weak_trend(횡보/약한 추세), ADX below 20(평균 방향 지수 20 미만)이 강했다.
- selected_research_baseline(선택 연구 기준선)으로 올리지 않는 이유: validation/OOS density(검증/표본외 밀도) 5.0 미만, validation PF(검증 수익 팩터) 1.10 미만, validation cost-stressed expectancy(검증 비용 압박 기대값) 음수, same-move density survival(동일 이동 밀도 생존) 실패다.
- next_hypothesis_branch(다음 가설 가지): `validation_adx20_25_or_late_session_damage_repair_after_c08b_without_same_move_split`

## Latest Run50AD Intermediate Evidence(최신 50AD 중간 근거)

- packet(묶음): `stage56_run50AD_c12_rf_path_repair_v1`
- report(보고서): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50AD_reopen_batch.md`
- summary_csv(요약 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50AD_summary.csv`
- audit_csv(감사 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50AD_audit.csv`
- aggregate_summary(합산 요약): `docs/agent_control/packets/stage56_run50AD_c12_rf_path_repair_v1/aggregate_summary.json`
- attribution_report(귀속 보고서): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50AD_lv26b_market_weather_attribution.md`
- selected_research_baseline(선택 연구 기준선): `none`
- current_judgment(현재 판정): `in_progress_no_selected_research_baseline`

Run50AC(실행50AC)는 Windows path length(윈도우 경로 길이) 문제로 blocked(차단)됐고, run50AD(실행50AD)는 같은 hypothesis family(가설군)를 짧은 run id(실행 ID)로 수리해 실제 MT5 validation/OOS(메타트레이더5 검증/표본외)를 완료했다. 효과(effect, 효과): 실패 시도를 환경 중단으로 쓰지 않고, 수리 실행으로 근거를 만들었다.

- closest intermediate variant(가장 가까운 중간 변형): `lv26b`
- A+B actual routed total(A+B 실제 라우팅 전체) validation(검증): 3.836066 trades/day(일 거래 수), net(순손익) 23.40, PF(수익 팩터) 1.01, max DD(최대 손실) 381.69
- A+B actual routed total(A+B 실제 라우팅 전체) OOS(표본외): 2.533333 trades/day(일 거래 수), net(순손익) 312.41, PF(수익 팩터) 1.23, max DD(최대 손실) 118.77
- Tier A only(Tier A 단독) OOS(표본외): net(순손익) 414.56, PF(수익 팩터) 1.31
- Tier B fallback-only OOS(Tier B 대체 전용 표본외): net(순손익) 4.41, PF(수익 팩터) 1.24지만 validation(검증)은 net(순손익) -495.38, PF(수익 팩터) 0.01로 매우 약하다.
- MFE capture read(MFE 포착 판독): OOS MFE capture ratio(표본외 MFE 포착 비율)는 0.613230으로 d390h10 reference(d390h10 참조) 0.628265보다 -0.015034 낮아 materially worse(중대 악화)는 아니다.
- same-move read(동일 이동 판독): OOS same-move re-entry ratio(표본외 동일 이동 재진입 비율)는 0.242915로 낮지만 12-bar cooldown(12봉 쿨다운) 뒤 OOS density(표본외 밀도)는 1.917949 trades/day(일 거래 수)라 density(밀도)가 기준까지 생존하지 못했다.
- attribution read(귀속 판독): buy vol_low firewall(매수 저변동성 방화벽)은 OOS buy damage(표본외 매수 손상)를 고쳤지만 validation early/buy ADX 20-25(검증 초반/매수 평균 방향 지수 20-25)가 약했고 threshold relaxation(임계값 완화)은 같은 결과로 포화됐다.
- selected_research_baseline(선택 연구 기준선)으로 올리지 않는 이유: validation/OOS density(검증/표본외 밀도) 5.0 미만, validation PF(검증 수익 팩터) 1.10 미만, validation cost-stressed expectancy(검증 비용 압박 기대값) 음수, same-move density survival(동일 이동 밀도 생존) 실패다.
- next_hypothesis_branch(다음 가설 가지): `recover_density_after_buy_vol_low_firewall_with_session_or_side_axis_without_same_move_split`

## Latest Run50AB Intermediate Evidence(최신 50AB 중간 근거)

- packet(묶음): `stage56_run50AB_cooldown12_density_repair_v1`
- report(보고서): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50AB_reopen_batch.md`
- summary_csv(요약 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50AB_summary.csv`
- audit_csv(감사 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50AB_audit.csv`
- aggregate_summary(합산 요약): `docs/agent_control/packets/stage56_run50AB_cooldown12_density_repair_v1/aggregate_summary.json`
- attribution_report(귀속 보고서): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50AB_nfab_c12_h08_s300l210_b_market_weather_attribution.md`
- selected_research_baseline(선택 연구 기준선): `none`
- current_judgment(현재 판정): `in_progress_no_selected_research_baseline`

Run50AB(실행50AB)는 actual 12-bar cooldown(실제 12봉 쿨다운), hold10/hold8/hold6(10봉/8봉/6봉 보유), lower threshold(낮은 임계값), matched Tier B comparison(대응 Tier B 비교)을 실제 MT5 validation/OOS(검증/표본외)로 시험했다. 효과(effect, 효과): hold compression(보유 압축)이 profitable move split(수익 이동 분할)인지 직접 감사했다.

- closest intermediate variant(가장 가까운 중간 변형): `nfab_c12_h08_s300l210_b`
- A+B actual routed total(A+B 실제 라우팅 전체) validation(검증): 5.054645 trades/day(일 거래 수), net(순손익) 71.06, PF(수익 팩터) 1.03, max DD(최대 손실) 479.71
- A+B actual routed total(A+B 실제 라우팅 전체) OOS(표본외): 3.430769 trades/day(일 거래 수), net(순손익) 139.42, PF(수익 팩터) 1.08, max DD(최대 손실) 182.98
- Tier A only(Tier A 단독) OOS(표본외): net(순손익) 50.74, PF(수익 팩터) 1.03
- Tier B fallback-only OOS(Tier B 대체 전용 표본외): net(순손익) -11.43, PF(수익 팩터) 0.67로 negative(음수)다.
- MFE capture read(MFE 포착 판독): OOS MFE capture ratio(표본외 MFE 포착 비율)는 0.581873이고 d390h10 reference(d390h10 참조)보다 -0.046392 낮다.
- same-move read(동일 이동 판독): OOS same-move re-entry ratio(표본외 동일 이동 재진입 비율)는 0.325859이고 12-bar cooldown(12봉 쿨다운) 뒤 OOS density(표본외 밀도)는 2.312821 trades/day(일 거래 수)다.
- attribution read(귀속 판독): validation early session(검증 초반 세션) -76.69, validation vol_low(검증 저변동성) -50.35, validation ADX 20-25(검증 평균 방향 지수 20-25) -40.64가 약했다. OOS(표본외)는 mid session(중반 세션) -30.73, downtrend(하락 추세) -55.33, ADX 20-25(평균 방향 지수 20-25) -22.81, ADX >25(평균 방향 지수 25 초과) -32.52가 약했다.
- selected_research_baseline(선택 연구 기준선)으로 올리지 않는 이유: OOS density(표본외 밀도) 5.0 미만, validation/OOS PF(검증/표본외 수익 팩터) 1.10 미만, cost-stressed expectancy(비용 압박 기대값) 음수, same-move density audit(동일 이동 밀도 감사) 실패, Tier B fallback-only OOS(Tier B 대체 전용 표본외) 음수다.
- next_hypothesis_branch(다음 가설 가지): `cooldown12_regime_firewall_or_side_specific_adx_trend_repair_without_same_move_split`

## Latest Run50AA Intermediate Evidence(최신 50AA 중간 근거)

- packet(묶음): `stage56_run50AA_same_move_cost_repair_v1`
- report(보고서): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50AA_reopen_batch.md`
- summary_csv(요약 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50AA_summary.csv`
- audit_csv(감사 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50AA_audit.csv`
- aggregate_summary(합산 요약): `docs/agent_control/packets/stage56_run50AA_same_move_cost_repair_v1/aggregate_summary.json`
- attribution_report(귀속 보고서): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50AA_nfaa_s23l13_c6_l30_b_market_weather_attribution.md`
- selected_research_baseline(선택 연구 기준선): `none`
- current_judgment(현재 판정): `in_progress_no_selected_research_baseline`

Run50AA(실행50AA)는 cooldown6(6봉 쿨다운), buy ADX below 30/35(매수 평균 방향 지수 30/35 미만 허용), 낮은 threshold(임계값), matched Tier B comparison(대응 Tier B 비교)을 실제 MT5 validation/OOS(검증/표본외)로 시험했다. 효과(effect, 효과): run50Z(실행50Z)의 cost-positive branch(비용 양수 가지)에서 밀도 회복이 가능한지 확인했다.

- closest intermediate variant(가장 가까운 중간 변형): `nfaa_s23l13_c6_l30_b`
- A+B actual routed total(A+B 실제 라우팅 전체) validation(검증): 4.464481 trades/day(일 거래 수), net(순손익) 288.34, PF(수익 팩터) 1.14, max DD(최대 손실) 171.39
- A+B actual routed total(A+B 실제 라우팅 전체) OOS(표본외): 3.020513 trades/day(일 거래 수), net(순손익) 308.82, PF(수익 팩터) 1.21, max DD(최대 손실) 168.45
- Tier A only(Tier A 단독) OOS(표본외): net(순손익) 305.18, PF(수익 팩터) 1.20
- Tier B fallback-only OOS(Tier B 대체 전용 표본외): net(순손익) -10.26, PF(수익 팩터) 0.66으로 negative(음수)다.
- same-move read(동일 이동 판독): OOS same-move re-entry ratio(표본외 동일 이동 재진입 비율)는 0.504244이고 12-bar cooldown(12봉 쿨다운) 뒤 OOS density(표본외 밀도)는 1.497436 trades/day(일 거래 수)다.
- attribution read(귀속 판독): validation early session(검증 초반 세션), validation vol_mid(검증 중간 변동성), validation ADX 20-25(검증 평균 방향 지수 20-25)가 약했고, OOS(표본외)는 mid session(중반 세션), vol_low(저변동성), ADX 20-25(평균 방향 지수 20-25)만 작게 약했다.
- selected_research_baseline(선택 연구 기준선)으로 올리지 않는 이유: validation/OOS density(검증/표본외 밀도) 5.0 미만, same-move density audit(동일 이동 밀도 감사) 실패, Tier B fallback-only OOS(Tier B 대체 전용 표본외) 음수다.

## Latest Run50Z Intermediate Evidence(최신 50Z 중간 근거)

- packet(묶음): `stage56_run50Z_partial_buy_adx_reintro_v1`
- report(보고서): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50Z_reopen_batch.md`
- summary_csv(요약 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50Z_summary.csv`
- audit_csv(감사 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50Z_audit.csv`
- aggregate_summary(합산 요약): `docs/agent_control/packets/stage56_run50Z_partial_buy_adx_reintro_v1/aggregate_summary.json`
- selected_research_baseline(선택 연구 기준선): `none`
- current_judgment(현재 판정): `in_progress_no_selected_research_baseline`

Run50Z(실행50Z)는 partial buy ADX reintroduction(부분 매수 평균 방향 지수 재도입)과 matched Tier B comparison(대응 Tier B 비교)을 실제 MT5 validation/OOS(검증/표본외)로 시험했다. 효과(effect, 효과): run50Y(실행50Y)의 품질 회복과 run50X(실행50X)의 밀도 회복 사이의 tradeoff(상충)를 더 좁게 확인했다.

- closest intermediate variant(가장 가까운 중간 변형): `nfz_s31l18_c3_s2030_b`
- A+B actual routed total(A+B 실제 라우팅 전체) validation(검증): 7.196721 trades/day(일 거래 수), net(순손익) 451.99, PF(수익 팩터) 1.15, max DD(최대 손실) 249.56
- A+B actual routed total(A+B 실제 라우팅 전체) OOS(표본외): 5.056410 trades/day(일 거래 수), net(순손익) 251.32, PF(수익 팩터) 1.10, max DD(최대 손실) 142.59
- Tier A only(Tier A 단독) OOS(표본외): net(순손익) 201.81, PF(수익 팩터) 1.08
- Tier B fallback-only OOS(Tier B 대체 전용 표본외): net(순손익) -2.52, PF(수익 팩터) 0.91로 negative(음수)다.
- same-move read(동일 이동 판독): OOS same-move re-entry ratio(표본외 동일 이동 재진입 비율)는 0.748479이고 12-bar cooldown(12봉 쿨다운) 뒤 OOS density(표본외 밀도)는 1.271795 trades/day(일 거래 수)다.
- branch read(가지 판독): partial buy ADX block(부분 매수 평균 방향 지수 차단)은 same-move ratio(동일 이동 비율)를 줄였지만 OOS density(표본외 밀도)가 5 미만이었다. cooldown6(6봉 쿨다운) 변형은 OOS cost-stressed expectancy(표본외 비용 압박 기대값)를 양수로 만들었지만 밀도는 2.979487에 그쳤다.
- selected_research_baseline(선택 연구 기준선)으로 올리지 않는 이유: cost-stressed expectancy(비용 압박 기대값) 음수 또는 density(밀도) 부족, same-move density audit(동일 이동 밀도 감사) 실패, Tier B fallback-only OOS(Tier B 대체 전용 표본외) 음수다.

## Latest Run50Y Intermediate Evidence(최신 50Y 중간 근거)

- packet(묶음): `stage56_run50Y_buy_side_firewall_tierb_v1`
- report(보고서): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50Y_reopen_batch.md`
- summary_csv(요약 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50Y_summary.csv`
- audit_csv(감사 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50Y_audit.csv`
- aggregate_summary(합산 요약): `docs/agent_control/packets/stage56_run50Y_buy_side_firewall_tierb_v1/aggregate_summary.json`
- attribution_report(귀속 보고서): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50Y_nfy_s31l18_c3_adx_b_market_weather_attribution.md`
- selected_research_baseline(선택 연구 기준선): `none`
- current_judgment(현재 판정): `in_progress_no_selected_research_baseline`

Run50Y(실행50Y)는 buy ADX 20+(매수 평균 방향 지수 20 이상) firewall(방화벽), buy vol_low(매수 저변동성) firewall(방화벽), Tier B disabled/A+B routed comparison(Tier B 비활성화/A+B 실제 라우팅 비교)을 실제 MT5 validation/OOS(검증/표본외)로 시험했다. 효과(effect, 효과): run50X(실행50X)의 손상 원인을 buy-side(매수 방향), Tier B(티어 B), same-move split(동일 이동 분할)로 분리했다.

- closest intermediate variant(가장 가까운 중간 변형): `nfy_s31l18_c3_adx_b`
- A+B actual routed total(A+B 실제 라우팅 전체) validation(검증): 3.868852 trades/day(일 거래 수), net(순손익) 166.36, PF(수익 팩터) 1.09, max DD(최대 손실) 159.92
- A+B actual routed total(A+B 실제 라우팅 전체) OOS(표본외): 2.625641 trades/day(일 거래 수), net(순손익) 378.86, PF(수익 팩터) 1.29, max DD(최대 손실) 137.04
- Tier A only(Tier A 단독) OOS(표본외): net(순손익) 420.75, PF(수익 팩터) 1.33
- Tier B fallback-only OOS(Tier B 대체 전용 표본외): net(순손익) -6.61, PF(수익 팩터) 0.59로 negative(음수)다.
- MFE capture read(MFE 포착 판독): OOS MFE capture ratio(표본외 MFE 포착 비율)는 0.628193으로 run50X(실행50X)보다 높다.
- same-move read(동일 이동 판독): OOS same-move re-entry ratio(표본외 동일 이동 재진입 비율)는 0.474609로 낮아졌지만 12-bar cooldown(12봉 쿨다운) 뒤 OOS density(표본외 밀도)는 1.379487 trades/day(일 거래 수)다.
- attribution read(귀속 판독): strict buy ADX 20+ block(강한 매수 평균 방향 지수 20 이상 차단) 뒤 OOS(표본외)는 모든 session(세션)이 양수였지만 validation early session(검증 초반 세션)은 -133.52로 약했다. 효과(effect, 효과): 다음 가지는 일부 buy ADX(매수 평균 방향 지수) 기회를 되살려 밀도를 회복해야 한다.
- selected_research_baseline(선택 연구 기준선)으로 올리지 않는 이유: validation/OOS density(검증/표본외 밀도) 5.0 미만, validation PF(검증 수익 팩터) 1.10 미만, same-move density audit(동일 이동 밀도 감사) 실패, Tier B fallback-only OOS(Tier B 대체 전용 표본외) 음수다.

## Latest Run50X Intermediate Evidence(최신 50X 중간 근거)

- packet(묶음): `stage56_run50X_nonflat_adx_soft_firewall_v1`
- report(보고서): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50X_reopen_batch.md`
- summary_csv(요약 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50X_summary.csv`
- audit_csv(감사 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50X_audit.csv`
- aggregate_summary(합산 요약): `docs/agent_control/packets/stage56_run50X_nonflat_adx_soft_firewall_v1/aggregate_summary.json`
- attribution_report(귀속 보고서): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50X_nfx_s33l20_c3_s2030_market_weather_attribution.md`
- selected_research_baseline(선택 연구 기준선): `none`
- current_judgment(현재 판정): `in_progress_no_selected_research_baseline`

Run50X(실행50X)는 wider short ADX 20-30 firewall(더 넓은 숏 평균 방향 지수 20-30 방화벽), soft long ADX block(완만한 롱 평균 방향 지수 차단), 2~3 bar cooldown(2~3봉 쿨다운)을 실제 MT5 validation/OOS(검증/표본외)로 시험했다. 효과(effect, 효과): run50W(실행50W)보다 OOS PF(표본외 수익 팩터)를 기준에 더 가깝게 끌어올렸는지 확인했다.

- closest intermediate variant(가장 가까운 중간 변형): `nfx_s33l20_c3_s2030`
- A+B actual routed total(A+B 실제 라우팅 전체) validation(검증): 7.196721 trades/day(일 거래 수), net(순손익) 451.99, PF(수익 팩터) 1.15, max DD(최대 손실) 249.56
- A+B actual routed total(A+B 실제 라우팅 전체) OOS(표본외): 5.056410 trades/day(일 거래 수), net(순손익) 251.32, PF(수익 팩터) 1.10, max DD(최대 손실) 142.59
- Tier A only(Tier A 단독) OOS(표본외): net(순손익) 201.81, PF(수익 팩터) 1.08
- Tier B fallback-only OOS(Tier B 대체 전용 표본외): net(순손익) -2.52, PF(수익 팩터) 0.91로 negative(음수)다.
- MFE capture read(MFE 포착 판독): OOS MFE capture ratio(표본외 MFE 포착 비율)는 0.605995다.
- same-move read(동일 이동 판독): OOS same-move re-entry ratio(표본외 동일 이동 재진입 비율)는 0.748479이고, 12-bar cooldown(12봉 쿨다운) 뒤 OOS density(표본외 밀도)는 1.271795 trades/day(일 거래 수)다. 효과(effect, 효과): 5+ trades/day(일 거래 수) 밀도는 아직 cooldown(쿨다운) 뒤 생존하지 않는다.
- attribution read(귀속 판독): OOS buy vol_low(표본외 매수 저변동성) -285.35, buy ADX 20-25(매수 평균 방향 지수 20-25) -111.11, buy ADX >25(매수 평균 방향 지수 25 초과) -116.97이 약했고, sell ADX >25(매도 평균 방향 지수 25 초과)는 +281.21로 강했다. 효과(effect, 효과): 다음 후보는 buy-side(매수 방향) 저변동성/ADX 손상을 막되 sell-side(매도 방향) 고ADX 이익은 보존해야 한다.
- selected_research_baseline(선택 연구 기준선)으로 올리지 않는 이유: cost-stressed expectancy(비용 압박 기대값) 음수, same-move audit(동일 이동 감사) 실패, Tier B fallback-only OOS(Tier B 대체 전용 표본외) 음수다.

## Latest Run50W Intermediate Evidence(최신 50W 중간 근거)

- packet(묶음): `stage56_run50W_nonflat_regime_firewall_v1`
- report(보고서): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50W_reopen_batch.md`
- summary_csv(요약 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50W_summary.csv`
- audit_csv(감사 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50W_audit.csv`
- aggregate_summary(합산 요약): `docs/agent_control/packets/stage56_run50W_nonflat_regime_firewall_v1/aggregate_summary.json`
- attribution_report(귀속 보고서): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50W_nfw_s35l22_c2_sadx_market_weather_attribution.md`
- selected_research_baseline(선택 연구 기준선): `none`
- current_judgment(현재 판정): `in_progress_no_selected_research_baseline`

Run50W(실행50W)는 run50V(실행50V)의 core/mixed Tier B gate(핵심/혼합 Tier B 선별)를 유지하고, short ADX 20-25 firewall(숏 평균 방향 지수 20-25 방화벽), 일부 long ADX >25 firewall(롱 평균 방향 지수 25 초과 방화벽), 1~3 bar reentry cooldown(1~3봉 재진입 쿨다운)을 실제 MT5 validation/OOS(검증/표본외)로 시험했다. 효과(effect, 효과): validation PF(검증 수익 팩터)를 살리면서 density(밀도)가 유지되는지, 그리고 same-move split(동일 이동 분할)이 줄어드는지 확인했다.

- closest intermediate variant(가장 가까운 중간 변형): `nfw_s35l22_c2_sadx`
- A+B actual routed total(A+B 실제 라우팅 전체) validation(검증): 8.185792 trades/day(일 거래 수), net(순손익) 600.73, PF(수익 팩터) 1.18, max DD(최대 손실) 214.55
- A+B actual routed total(A+B 실제 라우팅 전체) OOS(표본외): 5.830769 trades/day(일 거래 수), net(순손익) 139.96, PF(수익 팩터) 1.05, max DD(최대 손실) 267.00
- Tier A only(Tier A 단독) OOS(표본외): net(순손익) 167.59, PF(수익 팩터) 1.06
- Tier B fallback-only OOS(Tier B 대체 전용 표본외): net(순손익) 1.21, PF(수익 팩터) 1.05로 non-negative(비음수)다.
- MFE capture read(MFE 포착 판독): best OOS MFE capture ratio(최선 표본외 MFE 포착 비율)는 0.594122로 d390h10 reference(d390h10 참조)보다 낮다.
- same-move read(동일 이동 판독): best OOS same-move re-entry ratio(최선 표본외 동일 이동 재진입 비율)는 0.780123이고 12-bar cooldown(12봉 쿨다운) 뒤 OOS density(표본외 밀도)는 1.282051 trades/day(일 거래 수)로 떨어진다. 효과(effect, 효과): density gain(밀도 증가)은 아직 same-move split trading(동일 이동 분할 거래)에 크게 기대고 있다.
- attribution read(귀속 판독): validation(검증)은 long/buy ADX >25(롱/매수 평균 방향 지수 25 초과)가 강했지만 OOS(표본외)는 buy downtrend(매수 하락 추세), buy ADX >25(매수 평균 방향 지수 25 초과), buy vol_low(매수 저변동성)가 약했다. 효과(effect, 효과): 다음 가지는 hard long ADX >25 block(강한 롱 평균 방향 지수 25 초과 차단)보다 softer long-high-ADX firewall(완만한 롱 고ADX 방화벽)이나 buy-side OOS damage filter(매수 방향 표본외 손상 필터)를 시험한다.
- selected_research_baseline(선택 연구 기준선)으로 올리지 않는 이유: OOS PF(표본외 수익 팩터) 1.10 미만, cost-stressed expectancy(비용 압박 기대값) 음수, same-move audit(동일 이동 감사) 실패다.

## Latest Run50V Intermediate Evidence(최신 50V 중간 근거)

- packet(묶음): `stage56_run50V_nonflat_vol_low_hold6_tierb_gate_repair_v1`
- report(보고서): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50V_reopen_batch.md`
- summary_csv(요약 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50V_summary.csv`
- audit_csv(감사 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50V_audit.csv`
- aggregate_summary(합산 요약): `docs/agent_control/packets/stage56_run50V_nonflat_vol_low_hold6_tierb_gate_repair_v1/aggregate_summary.json`
- attribution_report(귀속 보고서): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50V_nfv_h6_s37l24_bcm_market_weather_attribution.md`
- selected_research_baseline(선택 연구 기준선): `none`
- current_judgment(현재 판정): `in_progress_no_selected_research_baseline`

Run50V(실행50V)는 run50U(실행50U)의 gated Tier B(Tier B 선별) long-path failure(긴 경로 실패)를 짧은 variant_id(변형 ID)로 수리하고, core/mixed/macro Tier B subtype gate(핵심/혼합/거시 Tier B 하위 유형 선별)를 실제 MT5 validation/OOS(검증/표본외)로 시험했다. 효과(effect, 효과): Tier B fallback-only OOS(Tier B 대체 전용 표본외)가 양수로 바뀌는지 확인했다.

- best intermediate variant(최선 중간 변형): `nfv_h6_s37l24_bcm`
- A+B actual routed total(A+B 실제 라우팅 전체) validation(검증): 7.054645 trades/day(일 거래 수), net(순손익) 153.96, PF(수익 팩터) 1.04, max DD(최대 손실) 256.52
- A+B actual routed total(A+B 실제 라우팅 전체) OOS(표본외): 5.297436 trades/day(일 거래 수), net(순손익) 107.69, PF(수익 팩터) 1.04, max DD(최대 손실) 267.28
- Tier A only(Tier A 단독) OOS(표본외): net(순손익) 92.04, PF(수익 팩터) 1.03
- Tier B fallback-only OOS(Tier B 대체 전용 표본외): net(순손익) 10.05, PF(수익 팩터) 1.74로 non-negative(비음수)다.
- MFE capture read(MFE 포착 판독): best OOS MFE capture ratio(최선 표본외 MFE 포착 비율)는 0.589626으로 낮아졌고, 품질 개선 없이 density(밀도)만 유지한 상태다.
- same-move read(동일 이동 판독): best OOS same-move re-entry ratio(최선 표본외 동일 이동 재진입 비율)는 0.769603이고 12-bar re-entry count(12봉 재진입 수)는 795이다. 효과(effect, 효과): density gain(밀도 증가)은 여전히 same-move split trading(동일 이동 분할 거래)에 주로 기대며, 12-bar cooldown(12봉 쿨다운) 뒤 OOS density(표본외 밀도)는 1.220513 trades/day(일 거래 수)로 떨어진다.
- attribution read(귀속 판독): validation(검증)은 ADX 20-25(평균 방향 지수 20-25), mid session(중반 세션), vol_mid(중간 변동성)가 약했고 OOS(표본외)는 downtrend(하락 추세), adx_gt25(평균 방향 지수 25 초과), mid session(중반 세션)이 약했다. 효과(effect, 효과): 다음 가지는 단일 필터보다 regime-inversion repair(국면 반전 수리)와 same-move firewall(동일 이동 방화벽) 조합으로 잡는다.
- selected_research_baseline(선택 연구 기준선)으로 올리지 않는 이유: validation/OOS PF(검증/표본외 수익 팩터) 1.10 미만, cost-stressed expectancy(비용 압박 기대값) 음수, same-move audit(동일 이동 감사) 실패다.

## Latest Run50U Intermediate Evidence(최신 50U 중간 근거)

- packet(묶음): `stage56_run50U_nonflat_vol_low_hold6_short_filter_v1`
- report(보고서): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50U_reopen_batch.md`
- summary_csv(요약 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50U_summary.csv`
- audit_csv(감사 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50U_audit.csv`
- failed_attempt_repair_note(실패 시도 수리 기록): `docs/agent_control/packets/stage56_run50U_nonflat_vol_low_hold6_short_filter_v1/failed_attempt_long_path_repair.json`
- selected_research_baseline(선택 연구 기준선): `none`
- current_judgment(현재 판정): `in_progress_no_selected_research_baseline`

Run50U(실행50U)는 hold6(6봉 보유), vol_low block(저변동성 차단), short threshold filter(숏 임계값 필터)를 실제 MT5 validation/OOS(검증/표본외)로 시험했다. 효과(effect, 효과): sell-side damage(매도 방향 손상)를 줄이면 PF(수익 팩터)가 기준까지 살아나는지 확인했다. best intermediate variant(최선 중간 변형) `nf_vollow_h06_s370l240_b`는 validation/OOS(검증/표본외) 7.278689/5.456410 trades/day(일 거래 수), PF(수익 팩터) 1.04/1.05, net(순손익) 155.07/151.12였지만, cost stress(비용 압박), same-move audit(동일 이동 감사), Tier B fallback-only OOS(Tier B 대체 전용 표본외) 음수로 selected_research_baseline(선택 연구 기준선)이 아니다. 마지막 gated Tier B(Tier B 선별) 변형은 long-path failure(긴 경로 실패)로 차단됐고 run50V(실행50V)에서 수리 재실행했다.

## Latest Run50T Intermediate Evidence(최신 50T 중간 근거)

- packet(묶음): `stage56_run50T_nonflat_vol_low_hold_compression_v1`
- report(보고서): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50T_reopen_batch.md`
- summary_csv(요약 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50T_summary.csv`
- audit_csv(감사 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50T_audit.csv`
- aggregate_summary(합산 요약): `docs/agent_control/packets/stage56_run50T_nonflat_vol_low_hold_compression_v1/aggregate_summary.json`
- selected_research_baseline(선택 연구 기준선): `none`
- current_judgment(현재 판정): `in_progress_no_selected_research_baseline`

Run50T(실행50T)는 run50S(실행50S)의 vol_low block(저변동성 차단)에 hold8/hold6 compression(8봉/6봉 보유 압축)을 붙여 실제 MT5 validation/OOS(검증/표본외)로 시험했다. 효과(effect, 효과): shorter hold(짧은 보유)가 density(밀도)를 회복하는지, 아니면 same-move split trading(동일 이동 분할 거래)을 늘리는지 확인했다.

- best intermediate variant(최선 중간 변형): `nf_vollow_h06_s350l240_b`
- A+B actual routed total(A+B 실제 라우팅 전체) validation(검증): 7.311475 trades/day(일 거래 수), net(순손익) 116.61, PF(수익 팩터) 1.03, max DD(최대 손실) 256.52
- A+B actual routed total(A+B 실제 라우팅 전체) OOS(표본외): 5.471795 trades/day(일 거래 수), net(순손익) 146.50, PF(수익 팩터) 1.05, max DD(최대 손실) 260.72
- Tier A only(Tier A 단독) OOS(표본외): net(순손익) 87.01, PF(수익 팩터) 1.03
- Tier B fallback-only OOS(Tier B 대체 전용 표본외): net(순손익) -49.91, PF(수익 팩터) 0.79로 damaging(손상)했다.
- MFE capture read(MFE 포착 판독): best OOS MFE capture ratio(최선 표본외 MFE 포착 비율)는 0.599617로 d390h10 reference(d390h10 참조)보다 낮지만, current gate(현재 게이트)의 주요 실패 원인은 density(밀도)가 아니라 PF(수익 팩터), cost stress(비용 압박), same-move split(동일 이동 분할), Tier B rule(Tier B 규칙)이다.
- same-move read(동일 이동 판독): best OOS same-move re-entry ratio(최선 표본외 동일 이동 재진입 비율)는 0.778819이고 12-bar re-entry count(12봉 재진입 수)는 831이다. 효과(effect, 효과): hold6(6봉 보유)의 density gain(밀도 증가)은 same-move split trading(동일 이동 분할 거래)에 주로 기대며, 12-bar cooldown(12봉 쿨다운) 뒤 density(밀도)가 생존하지 않는다.
- selected_research_baseline(선택 연구 기준선)으로 올리지 않는 이유: validation/OOS PF(검증/표본외 수익 팩터) 1.10 미만, cost-stressed expectancy(비용 압박 기대값) 음수, same-move audit(동일 이동 감사) 실패, Tier B fallback-only OOS(Tier B 대체 전용 표본외) 음수다.

## Latest Run50S Intermediate Evidence(최신 50S 중간 근거)

- packet(묶음): `stage56_run50S_nonflat_vol_low_block_v1`
- report(보고서): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50S_reopen_batch.md`
- summary_csv(요약 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50S_summary.csv`
- audit_csv(감사 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50S_audit.csv`
- aggregate_summary(합산 요약): `docs/agent_control/packets/stage56_run50S_nonflat_vol_low_block_v1/aggregate_summary.json`
- writer_repair_note(쓰기 복구 기록): `docs/agent_control/packets/stage56_run50S_nonflat_vol_low_block_v1/writer_repair_note.json`
- selected_research_baseline(선택 연구 기준선): `none`
- current_judgment(현재 판정): `in_progress_no_selected_research_baseline`

Run50S(실행50S)는 run50R(실행50R) market/weather attribution(시장 상태 귀속)에서 vol_low(저변동성)가 OOS(표본외)를 크게 깎는 단서를 바탕으로, historical_vol_20(20봉 역사 변동성) feature index(피처 인덱스) 32의 vol_low(저변동성) 구간을 차단하고 threshold relaxation(임계값 완화)을 실제 MT5 validation/OOS(검증/표본외)로 시험했다. 효과(effect, 효과): 낮은 변동성 손상을 제거해 Tier B(티어 B) 손상과 PF(수익 팩터)가 회복되는지 확인했다.

- best intermediate variant(최선 중간 변형): `nf_vollow_c0_s350l240_b`
- A+B actual routed total(A+B 실제 라우팅 전체) validation(검증): 5.748634 trades/day(일 거래 수), net(순손익) 24.39, PF(수익 팩터) 1.01, max DD(최대 손실) 314.45
- A+B actual routed total(A+B 실제 라우팅 전체) OOS(표본외): 4.200000 trades/day(일 거래 수), net(순손익) 187.83, PF(수익 팩터) 1.07, max DD(최대 손실) 223.35
- Tier A only(Tier A 단독) OOS(표본외): net(순손익) 51.22, PF(수익 팩터) 1.02
- Tier B fallback-only OOS(Tier B 대체 전용 표본외): net(순손익) 43.40, PF(수익 팩터) 1.20으로 non-negative(비음수)다.
- MFE capture read(MFE 포착 판독): best OOS MFE capture ratio(최선 표본외 MFE 포착 비율)는 0.619438로 d390h10 reference(d390h10 참조)보다 materially worse(중대 악화)는 아니다.
- same-move read(동일 이동 판독): best OOS same-move re-entry ratio(최선 표본외 동일 이동 재진입 비율)는 0.715507이고 12-bar re-entry count(12봉 재진입 수)는 586이다. 효과(effect, 효과): vol_low block(저변동성 차단)은 Tier B(티어 B)를 안정화했지만 density gain(밀도 증가)은 여전히 same-move split trading(동일 이동 분할 거래)에 기대고, 12-bar cooldown(12봉 쿨다운) 뒤 OOS density(표본외 밀도)는 1.194872 trades/day(일 거래 수)로 떨어진다.
- selected_research_baseline(선택 연구 기준선)으로 올리지 않는 이유: OOS density(표본외 밀도) 5.0 미만, validation/OOS PF(검증/표본외 수익 팩터) 1.10 미만, cost-stressed expectancy(비용 압박 기대값) 음수, same-move audit(동일 이동 감사) 실패다.

## Latest Run50R Intermediate Evidence(최신 50R 중간 근거)

- packet(묶음): `stage56_run50R_nonflat_adx_band_block_v1`
- report(보고서): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50R_reopen_batch.md`
- summary_csv(요약 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50R_summary.csv`
- audit_csv(감사 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50R_audit.csv`
- aggregate_summary(합산 요약): `docs/agent_control/packets/stage56_run50R_nonflat_adx_band_block_v1/aggregate_summary.json`
- writer_repair_note(쓰기 복구 기록): `docs/agent_control/packets/stage56_run50R_nonflat_adx_band_block_v1/writer_repair_note.json`
- selected_research_baseline(선택 연구 기준선): `none`
- current_judgment(현재 판정): `in_progress_no_selected_research_baseline`

Run50R(실행50R)은 run50Q(실행50Q) attribution(귀속)에서 ADX 20~25(ADX 20~25 구간)가 validation/OOS(검증/표본외)를 흔드는 단서를 바탕으로, both-side ADX band block(양방향 ADX 구간 차단)을 실제 MT5 validation/OOS(검증/표본외)로 시험했다. 효과(effect, 효과): 밀도(density, 밀도)가 5+ trades/day(일 거래 수)에 닿는지 확인하면서 ADX band(ADX 구간) 차단이 PF(수익 팩터)와 same-move split(동일 이동 분할)을 개선하는지 봤다.

- best intermediate variant(최선 중간 변형): `nf_adxblk_c0_s380l270_b`
- A+B actual routed total(A+B 실제 라우팅 전체) validation(검증): 7.655738 trades/day(일 거래 수), net(순손익) 1.24, PF(수익 팩터) 1.00, max DD(최대 손실) 281.89
- A+B actual routed total(A+B 실제 라우팅 전체) OOS(표본외): 5.164103 trades/day(일 거래 수), net(순손익) 67.89, PF(수익 팩터) 1.02, max DD(최대 손실) 319.83
- Tier A only(Tier A 단독) OOS(표본외): net(순손익) 38.74, PF(수익 팩터) 1.01
- Tier B fallback-only OOS(Tier B 대체 전용 표본외): net(순손익) -28.31, PF(수익 팩터) 0.90으로 damaging(손상)했다.
- MFE capture read(MFE 포착 판독): best OOS MFE capture ratio(최선 표본외 MFE 포착 비율)는 0.606297로 d390h10 reference(d390h10 참조)보다 낮지만 materially worse(중대 악화)로만 볼 정도는 아니다.
- same-move read(동일 이동 판독): best OOS same-move re-entry ratio(최선 표본외 동일 이동 재진입 비율)는 0.756703이고 12-bar re-entry count(12봉 재진입 수)는 762다. 효과(effect, 효과): density gain(밀도 증가)은 여전히 same-move split trading(동일 이동 분할 거래)에 크게 기대고, 12-bar cooldown(12봉 쿨다운) 뒤 OOS density(표본외 밀도)는 1.256410 trades/day(일 거래 수)로 떨어진다.
- selected_research_baseline(선택 연구 기준선)으로 올리지 않는 이유: validation/OOS PF(검증/표본외 수익 팩터) 1.10 미만, cost-stressed expectancy(비용 압박 기대값) 음수, same-move audit(동일 이동 감사) 실패, Tier B fallback-only OOS(Tier B 대체 전용 표본외) 음수다.

## Latest Run50Q Intermediate Evidence(최신 50Q 중간 근거)

- packet(묶음): `stage56_run50Q_nonflat_side_adx_cooldown_interp_v1`
- report(보고서): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50Q_reopen_batch.md`
- summary_csv(요약 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50Q_summary.csv`
- audit_csv(감사 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50Q_audit.csv`
- aggregate_summary(합산 요약): `docs/agent_control/packets/stage56_run50Q_nonflat_side_adx_cooldown_interp_v1/aggregate_summary.json`
- writer_repair_note(쓰기 복구 기록): `docs/agent_control/packets/stage56_run50Q_nonflat_side_adx_cooldown_interp_v1/writer_repair_note.json`
- selected_research_baseline(선택 연구 기준선): `none`
- current_judgment(현재 판정): `in_progress_no_selected_research_baseline`

Run50Q(실행50Q)는 run50P(실행50P)의 0봉/2봉 cooldown(쿨다운) 사이를 1봉 cooldown(쿨다운)으로 보간했다. 효과(effect, 효과): density(밀도)를 유지하면서 same-move split(동일 이동 분할)과 품질 손상을 줄일 수 있는지 확인했다.

- best intermediate variant(최선 중간 변형): `nf_h10c1_s390l280_b_sadx`
- A+B actual routed total(A+B 실제 라우팅 전체) validation(검증): 7.530055 trades/day(일 거래 수), net(순손익) -8.43, PF(수익 팩터) 1.00, max DD(최대 손실) 288.32
- A+B actual routed total(A+B 실제 라우팅 전체) OOS(표본외): 5.102564 trades/day(일 거래 수), net(순손익) 99.37, PF(수익 팩터) 1.03, max DD(최대 손실) 278.00
- Tier A only(Tier A 단독) OOS(표본외): net(순손익) -4.22, PF(수익 팩터) 1.00
- Tier B fallback-only OOS(Tier B 대체 전용 표본외): net(순손익) -36.33, PF(수익 팩터) 0.88로 damaging(손상)했다.
- MFE capture read(MFE 포착 판독): best OOS MFE capture ratio(최선 표본외 MFE 포착 비율)는 0.607672로 d390h10 reference(d390h10 참조)보다 낮지만 materially worse(중대 악화)로만 볼 정도는 아니다.
- same-move read(동일 이동 판독): best OOS same-move re-entry ratio(최선 표본외 동일 이동 재진입 비율)는 0.767839이고 12-bar re-entry count(12봉 재진입 수)는 764다. 효과(effect, 효과): density gain(밀도 증가)은 아직 same-move split trading(동일 이동 분할 거래)에 크게 기대고 있다.
- selected_research_baseline(선택 연구 기준선)으로 올리지 않는 이유: validation net(검증 순손익) 음수, validation/OOS PF(검증/표본외 수익 팩터) 1.10 미만, cost-stressed expectancy(비용 압박 기대값) 음수, same-move audit(동일 이동 감사) 실패, Tier B fallback-only OOS(Tier B 대체 전용 표본외) 음수다.

## Latest Run50P Intermediate Evidence(최신 50P 중간 근거)

- packet(묶음): `stage56_run50P_nonflat_side_adx_density_v1`
- report(보고서): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50P_reopen_batch.md`
- summary_csv(요약 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50P_summary.csv`
- audit_csv(감사 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50P_audit.csv`
- aggregate_summary(합산 요약): `docs/agent_control/packets/stage56_run50P_nonflat_side_adx_density_v1/aggregate_summary.json`
- writer_repair_note(쓰기 복구 기록): `docs/agent_control/packets/stage56_run50P_nonflat_side_adx_density_v1/writer_repair_note.json`
- selected_research_baseline(선택 연구 기준선): `none`
- current_judgment(현재 판정): `in_progress_no_selected_research_baseline`

Run50P(실행50P)은 run50K(실행50K)의 dense non-flat model axis(조밀 비무포지션 가중 모델 축)에 run50N(실행50N)의 short ADX filter(숏 ADX 필터)를 붙였다. 효과(effect, 효과): density(밀도)를 모델 축으로 확보하고 품질은 방향 필터로 회복할 수 있는지 확인했다.

- best intermediate variant(최선 중간 변형): `nf_h10c2_s390l280_b_sadx`
- A+B actual routed total(A+B 실제 라우팅 전체) validation(검증): 7.136612 trades/day(일 거래 수), net(순손익) 116.66, PF(수익 팩터) 1.03, max DD(최대 손실) 270.68
- A+B actual routed total(A+B 실제 라우팅 전체) OOS(표본외): 4.758974 trades/day(일 거래 수), net(순손익) 140.04, PF(수익 팩터) 1.05, max DD(최대 손실) 250.38
- Tier B fallback-only OOS(Tier B 대체 전용 표본외): net(순손익) 5.00, PF(수익 팩터) 1.02로 non-negative(비음수)이지만 기준선 품질을 만들지 못했다.
- MFE capture read(MFE 포착 판독): best OOS MFE capture ratio(최선 표본외 MFE 포착 비율)는 0.614114로 d390h10 reference(d390h10 참조)보다 낮지만 materially worse(중대 악화)로만 볼 정도는 아니다.
- same-move read(동일 이동 판독): best OOS same-move re-entry ratio(최선 표본외 동일 이동 재진입 비율)는 0.724138이고 12-bar re-entry count(12봉 재진입 수)는 672다. 효과(effect, 효과): density gain(밀도 증가)은 여전히 same-move split trading(동일 이동 분할 거래)에 많이 기대고 있다.
- selected_research_baseline(선택 연구 기준선)으로 올리지 않는 이유: OOS density(표본외 밀도) 5.0 미만, validation/OOS PF(검증/표본외 수익 팩터) 1.10 미만, cost-stressed expectancy(비용 압박 기대값) 음수, same-move audit(동일 이동 감사) 실패다.

## Latest Run50O Intermediate Evidence(최신 50O 중간 근거)

- packet(묶음): `stage56_run50O_hold6_side_adx_density_v1`
- report(보고서): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50O_reopen_batch.md`
- summary_csv(요약 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50O_summary.csv`
- audit_csv(감사 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50O_audit.csv`
- aggregate_summary(합산 요약): `docs/agent_control/packets/stage56_run50O_hold6_side_adx_density_v1/aggregate_summary.json`
- selected_research_baseline(선택 연구 기준선): `none`
- current_judgment(현재 판정): `in_progress_no_selected_research_baseline`

Run50O(실행50O)은 default Stage07 LogReg(기본 Stage07 로지스틱 회귀) hold6(6봉 보유) 계열에 run50N(실행50N)의 short ADX filter(숏 ADX 필터)를 붙였다. 효과(effect, 효과): OOS density(표본외 밀도)를 5에 가깝게 되돌릴 때 품질과 same-move audit(동일 이동 감사)이 같이 살아나는지 확인했다.

- best intermediate variant(최선 중간 변형): `d320h06_sadx_c0_b045`
- A+B actual routed total(A+B 실제 라우팅 전체) validation(검증): 6.398907 trades/day(일 거래 수), net(순손익) 143.47, PF(수익 팩터) 1.04, max DD(최대 손실) 285.05
- A+B actual routed total(A+B 실제 라우팅 전체) OOS(표본외): 4.882051 trades/day(일 거래 수), net(순손익) 60.50, PF(수익 팩터) 1.02, max DD(최대 손실) 240.54
- Tier B fallback-only OOS(Tier B 대체 전용 표본외): net(순손익) -44.61, PF(수익 팩터) 0.82로 damaging(손상)했다.
- MFE capture read(MFE 포착 판독): best OOS MFE capture ratio(최선 표본외 MFE 포착 비율)는 0.605966이고 d390h10 reference(d390h10 참조)보다 낮다.
- same-move read(동일 이동 판독): best OOS same-move re-entry ratio(최선 표본외 동일 이동 재진입 비율)는 0.742647이고 12-bar re-entry count(12봉 재진입 수)는 707이다. 효과(effect, 효과): density gain(밀도 증가)은 주로 same-move split trading(동일 이동 분할 거래)로 읽는다.
- selected_research_baseline(선택 연구 기준선)으로 올리지 않는 이유: OOS density(표본외 밀도) 5.0 미만, validation/OOS PF(검증/표본외 수익 팩터) 1.10 미만, cost-stressed expectancy(비용 압박 기대값) 음수, same-move audit(동일 이동 감사) 실패, Tier B fallback-only OOS(Tier B 대체 전용 표본외) 음수다.

## Latest Run50N Intermediate Evidence(최신 50N 중간 근거)

- packet(묶음): `stage56_run50N_side_adx_filter_v1`
- report(보고서): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50N_reopen_batch.md`
- summary_csv(요약 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50N_summary.csv`
- audit_csv(감사 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50N_audit.csv`
- aggregate_summary(합산 요약): `docs/agent_control/packets/stage56_run50N_side_adx_filter_v1/aggregate_summary.json`
- writer_repair_note(쓰기 복구 기록): `docs/agent_control/packets/stage56_run50N_side_adx_filter_v1/writer_repair_note.json`
- selected_research_baseline(선택 연구 기준선): `none`
- current_judgment(현재 판정): `in_progress_no_selected_research_baseline`

Run50N(실행50N)은 run50M(실행50M)의 direction/ADX attribution(방향/ADX 귀속)에서 나온 `skip_short_adx_20_25` 단서를 실제 EA side filter(방향 필터) 입력으로 검증했다. 효과(effect, 효과): post-hoc aggregation(사후 합산)이 아니라 single MT5 tester account path(단일 MT5 테스터 계정 경로)의 actual routed total(실제 라우팅 전체)을 남겼다.

- best intermediate variant(최선 중간 변형): `c6s330l235_b_sadx`
- A+B actual routed total(A+B 실제 라우팅 전체) validation(검증): 6.196721 trades/day(일 거래 수), net(순손익) 256.42, PF(수익 팩터) 1.09, max DD(최대 손실) 237.16
- A+B actual routed total(A+B 실제 라우팅 전체) OOS(표본외): 4.005128 trades/day(일 거래 수), net(순손익) 508.97, PF(수익 팩터) 1.25, max DD(최대 손실) 171.29
- Tier A only(Tier A 단독) OOS(표본외): net(순손익) 536.95, PF(수익 팩터) 1.27
- Tier B fallback-only OOS(Tier B 대체 전용 표본외): net(순손익) 18.42, PF(수익 팩터) 1.08로 non-negative(비음수)였지만 A+B actual routed total(A+B 실제 라우팅 전체)은 A-only(A 단독)보다 OOS net(표본외 순손익)이 낮았다.
- MFE capture read(MFE 포착 판독): best OOS MFE capture ratio(최선 표본외 MFE 포착 비율)는 0.619893이고 d390h10 reference(d390h10 참조)보다 materially worse(중대 악화)는 아니다.
- same-move read(동일 이동 판독): best OOS same-move re-entry ratio(최선 표본외 동일 이동 재진입 비율)는 0.661972이고 12-bar re-entry count(12봉 재진입 수)는 517이다. 효과(effect, 효과): short ADX filter(숏 ADX 필터)는 품질은 개선했지만 density gain(밀도 증가)이 cooldown(쿨다운) 뒤 생존한다는 근거는 아직 없다.
- selected_research_baseline(선택 연구 기준선)으로 올리지 않는 이유: OOS density(표본외 밀도) 5.0 미만, validation PF(검증 수익 팩터) 1.10 미만, validation cost-stressed expectancy(검증 비용 압박 기대값) 음수, same-move audit(동일 이동 감사) 실패다.

## Latest Run50M Intermediate Evidence(최신 50M 중간 근거)

- packet(묶음): `stage56_run50M_cooldown_threshold_interpolation_v1`
- report(보고서): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50M_reopen_batch.md`
- summary_csv(요약 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50M_summary.csv`
- audit_csv(감사 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50M_audit.csv`
- aggregate_summary(합산 요약): `docs/agent_control/packets/stage56_run50M_cooldown_threshold_interpolation_v1/aggregate_summary.json`
- selected_research_baseline(선택 연구 기준선): `none`
- current_judgment(현재 판정): `in_progress_no_selected_research_baseline`

Run50M(실행50M)은 run50L(실행50L)의 6봉/12봉 cooldown(쿨다운) 간격을 threshold(임계값) 보간으로 다시 압박했다. 효과(effect, 효과): OOS density(표본외 밀도)를 5+로 회복할 때 품질과 same-move audit(동일 이동 감사)이 같이 살아나는지 확인했다.

- best intermediate variant(최선 중간 변형): `nf150_c8_h10_s340l240_b045`
- A+B actual routed total(A+B 실제 라우팅 전체) validation(검증): 6.415301 trades/day(일 거래 수), net(순손익) 91.64, PF(수익 팩터) 1.03, max DD(최대 손실) 254.78
- A+B actual routed total(A+B 실제 라우팅 전체) OOS(표본외): 4.066667 trades/day(일 거래 수), net(순손익) 233.06, PF(수익 팩터) 1.11, max DD(최대 손실) 188.43
- closest quality variant(품질 근접 변형): `nf150_c6_h10_s350l250_b045`는 OOS(표본외) net(순손익) 590.30, PF(수익 팩터) 1.28, cost-stressed expectancy(비용 압박 기대값) 0.183218였지만 OOS density(표본외 밀도)는 4.430769였다.
- Tier B fallback-only OOS(Tier B 대체 전용 표본외): net(순손익) 15.82~16.67, PF(수익 팩터) 1.07로 non-negative(비음수)이지만, validation PF(검증 수익 팩터)와 density(밀도) 문제를 해결하지 못했다.
- MFE capture read(MFE 포착 판독): best OOS MFE capture ratio(최선 표본외 MFE 포착 비율)는 0.588035이고 d390h10 reference(d390h10 참조) 대비 -0.040230이라 materially worse(중대 악화)는 아니다.
- same-move read(동일 이동 판독): best OOS same-move re-entry ratio(최선 표본외 동일 이동 재진입 비율)는 0.683480이고 12-bar cooldown read(12봉 쿨다운 판독)는 1.287179 trades/day(일 거래 수)라 density gain(밀도 증가)이 생존하지 못했다.
- selected_research_baseline(선택 연구 기준선)으로 올리지 않는 이유: OOS density(표본외 밀도) 5.0 미만, validation PF(검증 수익 팩터) 1.10 미만, cost-stressed expectancy(비용 압박 기대값) 실패, same-move audit(동일 이동 감사) 실패다.

## Latest Run50K Intermediate Evidence(최신 50K 중간 근거)

- packet(묶음): `stage56_run50K_model_axis_density_repair_v1`
- report(보고서): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50K_reopen_batch.md`
- summary_csv(요약 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50K_summary.csv`
- audit_csv(감사 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50K_audit.csv`
- aggregate_summary(합산 요약): `docs/agent_control/packets/stage56_run50K_model_axis_density_repair_v1/aggregate_summary.json`
- selected_research_baseline(선택 연구 기준선): `none`
- current_judgment(현재 판정): `in_progress_no_selected_research_baseline`

Run50K(실행50K)는 non-flat weighted model(비무포지션 가중 모델), recent-train model(최근 학습 모델), A-only/A+B comparison(A 단독/A+B 비교)을 실제 MT5 validation/OOS(검증/표본외)로 시험했다. 효과(effect, 효과): threshold-only axis(임계값 전용 축)를 넘어 model axis(모델 축)가 밀도와 품질을 동시에 살릴 수 있는지 확인했다.

- best intermediate variant(최선 중간 변형): `nf150_h10_s420l360_b045`
- A+B actual routed total(A+B 실제 라우팅 전체) validation(검증): 7.704918 trades/day(일 거래 수), net(순손익) 120.56, PF(수익 팩터) 1.03, max DD(최대 손실) 284.39
- A+B actual routed total(A+B 실제 라우팅 전체) OOS(표본외): 5.323077 trades/day(일 거래 수), net(순손익) -53.42, PF(수익 팩터) 0.98, max DD(최대 손실) 365.34
- Tier B fallback-only OOS(Tier B 대체 전용 표본외): net(순손익) -38.17, PF(수익 팩터) 0.87로 negative(음수)다.
- hold/re-entry audit(보유/재진입 감사): best OOS same-move re-entry ratio(최선 표본외 동일 이동 재진입 비율)는 0.786127이고 12-bar cooldown read(12봉 쿨다운 판독)는 1.138462 trades/day(일 거래 수)라 density gain(밀도 증가)이 생존하지 못했다.
- selected_research_baseline(선택 연구 기준선)으로 올리지 않는 이유: OOS net(표본외 순손익) 음수, validation/OOS PF(검증/표본외 수익 팩터) 1.10 미만, cost-stressed expectancy(비용 압박 기대값) 음수, same-move audit(동일 이동 감사) 실패, Tier B fallback-only OOS(Tier B 대체 전용 표본외) 음수다.

## Prior Stage56 Run50B Dense Engine Grid(이전 56단계 50B 두꺼운 엔진 격자)

- current stage(현재 단계): `56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection`
- current run(현재 실행): `run50B_tier_a_dense_engine_grid_v1`
- judgment(판정): `reviewed_completed_tier_a_dense_engine_grid_runtime_probe_only`
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

Stage56(56단계)은 v2의 `research baseline(연구 기준선)` base engine(기본 엔진)을 고르기 위해 열렸다. Run50B(실행50B)는 Stage07 LogReg(로지스틱 회귀) Tier A(티어 A) 모델을 실제 MT5 closed trades(닫힌 거래) 기준으로 4개 threshold/hold(임계값/보유) 변형에서 실행했다. d34h06은 density frontier(밀도 경계)이고 d40h12는 quality frontier(품질 경계)다. 아직 selected research baseline(선택 연구 기준선), live readiness(실거래 준비), runtime authority(런타임 권위), operating promotion(운영 승격), operating reference(운영 참조)는 없다. 다음 행동(action, 행동)은 run50C bracket micro-grid(구간 미세 격자)이며, effect(효과)는 밀도와 품질을 동시에 만족하는 좁은 후보가 있는지 확인하는 것이다.

## Latest Overnight Campaign Budget Stop(최신 야간 캠페인 예산 중지)

- campaign_id(캠페인 ID): `OVERNIGHT-AUTONOMOUS-ADAPTER-CAMPAIGN-01`
- judgment(판정): `campaign_budget_exhausted_candidates_preserved_for_user_review`
- stop_reason(중지 이유): `runtime_budget_exhausted_after_stage55_main_sync`
- preserved candidates(보존 후보): `spf03_block_early_or_trend_buy`, `csp03_midlate_longs_strong_shorts`, `rfp02_csp03_primary_csp05_fallback`

Codex self-completion(코덱스 자체 완료)은 금지된다. Candidate discovery(후보 발견)는 user review(사용자 검토) 입력일 뿐이며 baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), operating reference(운영 참조)를 만들지 않는다.

## Latest Stage55 Tier-B Fallback Side-Filter Routing Filter(최신 55단계 Tier B 대체 방향 필터 라우터)

- current run(현재 실행): `run49A_tier_b_fallback_side_filter_router_v1`

Stage55(55단계) `55_adapter_routing__tier_b_fallback_side_filter_router`는 tier-b fallback side-filter routing filter(Tier B 대체 방향 필터 라우터)를 `reviewed_completed_adapter_candidate_runtime_probe_only`로 기록했다. selected candidate(선택 후보)는 `rfp02_csp03_primary_csp05_fallback`이고, boundary(경계)는 runtime_probe_only(런타임 탐침 전용)이다. baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), operating reference(운영 참조)는 없다.

## Latest Stage54 Cost-Aware Side Permission Filter(理쒖떊 53?④퀎 諛⑺뼢 ?덉슜 ?꾪꽣)

- current run(?꾩옱 ?ㅽ뻾): `run48A_cost_aware_side_permission_filter_v1`

Stage54(53?④퀎) `54_adapter_signal__cost_aware_side_permission_filter`??side-specific permission filter(諛⑺뼢蹂??덉슜 ?꾪꽣)瑜?`reviewed_completed_adapter_candidate_runtime_probe_only`濡?湲곕줉?덈떎. selected candidate(?좏깮 ?꾨낫)??`csp03_midlate_longs_strong_shorts`?닿퀬, boundary(寃쎄퀎)??runtime_probe_only(?고????먯묠 ?꾩슜)?대떎. baseline(湲곗???, promotion(?밴꺽), runtime authority(?고???沅뚯쐞), live readiness(?ㅺ굅??以鍮?, operating reference(?댁쁺 李몄“)???녿떎.

## Latest Campaign Repair(최신 캠페인 수정)

- current repair(현재 수정): `repair_stage53_premature_self_completion_v1`

Stage53(53단계) `spf03_block_early_or_trend_buy`는 `adapter_candidate_observed_user_review_required` 후보 근거로 재분류됐다. Campaign(캠페인)은 `campaign_in_progress_user_review_required_candidate_observed`로 다시 열렸고, next stage(다음 단계)는 Stage54(54단계)다. 효과(effect, 효과)는 후보 근거를 보존하면서 Codex self-completion(코덱스 자체 완료)을 막는 것이다.
﻿## Latest Stage53 Side Permission Filter(최신 53단계 방향 허용 필터)

- current run(현재 실행): `run47A_side_specific_short_permission_filter_v1`

Stage53(53단계) `53_adapter_signal__side_specific_short_permission_filter`는 side-specific permission filter(방향별 허용 필터)를 `reviewed_completed_adapter_candidate_runtime_probe_only`로 기록했다. selected candidate(선택 후보)는 `spf03_block_early_or_trend_buy`이고, boundary(경계)는 runtime_probe_only(런타임 탐침 전용)이다. baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), operating reference(운영 참조)는 없다.

## Latest Stage52 ATR SL/TP Adapter(최신 52단계 ATR 손절/익절 어댑터)

- current run(현재 실행): `run46A_atr_based_adaptive_stop_takeprofit_adapter_v1`

Stage52(52단계) `52_sl_tp_policy__atr_based_adaptive_stop_takeprofit_adapter`는 mandatory ATR SL/TP(필수 ATR 손절/익절) adapter stage(어댑터 단계)를 `reviewed_completed_negative_memory_runtime_probe_only`로 기록했다. selected candidate(선택 후보)는 `atr01_sl1p0_tp1p5`이고, boundary(경계)는 runtime_probe_only(런타임 탐침 전용)이다. baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), operating reference(운영 참조)는 없다.

## Latest Stage51 Closeout(최신 51단계 마감)

- current run(현재 실행): `run45E_stage51_closeout_v1`

Stage51(51단계) `51_risk_filter__q2_short_late_di_loss_firewall` closed(마감) as `reviewed_closed_positive_q2_loss_firewall_runtime_probe_only`. It preserves(보존) `fw02_block_di_short_mild` as a Q2 loss firewall(Q2 손실 방화벽) runtime_probe(런타임 탐침) clue(단서), but creates(생성) no baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), or operating reference(운영 기준).

## Latest Stage51 Q2 Loss Firewall(최신 51단계 Q2 손실 방화벽)

Stage51(51단계) `51_risk_filter__q2_short_late_di_loss_firewall` recorded(기록) `stage51_run45ABCDE_q2_loss_firewall_v1` as `reviewed_completed_positive_q2_loss_firewall_runtime_probe_only`. It tested(시험) Q2 short/late/DI firewall(Q2 숏/후반/DI 방화벽) variants(변형) through actual MT5 WFO(실제 MT5 워크포워드), routed Tier B fallback(라우팅 Tier B 대체), cost sensitivity(비용 민감도), and overlap concentration(중복 집중도). The result remains runtime_probe(런타임 탐침) only, with no baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), or operating reference(운영 기준).

## Latest Stage51 Q2 Loss Firewall(최신 51단계 Q2 손실 방화벽)

- current run(현재 실행): `run45E_stage51_closeout_v1`

Stage51(51단계) `51_risk_filter__q2_short_late_di_loss_firewall` recorded(기록) `stage51_run45ABCDE_q2_loss_firewall_v1` as `reviewed_completed_positive_q2_loss_firewall_runtime_probe_only`. It tested(시험) Q2 short/late/DI firewall(Q2 숏/후반/DI 방화벽) variants(변형) through actual MT5 WFO(실제 MT5 워크포워드), routed Tier B fallback(라우팅 Tier B 대체), cost sensitivity(비용 민감도), and overlap concentration(중복 집중도). The result remains runtime_probe(런타임 탐침) only, with no baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), or operating reference(운영 기준).

## Latest Stage50 Follow-up Suite(최신 50단계 후속 묶음)

Stage50(50단계) completed(완료) `stage50_run44BCDE_followup_suite_v1` as `reviewed_completed_inconclusive_followup_runtime_probe_only`. It covered(포괄) Q2 forensics(Q2 부검), Tier B routed WFO(Tier B 라우팅 WFO), cost sensitivity(비용 민감도), and trade overlap concentration(거래 중복 집중도). The result remains runtime_probe(런타임 탐침) only, with no baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), or operating reference(운영 기준).

## Latest Stage50 ADX WFO Stress(최신 50단계 ADX WFO 압박)

Stage50(50단계) `50_robustness_protocol__tier_a_adx_reference_surface_wfo_stress` recorded(기록) `run44A_tier_a_adx_reference_surface_wfo_stress_v1` as `reviewed_completed_positive_robustness_runtime_probe_only`. It tested(시험) the Stage49(49단계) `Tier A only adx_20_25` reference surface(기준 표면) across rolling MT5 windows(롤링 MT5 윈도우). The result remains runtime_probe(런타임 탐침) only, with no baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), or operating reference(운영 기준).

## Latest Stage49 Closeout(최신 49단계 마감)

Stage49(49단계) closed(마감) as `reviewed_closed_positive_reference_surface_runtime_probe_only` after run43K/run43L/run43M/run43N. The preserved reference surface(보존 참고 표면)는 `Tier A only adx_20_25`이며, baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), operating reference(운영 기준)는 만들지 않았다.

## Latest Stage49 Deep Follow-up Suite(최신 49단계 심화 후속 묶음)

Stage49(49단계) completed(완료) run43G/run43H/run43I/run43J as `reviewed_completed_positive_deep_followup_runtime_probe_only`. Selected variant(선택 변형)는 `adx_20_25`이고, 이 묶음은 deep followup runtime probe only(심화 후속 런타임 탐침 전용)라서 baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), operating reference(운영 기준)를 만들지 않았다.

## Latest Stage49 Follow-up Suite(최신 49단계 후속 실험 묶음)

Stage49(49단계) completed(완료) run43C/run43D/run43E/run43F as `reviewed_completed_positive_followup_runtime_probe_only`. ADX band robustness(ADX 구간 강건성)는 `passed`이고, 이 묶음은 followup runtime probe only(후속 런타임 탐침 전용)라서 baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), operating reference(운영 기준)를 만들지 않았다.

## Latest Stage49 Reversal Selection MT5 Linkage(최신 49단계 반전 선별 MT5 수익 연동)

Stage49(49단계) `49_trade_lifecycle__compression_stress_mfe_capture_exit_timing` added(추가) `run43B_reversal_selection_rule_mt5_linkage_v1` as `reviewed_completed_positive_runtime_linkage_probe_only`. The rule(규칙) `skip_short_adx_20_25` changes short ADX 20-25 entries(숏 ADX 20-25 진입)를 flat(무진입)으로 바꿔 actual MT5 Strategy Tester(실제 MT5 전략 테스터) profit linkage(수익 연동)를 확인했다. No baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), or operating reference(운영 기준) was created.

## Latest Stage49 MFE Capture Exit Timing(최신 49단계 MFE 포착 청산 타이밍)

Stage49(49단계) `49_trade_lifecycle__compression_stress_mfe_capture_exit_timing` finished(완료) `run43A_compression_stress_mfe_capture_exit_timing_scout_v1` as `reviewed_completed_inconclusive_counterfactual_exit_timing_scout_only`. Stage48(48단계) run42B trade-level records(거래 단위 기록)를 사용해 fixed take-profit(고정 익절) counterfactual(반사실)을 봤고, common target(공통 목표)은 both splits(양쪽 분할)를 동시에 개선하지 못했다. No baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), or operating reference(운영 기준) was created.

## Latest Stage48 Trade-Level Supplement(최신 48단계 거래 단위 보강)

Stage48(48단계) `48_robustness_attribution__survivor_cluster_concentration_scout` added(추가) `run42B_trade_level_cluster_telemetry_supplement_v1` for Stage45(45단계) `c08_extreme_compression_stress`. It copied and parsed(복사 및 파싱) existing MT5 terminal reports(기존 MT5 터미널 보고서) into `735` closed trade rows(닫힌 거래 행). Judgment(판정)은 `reviewed_completed_inconclusive_trade_level_runtime_supplement_only`이며, baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), operating reference(운영 기준)는 없다.

## Latest Stage48 Survivor Cluster Concentration(최신 48단계 생존 후보 군집 집중)

Stage48(48단계) `48_robustness_attribution__survivor_cluster_concentration_scout` finished(완료) as `reviewed_completed_inconclusive_concentration_attribution_scout_only` with `42` source candidates(원천 후보), `84` source MT5 KPI(MT5 핵심 성과 지표) rows, and `84` concentration(집중) rows. It is attribution_scout_only(귀속 탐색 전용); no baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), or operating reference(운영 기준) was created.

## Latest Stage47 AUTO-CAMPAIGN-02 Runtime Probe

Stage47 `47_meta_signal__cross_model_agreement_disagreement_scout` finished as `reviewed_completed_inconclusive_runtime_probe_only` with `24` MT5 attempts and `72` MT5 KPI rows. It is independent from Stage38-42 and prior campaign stages; no baseline, promotion, runtime authority, live readiness, or operating reference was created.

## Latest Stage46 AUTO-CAMPAIGN-02 Runtime Probe

Stage46 `46_feature_interaction__nonlinear_pairwise_structure_scout` finished as `reviewed_completed_negative_memory_runtime_probe_only` with `16` MT5 attempts and `48` MT5 KPI rows. It is independent from Stage38-42 and prior campaign stages; no baseline, promotion, runtime authority, live readiness, or operating reference was created.

## Latest Stage45 AUTO-CAMPAIGN-02 Runtime Probe

Stage45 `45_volatility_mechanism__compression_expansion_signal_rebuild` finished as `reviewed_completed_inconclusive_runtime_probe_only` with `24` MT5 attempts and `72` MT5 KPI rows. It is independent from Stage38-42 and prior campaign stages; no baseline, promotion, runtime authority, live readiness, or operating reference was created.

## Latest Stage44 AUTO-CAMPAIGN-02 Runtime Probe

Stage44 `44_robustness_protocol__rolling_walkforward_split_stability` finished as `reviewed_completed_inconclusive_runtime_probe_only` with `24` MT5 attempts and `72` MT5 KPI rows. It is independent from Stage38-42 and prior campaign stages; no baseline, promotion, runtime authority, live readiness, or operating reference was created.

## Latest Stage43 AUTO-CAMPAIGN-02 Runtime Probe

Stage43 `43_model_rebuild__low_complexity_feature_subset_regularized_signal` finished as `reviewed_completed_inconclusive_runtime_probe_only` with `24` MT5 attempts and `72` MT5 KPI rows. It is independent from Stage38-42 and prior campaign stages; no baseline, promotion, runtime authority, live readiness, or operating reference was created.

## Latest Stage47 AUTO-CAMPAIGN-02 Runtime Probe

Stage47 `47_meta_signal__cross_model_agreement_disagreement_scout` finished as `reviewed_completed_inconclusive_runtime_probe_only` with `24` MT5 attempts and `72` MT5 KPI rows. It is independent from Stage38-42 and prior campaign stages; no baseline, promotion, runtime authority, live readiness, or operating reference was created.

## Latest Stage46 AUTO-CAMPAIGN-02 Runtime Probe

Stage46 `46_feature_interaction__nonlinear_pairwise_structure_scout` finished as `reviewed_completed_negative_memory_runtime_probe_only` with `16` MT5 attempts and `48` MT5 KPI rows. It is independent from Stage38-42 and prior campaign stages; no baseline, promotion, runtime authority, live readiness, or operating reference was created.

## Latest Stage45 AUTO-CAMPAIGN-02 Runtime Probe

Stage45 `45_volatility_mechanism__compression_expansion_signal_rebuild` finished as `reviewed_completed_inconclusive_runtime_probe_only` with `32` MT5 attempts and `96` MT5 KPI rows. It is independent from Stage38-42 and prior campaign stages; no baseline, promotion, runtime authority, live readiness, or operating reference was created.

## Latest Stage44 AUTO-CAMPAIGN-02 Runtime Probe

Stage44 `44_robustness_protocol__rolling_walkforward_split_stability` finished as `reviewed_completed_inconclusive_runtime_probe_only` with `24` MT5 attempts and `72` MT5 KPI rows. It is independent from Stage38-42 and prior campaign stages; no baseline, promotion, runtime authority, live readiness, or operating reference was created.

## Latest Stage43 AUTO-CAMPAIGN-02 Runtime Probe

Stage43 `43_model_rebuild__low_complexity_feature_subset_regularized_signal` finished as `reviewed_completed_inconclusive_runtime_probe_only` with `24` MT5 attempts and `72` MT5 KPI rows. It is independent from Stage38-42 and prior campaign stages; no baseline, promotion, runtime authority, live readiness, or operating reference was created.

## Latest Stage47 AUTO-CAMPAIGN-02 Runtime Probe

Stage47 `47_meta_signal__cross_model_agreement_disagreement_scout` finished as `reviewed_completed_inconclusive_runtime_probe_only` with `24` MT5 attempts and `72` MT5 KPI rows. It is independent from Stage38-42 and prior campaign stages; no baseline, promotion, runtime authority, live readiness, or operating reference was created.

## Latest Stage46 AUTO-CAMPAIGN-02 Runtime Probe

Stage46 `46_feature_interaction__nonlinear_pairwise_structure_scout` finished as `reviewed_completed_negative_memory_runtime_probe_only` with `16` MT5 attempts and `48` MT5 KPI rows. It is independent from Stage38-42 and prior campaign stages; no baseline, promotion, runtime authority, live readiness, or operating reference was created.

## Latest Stage45 AUTO-CAMPAIGN-02 Runtime Probe

Stage45 `45_volatility_mechanism__compression_expansion_signal_rebuild` finished as `reviewed_completed_inconclusive_runtime_probe_only` with `24` MT5 attempts and `72` MT5 KPI rows. It is independent from Stage38-42 and prior campaign stages; no baseline, promotion, runtime authority, live readiness, or operating reference was created.

## Latest Stage44 AUTO-CAMPAIGN-02 Runtime Probe

Stage44 `44_robustness_protocol__rolling_walkforward_split_stability` finished as `reviewed_completed_inconclusive_runtime_probe_only` with `24` MT5 attempts and `72` MT5 KPI rows. It is independent from Stage38-42 and prior campaign stages; no baseline, promotion, runtime authority, live readiness, or operating reference was created.

## Latest Stage43 AUTO-CAMPAIGN-02 Runtime Probe

Stage43 `43_model_rebuild__low_complexity_feature_subset_regularized_signal` finished as `reviewed_completed_inconclusive_runtime_probe_only` with `24` MT5 attempts and `72` MT5 KPI rows. It is independent from Stage38-42 and prior campaign stages; no baseline, promotion, runtime authority, live readiness, or operating reference was created.

## Latest Stage47 AUTO-CAMPAIGN-02 Runtime Probe

Stage47 `47_meta_signal__cross_model_agreement_disagreement_scout` finished as `reviewed_completed_negative_memory_runtime_probe_only` with `16` MT5 attempts and `48` MT5 KPI rows. It is independent from Stage38-42 and prior campaign stages; no baseline, promotion, runtime authority, live readiness, or operating reference was created.

## Latest Stage46 AUTO-CAMPAIGN-02 Runtime Probe

Stage46 `46_feature_interaction__nonlinear_pairwise_structure_scout` finished as `reviewed_completed_negative_memory_runtime_probe_only` with `16` MT5 attempts and `48` MT5 KPI rows. It is independent from Stage38-42 and prior campaign stages; no baseline, promotion, runtime authority, live readiness, or operating reference was created.

## Latest Stage45 AUTO-CAMPAIGN-02 Runtime Probe

Stage45 `45_volatility_mechanism__compression_expansion_signal_rebuild` finished as `reviewed_completed_negative_memory_runtime_probe_only` with `16` MT5 attempts and `48` MT5 KPI rows. It is independent from Stage38-42 and prior campaign stages; no baseline, promotion, runtime authority, live readiness, or operating reference was created.

## Latest Stage44 AUTO-CAMPAIGN-02 Runtime Probe

Stage44 `44_robustness_protocol__rolling_walkforward_split_stability` finished as `reviewed_completed_negative_memory_runtime_probe_only` with `16` MT5 attempts and `48` MT5 KPI rows. It is independent from Stage38-42 and prior campaign stages; no baseline, promotion, runtime authority, live readiness, or operating reference was created.

## Latest Stage43 AUTO-CAMPAIGN-02 Runtime Probe

Stage43 `43_model_rebuild__low_complexity_feature_subset_regularized_signal` finished as `reviewed_completed_negative_memory_runtime_probe_only` with `16` MT5 attempts and `48` MT5 KPI rows. It is independent from Stage38-42 and prior campaign stages; no baseline, promotion, runtime authority, live readiness, or operating reference was created.

## Latest Stage42 Session Structure Signal Reliability(최신 42단계 세션 구조 신호 신뢰도)

Stage42(42단계) `42_session_structure__cash_open_close_signal_reliability_scout`는 session/time-structure(세션/시간 구조) runtime probe(런타임 탐침)로 열렸다. Stage38/39/40/41(38/39/40/41단계)은 negative memory(부정 기억)로만 사용했고, permission/abstention(허용/기권), exit overlay(청산 오버레이), candle morphology(캔들 형태), label/horizon micro-tuning(라벨/수평선 미세조정)은 주 메커니즘으로 쓰지 않았다.

- run_id(실행 ID): `run36A_session_structure_signal_reliability_broad_mt5_probe_v1`
- judgment(판정): `reviewed_completed_negative_memory_runtime_probe_only`
- MT5 evidence(MT5 근거): `present`
- MT5 attempts(MT5 시도): `34`
- MT5 KPI rows(MT5 KPI 행): `102`
- micro_search_gate(미세 탐색 게이트): `failed`
- promotion_candidate_gate(승격 후보 게이트): `failed`
- boundary(경계): `runtime_probe_only_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_operating_reference`

Effect(효과): current truth(현재 진실)는 Stage42(42단계)를 runtime_probe_only(런타임 탐침 전용) session/time-structure(세션/시간 구조) 연구로만 기록한다.

## Latest Stage41 Directional Asymmetric Label Horizon(최신 41단계 방향 비대칭 라벨 수평선)

Stage41(41단계) `41_label_horizon__directional_asymmetric_return_target_rebuild`는 label/horizon redesign(라벨/수평선 재설계) runtime probe(런타임 탐침)로 열렸다. Stage38/39/40(38/39/40단계)은 negative memory(부정 기억)로만 사용했고, permission/abstention(허용/기권), exit overlay(청산 오버레이), candle morphology(캔들 형태) 재시도는 하지 않았다.

- run_id(실행 ID): `run35A_directional_asymmetric_label_horizon_broad_mt5_probe_v1`
- judgment(판정): `reviewed_completed_negative_memory_runtime_probe_only`
- MT5 evidence(MT5 근거): `present`
- MT5 attempts(MT5 시도): `34`
- MT5 KPI rows(MT5 KPI 행): `102`
- micro_search_gate(미세 탐색 게이트): `failed`
- promotion_candidate_gate(승격 후보 게이트): `failed`
- boundary(경계): `runtime_probe_only_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_operating_reference`

Effect(효과): current truth(현재 진실)는 Stage41(41단계)을 runtime_probe_only(런타임 탐침 전용) label/horizon(라벨/수평선) 연구로만 기록한다.

## Latest Stage40 Candle Morphology Signal Quality(최신 40단계 캔들 형태 신호 품질)

Stage40(40단계) `40_feature_structure__candle_morphology_signal_quality_scout`는 legacy Stage32(레거시 32단계) candle morphology(캔들 형태)를 idea-only(아이디어 전용) seed(씨앗)로만 가져와 run34A(실행34A) MT5 runtime probe(런타임 탐침)를 수행했다. legacy 34D/29N(레거시 34D/29N), baseline(기준선), promotion(승격), operating reference(운영 기준)는 상속하지 않는다.

- run_id(실행 ID): `run34A_candle_morphology_signal_quality_broad_mt5_probe_v1`
- judgment(판정): `reviewed_completed_negative_memory_runtime_probe_only`
- MT5 evidence(MT5 근거): `present`
- MT5 attempts(MT5 시도): `34`
- MT5 KPI rows(MT5 KPI 행): `102`
- micro_search_gate(미세 탐색 게이트): `failed`
- promotion_candidate_gate(승격 후보 게이트): `failed`
- boundary(경계): `runtime_probe_only_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_operating_reference`

효과(effect, 효과): 현재 진실(current truth, 현재 진실)은 Stage40(40단계)을 candle morphology(캔들 형태) runtime_probe_only(런타임 탐침 전용)로만 기록한다.

## Latest AUTO-CAMPAIGN-01 Stage40 Volatility Squeeze Expansion(최신 AUTO-CAMPAIGN-01 40단계 변동성 수축/확장)

Campaign(캠페인) `AUTO-CAMPAIGN-01-INDEPENDENT-ALPHA-TOPIC-SCOUT`는 independent_topic_scout(독립 주제 탐색)로 Stage40(40단계) `40_feature_interaction__volatility_squeeze_expansion_scout`를 선택했다. 선택 이유는 volatility squeeze/expansion(변동성 수축/확장) interaction(상호작용)이 Stage38 permission/abstention(허용/기권) 또는 Stage39 exit overlay(청산 덮개)의 직접 후속이 아니기 때문이다.

- run_id(실행 ID): `run34A_volatility_squeeze_expansion_broad_mt5_probe_v1`
- judgment(판정): `reviewed_completed_negative_memory_runtime_probe_only`
- MT5 evidence(MT5 근거): `present`
- MT5 attempts(MT5 시도): `36`
- MT5 KPI rows(MT5 KPI 행): `105`
- micro_search_gate(미세 탐색 게이트): `passed`
- promotion_candidate_gate(승격 후보 게이트): `failed`
- partial runtime blocker(부분 런타임 차단): `m01` validation(검증) micro attempt(미세 시도) 1개가 feature_csv_open_failed_5003(피처 CSV 열기 실패 5003)로 KPI 행 없이 차단됐다.
- boundary(경계): no baseline(기준선 없음), no promotion(승격 없음), no runtime authority(런타임 권위 없음), no live readiness(실거래 준비 없음), no operating reference(운영 기준 없음)

효과(effect, 효과): 현재 진실(current truth, 현재 진실)은 Stage40(40단계)을 exploration-only runtime probe(탐색 전용 런타임 탐침)로만 기록한다.

## Latest Stage39 RUN33A Exit Risk Non-Entry Overlay(최신 39단계 33A 청산 위험 비진입 덧씌움)

Stage39(39단계) `run33A_exit_risk_non_entry_overlay_broad_mt5_probe_v1`는 Stage38 c01 base entry(38단계 c01 기준 진입)를 고정하고 Stage24 survival(생존), Stage25 hazard(위험률), Stage27 tail pressure(꼬리 압력)를 post-entry overlay(진입 후 덧씌움)로 MT5 Strategy Tester(전략 테스터)에 실행했다.

결과(result, 결과): `reviewed_completed_negative_memory_runtime_probe_only`. MT5 KPI records(MT5 핵심 성과 지표 기록): `102`. Micro-search gate(미세 탐색 게이트): `failed`.

효과(effect, 효과): actual Stage39 MT5 artifacts(실제 39단계 MT5 산출물)를 가져왔지만 baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), operating reference(운영 기준)는 만들지 않았다.

## Latest Stage38 RUN32A Permission/Abstention Runtime Probe(최신 38단계 32A 실행 허용/기권 런타임 탐침)

Stage38(38단계) `run32A_permission_abstention_overlap_broad_mt5_probe_v1`는 Stage23 permission(허용), Stage30 calibration/abstention(보정/기권), Stage26 entropy(엔트로피), Stage27 tail pressure(꼬리 압력), Stage19 EBM direction(EBM 방향)을 같은 timestamp table(시각 테이블)에 겹쳐 MT5(`MetaTrader 5`, 메타트레이더5) runtime_probe(런타임 탐침)로 실행했다.

결과(result, 결과): `reviewed_completed_inconclusive_runtime_probe_only`. MT5 KPI records(MT5 핵심 성과 지표 기록): `102`.

효과(effect, 효과): decision layer(결정 계층)의 entry permission(진입 허용)과 abstention(기권) 겹침을 확인했지만 baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), operating reference(운영 기준)는 만들지 않았다.

## Latest Stage37 State Context Router(최신 37단계 상태 문맥 라우터)

- active stage(활성 단계): `37_state_context__single_base_filter_or_state_router`
- current run(현재 실행): `run31A_state_context_router_broad_mt5_probe_v1`
- latest packet(최신 묶음): `stage37_run31A_state_context_router_broad_mt5_probe_v1`
- result judgment(결과 판정): `state_context_not_useful_or_inconclusive`
- external verification(외부 검증): `completed`

Stage37(37단계)는 HMM state(은닉 상태), Markov state(마르코프 상태), KMeans state(K-평균 상태), 단순 context(문맥), 모델 반응(model response, 모델 반응)을 같은 timestamp(시각)에 붙이고 broad MT5 routed probe(넓은 MT5 라우팅 탐침)를 실행했다.

효과(effect, 효과): 다음 작업(next work, 다음 작업)은 구조 단서(structure clue, 구조 단서)를 참고할 수 있지만 baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비)는 아직 없다.

## Latest Stage36 Closeout(최신 36단계 마감)

- active stage(활성 단계): `36_model_selection__cross_model_characteristic_synthesis`
- current run(현재 실행): `stage36_cross_model_characteristic_synthesis_closeout_v1`
- source run(원천 실행): `run30A_cross_model_characteristic_synthesis_v1`
- latest packet(최신 묶음): `stage36_run30A_cross_model_characteristic_synthesis_v1`
- status(상태): `reviewed_closed_reference_only(검토 후 마감, 참고 전용)`
- next action(다음 행동): `choose_one_micro_probe_frontier_or_open_next_topic`

Stage36(36단계)은 Stage10-35(10-35단계) 모델군(model family, 모델군)을 특성 축(characteristic axis, 특성 축), MT5 linkage(MT5 연결), selection reference(선택 참고), micro-probe frontier(미세탐침 전선)로 정리하고 마감했다.

효과(effect, 효과): 다음 stage(단계)는 이 stage(단계)만 보고 모델 선택 방향을 고를 수 있다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

## Latest Stage35 Closeout(최신 35단계 마감)

- active stage(활성 단계): `35_context_map__unsupervised_market_state_atlas`
- current run(현재 실행): `stage35_context_map_closeout_v1`
- latest packet(최신 묶음): `stage35_context_map_closeout_v1`
- status(상태): `reviewed_closed_no_stage36_opened`
- next action(다음 행동): `none_stage35_closed_stage36_not_opened`

Stage35(35단계)는 RUN29A-RUN29C(29A-29C 실행) MT5 runtime probe(MT5 런타임 탐침)를 끝으로 마감했다.

결과(result, 결과): 남은 4개 후보는 no-October OOS(10월 제외 표본외)와 OOS second half(표본외 후반)를 함께 통과하지 못했다. 더 파볼 Stage35 후보는 없다.

효과(effect, 효과): Stage36(36단계)은 열지 않고, fragile seed(취약 씨앗)만 보존한다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

## Latest Stage35 RUN29C Candidate Four Deep Dive(최신 35단계 RUN29C 후보 4개 심화)

- active stage(활성 단계): `35_context_map__unsupervised_market_state_atlas`
- current run(현재 실행): `run29C_stage35_candidate_four_deep_dive_mt5_probe_v1`
- latest packet(최신 묶음): `stage35_run29C_candidate_four_deep_dive_mt5_probe_v1`
- external verification(외부 검증): `completed`
- MT5 attempts(MT5 시도): `36`

RUN29C(29C 실행)는 RUN29B(29B 실행)의 1/2/3/4 후보를 hold stress(보유 기간 압박)와 OOS drift stress(표본외 변화 압박)로 다시 확인했다.

효과(effect, 효과): Stage35(35단계) 후보를 좁히되 baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.

## Latest Stage35 Closeout(최신 35단계 마감)

- active stage(활성 단계): `35_context_map__unsupervised_market_state_atlas`
- current run(현재 실행): `stage35_context_map_closeout_v1`
- latest packet(최신 묶음): `stage35_context_map_closeout_v1`
- status(상태): `reviewed_closed_no_stage36_opened`
- next action(다음 행동): `none_stage35_closed_stage36_not_opened`

Stage35(35단계)는 RUN29A-RUN29C(29A-29C 실행) MT5 runtime probe(MT5 런타임 탐침)를 끝으로 마감했다.

결과(result, 결과): 남은 4개 후보는 no-October OOS(10월 제외 표본외)와 OOS second half(표본외 후반)를 함께 통과하지 못했다. 더 파볼 Stage35 후보는 없다.

효과(effect, 효과): Stage36(36단계)은 열지 않고, fragile seed(취약 씨앗)만 보존한다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

## Latest Stage35 RUN29C Candidate Four Deep Dive(최신 35단계 RUN29C 후보 4개 심화)

- active stage(활성 단계): `35_context_map__unsupervised_market_state_atlas`
- current run(현재 실행): `run29C_stage35_candidate_four_deep_dive_mt5_probe_v1`
- latest packet(최신 묶음): `stage35_run29C_candidate_four_deep_dive_mt5_probe_v1`
- external verification(외부 검증): `completed`
- MT5 attempts(MT5 시도): `36`

RUN29C(29C 실행)는 RUN29B(29B 실행)의 1/2/3/4 후보를 hold stress(보유 기간 압박)와 OOS drift stress(표본외 변화 압박)로 다시 확인했다.

효과(effect, 효과): Stage35(35단계) 후보를 좁히되 baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.

## Latest Stage35 RUN29B Worthwhile Deep Sweep(최신 35단계 RUN29B 더 파볼 축 깊은 훑기)

## Current Re-entry Snapshot(현재 재진입 스냅샷)

- active branch(활성 브랜치): `main`
- active stage(활성 단계): `35_context_map__unsupervised_market_state_atlas`
- current run(현재 실행): `run29B_stage35_worthwhile_deep_sweep_mt5_probe_v1`
- latest packet(최신 묶음): `stage35_run29B_worthwhile_deep_sweep_mt5_probe_v1`
- next action(다음 행동): `judge_stage35_run29B_clues_then_close_or_open_one_narrow_followup`

RUN29B(29B 실행)는 session timing(세션 시간), return-volatility state(수익률/변동성 상태), trend-momentum state(추세/모멘텀 상태), 그리고 2025-10 drift stress(2025년 10월 변화 압박)를 모두 MT5 runtime probe(MT5 런타임 탐침)에 연결했다.

결과(result, 결과): variants(변형) `19`, MT5 attempts(MT5 시도) `32`, MT5 KPI records(MT5 핵심 성과 지표 기록) `32`, external verification(외부 검증) `completed`.

효과(effect, 효과): Stage35(35단계)에서 남은 단서를 넓게 판독했지만 baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.

## Latest Stage35 RUN29A Unsupervised Market State Atlas(최신 35단계 RUN29A 비지도 시장 상태 지도)

## Current Re-entry Snapshot(현재 재진입 스냅샷)

- active branch(활성 브랜치): `main`
- active stage(활성 단계): `35_context_map__unsupervised_market_state_atlas`
- current run(현재 실행): `run29A_unsupervised_market_state_atlas_mt5_probe_v1`
- latest packet(최신 묶음): `stage35_run29A_unsupervised_market_state_atlas_mt5_probe_v1`
- next action(다음 행동): `continue_stage35_with_extreme_sweep_or_close_if_user_requests`

Stage35(35단계)를 unsupervised market state atlas(비지도 시장 상태 지도) 주제로 열고 RUN29A(29A 실행)를 기록했다.

결과(result, 결과): `5`개 non-overlapping topics(비중복 주제)를 골라 Python(파이썬) atlas state(지도 상태)를 만들고 MT5 runtime probe(MT5 런타임 탐침)를 시도했다. external verification(외부 검증)은 `completed`다.

효과(effect, 효과): Stage34(34단계) 꼬리를 잇지 않고 새 문맥 지도 주제로 이동했다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

## Latest Stage34 Closeout(최신 34단계 마감)

## Current Re-entry Snapshot(현재 재진입 스냅샷)

- active branch(활성 브랜치): `main(메인)`
- active stage(활성 단계): `34_regime_mechanism__tier_a_markov_long_permission_attribution`
- current run(현재 실행): `stage34_tier_a_markov_long_permission_attribution_closeout_v1`
- latest packet(최신 묶음): `stage34_tier_a_markov_long_permission_attribution_closeout_v1`
- next action(다음 행동): `none_stage35_not_opened(없음, 35단계 미개방)`

Stage34(34단계) `34_regime_mechanism__tier_a_markov_long_permission_attribution`를 reviewed closed(검토 후 닫힘)로 마감했다.

결과(result, 결과): `vol_high/adx_20_25` interaction(고변동/ADX 20-25 상호작용), 2025-10(2025년 10월) 의존, 낮은 OOS(표본외) 거래 수, 긴 hold duration(보유 기간)을 보존 단서로 남겼다.

효과(effect, 효과): main seed(메인 씨앗), baseline(기준선), promotion(승격), runtime authority(런타임 권위)를 만들지 않고 Stage34(34단계)를 닫는다. Stage35(35단계)는 열지 않는다.

## Latest Stage34 RUN28F Vol/ADX Dependency(최신 34단계 28F 변동성/ADX 의존성)

Stage34(34단계) `run28F_tier_a_markov_vol_adx_component_dependency_probe_v1`를 vol/adx component plus hold diagnostics(변동성/ADX 구성요소 + 보유 진단)로 완료했다.

결과(result, 결과): Python(파이썬) OOS(표본외) best net(최고 순손익)은 `exclude_vol_high`이고, 긴 hold duration(보유 기간)은 validation/OOS(검증/표본외) 평균 `377.271186` / `391.057143` bars(봉)다.

효과(effect, 효과): 후보는 보존하지만 main seed(메인 씨앗), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다. 이 단서는 Stage34(34단계) closeout(마감)에 흡수됐다.

## Latest Stage34 RUN28E Broader Entry Proxy(최신 34단계 28E 넓은 진입 대리)

## Current Re-entry Snapshot(현재 재진입 스냅샷)

- active branch(활성 브랜치): `codex/run28c-local`
- active stage(활성 단계): `34_regime_mechanism__tier_a_markov_long_permission_attribution`
- current run(현재 실행): `run28E_tier_a_markov_broader_entry_proxy_probe_v1`
- latest packet(최신 묶음): `stage34_run28E_tier_a_markov_broader_entry_proxy_probe_v1`
- next action(다음 행동): `run28F_tier_a_markov_vol_adx_component_dependency_probe_v1`

Stage34(34단계) `run28E_tier_a_markov_broader_entry_proxy_probe_v1`를 monthly robustness plus MT5 runtime probe(월별 버팀 + MT5 런타임 탐침)로 완료했다.

결과(result, 결과): `exclude_vol_high_or_adx_20_25`는 월 하나를 빼도 OOS(표본외) PF(수익 팩터)가 1 아래로 깨지지는 않았다. 다만 2025-10(2025년 10월)을 빼면 OOS(표본외) net(순손익)이 `4.91`까지 얇다. MT5(메타트레이더5) probe(탐침)는 validation/OOS(검증/표본외) trades(거래 수) `59` / `35`를 기록했다.

효과(effect, 효과): 후보는 보존하지만 main seed(메인 씨앗), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다. 다음은 `vol_high`와 `adx_20_25`를 분리해 의존성 원인을 본다.

## Latest Stage34 RUN28D Frequency Floor(최신 34단계 28D 실행 거래 수 하한)

## Current Re-entry Snapshot(현재 재진입 스냅샷)

- active branch(활성 브랜치): `codex/run28c-local`
- active stage(활성 단계): `34_regime_mechanism__tier_a_markov_long_permission_attribution`
- current run(현재 실행): `run28D_tier_a_markov_entry_proxy_frequency_floor_probe_v1`
- latest packet(최신 묶음): `stage34_run28D_tier_a_markov_entry_proxy_frequency_floor_probe_v1`
- next action(다음 행동): `run28E_tier_a_markov_broader_entry_proxy_probe_v1`

Stage34(34단계) `run28D_tier_a_markov_entry_proxy_frequency_floor_probe_v1`를 reviewed frequency floor probe(검토된 거래 수 하한 탐침)로 완료했다.

결과(result, 결과): `keep_late_or_vol_mid`는 validation/OOS trades(검증/표본외 거래 수) `40` / `26`라 얇다. `exclude_vol_high_or_adx_20_25`는 validation/OOS trades(검증/표본외 거래 수) `59` / `32`로 더 넓지만 PF(수익 팩터)는 낮다.

효과(effect, 효과): main seed(메인 씨앗)는 교체하지 않는다. run28C(28C 실행)의 1차 후보는 thin modifier clue(얇은 수정 단서)로 보존하고, 다음은 더 넓은 보조 후보를 찔러본다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

## Latest Stage34 RUN28C Entry-Time Hold Proxy(최신 34단계 28C 실행 진입 시점 보유 대리 신호)

## Current Re-entry Snapshot(현재 재진입 스냅샷)

- active branch(활성 브랜치): `main`
- active stage(활성 단계): `34_regime_mechanism__tier_a_markov_long_permission_attribution`
- current run(현재 실행): `run28C_tier_a_markov_long_permission_entry_time_hold_proxy_probe_v1`
- latest packet(최신 묶음): `stage34_run28C_tier_a_markov_long_permission_entry_time_hold_proxy_probe_v1`
- next action(다음 행동): `run28D_tier_a_markov_entry_proxy_runtime_probe_v1`

Stage34(34단계) `run28C_tier_a_markov_long_permission_entry_time_hold_proxy_probe_v1`를 reviewed entry-time proxy probe(검토된 진입 시점 대리 신호 탐침)로 완료했다.

결과(result, 결과): `keep_late_or_vol_mid`가 primary candidate(1차 후보)다. validation PF(검증 수익 팩터) `2.224467`, OOS PF(표본외 수익 팩터) `2.132004`지만 sample margin(표본 여유)이 얇다.

효과(effect, 효과): 이 후보는 run28D(28D 실행) MT5 runtime probe(MT5 런타임 탐침)로 넘길 수 있는 단서다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

## Latest Stage34 RUN28B Segment Stress(최신 34단계 28B 실행 구간 압박)

## Current Re-entry Snapshot(현재 재진입 스냅샷)

- active branch(활성 브랜치): `main(메인)`
- active stage(활성 단계): `34_regime_mechanism__tier_a_markov_long_permission_attribution`
- current run(현재 실행): `run28B_tier_a_markov_long_permission_segment_stress_probe_v1`
- latest packet(최신 묶음): `stage34_run28B_tier_a_markov_long_permission_segment_stress_probe_v1`
- next action(다음 행동): `run28C_tier_a_markov_long_permission_entry_time_hold_proxy_probe_v1`

Stage34(34단계) `run28B_tier_a_markov_long_permission_segment_stress_probe_v1`를 reviewed segment stress probe(검토된 구간 압박 탐침)로 완료했다.

결과(result, 결과): 가장 강한 단서는 hold shape(보유 형태)였다. `exclude_short_hold_0_12`는 validation/OOS PF(검증/표본외 수익 팩터)를 같이 올렸고, `keep_hold_gt_96_only`는 긴 보유가 수익 대부분을 들고 있음을 보였다. 다만 hold bucket(보유 버킷)은 ex-post information(사후 정보)이라 직접 runtime rule(런타임 규칙)이 아니다.

효과(effect, 효과): Tier A Markov long permission(티어 A 마르코프 롱 허용)은 보존하지만, 다음 행동(next action, 다음 행동)은 entry-time hold proxy(진입 시점 보유 대리 신호)를 찾는 `run28C_tier_a_markov_long_permission_entry_time_hold_proxy_probe_v1`다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

## Current Re-entry Snapshot(현재 재진입 스냅샷)

- active branch(활성 브랜치): `main(메인)`
- active stage(활성 단계): `34_regime_mechanism__tier_a_markov_long_permission_attribution`
- current run(현재 실행): `run28B_tier_a_markov_long_permission_segment_stress_probe_v1`
- latest packet(최신 묶음): `stage34_run28B_tier_a_markov_long_permission_segment_stress_probe_v1`
- next action(다음 행동): `run28C_tier_a_markov_long_permission_entry_time_hold_proxy_probe_v1`

Stage34(34단계) `run28B_tier_a_markov_long_permission_segment_stress_probe_v1`를 reviewed segment stress probe(검토된 구간 압박 탐침)로 완료했다.

결과(result, 결과): 가장 강한 단서는 hold shape(보유 형태)였다. `exclude_short_hold_0_12`는 validation/OOS PF(검증/표본외 수익 팩터)를 같이 올렸고, `keep_hold_gt_96_only`는 긴 보유가 수익 대부분을 들고 있음을 보였다. 다만 hold bucket(보유 버킷)은 ex-post information(사후 정보)이라 직접 runtime rule(런타임 규칙)이 아니다.

효과(effect, 효과): Tier A Markov long permission(티어 A 마르코프 롱 허용)은 보존하지만, 다음 행동(next action, 다음 행동)은 entry-time hold proxy(진입 시점 보유 대리 신호)를 찾는 `run28C_tier_a_markov_long_permission_entry_time_hold_proxy_probe_v1`다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

## Latest Stage34 RUN28A Attribution(최신 34단계 28A 실행 귀속)

## Current Re-entry Snapshot(현재 재진입 스냅샷)

- active branch(활성 브랜치): `main(메인)`
- active stage(활성 단계): `34_regime_mechanism__tier_a_markov_long_permission_attribution`
- current run(현재 실행): `run28A_tier_a_markov_long_permission_attribution_scout_v1`
- latest packet(최신 묶음): `stage34_run28A_tier_a_markov_long_permission_attribution_scout_v1`
- next action(다음 행동): `run28B_tier_a_markov_long_permission_segment_stress_probe_v1`

Stage34(34단계) `run28A_tier_a_markov_long_permission_attribution_scout_v1`를 reviewed attribution scout(검토된 귀속 탐침)로 완료했다.

결과(result, 결과): Tier A(티어 A) validation/OOS(검증/표본외) long-only(롱 전용) PF(수익 팩터)는 각각 `1.771465` / `1.224214`다. state/confidence/entropy(상태/신뢰/엔트로피)는 모든 Tier A 체결 거래에서 이미 high gate(높은 게이트)였고, profit(수익)은 time segment(시간 구간)와 hold shape(보유 형태)에서 갈렸다.

효과(effect, 효과): Stage34(34단계)는 Markov long permission(마르코프 롱 허용)을 보존 단서로 남기되, baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다. 다음 행동(next action, 다음 행동)은 `run28B_tier_a_markov_long_permission_segment_stress_probe_v1`다.

## Latest Stage33 Tier A Markov Long Permission Source(최신 33단계 티어 A 마르코프 롱 허용 원천)

## Current Re-entry Snapshot(현재 재진입 스냅샷)

- active branch(활성 브랜치): `main(메인)`
- active stage(활성 단계): `33_regime_mechanism__tier_a_markov_long_permission_source`
- current run(현재 실행): `run27A_tier_a_markov_long_permission_source_scout_v1`
- latest packet(최신 묶음): `stage33_tier_a_markov_long_permission_open_v1`
- next action(다음 행동): `run27A_tier_a_markov_long_permission_source_scout_v1` structural attribution scout(구조 귀속 탐침)

효과(effect, 효과): Stage33(33단계)는 Tier A Markov state long permission filter(티어 A 마르코프 상태 롱 허용 필터)의 source(원천)를 확인하기 위해 열린다. 아직 run result(실행 결과), KPI(핵심 성과 지표), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

## Latest Stage29-32 Native Revalidation Supplement(최신 29-32단계 원본 재검증 보강)

## Current Re-entry Snapshot(현재 재진입 스냅샷)

- active branch(활성 브랜치): `main(메인)`
- active stage(활성 단계): `32_sequence_model__tcn_temporal_convolution_context`
- current run(현재 실행): `run26D_torch_tcn_native_temporal_runtime_probe_v1`
- latest packet(최신 묶음): `stage29_32_native_revalidation_supplement_v1`
- next action(다음 행동): `open_new_stage_topic_if_requested`

효과(effect, 효과): Stage29-32(29-32단계)는 goal complete(목표 완료) 상태이고, 보강 묶음(packet, 묶음)을 active run(활성 실행)으로 오해하지 않는다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

Stage29~32(29~32단계) native revalidation(원본 재검증)을 `stage29_32_native_revalidation_supplement_v1`로 완료했다.

결과(result, 결과): river(리버), torch(파이토치), pytorch-tabnet(파이토치 탭넷) 설치 후 Stage29(29단계) River native(리버 원본), Stage30(30단계) native-source calibration(원본 기반 보정), Stage31(31단계) TabNet native(탭넷 원본), Stage32(32단계) Torch TCN native(파이토치 TCN 원본)를 MT5 score-table runtime_probe(MT5 점수표 런타임 탐침)로 재검증했다.

효과(effect, 효과): proxy gap(대리 구현 격차)을 보강했지만 baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않았다. summary(요약): `docs/workspace/stage29_32_native_revalidation_supplement.md`.

## Latest Stage29-32 Goal Completion(최신 29-32단계 목표 완료)

Stage29~32(29~32단계)를 reviewed closeout(검토된 마감)으로 닫았다.

결과(result, 결과): Stage29(29단계) `run23B_river_online_drift_runtime_probe_v1`, Stage30(30단계) `run24B_probability_calibration_abstention_runtime_probe_v1`, Stage31(31단계) `run25B_tabnet_attentive_tabular_runtime_probe_v1`, Stage32(32단계) `run26B_tcn_temporal_convolution_runtime_probe_v1` 모두 MT5 runtime_probe(MT5 런타임 탐침) external verification(외부 검증) `completed(완료)`다. 각 runtime run(런타임 실행)은 MT5 KPI records(MT5 핵심 성과 지표 기록) `10`, normalized records(정규화 기록) `6`, parser errors(파서 오류) `0`이다.

효과(effect, 효과): River online ML(리버 온라인 머신러닝), calibration/abstention(보정/기권), TabNet proxy(탭넷 대체), TCN proxy(TCN 대체)의 원래 특징 단서(characteristic clue, 특징 단서)를 보존했고, 이후 native revalidation supplement(원본 재검증 보강)로 River/TabNet/TCN package gap(패키지 격차)을 보강했다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않았다.

## Latest Stage28 RUN22C Supplement(최신 28단계 22C 실행 보강)

Stage28(28단계) `run22C_markov_regression_supplement_state_variance_attribution_v1`를 보강 묶음(supplement packet, 보강 묶음)으로 완료했다.

결과(result, 결과): `inconclusive_markov_regression_supplement_completed`. 당시 Stage29(29단계)는 opened_not_started(열림, 미시작) 상태였고 다음 행동(next action, 다음 행동)은 `run23A_river_online_drift_learning_scout_v1`였다.

효과(effect, 효과): Markov state count(마르코프 상태 수) 2/3개, switching variance(전환 분산), Tier A/B attribution(티어 A/B 귀속), native statsmodels runtime(원본 스탯스모델 런타임)과 MT5 score-table handoff(MT5 점수표 인계) 차이를 보강했고, baseline(기준선)이나 promotion(승격)은 만들지 않았다.

## Latest Stage28 Closeout / Stage29 Open(최신 28단계 마감 / 29단계 개방)

Stage28(28단계) Markov regression(마르코프 회귀)을 reviewed closeout(검토된 마감)으로 닫고 Stage29(29단계) `29_adaptive_model__river_online_drift_learning`를 open-only(개방만) 상태로 열었다.

결과(result, 결과): `closed_inconclusive_markov_regression_state_characteristics_exhausted`. active branch(활성 브랜치): `codex/stage28-markov-regression`. next exact action(다음 정확한 행동): `run23A_river_online_drift_learning_scout_v1`.

효과(effect, 효과): Stage28(28단계)의 state-link(상태 연결) 단서와 MT5 runtime_probe(MT5 런타임 탐침) 근거는 보존하고, baseline(기준선), promotion(승격), runtime authority(런타임 권위) 없이 River online ML(리버 온라인 머신러닝) topic pivot(주제 전환)으로 이동한다.

## Latest Stage28 RUN22B Markov Runtime Probe(최신 28단계 22B 실행 마르코프 런타임 탐침)

Stage28(28단계) `run22B_markov_regression_state_runtime_probe_v1`를 MT5 runtime_probe(MT5 런타임 탐침)로 실행했다.

결과(result, 결과): `inconclusive_markov_regression_state_runtime_probe_completed`. MT5 KPI records(MT5 핵심 성과 지표 기록): `10`. next exact action(다음 정확한 행동): `stage28_closeout_and_stage29_open_only`.

효과(effect, 효과): Markov regression(마르코프 회귀)의 sampled state handoff(표본 상태 인계)를 MT5 score-table runtime(MT5 점수표 런타임)으로 관찰했고 baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.

## Latest Stage20-27 Characteristic and Actual MT5 Rerun Synthesis(최신 20-27단계 특징 및 실제 MT5 재실행 종합)

Stage20~27(20~27단계)의 model family/topic exploration(모델군/주제 탐색)과 actual MT5 rerun(실제 MT5 재실행)을 `stage20_27_characteristic_synthesis_v1` 및 `stage20_27_actual_mt5_rerun_verification_v1`로 보강 정리했다.

결과(result, 결과): `completed_characteristic_and_actual_mt5_routed_rerun_synthesis_not_new_alpha_quality`. actual MT5 rerun(실제 MT5 재실행): `16/16` tester/runtime/report completed(테스터/런타임/보고서 완료). report(보고서): `docs/workspace/stage20_27_characteristic_synthesis.md`. 당시 Stage28 closeout(28단계 마감) 뒤 다음 정확한 행동(next exact action, 다음 정확한 행동)은 `run23A_river_online_drift_learning_scout_v1`였다.

효과(effect, 효과): GAM(일반화 가산 모델), ElasticNet Logistic(엘라스틱넷 로지스틱), HMM(은닉 마르코프 모델), supervised regime classifier(지도 국면 분류기), Survival model(생존 모델), hazard model(위험률 모델), NGBoost(자연 그래디언트 부스팅), quantile boosting(분위수 부스팅)의 특징 단서(characteristic clues, 특징 단서)와 MT5 trade shape(MT5 거래 모양)는 실제 routed validation/OOS(검증/표본외 라우팅) 재실행으로 보존하지만 baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다. full tier-view rerun(전체 티어 보기 재실행)은 아니다.

## Latest Stage28 RUN22A Markov Regression Scout(최신 28단계 22A 실행 마르코프 회귀 탐색)

Stage28(28단계) `run22A_markov_regression_state_link_scout_v1`를 Python structural scout(파이썬 구조 탐색)로 실행했다.

결과(result, 결과): `inconclusive_markov_regression_state_link_scout_completed`. selected variant(선택 변형): `v01_return_2state_switchvar`. next exact action(다음 정확한 행동): `run22B_markov_regression_state_runtime_probe_v1`.

효과(effect, 효과): Markov regression(마르코프 회귀)의 state-link(상태 연결) 단서는 보존하고, baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.

## Latest Stage27 Closeout / Stage28 Open(최신 27단계 마감 / 28단계 개방)

Stage27(27단계) quantile boosting(분위수 부스팅)을 reviewed closeout(검토된 마감)으로 닫고 Stage28(28단계) `28_regime_model__markov_switching_regression_state_link`를 open-only(개방만) 상태로 열었다.

결과(result, 결과): `closed_inconclusive_quantile_boosting_tail_characteristics_exhausted`. active branch(활성 브랜치): `codex/stage27-quantile-boosting`. next exact action(다음 정확한 행동): `run22A_markov_regression_state_link_scout_v1`.

효과(effect, 효과): Stage27(27단계)의 tail-risk surface(꼬리 위험 표면) 단서와 MT5 runtime_probe(MT5 런타임 탐침) 근거는 보존하고, baseline(기준선), promotion(승격), runtime authority(런타임 권위) 없이 Markov regression(마르코프 회귀) topic pivot(주제 전환)으로 이동한다.

## Latest Stage27 RUN21B Quantile Runtime Probe(최신 27단계 21B 실행 분위수 런타임 탐침)

Stage27(27단계) `run21B_quantile_boosting_tail_risk_runtime_probe_v1`를 MT5 runtime_probe(MT5 런타임 탐침)로 실행했다.

결과(result, 결과): `inconclusive_quantile_boosting_tail_runtime_probe_completed`. MT5 KPI records(MT5 핵심 성과 지표 기록): `10`. next exact action(다음 정확한 행동): `stage27_closeout_and_stage28_open_only`.

효과(effect, 효과): quantile boosting(분위수 부스팅)의 tail-risk surface(꼬리 위험 표면)를 MT5 score-table handoff(점수표 인계)로 관찰했고 baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.

## Latest Stage27 RUN21A Quantile Boosting Scout(최신 27단계 21A 실행 분위수 부스팅 탐색)

Stage27(27단계) `run21A_quantile_boosting_tail_risk_surface_scout_v1`를 reviewed structural scout(검토된 구조 탐색)로 완료했다.

결과(result, 결과): `inconclusive_quantile_boosting_tail_risk_surface_scout_completed`. selected variant(선택 변형): `v02_core42_tail_risk_surface`. next exact action(다음 정확한 행동): `run21B_quantile_boosting_tail_risk_runtime_probe_v1`.

효과(effect, 효과): quantile boosting(분위수 부스팅)의 tail-risk surface(꼬리 위험 표면)는 보존 단서로 남기고 baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.

## Latest Stage26 Closeout / Stage27 Open(최신 26단계 마감 / 27단계 개방)

Stage26(26단계) NGBoost(자연 그래디언트 부스팅)를 reviewed closeout(검토된 마감)으로 닫고 Stage27(27단계) `27_tail_model__quantile_boosting_risk_surface`를 open-only(개방만) 상태로 열었다.

결과(result, 결과): `closed_inconclusive_ngboost_distribution_characteristics_exhausted`. active branch(활성 브랜치): `codex/stage27-quantile-boosting`. next exact action(다음 정확한 행동): `run21A_quantile_boosting_tail_risk_surface_scout_v1`.

효과(effect, 효과): NGBoost(자연 그래디언트 부스팅)의 단서와 부정 기억은 보존하되 baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않고 quantile boosting(분위수 부스팅) topic pivot(주제 전환)으로 이동한다.

## Latest Stage26 RUN20B NGBoost Runtime Probe(최신 26단계 20B 실행 NGBoost 런타임 탐침)

Stage26(26단계) `run20B_ngboost_distribution_runtime_probe_v1`를 MT5 runtime_probe(MT5 런타임 탐침)로 실행했다.

결과(result, 결과): `inconclusive_ngboost_distribution_runtime_probe_completed`. MT5 KPI records(MT5 핵심 성과 지표 기록): `10`. next exact action(다음 정확한 행동): `stage26_closeout_and_stage27_open_only`.

효과(effect, 효과): NGBoost(자연 그래디언트 부스팅)의 distribution shape(분포 모양)을 MT5 score-table handoff(점수표 인계)로 관찰했고, baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.

## Latest Stage26 RUN20A NGBoost Scout(최신 26단계 20A 실행 NGBoost 탐색)

Stage26(26단계) `run20A_ngboost_probabilistic_distribution_scout_v1`를 reviewed structural scout(검토된 구조 탐색)로 완료했다.

결과(result, 결과): `inconclusive_ngboost_probabilistic_distribution_scout_completed`. selected variant(선택 변형): `v02_core42_distribution_surface`. next exact action(다음 정확한 행동): `run20B_ngboost_distribution_runtime_probe_v1`.

효과(effect, 효과): NGBoost(자연 그래디언트 부스팅)의 uncertainty/probability shape(불확실성/확률 모양)는 보존 단서로 남기고, baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.

## Latest Stage25 Closeout / Stage26 Open(최신 25단계 마감 / 26단계 개방)

Stage25(25단계) Hazard model(위험률 모델)을 reviewed closeout(검토된 마감)으로 닫고 Stage26(26단계) `26_model_family_challenge__ngboost_probabilistic_distribution_shape`를 open-only(개방만) 상태로 열었다.

결과(result, 결과): `closed_inconclusive_hazard_model_characteristics_exhausted`. active branch(활성 브랜치): `codex/stage26-ngboost-probabilistic`. next exact action(다음 정확한 행동): `run20A_ngboost_probabilistic_distribution_scout_v1`.

효과(effect, 효과): Hazard model(위험률 모델)의 단서와 부정 기억은 보존하되 baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않고 NGBoost(자연 그래디언트 부스팅) topic pivot(주제 전환)으로 이동한다.

## Latest Stage25 RUN19B Hazard Runtime Update(최신 25단계 실행19B 위험률 런타임 업데이트)

Stage25(25단계) `run19B_hazard_trade_lifecycle_runtime_probe_v1`를 MT5 runtime_probe(MT5 런타임 탐침)로 실행했다.

결과(result, 결과): `inconclusive_hazard_permission_runtime_probe_completed`. MT5 KPI records(MT5 핵심 성과 지표 기록): `10`. next exact action(다음 정확한 행동): `stage25_closeout_and_stage26_open_only`.

효과(effect, 효과): Hazard model(위험률 모델)의 fixed elapsed-bar risk(고정 경과 봉 위험)가 MT5 score table(점수표)로 전달되는지 확인했고, Stage25(25단계) closeout(마감) 판단 근거를 만들었다.

## Latest Stage25 RUN19A Hazard Update(최신 25단계 실행19A 위험률 업데이트)

Stage25(25단계) `run19A_hazard_trade_lifecycle_risk_scout_v1`를 Python structural scout(파이썬 구조 탐색)로 실행했다.

결과(result, 결과): `inconclusive_hazard_trade_lifecycle_risk_scout_completed`. selected variant(선택 변형): `v04_logit_core24_reversal_after_favorable_1x`. next exact action(다음 정확한 행동): `run19B_hazard_trade_lifecycle_runtime_probe_v1`.

효과(effect, 효과): Hazard model(위험률 모델)을 entry score(진입 점수)가 아니라 bar-by-bar loss/reversal risk(봉별 손실/반전 위험)로 읽었다. MT5 runtime_probe(MT5 런타임 탐침)는 다음 실행이다.

## Latest Stage24 Closeout / Stage25 Open(최신 24단계 마감 / 25단계 개방)

Stage24(24단계) Survival model(생존 모델)을 reviewed closeout(검토된 마감)으로 닫고 Stage25(25단계) `25_exit_model__hazard_trade_lifecycle_risk`를 open-only(개방만) 상태로 열었다.

결과(result, 결과): `closed_inconclusive_survival_model_characteristics_exhausted`. active branch(활성 브랜치): `codex/stage25-hazard-model`. next exact action(다음 정확한 행동): `run19A_hazard_trade_lifecycle_risk_scout_v1`.

효과(effect, 효과): Survival model(생존 모델)의 hold/exit clue(보유/청산 단서)는 보존하지만 baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않고 hazard model(위험률 모델)로 topic pivot(주제 전환)한다.

## Latest Stage24 RUN18B Survival Runtime Update(최신 24단계 실행18B 생존 런타임 업데이트)

Stage24(24단계) `run18B_survival_time_to_event_runtime_probe_v1`를 MT5 runtime_probe(MT5 런타임 탐침)로 실행했다.

결과(result, 결과): `inconclusive_survival_permission_runtime_probe_completed`. MT5 KPI records(MT5 핵심 성과 지표 기록): `10`. next exact action(다음 정확한 행동): `stage24_closeout_and_stage25_open_only`.

효과(effect, 효과): Survival model(생존 모델)의 risk score(위험 점수)를 close-on-flat(평탄 시 청산) runtime behavior(런타임 행동)로 넘겨 확인했다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

## Latest Stage24 RUN18A Survival Update(최신 24단계 실행18A 생존 업데이트)

Stage24(24단계) `run18A_survival_time_to_event_hold_shape_scout_v1`를 Python structural scout(파이썬 구조 탐색)로 실행했다.

결과(result, 결과): `inconclusive_survival_time_to_event_hold_shape_scout_completed`. selected variant(선택 변형): `v04_weibull_aft_core24_abs_move_3x`. next exact action(다음 정확한 행동): `run18B_survival_time_to_event_runtime_probe_v1`.

효과(effect, 효과): Survival model(생존 모델)을 entry score(진입 점수)가 아니라 time-to-event(사건까지 시간), censoring(검열), hold/exit clock(보유/청산 시계)으로 읽었다. MT5 runtime_probe(MT5 런타임 탐침)는 다음 실행이다.

## Latest Stage23 Closeout / Stage24 Open(최신 23단계 마감 / 24단계 개방)

Stage23(23단계) supervised regime classifier(지도 국면 분류기)를 reviewed closeout(검토된 마감)으로 닫고 Stage24(24단계) `24_exit_model__survival_time_to_event_hold_shape`를 open-only(개방만) 상태로 열었다.

결과(result, 결과): `closed_inconclusive_supervised_regime_classifier_characteristics_exhausted`. active branch(활성 브랜치): `codex/stage24-survival-model`. next exact action(다음 정확한 행동): `run18A_survival_time_to_event_hold_shape_scout_v1`.

효과(effect, 효과): Stage23(23단계)의 permission/filter(허용/필터) 단서는 보존하지만 baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않고 Survival model(생존 모델)로 topic pivot(주제 전환)한다.

## Latest Stage23 RUN17B Supervised Regime Runtime Update(최신 23단계 실행17B 지도 국면 런타임 업데이트)

Stage23(23단계) `run17B_supervised_regime_classifier_runtime_probe_v1`를 MT5(`MetaTrader 5`, 메타트레이더5) runtime_probe(런타임 탐침)로 실행했다.

결과(result, 결과): `inconclusive_supervised_regime_classifier_runtime_probe_completed`. MT5 KPI records(MT5 핵심 성과 지표 기록): `10`. next exact action(다음 정확한 행동): `stage23_closeout_and_stage24_open_only`.

효과(effect, 효과): run17A Python structural scout(파이썬 구조 탐색)를 ONNX runtime handoff(온닉스 런타임 인계) 확인으로 전진시켰다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

## Latest Stage23 RUN17A Supervised Regime Update(최신 23단계 실행17A 지도 국면 업데이트)

Stage23(23단계) `run17A_supervised_regime_classifier_filter_scout_v1`를 Python structural scout(파이썬 구조 탐색)로 실행했다.

결과(result, 결과): `inconclusive_supervised_regime_classifier_filter_scout_completed`. selected variant(선택 변형): `v05_logistic_core24_compact_filter`. next exact action(다음 정확한 행동): `run17B_supervised_regime_classifier_runtime_probe_v1`.

효과(effect, 효과): p_flat(평탄 확률)을 block/abstain(차단/기권) 후보로 읽는 supervised regime classifier(지도 국면 분류기) 특성을 기록했고, MT5 runtime_probe(MT5 런타임 탐침)는 다음 실행으로 남긴다.

## Latest Stage22 Closeout / Stage23 Open(최신 22단계 마감 / 23단계 개방)

Stage22(22단계) HMM(`Hidden Markov Model`, 은닉 마르코프 모델)을 reviewed closeout(검토된 마감)으로 닫고 Stage23(23단계) `23_regime_model__supervised_regime_classifier_filter`를 open-only(개방만) 상태로 열었다.

결과(result, 결과): `closed_inconclusive_hmm_state_characteristics_exhausted`. active branch(활성 브랜치): `codex/stage23-supervised-regime-classifier`. next exact action(다음 정확한 행동): `run17A_supervised_regime_classifier_filter_scout_v1`.

효과(effect, 효과): HMM(은닉 마르코프 모델) 단서는 보존하지만 baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않고 supervised regime classifier(지도 국면 분류기)로 topic pivot(주제 전환)한다.

## Latest Stage22 RUN16B HMM Runtime Update(최신 22단계 실행16B HMM 런타임 업데이트)

Stage22(22단계) `run16B_hmm_state_runtime_probe_v1`를 MT5(`MetaTrader 5`, 메타트레이더5) runtime_probe(런타임 탐침)로 실행했다.

결과(result, 결과): `inconclusive_hmm_state_policy_runtime_probe_completed`. MT5 KPI records(MT5 핵심 성과 지표 기록): `10`. next exact action(다음 정확한 행동): `stage22_closeout_and_stage23_open_only`.

효과(effect, 효과): HMM(은닉 마르코프 모델) hidden state(숨은 상태)가 table handoff(테이블 인계)로 runtime(런타임)에 전달되는지 검증했다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

## Latest Stage22 RUN16B HMM Runtime Update(최신 22단계 실행16B HMM 런타임 업데이트)

Stage22(22단계) `run16B_hmm_state_runtime_probe_v1`를 MT5(`MetaTrader 5`, 메타트레이더5) runtime_probe(런타임 탐침)로 실행했다.

결과(result, 결과): `blocked_hmm_state_policy_runtime_probe_after_attempt`. MT5 KPI records(MT5 핵심 성과 지표 기록): `0`. next exact action(다음 정확한 행동): `repair run16B HMM state runtime probe and rerun the same six MT5 attempts`.

효과(effect, 효과): HMM(은닉 마르코프 모델) hidden state(숨은 상태)가 table handoff(테이블 인계)로 runtime(런타임)에 전달되는지 검증했다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

## Latest Stage22 RUN16A HMM Update(최신 22단계 실행16A HMM 업데이트)

Stage22(22단계) `run16A_hmm_hidden_state_segmentation_scout_v1`를 Python structural scout(파이썬 구조 탐색)로 실행했다.

결과(result, 결과): `inconclusive_hmm_hidden_state_structural_scout_completed`. selected variant(선택 변형): `v02_core17_4state_diag`. next exact action(다음 정확한 행동): `run16B_hmm_state_runtime_probe_v1`.

효과(effect, 효과): HMM(`Hidden Markov Model`, 은닉 마르코프 모델) hidden state(은닉 상태)의 Tier A separate(Tier A 분리), Tier B separate(Tier B 분리), Tier A+B combined(Tier A+B 합산)를 남겼지만, MT5 runtime_probe(MT5 런타임 탐침), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 아직 없다.

## Latest Stage21 Closeout Stage22 Open(최신 21단계 마감 22단계 개방)

Stage21(21단계) ElasticNet Logistic(엘라스틱넷 로지스틱)은 `closed_inconclusive_elasticnet_logistic_model_characteristics_exhausted`로 닫혔고, Stage22(22단계) HMM(`Hidden Markov Model`, 은닉 마르코프 모델)은 `opened_not_started`로 열렸다.

효과(effect, 효과): 다음 작업은 Stage22(22단계) `run16A_hmm_hidden_state_segmentation_scout_v1` broad scout(넓은 탐색)이며, Stage21(21단계)의 model(모델), coefficient(계수), threshold(임계값), ONNX file(온닉스 파일)은 baseline(기준선)으로 상속하지 않는다.

## Latest Stage21 RUN15B ElasticNet Logistic Runtime Update(최신 21단계 실행15B 엘라스틱넷 로지스틱 런타임 업데이트)

Stage21(21단계) `run15B_elasticnet_logistic_onnx_runtime_probe_v1`를 MT5(`MetaTrader 5`, 메타트레이더5) runtime_probe(런타임 탐침)로 실행했다.

결과(result, 결과): `inconclusive_elasticnet_logistic_onnx_runtime_probe_completed`. MT5 KPI records(MT5 핵심 성과 지표 기록): `10`. next exact action(다음 정확한 행동): `stage21_closeout_and_stage22_open_only`.

효과(effect, 효과): Stage21(21단계)은 Python structural scout(파이썬 구조 탐색)에서 ONNX runtime handoff(온닉스 런타임 인계) 확인으로 전진했다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

## Latest Stage21 RUN15B ElasticNet Logistic Runtime Update(최신 21단계 실행15B 엘라스틱넷 로지스틱 런타임 업데이트)

Stage21(21단계) `run15B_elasticnet_logistic_onnx_runtime_probe_v1`를 MT5(`MetaTrader 5`, 메타트레이더5) runtime_probe(런타임 탐침)로 실행했다.

결과(result, 결과): `blocked_elasticnet_logistic_onnx_runtime_probe_after_attempt`는 위 completed(완료) 재실행으로 superseded(대체됨)했다. 당시 MT5 KPI records(MT5 핵심 성과 지표 기록)는 `0`이고, repair action(수정 행동)은 ONNX label output(온닉스 라벨 출력)을 probability-only output(확률 전용 출력)으로 낮춘 것이다.

효과(effect, 효과): Stage21(21단계)은 Python structural scout(파이썬 구조 탐색)에서 ONNX runtime handoff(온닉스 런타임 인계) 확인으로 전진했다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

## Latest Stage21 RUN15B ElasticNet Logistic Runtime Update(최신 21단계 실행15B 엘라스틱넷 로지스틱 런타임 업데이트)

Stage21(21단계) `run15B_elasticnet_logistic_onnx_runtime_probe_v1`를 MT5(`MetaTrader 5`, 메타트레이더5) runtime_probe(런타임 탐침)로 실행했다.

결과(result, 결과): `blocked_elasticnet_logistic_onnx_runtime_probe_after_attempt`는 위 completed(완료) 재실행으로 superseded(대체됨)했다. 당시 MT5 KPI records(MT5 핵심 성과 지표 기록)는 `0`이고, repair action(수정 행동)은 ONNX label output(온닉스 라벨 출력)을 probability-only output(확률 전용 출력)으로 낮춘 것이다.

효과(effect, 효과): Stage21(21단계)은 Python structural scout(파이썬 구조 탐색)에서 ONNX runtime handoff(온닉스 런타임 인계) 확인으로 전진했다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

## Latest Stage21 RUN15B ElasticNet Logistic Runtime Update(최신 21단계 실행15B 엘라스틱넷 로지스틱 런타임 업데이트)

Stage21(21단계) `run15B_elasticnet_logistic_onnx_runtime_probe_v1`를 MT5(`MetaTrader 5`, 메타트레이더5) runtime_probe(런타임 탐침)로 실행했다.

결과(result, 결과): `blocked_elasticnet_logistic_onnx_runtime_probe_after_attempt`는 위 completed(완료) 재실행으로 superseded(대체됨)했다. 당시 MT5 KPI records(MT5 핵심 성과 지표 기록)는 `0`이고, repair action(수정 행동)은 ONNX label output(온닉스 라벨 출력)을 probability-only output(확률 전용 출력)으로 낮춘 것이다.

효과(effect, 효과): Stage21(21단계)은 Python structural scout(파이썬 구조 탐색)에서 ONNX runtime handoff(온닉스 런타임 인계) 확인으로 전진했다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

## Latest Stage21 RUN15A ElasticNet Logistic Update(최신 21단계 실행15A 엘라스틱넷 로지스틱 업데이트)

Stage21(21단계) `run15A_elasticnet_logistic_linear_sanity_scout_v1`를 Python structural scout(파이썬 구조 탐색)로 실행했다.

결과(result, 결과): `inconclusive_elasticnet_logistic_sparse_linear_scout_completed`. selected variant(선택 변형): `v01_core42_balanced_enet025`. next exact action(다음 정확한 행동): `run15B_elasticnet_logistic_onnx_runtime_probe_v1`.

효과(effect, 효과): ElasticNet Logistic(엘라스틱넷 로지스틱)의 sparse linear probability shape(희소 선형 확률 모양), coefficient sign(계수 부호), Tier A separate(Tier A 분리), Tier B separate(Tier B 분리), Tier A+B combined(Tier A+B 합산)를 남겼다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

## Latest Stage20 Closeout Stage21 Open(최신 20단계 마감 21단계 개방)

Stage20(20단계) GAM(`Generalized Additive Model`, 일반화 가산 모델)은 `closed_inconclusive_gam_model_characteristics_exhausted`로 닫혔고, Stage21(21단계) ElasticNet Logistic(엘라스틱넷 로지스틱)은 `opened_not_started`로 열렸다.

효과(effect, 효과): 다음 작업은 Stage21(21단계) `run15A_elasticnet_logistic_linear_sanity_scout_v1` broad scout(넓은 탐색)이며, Stage20(20단계)의 model(모델), threshold(임계값), runtime file(런타임 파일)은 baseline(기준선)으로 상속하지 않는다.

## Superseded Stage20 RUN14B Materialize-Only Note(대체된 20단계 실행14B 물질화 전용 기록)

Stage20(20단계) `run14B_gam_runtime_handoff_probe_v1`를 MT5(`MetaTrader 5`, 메타트레이더5) runtime_probe(런타임 탐침)로 실행했다.

결과(result, 결과): `inconclusive_gam_piecewise_score_table_runtime_probe_completed`. MT5 KPI records(MT5 핵심 성과 지표 기록): `10`. next exact action(다음 정확한 행동): `write Stage20 closeout packet and open Stage21 open-only`.

효과(effect, 효과): Stage20(20단계)은 Python structural scout(파이썬 구조 탐색)에서 runtime handoff(런타임 인계) 확인 단계로 전진했다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

## Latest Stage20 RUN14B GAM Runtime Update(최신 20단계 실행14B GAM 런타임 업데이트)

Stage20(20단계) `run14B_gam_runtime_handoff_probe_v1`를 MT5(`MetaTrader 5`, 메타트레이더5) runtime_probe(런타임 탐침)로 실행했다.

결과(result, 결과): `blocked_gam_piecewise_score_table_runtime_probe_after_attempt`는 위 completed(완료) MT5 runtime_probe(런타임 탐침)로 superseded(대체됨)했다. MT5 KPI records(MT5 핵심 성과 지표 기록): 이 materialize-only(물질화 전용) attempt(시도)는 `0`이다.

효과(effect, 효과): Stage20(20단계)은 Python structural scout(파이썬 구조 탐색)에서 runtime handoff(런타임 인계) 확인 단계로 전진했다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

## Latest Stage20 RUN14A GAM Update(최신 20단계 실행14A GAM 업데이트)


Stage20(20단계)은 `run14A_gam_additive_shape_scout_v1`로 GAM(`Generalized Additive Model`, 일반화 가산 모델) additive smooth shape(가산 부드러운 모양)를 Python structural scout(파이썬 구조 탐색)로 실행했다.

결과(result, 결과): `inconclusive_gam_additive_shape_structural_scout_completed`. selected variant(선택 변형)는 `v02_core24_smoother`, best overall variant(전체 최고 변형)는 `v03_proxy_context20_tier_a`다.

효과(effect, 효과): Tier A separate(Tier A 분리), Tier B separate(Tier B 분리), Tier A+B combined(Tier A+B 합산) Python records(파이썬 기록)를 남겼지만, MT5(`MetaTrader 5`, 메타트레이더5) runtime_probe(런타임 탐침), closeout(마감), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 아직 없다. 다음 정확한 행동(next exact action, 다음 정확한 행동)은 `run14B_gam_runtime_handoff_probe_v1`에서 GAM score representation(GAM 점수 표현)을 MT5 handoff(메타트레이더5 인계) 가능하게 만들고 sentinel run(감시 실행)을 먼저 수행하는 것이다.

Stage20-32(20-32단계) goal operating plan(목표 운영 계획)을 `docs/workspace/stage20_32_goal_operating_plan.md`로 채택했다. decision memo(결정 메모)는 `docs/decisions/2026-05-05_stage20_32_goal_operating_plan.md`에 둔다.

효과(effect, 효과): Stage20(20단계)부터 Stage32(32단계)까지 각 model/topic exploration(모델/주제 탐색)은 고유 특성 탐색, MT5(`MetaTrader 5`, 메타트레이더5) runtime_probe(런타임 탐침), reviewed closeout(검토된 마감), 다음 stage(단계) open-only(개방만) 순서로 진행한다.

MT5 batch safety/recovery(MT5 배치 안전/복구)는 blind batch(무검토 배치)를 금지하고, small tranche(작은 묶음) 또는 sentinel run(감시 실행) 뒤 log/report/telemetry/KPI/parser(로그/보고서/기록/핵심 성과 지표/파서)를 확인한다. 문제 발생 시 기본 목표는 stop(중지)이 아니라 repair-and-continue(수정 후 계속 진행)다.

효과(effect, 효과): 이 계획은 baseline(기준선), promotion(승격), runtime authority(런타임 권위)를 만들지 않는다. 현재 진행 기준은 Stage20(20단계) closeout(마감) 이후 열린 Stage21(21단계) `run15A` scout(탐색)다.

## Latest Stage19 RUN13AD Axis Exhaustion Update(최신 19단계 실행13AD 축 소진 업데이트)

Stage19(19단계)는 `run13AD_ebm_axis_exhaustion_followthrough_v1`에서 EBM(`Explainable Boosting Machine`, 설명가능 부스팅 머신) 1/2/3/4 축을 추가로 파고 follow-up(후속 탐침) 여지를 판정했다.

결과(result, 결과): `inconclusive_ebm_axis_exhaustion_followthrough_completed`. follow-up action(후속 행동)은 `followup_completed_no_new_runtime_followup_recommended`이다.

효과(effect, 효과): feature(피처), hold(보유), Tier B routing(티어 B 라우팅), side compression(방향 압축)을 더 봤지만 edge(거래 우위), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

## Latest Stage19 Closeout and Stage20 Open(최신 19단계 마감과 20단계 개방)

Stage19(19단계)는 EBM(`Explainable Boosting Machine`, 설명가능 부스팅 머신) `run13A-run13AH(실행13A-실행13AH)` 탐색을 `closed_inconclusive_ebm_model_characteristics_exhausted`로 닫았다.

효과(effect, 효과): EBM(설명가능 부스팅 머신)은 MQL5(엠큐엘5) score table(점수표) runtime(런타임), feature contribution(피처 기여도), hold axis(보유 축), Tier A/B routing(티어 A/B 라우팅), subtype(하위유형), side compression(방향 압축), follow-up exhaustion(후속 소진) 단서를 보존하지만 edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

Stage20(20단계)는 `20_model_family_challenge__gam_additive_smooth_shape`로 열렸다.

효과(effect, 효과): Stage20(20단계)은 GAM(`Generalized Additive Model`, 일반화 가산 모델) smooth additive effect(부드러운 가산 효과)를 보는 새 topic pivot(주제 전환)이며, 현재 `run14A_gam_additive_shape_scout_v1` Python structural scout(파이썬 구조 탐색)만 완료했다. MT5(`MetaTrader 5`, 메타트레이더5) runtime_probe(런타임 탐침)는 아직 없다.

## Latest Stage19 RUN13T MT5 Axis Extension Update(최신 19단계 실행13T MT5 축 확장 업데이트)

Stage19(19단계)는 `run13T_ebm_mt5_axis_extension_v1`에서 EBM(`Explainable Boosting Machine`, 설명가능 부스팅 머신) feature mask(피처 마스크), hold micro-axis(보유 미세 축), Tier B subtype filter(티어 B 하위유형 필터), hold4 side axis(4봉 방향 축)을 MT5(`MetaTrader 5`, 메타트레이더5)로 더 확인했다.

결과(result, 결과): `inconclusive_ebm_mt5_axis_extension_completed`. best OOS hold(표본외 최고 보유)는 `4`이고 net(순손익)은 `134.3`이다. hold4 long-minus-short(4봉 매수-매도 차이)는 `95.8`이다.

효과(effect, 효과): 1/2/3/4 축을 MT5 런타임까지 밀었지만 edge(거래 우위), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

## Latest Stage19 RUN13M Deep Axis Update(최신 19단계 실행13M 심층 축 업데이트)

Stage19(19단계)는 `run13M_ebm_deep_axis_followup_v1`에서 EBM(`Explainable Boosting Machine`, 설명가능 부스팅 머신) feature mask(피처 마스크), hold axis(보유 축), Tier B subtype(티어 B 하위유형), side axis(방향 축)을 추가로 확인했다.

결과(result, 결과): `inconclusive_ebm_deep_axis_followup_completed`. best requested OOS hold(요청 축 표본외 최고 보유)는 `4`이고 net(순손익)은 `134.3`이다. q90 hold6(q90 6봉) long-minus-short(매수-매도 차이)는 `11.56`이다.

효과(effect, 효과): MT5(`MetaTrader 5`, 메타트레이더5) runtime probe(런타임 탐침)는 더 늘렸지만 edge(거래 우위), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

## Latest Stage19 RUN13H Attribution Update(최신 19단계 실행13H 귀속 업데이트)

Stage19(19단계)는 `run13H_ebm_feature_hold6_routing_attribution_v1`에서 EBM(`Explainable Boosting Machine`, 설명가능 부스팅 머신) feature contribution(피처 기여도), hold6/q90(6봉/q90), Tier A/B routing(티어 A/B 라우팅)을 해부했다.

결과(result, 결과): `inconclusive_ebm_feature_hold6_routing_attribution_completed`. hold6 OOS net(6봉 표본밖 순손익)은 `39.65`지만 validation net(검증 순손익)은 `-188.66`이다.

효과(effect, 효과): EBM(설명가능 부스팅 머신)은 계속 볼 단서가 있지만 edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

## Latest Stage19 RUN13B-RUN13G MT5 Runtime Update(최신 19단계 실행13B-13G MT5 런타임 업데이트)

Stage19(19단계)는 EBM(`Explainable Boosting Machine`, 설명가능 부스팅 머신) RUN13B-RUN13G(실행13B-13G)를 MT5(`MetaTrader 5`, 메타트레이더5) runtime_probe(런타임 탐침)로 실행했다.

결과(result, 결과): `inconclusive_ebm_mt5_runtime_batch_completed`. primary runtime failure(주 런타임 실패): `none(없음)`.

효과(effect, 효과): q90 handoff(q90 인계), q80 density(q80 밀도), q95 sparse tail(q95 희소 꼬리), direction asymmetry(방향 비대칭), hold6/hold18(6봉/18봉 보유) 축을 보존하지만 edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

## Latest Stage19 RUN13A Update(최신 19단계 실행13A 업데이트)

Stage19(19단계)는 EBM(`Explainable Boosting Machine`, 설명가능 부스팅 머신) `run13A_ebm_main_effect_shape_scout_v1`를 Python structural scout(파이썬 구조 탐색)로 완료했다.

효과(effect, 효과): selected variant(선택 변형) `v01_main_effects_broad_bins`와 top shape terms(상위 모양 항)를 보존하지만, MT5(`MetaTrader 5`, 메타트레이더5) runtime_probe(런타임 탐침), edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

## Latest Stage18 Closeout and Stage19-32 Work Order(최신 18단계 종료와 19-32단계 작업서)

Stage18(18단계)은 CatBoost(`Categorical Boosting`, 범주형 부스팅/캣부스트) run12A-run12P(실행12A-실행12P)를 MT5(`MetaTrader 5`, 메타트레이더5)와 KPI(`Key Performance Indicator`, 핵심 성과 지표)까지 확인한 뒤 `closed_inconclusive_catboost_model_characteristics_exhausted`로 닫았다.

효과(effect, 효과): long bias(매수 편향), q85 threshold(q85 임계값), hold6(6봉 보유), high confidence/high margin(높은 확신/높은 여백), low-vol or mid-session(저변동성 또는 중반 세션) 단서는 보존하지만 edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.

Stage19-32(19-32단계) 작업서(work order, 작업서)는 EBM(`Explainable Boosting Machine`, 설명가능 부스팅 머신), GAM(`Generalized Additive Model`, 일반화 가산 모델), ElasticNet Logistic(엘라스틱넷 로지스틱), HMM(`Hidden Markov Model`, 은닉 마르코프 모델), regime classifier(국면 분류기), Survival model(생존 모델), hazard model(위험률 모델), NGBoost(`Natural Gradient Boosting`, 자연 그래디언트 부스팅), quantile boosting(분위수 부스팅), Markov regression(마르코프 회귀), River online ML(리버 온라인 머신러닝), calibration/abstention(보정/기권), TabNet(탭넷), TCN(`Temporal Convolutional Network`, 시간 합성곱 네트워크)을 각각 독립 단계로 잡았다.

효과(effect, 효과): Stage19(19단계)는 CatBoost(캣부스트) continuation(연속 단계)이 아니라 EBM(설명가능 부스팅 머신) 새 model-family question(모델군 질문)으로 시작했고, Stage26-32(26-32단계)는 Stage25(25단계) 이후 future queue(미래 큐)일 뿐이다. 새 stage folder(단계 폴더), run(실행), KPI(`Key Performance Indicator`, 핵심 성과 지표), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않았다.

## Latest Stage18 RUN12D-RUN12M Update(최신 18단계 실행12D-실행12M 업데이트)

Stage18(18단계) CatBoost(`Categorical Boosting`, 범주형 부스팅/캣부스트) 후속 10개 주제를 MT5(`MetaTrader 5`, 메타트레이더5)와 KPI(`Key Performance Indicator`, 핵심 성과 지표)까지 연결했다.

효과(effect, 효과): `inconclusive_catboost_followup_batch_mt5_kpi_completed`로 기록했다. 이 판독은 runtime_probe(런타임 탐침)와 model characteristic read(모델 특성 판독)만 허용하며 edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.
## Latest Stage18 RUN12A-RUN12C Update(최신 18단계 실행12A-실행12C 업데이트)

Stage18(18단계)는 CatBoost(`Categorical Boosting`, 범주형 부스팅/캣부스트) ordered boosting(순서 부스팅) 모델 특성을 세 주제로 MT5(`MetaTrader 5`, 메타트레이더5)와 KPI(`Key Performance Indicator`, 핵심 성과 지표)까지 확인했다.

효과(effect, 효과): `inconclusive_catboost_model_characteristic_mt5_kpi_completed`로 기록했다. run12A(실행12A)는 ordered probability shape(순서 부스팅 확률 모양), run12B(실행12B)는 q80 signal density(q80 신호 밀도), run12C(실행12C)는 direction balance(방향 균형)를 본다. edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.
## Historical Stage18 Topic Open(이전 18단계 주제 개방)

Stage18(18단계)는 `18_model_family_challenge__catboost_ordered_boosting_scout`로 열렸다. 주제는 CatBoost(`Categorical Boosting`, 범주형 부스팅/캣부스트) ordered boosting(순서 부스팅)이다.

효과(effect, 효과): 첫 후보는 `run12A_catboost_ordered_boosting_characteristic_scout_v1`이지만, 아직 run(실행), KPI(`Key Performance Indicator`, 핵심 성과 지표), MT5(`MetaTrader 5`, 메타트레이더5) runtime_probe(런타임 탐침), edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

## Latest Stage17 RUN11G Closeout(최신 17단계 실행11G 마감)

Stage17(17단계)은 `run11G_xgb_dart_attribution_closeout_v1`에서 DART(`Dropouts meet Multiple Additive Regression Trees`, 드롭아웃 부스팅) 귀속을 확인하고 닫혔다.

효과(effect, 효과): Stage18(18단계)는 CatBoost(캣부스트) ordered boosting(순서 부스팅) 주제로 열렸다. Stage17(17단계)은 edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)를 만들지 않고 닫혔다.
## Latest Stage17 RUN11F Update(최신 17단계 실행11F 업데이트)

Stage17(17단계)은 `run11F_xgb_dart_booster_probe_v1`로 DART(`Dropouts meet Multiple Additive Regression Trees`, 드롭아웃 부스팅) 내부 부스터 축을 MT5(`MetaTrader 5`, 메타트레이더5)와 KPI(`Key Performance Indicator`, 핵심 성과 지표)까지 확인했다.

효과(effect, 효과): DART ONNX(`Open Neural Network Exchange`, 오픈 뉴럴 네트워크 교환) weight_drop(드롭 가중치) 동등성을 보정한 뒤 `keep_stage17_open_for_dart_followup_attribution`로 기록했다. edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.
## Latest Stage17 RUN11E Closeout(최신 17단계 실행11E 마감)

Stage17(17단계)은 `run11E_xgb_feature_driver_saturation_v1`에서 새 feature driver(피처 동인)가 더 보이지 않아 closeout(마감)했다.

효과(effect, 효과): XGBoost(`Extreme Gradient Boosting`, 익스트림 그래디언트 부스팅) 특성 단서는 보존하지만 edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.
## Latest Stage17 RUN11D Update(최신 17단계 실행11D 업데이트)

Stage17(17단계)은 `run11D_xgb_trade_shape_attribution_v1`으로 XGBoost(`Extreme Gradient Boosting`, 익스트림 그래디언트 부스팅) trade shape attribution(거래 모양 귀속)을 완료했다.

효과(effect, 효과): run11C의 MT5(`MetaTrader 5`, 메타트레이더5) KPI(`Key Performance Indicator`, 핵심성과지표) 근거를 재사용했고 `keep_stage17_open_for_probability_feature_driver_probe`로 판독했다. edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.
# Current Working State

- updated_on: `2026-05-05`
- project_mode: `clean_stage_restart`
- active_stage: `22_regime_model__hmm_hidden_state_segmentation(22단계 HMM 은닉 상태 분할)`
- active_branch: `codex/stage22-hmm-hidden-state`
- current run(현재 실행): `run16A_hmm_hidden_state_segmentation_scout_v1`

## Latest Stage Transition Update(최신 단계 전환 업데이트)

Stage16(16단계)는 QDA(`Quadratic Discriminant Analysis`, 이차 판별 분석) `run08A`~`run10L` exploration(탐색)을 MT5(`MetaTrader 5`, 메타트레이더5) runtime_probe(런타임 탐침)와 KPI(`Key Performance Indicator`, 핵심성과지표) 정규화까지 검토하고 닫았다.

효과(effect, 효과): recommendation(권고)은 `close_stage16_preserve_qda_clues`로 확정했다. 이 closeout(종료 기록)은 QDA(이차 판별 분석) 단서를 보존하지만 edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.

Stage17(17단계)는 `17_model_family_challenge__xgboost_regularized_boosting_scout`로 XGBoost(`Extreme Gradient Boosting`, 익스트림 그래디언트 부스팅) regularized boosting(규제 부스팅) 주제를 끝까지 탐색하고 `run11G_xgb_dart_attribution_closeout_v1`에서 닫았다.

효과(effect, 효과): run11A~run11G(실행11A~실행11G)의 MT5(`MetaTrader 5`, 메타트레이더5)와 KPI(`Key Performance Indicator`, 핵심성과지표) 근거를 Stage17(17단계) 보존 단서로 남기고, baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.
## Latest Stage17 RUN11A Update(최신 17단계 실행11A 업데이트)

Stage17(17단계)은 `run11A_xgb_regularized_boosting_characteristic_scout_v1`로 XGBoost(`Extreme Gradient Boosting`, 익스트림 그래디언트 부스팅) 특성을 MT5(`MetaTrader 5`, 메타트레이더5) runtime_probe(런타임 탐침)와 KPI(`Key Performance Indicator`, 핵심성과지표)까지 연결했다.

효과(effect, 효과): `inconclusive_xgboost_characteristic_mt5_runtime_probe_completed`로 기록했다. XGBoost 특성은 보였지만, edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.
## Latest Stage17 Closeout Update(최신 17단계 마감 업데이트)

Stage17(17단계)은 run11B(실행11B) closeout(마감)을 성급한 판정으로 낮추고 run11C(실행11C) 방향 비대칭 탐침을 완료했다.

효과(effect, 효과): `closed_inconclusive_xgboost_frequency_pressure_runtime_probe_evidence`로 기록했다. edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.
## Latest Stage17 RUN11C Update(최신 17단계 실행11C 업데이트)

Stage17(17단계)은 `run11C_xgb_q80_direction_asymmetry_probe_v1`로 XGBoost(`Extreme Gradient Boosting`, 익스트림 그래디언트 부스팅) direction asymmetry(방향 비대칭)를 MT5(`MetaTrader 5`, 메타트레이더5)와 KPI(`Key Performance Indicator`, 핵심성과지표)까지 확인했다.

효과(effect, 효과): run11B(실행11B)의 성급한 closeout(마감)을 교정하고 `close_stage17_no_new_direction_characteristic_after_run11C`로 기록했다. edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.
## 쉬운 설명(Plain Read, 쉬운 설명)

프로젝트는 clean stage restart(깨끗한 단계 재시작) 이후 Stage 02~09(2~9단계)를 닫았다.

효과(effect, 효과): Stage 10(10단계)은 `run01Y/run01Z/run01AA/run01AB/run01AC(실행 01Y/01Z/01AA/01AB/01AC)` 200~220 closeout(마감) runtime_probe(런타임 탐침)로 닫혔다. Stage 11(11단계)은 `RUN02A~RUN02S(실행 02A~02S)` LGBM(`LightGBM`, 라이트GBM) training/threshold/divergent/idea burst/salvage extension scouts(학습/임계값/발산형/아이디어 무더기/회수 확장 탐색)를 MT5(`MetaTrader 5`, 메타트레이더5) runtime_probe(런타임 탐침)까지 실행했고, `RUN02T~RUN02V(실행 02T~02V)` priority structural probe(우선순위 구조 탐침)로 다음 방향을 좁혔다. `RUN02W(실행 02W)`는 fwd18(90분) 재학습을 MT5 runtime_probe(런타임 탐침)까지 확인했고, `RUN02X~RUN02Z(실행 02X~02Z)`는 fwd18 rank/inverse/context(90분 순위/역방향/문맥) 축을 판 결과다. `RUN02AA~RUN02AK(실행 02AA~02AK)`는 그 중심 표면의 ADX/routing/session stress(ADX/라우팅/세션 압박)를 완료했다. `run01Y(실행 01Y)`는 seed surface(씨앗 표면)와 comparison reference(비교 참고 표면)로만 둔다.

Stage 11(11단계)은 `stage11_alpha_robustness_closeout_packet_v1`로 닫혔다. Stage 12(12단계)는 ExtraTrees(`ExtraTrees`, 엑스트라 트리) standalone experiment(단독 실험)로 열렸고, `stage12_model_family_challenge_closeout_v1`로 닫혔다. `RUN03A(실행 03A)`는 Stage 10/11(10/11단계) 표면을 끌고 와서 `invalid_for_standalone_scope(단독 범위 무효)`로 낮췄고, `RUN03D(실행 03D)`는 source batch20 Python package(원천 20개 묶음 파이썬 패키지), `RUN03H(실행 03H)`는 all-variant MT5 runtime_probe(전체 변형 MT5 런타임 탐침), `RUN03J(실행 03J)`는 rolling WFO split probe(구르는 워크포워드 분할 탐침), `RUN03K~RUN03S(실행 03K~03S)`는 실패/회수 기억을 남긴 탐색 사례다.

아직 alpha result(알파 결과), alpha quality(알파 품질), live readiness(실거래 준비), operating promotion(운영 승격)은 없다.

## 닫힌 기반 진실(Closed Foundation Truth, 닫힌 기반 진실)

Stage 02(2단계)는 첫 shared feature frame freeze(공유 피처 프레임 동결 산출물)를 물질화했다.

- dataset_id(데이터셋 ID): `dataset_fpmarkets_v2_us100_m5_20220901_20260413_cashopen_fullcash_valid_freeze01`
- selected rows(선택 행 수): `54439`
- feature order hash(피처 순서 해시): `fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2`

Stage 03(3단계)는 첫 training label/split(학습 라벨/분할)을 물질화했다.

- training_dataset_id(학습 데이터셋 ID): `training_fpmarkets_v2_us100_m5_label_v1_fwd12_m5_logret_train_q33_3class_split_v1`
- train/validation/OOS(학습/검증/표본외): `29222/9844/7584`

Stage 04(4단계)는 MT5 price-proxy monthly top3 weights(MT5 가격 대리 월별 top3 가중치)와 58 feature(58개 피처) model input(모델 입력)을 물질화했다.

- model_input_dataset_id(모델 입력 데이터셋 ID): `model_input_fpmarkets_v2_us100_m5_label_v1_fwd12_split_v1_proxyw58_feature_set_v2`
- included features(포함 피처): `58`
- boundary(경계): price-proxy weights(가격 대리 가중치)는 actual NDX/QQQ weights(실제 NDX/QQQ 가중치)가 아니다.

Stage 05(5단계)는 feature integrity audit(피처 무결성 감사)를 닫았다.

- run_id(실행 ID): `20260425_stage05_feature_integrity_audit_v1`
- judgment(판정): `positive_feature_integrity_audit_passed`
- boundary(경계): feature integrity evidence(피처 무결성 근거)이지 model quality(모델 품질)가 아니다.

Stage 06(6단계)는 minimum fixture set(최소 표본 묶음) 기준 Python/MT5 runtime parity(파이썬/MT5 런타임 동등성)를 닫았다.

- run_id(실행 ID): `20260425_stage06_runtime_parity_closed_v1`
- judgment(판정): `positive_runtime_parity_passed`
- max abs diff(최대 절대 차이): `0.0000017512503873717833`
- boundary(경계): Stage 06(6단계) 최소 표본 묶음의 runtime authority(런타임 권위)이지 model quality(모델 품질)나 operating promotion(운영 승격)이 아니다.

Stage 07(7단계)는 baseline training smoke(기준선 학습 스모크)를 닫았다.

- run_id(실행 ID): `20260425_stage07_baseline_training_smoke_v1`
- model artifact id(모델 산출물 ID): `model_fpmarkets_v2_stage07_logreg_smoke_v1`
- validation accuracy(검증 정확도): `0.45672490857375053`
- OOS accuracy(표본외 정확도): `0.457542194092827`
- boundary(경계): Python-side training pipeline evidence(파이썬 측 학습 처리 흐름 근거)이지 alpha quality(알파 품질)가 아니다.

Stage 08(8단계)는 alpha entry protocol(알파 진입 규칙)과 Tier A/B reporting rule(티어 A/B 보고 규칙)을 닫았다.

- packet_id(묶음 ID): `stage08_alpha_entry_protocol_v1`
- status(상태): `reviewed_closed_handoff_to_stage09_complete_with_alpha_entry_protocol`
- policy(정책): `docs/policies/alpha_entry_protocol.md`
- report template(보고 틀): `docs/templates/alpha_exploration_report_template.md`
- boundary(경계): Stage 08(8단계)은 alpha result(알파 결과), alpha quality(알파 품질), live readiness(실거래 준비), operating promotion(운영 승격)을 만들지 않았다.

Stage 09(9단계)는 pre-alpha handoff packet(알파 전 인계 묶음)을 닫았다.

- packet_id(묶음 ID): `stage09_pre_alpha_handoff_packet_v1`
- status(상태): `reviewed_closed_handoff_to_stage10_complete_with_pre_alpha_handoff_packet`
- packet(묶음): `stages/09_pre_alpha_handoff__registry_publish_packet/03_reviews/pre_alpha_handoff_packet.md`
- decision(결정): `docs/decisions/2026-04-25_stage09_pre_alpha_handoff.md`
- boundary(경계): Stage 09(9단계)는 registry/current truth/publish boundary(등록부/현재 진실/게시 경계)를 닫았지만 alpha result(알파 결과)를 만들지 않았다.

## 현재 단계(Current Stage, 현재 단계)

`20_model_family_challenge__gam_additive_smooth_shape`

Stage20(20단계)의 질문(question, 질문)은 GAM(`Generalized Additive Model`, 일반화 가산 모델)이 smooth additive effect(부드러운 가산 효과)를 만들고, Stage19(19단계) EBM(`Explainable Boosting Machine`, 설명가능 부스팅 머신) 단서를 baseline(기준선)으로 상속하지 않고 새 모델 특성을 볼 수 있는지다.

효과(effect, 효과): Stage20(20단계)는 `run14A_gam_additive_shape_scout_v1` Python structural scout(파이썬 구조 탐색)를 완료했지만, MT5 runtime_probe(MT5 런타임 탐침)와 closeout(마감)은 아직 만들지 않았다. 작업서(work order, 작업서)는 기존 경로 `docs/workspace/stage19_25_model_research_work_order.md`에 두며, 내용은 Stage19-32(19-32단계)까지 확장됐다.

## 탐색 원칙(Exploration Rule, 탐색 원칙)

`Tier A(티어 A)`와 `Tier B(티어 B)`는 탐색 게이트(exploration gate, 탐색 제한문)가 아니다.

둘 다 완전히 탐색할 수 있다. 티어(tier, 티어)는 sample label(표본 라벨)이다.

효과(effect, 효과): 보고서(report, 보고서)는 무엇을 탐색했는지 정직하게 라벨링(labeling, 라벨링)하되, 티어(tier, 티어)를 아이디어 승인이나 거절로 쓰지 않는다.

Stage 10(10단계) 이후 alpha exploration run(알파 탐색 실행)은 Tier A(티어 A), Tier B(티어 B), Tier A+B combined(Tier A+B 합산)를 함께 남긴다.

MT5(`MetaTrader 5`, 메타트레이더5) routed run(라우팅 실행)에서는 이 뜻이 `Tier A primary(티어 A 우선)`, `Tier B fallback(티어 B 대체)`, `actual routed total(실제 라우팅 전체)`이다.

효과(effect, 효과): Tier A(티어 A)만 본 결과가 전체 alpha read(알파 판독)처럼 남지 않고, Tier B(티어 B)가 실제로 메운 구간과 전체 라우팅 결과를 같은 실행(run, 실행)에서 비교한다.

알파 단계 전환(alpha stage transition, 알파 단계 전환)은 baseline selection(기준선 선택)이 아니라 topic pivot(주제 전환)이다.

효과(effect, 효과): closeout(마감)은 seed surface(씨앗 표면), preserved clue(보존 단서), negative memory(부정 기억), invalid setup(무효 설정), blocked retry(차단 재시도)를 정리한다. 별도 promotion/operating packet(승격/운영 작업 묶음) 없이는 baseline(기준선)이나 operating reference(운영 기준)를 만들지 않는다.

Stage 10(10단계)의 기본 레인(lane, 레인)은 `exploration(탐색)`이고 첫 경계(boundary, 경계)는 `single_split_scout(단일 분할 탐색 판독)`다.

## 닫힌 Stage 10 묶음(Closed Stage 10 Packet, 닫힌 Stage 10 묶음)

`run01Y_run01AC_logreg_a_base_no_fallback_200_220_hold_threshold_closeout_v1`

- included runs(포함 실행): `run01Y hold9 base(9봉 기준)`, `run01Z hold6(6봉)`, `run01AA hold12(12봉)`, `run01AB margin0.025(마진 0.025)`, `run01AC strict probability(엄격 확률)`
- routing mode(라우팅 방식): `tier_a_primary_no_fallback`
- routed fallback enabled(라우팅 대체 사용): `false`
- seed/reference Tier A rule(씨앗/참고 Tier A 규칙): `short0.600_long0.450_margin0.000`
- seed/reference max hold bars(씨앗/참고 최대 보유 봉 수): `9`
- session slice(시간대 조각): `200 < minutes_from_cash_open <= 220`
- boundary(경계): `runtime_probe(런타임 탐침)`

효과(effect, 효과): run01Y(실행 01Y)의 좋은 점이 hold(보유)나 threshold(임계값) 한 점에만 묶였는지 확인했다.

MT5(`MetaTrader 5`, 메타트레이더5) 결과는 다음과 같다.

| run(실행) | slice/routing(구간/라우팅) | validation net/PF(검증 순수익/수익 팩터) | OOS net/PF(표본외 순수익/수익 팩터) | OOS DD/recovery(표본외 손실/회복) |
|---:|---:|---:|---:|---:|
| run01Y(실행 01Y) | hold9(9봉), base(기준) | `318.48 / 3.88` | `313.14 / 3.99` | `144.65 / 2.16` |
| run01Z(실행 01Z) | hold6(6봉), base(기준) | `264.14 / 2.99` | `109.65 / 1.66` | `161.79 / 0.68` |
| run01AA(실행 01AA) | hold12(12봉), base(기준) | `447.76 / 4.55` | `225.69 / 2.57` | `170.11 / 1.33` |
| run01AB(실행 01AB) | hold9(9봉), margin0.025(마진 0.025) | `318.48 / 3.88` | `313.14 / 3.99` | `144.65 / 2.16` |
| run01AC(실행 01AC) | hold9(9봉), strict probability(엄격 확률) | `143.91 / 2.30` | `219.09 / 5.53` | `147.09 / 1.49` |

효과(effect, 효과): run01Y(실행 01Y)가 현재 순수익(net profit, 순수익)과 recovery(회복계수)의 균형이 가장 좋다. hold6(6봉 보유)은 약하고, hold12(12봉 보유)는 validation(검증)은 좋아지지만 OOS(표본외)가 줄었다. margin0.025(마진 0.025)는 결과가 같아서 실제로 조건을 줄이지 못했고, strict probability(엄격 확률)는 OOS PF(표본외 수익 팩터)는 높지만 net/recovery(순수익/회복)가 낮아졌다.

Tier B fallback-only(Tier B 대체 구간 단독)는 run01Y/run01Z/run01AA/run01AB/run01AC(실행 01Y/01Z/01AA/01AB/01AC)에서 validation/OOS(검증/표본외) 모두 거래가 없었다.

효과(effect, 효과): 현재 해석(current interpretation, 현재 해석)에서 이번 closeout(마감)은 `200~220` 구간의 run01Y(실행 01Y)를 Stage 11(11단계)의 seed surface(씨앗 표면)와 reference surface(참고 표면)로 보존한다. baseline(기준선), alpha quality(알파 품질), operating promotion(운영 승격)은 아니다.

## 현재 Stage 11 상태(Current Stage 11 State, 현재 Stage 11 상태)

- status(상태): `reviewed_closed_no_next_stage_opened`
- current run packet(현재 실행 묶음): `run02AA_run02AK_fwd18_rank_stress_packet_v1`
- model family(모델 계열): `lightgbm_lgbmclassifier_multiclass`
- seed/reference surface(씨앗/참고 표면): `run01Y_logreg_a_base_no_fallback_hold9_session_mid_second_overlap_200_220_v1`
- selected slice(선택 구간): `200 < minutes_from_cash_open <= 220`
- selected hold(선택 보유): `9`
- selected threshold(선택 임계값): `a_tier_a_rankq0.960_short0.571_long0.654_margin0.120__b_tier_b_rankq0.960_short0.413_long0.457_margin0.080__hold9__slice_mid_second_overlap_200_220__model_lgbm_rank_target_inverse__ctx_di_spread_abs_lte8_adx_lte25`
- threshold method(임계값 방식): `rank-target quantile(순위 기반 분위수)`
- external verification status(외부 검증 상태): `completed(완료)`

stress packet(압박 묶음): `run02AA_run02AK_fwd18_rank_stress_packet_v1`
closeout packet(마감 묶음): `stage11_alpha_robustness_closeout_packet_v1`

효과(effect, 효과): RUN02Z(실행 02Z)의 중심 조건 `ADX<=25`, `200-220`, routed fallback(라우팅 대체)이 ADX/routing/session stress(ADX/라우팅/세션 압박)에서 가장 균형적으로 남았다. 하지만 거래 수가 작아서 alpha quality(알파 품질)나 promotion_candidate(승격 후보)는 아니다.

Stage 11(11단계)은 Stage 10(10단계) baseline(기준선)을 검증한 단계가 아니라 LightGBM(라이트GBM), label horizon(라벨 예측수평선), rank/context(순위/문맥)을 판 topic pivot(주제 전환) 단계다.

RUN02A(실행 02A)는 같은 run01Y(실행 01Y) threshold/slice/hold(임계값/구간/보유)를 LightGBM(라이트GBM)에 그대로 적용한 training-method scout(학습방법 탐색)다.

RUN02B(실행 02B)는 RUN01(실행 01)의 absolute grid(절대값 격자)를 반복하지 않고, RUN02A(실행 02A)의 LightGBM(라이트GBM) 확률 분포에서 validation quantile rank(검증 분위수 순위)로 임계값을 다시 정했다.

| view(보기) | rows(행) | signal count(신호 수) | signal coverage(신호 비율) | short/long(숏/롱) |
|---|---:|---:|---:|---:|
| Tier A separate(Tier A 분리) | `2884` | `338` | `0.11719833564493759` | `149/189` |
| Tier B separate(Tier B 분리) | `696` | `123` | `0.17672413793103448` | `38/85` |
| Tier A+B combined(Tier A+B 합산) | `3580` | `461` | `0.12877094972067038` | `187/274` |

효과(effect, 효과): RUN02B(실행 02B)는 RUN02A(실행 02A)보다 combined signal coverage(합산 신호 비율)를 `0.20642458100558658`에서 `0.12877094972067038`로 줄였지만, 거래 KPI(핵심 성과 지표)는 회복하지 못했다.

MT5(`MetaTrader 5`, 메타트레이더5) 결과는 다음과 같다.

| run(실행) | method(방식) | validation net/PF(검증 순수익/수익 팩터) | OOS net/PF(표본외 순수익/수익 팩터) | OOS DD/recovery(표본외 손실/회복) |
|---|---|---:|---:|---:|
| RUN02A(실행 02A) | run01Y absolute threshold(run01Y 절대 임계값) | `-496.88 / 0.25` | `-27.44 / 0.94` | `249.28 / -0.11` |
| RUN02B(실행 02B) | LGBM rank-target threshold(LGBM 순위 기반 임계값) | `-496.45 / 0.23` | `-92.09 / 0.76` | `293.51 / -0.31` |

RUN02C~RUN02F(실행 02C~02F)는 RUN01(실행 01)식 근처 튜닝을 피하고 direction/confidence/context(방향/확신/문맥)으로 발산시킨 묶음이다.

| run(실행) | idea(아이디어) | validation net/PF(검증 순수익/수익 팩터) | OOS net/PF(표본외 순수익/수익 팩터) | read(판독) |
|---|---|---:|---:|---|
| RUN02C(실행 02C) | long-only(롱만) | `-154.01 / 0.68` | `82.69 / 1.35` | OOS(표본외) 회수 가치는 있으나 validation(검증)이 약함 |
| RUN02D(실행 02D) | short-only(숏만) | `-18.33 / 0.89` | `-211.48 / 0.31` | short-only(숏만)는 OOS(표본외)에서 약함 |
| RUN02E(실행 02E) | extreme confidence(극단 확신) | `-115.17 / 0.31` | `-6.35 / 0.96` | OOS(표본외)는 거의 본전이나 validation(검증)이 약함 |
| RUN02F(실행 02F) | calm trend context gate(차분한 추세 문맥 제한) | `-234.03 / 0.46` | `-163.22 / 0.41` | 현재 문맥 제한 조건은 실패 |

효과(effect, 효과): RUN02C(실행 02C)와 RUN02E(실행 02E)는 회수 가치(salvage value, 회수 가치)를 남겼지만, 둘 다 validation/OOS(검증/표본외)를 동시에 회복하지 못했다. 그래서 지금은 LGBM(라이트GBM) 세부 조정보다 새 label/model/context(라벨/모델/문맥) 축을 여는 쪽이 낫다.

RUN02G~RUN02P(실행 02G~02P)는 RUN02C/RUN02E(실행 02C/02E)의 회수 가치를 바로 세부 탐색하지 않고, context/direction/confidence(문맥/방향/확신) 아이디어 10개로 더 넓게 발산시킨 묶음이다.

| run(실행) | idea(아이디어) | validation net/PF(검증 순수익/수익 팩터) | OOS net/PF(표본외 순수익/수익 팩터) | read(판독) |
|---|---|---:|---:|---|
| RUN02G(실행 02G) | long pullback(롱 되돌림) | `-138.39 / 0.54` | `238.68 / 3.44` | OOS(표본외) 회수 가치는 큼, validation(검증)은 약함 |
| RUN02H(실행 02H) | bull trend long(상승 추세 롱) | `-210.68 / 0.19` | `11.52 / 1.21` | 작은 OOS(표본외) 양수, validation(검증) 약함 |
| RUN02I(실행 02I) | low-vol extreme confidence(저변동성 극단 확신) | `-509.12 / 0.00` | `-231.42 / 0.00` | 실패 |
| RUN02J(실행 02J) | balanced midband(균형 중간대) | `70.10 / 1.29` | `-121.32 / 0.55` | validation(검증)만 양수 |
| RUN02K(실행 02K) | quiet return z-score(조용한 수익률 z점수) | `-496.54 / 0.02` | `-494.23 / 0.19` | 실패 |
| RUN02L(실행 02L) | range compression(횡보 압축) | `-352.49 / 0.34` | `-250.36 / 0.05` | 실패 |
| RUN02M(실행 02M) | high-vol momentum alignment(고변동성 모멘텀 정렬) | `-496.38 / 0.25` | `-305.93 / 0.31` | 실패 |
| RUN02N(실행 02N) | squeeze breakout(압축 돌파) | `-125.51 / 0.62` | `107.14 / 55.11` | OOS(표본외) 회수 가치는 있으나 거래 수 3개 |
| RUN02O(실행 02O) | bull vortex long(상승 보텍스 롱) | `-86.88 / 0.55` | `6.04 / 1.20` | 작은 OOS(표본외) 양수, validation(검증) 약함 |
| RUN02P(실행 02P) | bear vortex short(하락 보텍스 숏) | `1.78 / 1.02` | `24.33 / 1.37` | 양쪽 모두 양수지만 규모가 작아 불충분 |

효과(effect, 효과): RUN02G/RUN02N/RUN02P(실행 02G/02N/02P)는 회수 가치(salvage value, 회수 가치)를 남겼다. 하지만 RUN02G/RUN02N(실행 02G/02N)은 validation(검증)이 약하고, RUN02P(실행 02P)는 순수익(net profit, 순수익)과 거래 수가 작아서 아직 세부 탐색 후보일 뿐이다.

RUN02Q~RUN02S(실행 02Q~02S)는 위 세 가지 회수 후보를 동시에 더 파본 salvage extension(회수 확장) 묶음이다.

| run(실행) | idea(아이디어) | signals A/B/AB(신호 A/B/합산) | validation net/PF(검증 순수익/수익 팩터) | OOS net/PF(표본외 순수익/수익 팩터) | read(판독) |
|---|---|---:|---:|---:|---|
| RUN02Q(실행 02Q) | bear vortex short density(하락 보텍스 숏 밀도 확대) | `83/5/88` | `-139.28 / 0.62` | `-140.58 / 0.54` | 신호 밀도는 늘었지만 validation/OOS(검증/표본외)가 모두 음수 |
| RUN02R(실행 02R) | long pullback ADX repair(롱 되돌림 ADX 복구) | `51/3/54` | `275.78 / 2.44` | `-82.01 / 0.74` | validation(검증)은 복구됐지만 OOS(표본외)가 실패 |
| RUN02S(실행 02S) | squeeze density(압축 밀도 확대) | `19/7/26` | `-2.50 / 0.99` | `32.56 / 1.69` | 가장 가까운 생존 신호지만 거래 수가 작음 |

효과(effect, 효과): RUN02S(실행 02S)는 약한 회수 가치(weak salvage value, 약한 회수 가치)로 보존한다. RUN02Q(실행 02Q)는 bear-vortex short(하락 보텍스 숏)을 느슨하게 넓히면 손상이 커진다는 부정 기억(negative memory, 부정 기억)이고, RUN02R(실행 02R)는 validation-only repair(검증만 복구)로 남긴다.

RUN02T~RUN02V(실행 02T~02V)는 우선순위(priority, 우선순위) 1/2/3을 구조 탐침(structural probe, 구조 탐침)으로 정리한 묶음이다.

| run(실행) | priority(우선순위) | source(원천) | primary read(핵심 판독) | judgment(판정) |
|---|---:|---|---|---|
| RUN02T(실행 02T) | 1 | RUN02S(실행 02S) | fwd18(90분) OOS hit rate(표본외 적중률) `0.714286`, fwd12(60분)는 `0.285714`, 비교 가능 OOS 신호 `7`개 | `horizon_shift_worth_retraining_probe` |
| RUN02U(실행 02U) | 2 | RUN02S(실행 02S) | OOS(표본외) window(구간) 3개 모두 신호는 있지만 총 신호 `10`개뿐 | `wfo_lite_density_insufficient_for_full_wfo` |
| RUN02V(실행 02V) | 3 | RUN02P/RUN02Q(실행 02P/02Q) | RUN02Q(실행 02Q)는 RUN02P(실행 02P)보다 숏 신호가 `2.1x`지만 OOS 숏 hit rate(표본외 숏 적중률)는 `0.190476`로 낮음 | `short_specific_probe_inconclusive` |

효과(effect, 효과): 당시 판독은 full WFO(전체 워크포워드 최적화)보다 fwd18 label horizon(90분 라벨 예측수평선) 재학습 탐침의 정보량이 컸다는 것이다. 이 질문은 RUN02W~RUN02AK(실행 02W~02AK) 안에서 닫혔다.

RUN02W(실행 02W)는 그 1순위 질문을 MT5(메타트레이더5)까지 연결한 fwd18 retrain runtime_probe(fwd18 재학습 런타임 탐침)이다.

| view(보기) | validation net/PF(검증 순수익/수익 팩터) | OOS net/PF(표본외 순수익/수익 팩터) | read(판독) |
|---|---:|---:|---|
| Tier A only(Tier A 단독) | `-495.84 / 0.28` | `-132.97 / 0.75` | negative(부정) |
| Tier B fallback-only(Tier B 대체 단독) | `197.17 / 8.31` | `-105.73 / 0.70` | validation-only(검증만 양수) |
| Routed total(라우팅 전체) | `-496.25 / 0.28` | `-216.12 / 0.67` | negative(부정) |

효과(effect, 효과): fwd18(90분) 라벨만 바꾸는 단순 재학습은 MT5 거래 품질을 회복하지 못했다. 하지만 invalid(무효)는 아니며, fwd18 + context/rank threshold(문맥/순위 임계값) 확인으로 이어진 Stage 11(11단계) 내부 근거다.

RUN02X~RUN02Z(실행 02X~02Z)는 fwd18 + context/rank threshold(fwd18 + 문맥/순위 임계값)를 실제로 더 판 묶음이다.

| run(실행) | method(방식) | validation read(검증 판독) | OOS read(표본외 판독) | meaning(의미) |
|---|---|---:|---:|---|
| RUN02X(실행 02X) | direct fwd18 rank threshold(직접 fwd18 순위 임계값) | Tier A q96 hit(적중률) `0.25` | Tier A q96 hit(적중률) `0.15625` | direct(직접) 방향은 약함 |
| RUN02Y(실행 02Y) | inverse fwd18 rank threshold(역방향 fwd18 순위 임계값) | Tier A q96 hit(적중률) `0.604167` | Tier A q96 hit(적중률) `0.34375` | inverse(역방향)만으로는 부족 |
| RUN02Z(실행 02Z) | inverse rank + DI/ADX context(역방향 순위 + DI/ADX 문맥) | MT5 routed(라우팅) `386.06 / 7.25 / 9 trades(거래)` | MT5 routed(라우팅) `352.63 / 52.03 / 5 trades(거래)` | 작은 표본 양수 런타임 탐침 |

효과(effect, 효과): RUN02Z(실행 02Z)는 fwd18(90분) 모델이 고확신으로 말한 방향을 그대로 믿는 게 아니라, DI spread/ADX(DI 차이/ADX)가 낮은 문맥에서 inverse(역방향)로 쓰면 거래 품질이 살아날 수 있다는 첫 MT5(메타트레이더5) 단서를 남겼다. 다만 validation(검증) `9`거래, OOS(표본외) `5`거래라 아직 promotion_candidate(승격 후보)나 alpha quality(알파 품질)가 아니다.

RUN02AA~RUN02AK(실행 02AA~02AK)는 RUN02Z(실행 02Z)를 압박한 묶음이다.

| axis(축) | best read(최고 판독) | weak read(약한 판독) | meaning(의미) |
|---|---|---|---|
| ADX cutoff(ADX 절단값) | `ADX<=25` RUN02Z(실행 02Z) OOS `352.63 / 52.03 / 5 trades(거래)` | `ADX<=20` RUN02AA(실행 02AA) OOS `31.62 / 2.80 / 2 trades(거래)` | 너무 좁히면 OOS(표본외)가 마른다 |
| routing(라우팅) | routed(라우팅) RUN02Z(실행 02Z) OOS `352.63 / 5 trades(거래)` | Tier A-only(Tier A 단독) RUN02AD(실행 02AD) OOS `241.95 / 2 trades(거래)` | Tier B fallback(Tier B 대체)이 밀도와 순수익을 보탠다 |
| session slice(세션 구간) | `200-220` RUN02Z(실행 02Z) OOS `352.63 / 52.03` | `190-210` RUN02AI(실행 02AI)는 validation-heavy(검증 치우침) | 중심 구간 유지가 낫다 |

효과(effect, 효과): Stage 11(11단계) 안에서는 `ADX<=25`, routed(라우팅), `200-220` 중심이 가장 값진 닫힌 단서로 남는다. 표본이 작아서 운영 의미(operational meaning, 운영 의미)는 없다.

## 현재 Stage 12 상태(Current Stage 12 State, 현재 Stage 12 상태)

- 상태(status, 상태): `reviewed_closed_no_next_stage_opened(검토 후 닫힘, 다음 단계 미개방)`.
- 현재 묶음(current packet, 현재 묶음): `stage12_model_family_challenge_closeout_v1`.
- Stage12 latest historical run(Stage12 최신 과거 실행): `run03S_et_probability_shape_attribution_probe_v1`.
- 독립 경계(standalone boundary, 독립 경계): Stage10/11(10/11단계) 모델, 임계값, 기준선, 승격 이력은 사용하지 않는다.
- 원천 Python 패키지(source Python package, 원천 파이썬 패키지): `run03D_et_standalone_batch20_v1`.
- 주요 MT5 근거(main MT5 evidence, 주요 MT5 근거): `RUN03H~RUN03S(실행 03H~03S)`.
- 보존 단서(preserved clues, 보존 단서): `RUN03L(최근성 가중)`, `RUN03O(추세/횡보)`, `RUN03Q(위험선호 표본외)`.
- 부정 기억(negative memory, 부정 기억): ExtraTrees(엑스트라 트리) standalone(단독) 계열은 반복 WFO(워크포워드 최적화)에서 강한 안정성을 만들지 못했다.
- 선택 없음(no selection, 선택 없음): operating reference(운영 기준), promotion candidate(승격 후보), baseline(기준선), runtime authority(런타임 권위)는 만들지 않았다.
- Stage13 folder(Stage13 폴더): 이후 독립 MLP(다층 퍼셉트론) 주제로 열고 닫았다.
- 효과(effect, 효과): Stage12(12단계)는 탐색 사례와 실패 데이터를 남기고 닫혔고, Stage13(13단계)은 별도 모델 계열 탐색으로 보존되었다.


## 현재 KPI 재구축/운영 포맷 상태(Current KPI Rebuild / Operating Format State, 현재 KPI 재구축 / 운영 포맷 상태)

- 운영 포맷(operating format, 운영 포맷): `work_packet(작업 묶음)`, `run_plan(실행 계획)`, `skill_receipt(스킬 영수증)`, `KPI source authority(KPI 원천 권위)`, `n/a reason(해당없음 사유)` 계약이 물질화됐다.
- 목록 묶음(inventory packet, 목록 묶음): `kpi_rebuild_inventory_v1`, 대상 실행(target runs, 대상 실행) `70`.
- MT5 기록 묶음(MT5 recording packet, MT5 기록 묶음): `kpi_rebuild_mt5_recording_v1`, MT5 보고서 확인 실행 `65 / 70`, normalized KPI rows(정규화 KPI 행) `448`.
- MT5 실행 묶음(MT5 execution packet, MT5 실행 묶음): `kpi_rebuild_mt5_execution_v1`, 추가 테스터 실행 `22 / 22` 완료, 차단 실행(blocked runs, 차단 실행) `5`.
- 거래 귀속 묶음(trade attribution packet, 거래 귀속 묶음): `kpi_trade_attribution_v1`, 거래 귀속 필요 행 `266`, 채운 행 `241`, zero-trade rows(거래 0개 행) `25`, trade-level rows(거래 단위 행) `15,803`, parser errors(파서 오류) `0`.
- 티어 균형 보강 묶음(tier-balance completion packet, 티어 균형 보강 묶음): `kpi_tier_balance_completion_v1`, 보강 실행 `6 / 6`, MT5 시도 `36 / 36`, normalized KPI rows(정규화 KPI 행) `60`, trade attribution rows(거래 귀속 행) `35`, trade-level rows(거래 단위 행) `1,837`, parser errors(파서 오류) `0`.
- 런타임 근거 정리(runtime evidence cleanup, 런타임 근거 정리): `p0p1_runtime_evidence_cleanup`은 `routing_receipt(라우팅 영수증)`만 있는 병합된 코드/근거 정리다. 효과(effect, 효과)는 runtime evidence wiring(런타임 근거 배선)을 개선하지만, full closeout packet(전체 마감 묶음)이나 새 MT5 실행 결과를 뜻하지 않는다.
- GitHub 동기화(GitHub sync, 깃허브 동기화): KPI 재구축 산출물은 `1b557a463f49005bcf5e8bac5b128037b653fa0e`에 반영됐고, 이 문서 동기화 이후 최신 푸시 상태는 git HEAD(깃 HEAD)를 기준으로 읽는다.
- 효과(effect, 효과): KPI 재구축은 Stage 10~12(10~12단계) 증거를 같은 7-layer KPI(7층 KPI) 형식으로 읽게 하지만, Stage 12 알파 품질(alpha quality, 알파 품질)이나 운영 승격(operating promotion, 운영 승격)을 만들지는 않는다.

## 현재 코드 표면/모듈화 상태(Current Code Surface / Modularization State, 현재 코드 표면 / 모듈화 상태)

- 코드 표면 감사(code-surface audit, 코드 표면 감사): `python -m foundation.control_plane.code_surface_audit --root .`가 `pass(통과)`한다.
- 기준선(baseline, 기준선): `docs/agent_control/code_surface_baseline.yaml`이 큰 파일(line budget, 줄 예산)과 직접 import(가져오기) 금지 규칙을 가진다.
- 실제 수정(actual refactor, 실제 리팩터): MT5 Strategy Tester report parser(MT5 전략 테스터 보고서 파서)를 `foundation/mt5/strategy_report.py`로 옮겼고, `foundation/control_plane(제어면)`의 직접 Stage10 pipeline import(10단계 파이프라인 직접 가져오기)를 끊었다.
- 추가 경화(additional hardening, 추가 경화): `alpha_scout_common_foundation_v1`로 shared alpha helpers(공유 알파 도구)가 `ScoutRunContext(탐색 실행 문맥)`를 명시적으로 받게 됐고, stage_pipelines(단계 파이프라인) 간 직접 import(가져오기)를 감사로 막는다.
- 런타임 지원(runtime support, 런타임 지원): `foundation/mt5/runtime_support.py`는 더 이상 Stage10 orchestration(10단계 조율 파일)에 위임하지 않는다. 이제 decision surface(의사결정 표면), ONNX bridge(ONNX 연결), terminal runner(터미널 실행기), runtime artifacts(런타임 산출물), MQL5 compile(MQL5 컴파일)를 foundation-owned module(기반 소유 모듈)에서 가져온다.
- 남은 부채(remaining debt, 남은 부채): 큰 helper/support files(큰 도구/지원 파일)와 재사용 로직을 의미 수준에서 잡는 semantic code-surface audit(의미 코드 표면 감사)은 아직 더 강화할 수 있다.
- 효과(effect, 효과): 앞으로 큰 pipeline/EA(파이프라인/EA)를 더 키우거나 제어면에서 단계 파일을 직접 재사용하면 audit(감사)이 먼저 잡는다.

## 현재 Codex 제어면 상태(Current Codex Control Plane State, 현재 코덱스 제어면 상태)

- control packet(제어 묶음): `codex_control_plane_v2_incremental_v1`
- 핵심 구조(core structure, 핵심 구조): prompt(프롬프트)를 work family(작업군), surface(작업 표면), risk vector(위험축), decision lock(결정 고정), evidence gate(근거 제한문), final claim(최종 주장)으로 나눈다.
- 상태 감사(state sync audit, 상태 동기화 감사): RUN03E/RUN03F 충돌을 먼저 `blocked(차단)`로 잡았고, RUN03F 기준 동기화 후 `pass(통과)`했다.
- 마감 제한문(closeout gate, 마감 제한문): work packet schema(작업 묶음 스키마), skill receipt lint(스킬 영수증 존재 검사), skill receipt schema(스킬 영수증 내용 검사), state sync audit(상태 동기화 감사), code surface audit(코드 표면 감사), agent control contracts(에이전트 제어 계약), closeout report check(마감 보고서 검사), required gate coverage audit(필수 제한문 포함 감사)를 묶어 `completed(완료)` 주장을 제한한다.
- 계약 감사(contract audit, 계약 감사): `agent_control_contracts(에이전트 제어 계약)`는 이제 work family registry(작업군 등록부), surface registry(작업 표면 등록부), risk flag registry(위험축 등록부), skill receipt default schema(스킬 영수증 기본 스키마)를 모두 도달 가능한 코드 경로에서 검사한다.
- 공통 기반 묶음(common foundation packet, 공통 기반 묶음): `alpha_scout_common_foundation_v1`은 stage pipeline boundary(단계 파이프라인 경계), explicit run context(명시 실행 문맥), closeout support(마감 지원), plan-only self-correction(계획 전용 자기 수정)을 main(메인)에 맞췄다.
- 현재 동기화(current sync, 현재 동기화): `current_truth_sync_20260430_v1`은 Stage 12 전환/운영 묶음 기록을 decision memo(결정 메모), changelog(변경기록), architecture debt(구조 부채)에 맞춘 상태 동기화다.
- 효과(effect, 효과): Codex가 작업을 축소하거나 근거 없이 완료라고 말하면, 사람이 눈치채기 전에 기계 gate(제한문)가 먼저 막는 구조로 바뀌었다.

## 현재 경계(Current Boundary, 현재 경계)

현재 상태는 아직 alpha-ready(알파 준비 완료), official alpha result(공식 알파 결과), live readiness(실거래 준비), operating promotion(운영 승격)이 아니다.

Stage 10(10단계) `run01Y/run01Z/run01AA/run01AB/run01AC(실행 01Y/01Z/01AA/01AB/01AC)`를 실행했다는 뜻은 200~220 closeout runtime_probe(마감 런타임 탐침)를 완료했다는 뜻이다. Stage 11(11단계) `RUN02A~RUN02S(실행 02A~02S)`는 LightGBM(라이트GBM) 학습방법, LGBM-specific threshold(LGBM 전용 임계값), 발산형/아이디어 무더기/회수 확장 runtime_probe(런타임 탐침)를 완료했다는 뜻이다. `RUN02T~RUN02V(실행 02T~02V)`와 `RUN02X~RUN02Y(실행 02X~02Y)`는 Python structural probe(파이썬 구조 탐침)이고, `RUN02W/RUN02Z/RUN02AA~RUN02AK(실행 02W/02Z/02AA~02AK)`는 MT5 runtime_probe(MT5 런타임 탐침) 또는 그 인계물이다. `RUN02AL~RUN02AP(실행 02AL~02AP)`는 빠진 Tier A/B/routed(Tier A/B/라우팅) 보강 실행이다. Stage 12(12단계)는 `RUN03D(실행 03D)` source package(원천 패키지), `RUN03H(실행 03H)` all-variant MT5(전체 변형 MT5), `RUN03J(실행 03J)` rolling WFO(구르는 워크포워드), `RUN03K~RUN03S(실행 03K~03S)` 실패/회수 사례 근거를 남기고 닫혔다. alpha quality(알파 품질), operating_promotion(운영 승격), runtime authority(런타임 권위)는 없다.

KPI 재구축 묶음(KPI rebuild packets, KPI 재구축 묶음)은 evidence management(근거 관리) 산출물이다. 현재 판정을 더 정확히 읽게 하지만, 새 alpha quality(알파 품질), live readiness(실거래 준비), operating promotion(운영 승격)을 만들지 않는다.

코드 표면 감사(code-surface audit, 코드 표면 감사)는 운영 가드(operating guard, 운영 제한문)다. 큰 파일이 존재한다는 사실을 숨기지 않고, 새 코드가 그 부채를 더 키우는 일을 막는다.

Codex 제어면 v2(Control Plane v2, 제어면 v2)는 코덱스 작업 운영 가드다. 이것은 거래 alpha quality(알파 품질), live readiness(실거래 준비), runtime authority(런타임 권위), operating promotion(운영 승격)을 만들지 않는다.

`alpha_scout_common_foundation_v1(알파 탐색 공통 기반 묶음)`과 `p0p1_runtime_evidence_cleanup(P0/P1 런타임 근거 정리)`은 코드/운영 가드(code/operating guard, 코드/운영 제한문)다. 이것들은 run03F(실행 03F)의 거래 판정(trading judgment, 거래 판정)을 바꾸지 않고, 새 MT5 terminal run(새 MT5 터미널 실행)도 만들지 않는다.

## 닫힌 기억(Closed Memory, 닫힌 기억)

- Stage 12(12단계)는 `stage12_model_family_challenge_closeout_v1`로 닫혔고, Stage13(13단계)은 이후 독립 MLP(다층 퍼셉트론) 주제로 열고 닫았다.
- `RUN03D(실행 03D)` ExtraTrees(엑스트라 트리)는 최신 standalone Python batch package(단독 파이썬 20개 묶음)다.
- `RUN03C(실행 03C)` ExtraTrees(엑스트라 트리)는 이전 standalone MT5 runtime_probe(단독 MT5 런타임 탐침)다.
- `kpi_rebuild_inventory_v1/kpi_rebuild_mt5_recording_v1/kpi_rebuild_mt5_execution_v1/kpi_trade_attribution_v1/kpi_tier_balance_completion_v1(KPI 재구축 목록/MT5 기록/MT5 실행/거래 귀속/티어 균형 보강 묶음)`은 현재 교차 단계 KPI 증거다.
- `code_surface_audit(코드 표면 감사)`은 현재 코드 배치(code placement, 코드 배치)와 모듈화(module split, 모듈 분리)를 지키는 운영 가드다.
- `codex_control_plane_v2_incremental_v1(코덱스 제어면 v2 단계형 묶음)`은 작업군/표면/위험축/결정 고정/마감 제한문을 현재 운영 포맷으로 추가했다.
- `alpha_scout_common_foundation_v1(알파 탐색 공통 기반 묶음)`은 shared alpha helper(공유 알파 도구), stage pipeline boundary(단계 파이프라인 경계), self-correction plan-only(자기 수정 계획 전용) 흐름을 main(메인)에 맞춘 완료된 운영 경화 묶음이다.
- `p0p1_runtime_evidence_cleanup(P0/P1 런타임 근거 정리)`은 병합된 코드/근거 정리지만 현재 저장소에는 routing receipt(라우팅 영수증)만 있으므로, completed packet(완료 묶음)으로 주장하지 않는다.
- `current_truth_sync_20260430_v1(현재 진실 동기화 묶음)`은 Stage 12 전환 결정과 최신 운영 묶음 기록을 current truth(현재 진실)에 맞춘 상태 동기화다.
- `agent_control_contracts(에이전트 제어 계약)`의 죽은 코드(dead code, 죽은 코드)는 고쳐졌고, surface/risk/default schema(표면/위험축/기본 스키마) 누락 테스트가 추가됐다.
- `RUN03A(실행 03A)`는 Stage 10/11(10/11단계)을 끌고 와서 standalone evidence(단독 근거)가 아니다.
- Stage 11(11단계)은 `reviewed_closed_no_next_stage_opened(검토 후 닫힘, 다음 단계 미개방)` 상태다.
- `RUN02W(실행 02W)`는 fwd18-only retrain(fwd18 단독 재학습) 부정 런타임 기억이다.
- `RUN02X(실행 02X)` direct rank(직접 순위)는 구조 부정 기억이다.
- `RUN02Y(실행 02Y)` inverse rank alone(역방향 순위 단독)은 혼합 구조 기억이다.
- `RUN02Z/RUN02AA~RUN02AK(실행 02Z/02AA~02AK)`는 작은 표본 양수 중심 단서지만 promotion_candidate(승격 후보)가 아니다.
- `RUN02Q/RUN02R(실행 02Q/02R)`는 각각 느슨한 bear-vortex short density(하락 보텍스 숏 밀도 확대) 부정 기억과 validation-only repair(검증만 복구) 기억이다.
- 이 문서는 새 stage(단계)의 작업 지시를 남기지 않는다.

## 현재 진실이 아닌 것(Not Current Truth, 현재 진실 아님)

- 오래된 Stage 06 `Tier B(티어 B)` 점수판(scorecard, 점수판) 결론
- 오래된 Stage 07 이중 판정 팩(dual-verdict packet, 이중 판정 팩)
- `Tier A(티어 A)`만 탐색의 기준선(anchor, 기준선)이라는 주장
- `Tier B(티어 B)`가 model study(모델 연구) 전에 끝없는 pre-validation(사전검증)을 받아야 한다는 주장
- Stage 10(10단계) `run01Y(실행 01Y)`를 alpha baseline(알파 기준선), standard run(표준 실행), operating reference(운영 기준), winner(승자)로 읽는 주장
- MT5 price-proxy weights(MT5 가격 대리 가중치)를 actual index weights(실제 지수 가중치)로 읽는 주장
- Stage 07(7단계) baseline training smoke(기준선 학습 스모크)를 alpha quality(알파 품질)나 live readiness(실거래 준비)로 읽는 주장
- Stage 08(8단계) protocol(규칙)을 alpha result(알파 결과)로 읽는 주장
- Stage 09(9단계) handoff packet(인계 묶음)을 alpha result(알파 결과)로 읽는 주장
- Stage 10(10단계) `run01A(실행 01A)`부터 `run01AC(실행 01AC)`까지의 runtime probe(런타임 탐침)를 alpha quality(알파 품질), live readiness(실거래 준비), runtime authority expansion(런타임 권위 확장), operating promotion(운영 승격)으로 읽는 주장
- Stage 11(11단계) `RUN02T~RUN02V(실행 02T~02V)` Python structural probe(파이썬 구조 탐침)를 MT5 runtime result(MT5 런타임 결과), alpha quality(알파 품질), live readiness(실거래 준비), operating promotion(운영 승격)으로 읽는 주장
- Stage 11(11단계) `RUN02A~RUN02S/RUN02W/RUN02Z/RUN02AA~RUN02AK(실행 02A~02S/02W/02Z/02AA~02AK)` LightGBM MT5 runtime_probe(라이트GBM MT5 런타임 탐침)를 alpha quality(알파 품질), live readiness(실거래 준비), operating promotion(운영 승격)으로 읽는 주장
- Stage 11(11단계) `RUN02Z/RUN02AA~RUN02AK(실행 02Z/02AA~02AK)`의 작은 표본 양수를 promotion_candidate(승격 후보), operating_promotion(운영 승격), runtime_authority expansion(런타임 권위 확장)으로 읽는 주장
- Stage 12(12단계) `RUN03A(실행 03A)`를 standalone evidence(단독 근거)로 읽는 주장
- Stage 12(12단계) `RUN03B(실행 03B)` ExtraTrees standalone Python structural scout(엑스트라 트리 단독 파이썬 구조 탐침)를 MT5 runtime evidence(MT5 런타임 근거)로 읽는 주장
- Stage 12(12단계) `RUN03C(실행 03C)` standalone MT5 runtime_probe(단독 MT5 런타임 탐침)를 alpha quality(알파 품질), live readiness(실거래 준비), operating promotion(운영 승격)으로 읽는 주장
- Stage 12(12단계) `RUN03F(실행 03F)` Tier A/B/routed MT5 tier-balance supplement(Tier A/B/라우팅 MT5 티어 균형 보강)를 alpha quality(알파 품질), live readiness(실거래 준비), operating promotion(운영 승격)으로 읽는 주장
- `alpha_scout_common_foundation_v1(알파 탐색 공통 기반 묶음)`을 alpha quality(알파 품질), runtime authority(런타임 권위), live readiness(실거래 준비), operating promotion(운영 승격)으로 읽는 주장
- `p0p1_runtime_evidence_cleanup(P0/P1 런타임 근거 정리)`의 routing receipt(라우팅 영수증)만으로 completed packet(완료 묶음)이라고 읽는 주장
- `kpi_trade_attribution_v1(거래 귀속 묶음)`의 MFE/MAE(최대 유리/불리 이동)와 regime/slice attribution(국면/구간 귀속)을 운영 승격(operating promotion, 운영 승격)이나 새 알파 품질(alpha quality, 알파 품질)로 읽는 주장

## 2026-05-01 Stage 12 RUN03H All-Variant MT5 Probe

`run03H_et_batch20_all_variant_tier_balance_mt5_v1` records MT5(`MetaTrader 5`, 메타트레이더5) runtime_probe(런타임 탐침) evidence(근거) for all 20 RUN03G structural-scout(구조 탐침) variants(변형). Effect(효과)는 shortlist(선별 목록) 없이 Tier A(티어 A), Tier B fallback-only(Tier B 대체 전용), routed actual total(라우팅 실제 전체)을 같은 packet(묶음)에 남기는 것이다.

- external_verification_status(외부 검증 상태): `completed`
- judgment(판정): `inconclusive_all_variant_tier_balance_runtime_probe_completed`
- boundary(경계): `runtime_probe_only_not_alpha_quality_not_live_readiness_not_operating_promotion`

## RUN03I validation/OOS inversion attribution(검증/표본외 반전 귀속)

- run(실행): `run03I_et_validation_oos_inversion_attribution_v1`
- source run(원천 실행): `run03H_et_batch20_all_variant_tier_balance_mt5_v1`
- evidence(근거): RUN03H(실행 03H) MT5(`MetaTrader 5`, 메타트레이더5) 120개 attempt(시도)와 7-layer KPI(7층 핵심 성과 지표)
- routed validation positive variants(라우팅 검증 양수 변형): `0/20`
- routed OOS positive variants(라우팅 표본외 양수 변형): `19/20`
- tier read(티어 판독): Tier A(티어 A)는 OOS(표본외) lift(상승)를 주도했고, Tier B(티어 B)는 split(분할)별 반대 행동을 보였다.
- judgment(판정): `inconclusive_validation_oos_inversion_attribution_completed`
- boundary(경계): `existing_mt5_runtime_probe_attribution_only_not_alpha_quality_not_promotion`
- effect(효과): Stage 12(12단계)는 계속 탐색할 단서가 있지만, 다음은 WFO(`walk-forward optimization`, 워크포워드 최적화) 계열 broad probe(넓은 탐침)이어야 한다.

## RUN03J rolling WFO split probe(구르는 워크포워드 분할 탐침)

- run(실행): `run03J_et_rolling_wfo_split_probe_v1`
- source variants(원천 변형): `run03D_et_standalone_batch20_v1`
- reference MT5 evidence(참고 MT5 근거): `run03H_et_batch20_all_variant_tier_balance_mt5_v1`
- variants/folds(변형/접힘): `20` / `7`
- best routed variant(최상위 라우팅 변형): `v01_base_leaf20_q90`
- judgment(판정): `inconclusive_rolling_wfo_no_stable_repeatability_not_promotion`
- boundary(경계): `python_rolling_wfo_structural_probe_only_not_mt5_not_alpha_quality_not_promotion`
- effect(효과): Stage 12(12단계)는 반전 단서를 계속 탐색하되, 아직 baseline(기준선), promotion candidate(승격 후보), runtime authority(런타임 권위)를 만들지 않는다.

## RUN03K WFO fold07 MT5 failure probe(WFO 접힘 7 MT5 실패 데이터 탐침)

- run(실행): `run03K_et_wfo_fold07_all_variant_mt5_failure_probe_v1`
- source WFO(원천 워크포워드 최적화): `run03J_et_rolling_wfo_split_probe_v1`
- fold(접힘): `fold07`
- variants/attempts(변형/시도): `20` / `120`
- validation/test routed net total(검증/시험 라우팅 순수익 합계): `2179.37` / `2385.76`
- judgment(판정): `inconclusive_wfo_fold07_mt5_failure_probe_completed`
- boundary(경계): `runtime_probe_failure_data_only_not_alpha_quality_not_promotion_not_runtime_authority`
- effect(효과): RUN03J(실행 03J)의 약한 WFO(워크포워드 최적화) 결과를 MT5(메타트레이더5) failure data(실패 데이터)로 보존했다. alpha quality(알파 품질), promotion candidate(승격 후보), runtime authority(런타임 권위)는 아니다.

## RUN03L recency weighted single probe(최근성 가중 단일 탐침)

- run(실행): `run03L_et_recency_weighted_single_v1`
- source variant(원천 변형): `v01_base_leaf20_q90`
- changed variable(바뀐 변수): `sample_weight(표본 가중치)`
- Python routed validation/test hit(파이썬 라우팅 검증/시험 적중): `0.401285` / `0.414419`
- MT5 validation/test routed net(MT5 검증/시험 라우팅 순수익): `192.33` / `132.20`
- judgment(판정): `inconclusive_recency_weighted_single_runtime_probe_completed`
- boundary(경계): `runtime_probe_recency_weight_single_run_not_alpha_quality_not_promotion_not_runtime_authority`
- effect(효과): 아직 안 파본 recency weighting(최근성 가중) 축을 한 번만 확인했고, alpha quality(알파 품질)나 promotion candidate(승격 후보)는 만들지 않는다.

## RUN03M session age regime probe(세션 경과 국면 탐침)

- run(실행): `run03M_et_session_age_regime_probe_v1`
- fold07(접힘 7): `excluded(제외)`
- Python folds(파이썬 접힘): `fold01~fold06`
- MT5 fold(MT5 접힘): `fold05`
- best Python routed bucket(최상위 파이썬 라우팅 구간): `0-60`
- judgment(판정): `inconclusive_session_age_regime_runtime_probe_completed`
- boundary(경계): `runtime_probe_session_age_regime_not_alpha_quality_not_promotion_not_runtime_authority`
- effect(효과): 모델 변형이 아니라 session age(세션 경과 시간) 축을 확인했고, alpha quality(알파 품질)나 promotion candidate(승격 후보)는 만들지 않는다.

## RUN03N volatility regime probe(변동성 국면 탐침)

- run(실행): `run03N_et_volatility_regime_probe_v1`
- fold07(접힘 7): `excluded(제외)`
- Python folds(파이썬 접힘): `fold01~fold06`
- MT5 fold(MT5 접힘): `fold05`
- best Python routed bucket(최상위 파이썬 라우팅 구간): `high_vol_two_plus_flags`
- judgment(판정): `inconclusive_volatility_regime_runtime_probe_completed`
- boundary(경계): `runtime_probe_volatility_regime_not_alpha_quality_not_promotion_not_runtime_authority`
- effect(효과): 모델 변형이 아니라 volatility regime(변동성 국면) 축을 확인했고, alpha quality(알파 품질)나 promotion candidate(승격 후보)는 만들지 않는다.

## RUN03O trend/chop regime probe(추세/횡보 국면 탐침)

- run(실행): `run03O_et_trend_chop_regime_probe_v1`
- fold07(접힘 7): `excluded(제외)`
- Python folds(파이썬 접힘): `fold01~fold06`
- MT5 fold(MT5 접힘): `fold05`
- best Python routed bucket(최상위 파이썬 라우팅 구간): `chop_zero_trend_flags`
- judgment(판정): `inconclusive_trend_chop_regime_runtime_probe_completed`
- boundary(경계): `runtime_probe_trend_chop_regime_not_alpha_quality_not_promotion_not_runtime_authority`
- effect(효과): 모델 변형이 아니라 trend/chop regime(추세/횡보 국면) 축을 확인했고, alpha quality(알파 품질)나 promotion candidate(승격 후보)는 만들지 않는다.

## RUN03P mega-cap divergence regime probe(대형주 괴리 국면 탐침)

- run(실행): `run03P_et_mega_cap_divergence_probe_v1`
- fold07(접힘 7): `excluded(제외)`
- Python folds(파이썬 접힘): `fold01~fold06`
- MT5 fold(MT5 접힘): `fold05`
- best Python routed bucket(최상위 파이썬 라우팅 구간): `wide_or_dispersed_mega_cap_divergence`
- judgment(판정): `inconclusive_mega_cap_divergence_runtime_probe_completed`
- boundary(경계): `runtime_probe_mega_cap_divergence_not_alpha_quality_not_promotion_not_runtime_authority`
- effect(효과): 모델 변형이 아니라 mega-cap divergence regime(대형주 괴리 국면) 축을 확인했고, alpha quality(알파 품질)나 promotion candidate(승격 후보)는 만들지 않는다.

## RUN03Q macro proxy regime regime probe(거시 대리 국면 국면 탐침)

- run(실행): `run03Q_et_macro_proxy_regime_probe_v1`
- fold07(접힘 7): `excluded(제외)`
- Python folds(파이썬 접힘): `fold01~fold06`
- MT5 fold(MT5 접힘): `fold05`
- best Python routed bucket(최상위 파이썬 라우팅 구간): `macro_risk_on_relief`
- judgment(판정): `inconclusive_macro_proxy_regime_runtime_probe_completed`
- boundary(경계): `runtime_probe_macro_proxy_regime_not_alpha_quality_not_promotion_not_runtime_authority`
- effect(효과): 모델 변형이 아니라 macro proxy regime regime(거시 대리 국면 국면) 축을 확인했고, alpha quality(알파 품질)나 promotion candidate(승격 후보)는 만들지 않는다.

## RUN03R gap/overnight context regime probe(갭/야간 문맥 국면 탐침)

- run(실행): `run03R_et_gap_overnight_context_probe_v1`
- fold07(접힘 7): `excluded(제외)`
- Python folds(파이썬 접힘): `fold01~fold06`
- MT5 fold(MT5 접힘): `fold05`
- best Python routed bucket(최상위 파이썬 라우팅 구간): `gap_or_overnight_down_context`
- judgment(판정): `inconclusive_gap_overnight_context_runtime_probe_completed`
- boundary(경계): `runtime_probe_gap_overnight_context_not_alpha_quality_not_promotion_not_runtime_authority`
- effect(효과): 모델 변형이 아니라 gap/overnight context regime(갭/야간 문맥 국면) 축을 확인했고, alpha quality(알파 품질)나 promotion candidate(승격 후보)는 만들지 않는다.

## RUN03S probability-shape attribution regime probe(확률 모양 귀속 국면 탐침)

- run(실행): `run03S_et_probability_shape_attribution_probe_v1`
- fold07(접힘 7): `excluded(제외)`
- Python folds(파이썬 접힘): `fold01~fold06`
- MT5 fold(MT5 접힘): `fold05`
- best Python routed bucket(최상위 파이썬 라우팅 구간): `thin_probability_edge`
- judgment(판정): `inconclusive_probability_shape_attribution_runtime_probe_completed`
- boundary(경계): `runtime_probe_probability_shape_attribution_not_alpha_quality_not_promotion_not_runtime_authority`
- effect(효과): 모델 변형이 아니라 probability-shape attribution regime(확률 모양 귀속 국면) 축을 확인했고, alpha quality(알파 품질)나 promotion candidate(승격 후보)는 만들지 않는다.

## 2026-05-12 Stage56 closeout(56단계 종료, 비최종 중간 근거)

- active_stage(현재 단계): `56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection`
- closeout(종료): `stage56_closeout_v1`
- final_judgment(최종 판정): `baseline_candidate_only(기준선 후보 전용)`
- candidate(후보): `d38h10` LogReg(로지스틱 회귀) bracket micro-grid(구간 미세 격자)
- evidence(근거): actual MT5 closed trades(실제 MT5 청산 거래), run50C(실행50C) stage ledger(단계 장부), project ledger(프로젝트 장부), run_manifest(실행 목록), market-weather attribution(시장 상태 귀속)
- selected_research_baseline(선택 연구 기준선): `none`
- live readiness(실거래 준비), runtime authority(런타임 권위), operating promotion(운영 승격), operating reference(운영 참조): `none`
- effect(효과): 이 묶음은 후보를 보존하는 prior intermediate evidence(이전 중간 근거)이며, `stage56_reopen_goal_v1` 이후 Stage56(56단계)을 닫지 않는다.

## 2026-05-12 Stage56 reopened closeout(56단계 재개 종료, 비최종 중간 근거)

- active_stage(현재 단계): `56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection`
- closeout(종료): `stage56_reopened_closeout_v2`
- final_judgment(최종 판정): `stronger_baseline_candidate_only(강화 기준선 후보 전용)`
- candidate(후보): `d390h10` LogReg(로지스틱 회귀) deep repair suite(조밀 보정 묶음)
- evidence(근거): run50D(실행50D) 18개 variant(변형) actual MT5 closed trades(실제 MT5 청산 거래), stage ledger(단계 장부), project ledger(프로젝트 장부), run registry(실행 등록부), d390h10 market-weather attribution(시장 상태 귀속)
- selected_research_baseline(선택 연구 기준선): `none`
- live readiness(실거래 준비), runtime authority(런타임 권위), operating promotion(운영 승격), operating reference(운영 참조): `none`
- effect(효과): Stage56(56단계)은 d38h10보다 강한 연구 후보를 찾았지만, selected_research_baseline(선택 연구 기준선)을 찾지 못했으므로 `stage56_reopen_goal_v1` 이후 active_in_progress(활성 진행 중)로 계속된다.


