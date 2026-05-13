# Stage56 Selection Status(56단계 선택 상태)

- stage_status(단계 상태): `active_in_progress`
- latest_run_id(최신 실행 ID): `run50AH_stage56_s25_model_axis_oos_density_v1`
- current run(현재 실행): `run50AH_stage56_s25_model_axis_oos_density_v1`
- current_judgment(현재 판정): `in_progress_no_selected_research_baseline(진행 중, 선택 연구 기준선 없음)`
- selected_research_baseline(선택 연구 기준선): `none`
- prior_stronger_candidate_intermediate(이전 강화 후보 중간 근거): `d390h10_logreg_deep_repair_suite`
- prior_candidate_reference_intermediate(이전 후보 참고 중간 근거): `d38h10_logreg_bracket_micro_grid_preserved_prior`
- selected_shadow_candidate(선택 그림자 후보): `none`
- dense_engine_candidate(조밀 엔진 후보): `none`
- latest_batch_best_variant_intermediate(최신 묶음 최선 변형 중간 근거): `nf200s25b`
- latest_density_pass_quality_fail_variants(최신 밀도 통과 품질 실패 변형): `run50AH_nf200s25b_validation_quality_density_positive_but_oos_density_below_5_model_axis_nonflat200_same_move_density_not_survived`

## Latest Run50AH Intermediate Evidence(최신 50AH 중간 근거)

- packet(묶음): `stage56_run50AH_s25_model_axis_oos_density_v1`
- report(보고서): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50AH_reopen_batch.md`
- summary_csv(요약 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50AH_summary.csv`
- audit_csv(감사 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50AH_audit.csv`
- aggregate_summary(합산 요약): `docs/agent_control/packets/stage56_run50AH_s25_model_axis_oos_density_v1/aggregate_summary.json`
- attribution_report(귀속 보고서): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50AH_nf200s25b_market_weather_attribution.md`
- selected_research_baseline(선택 연구 기준선): `none`
- current_judgment(현재 판정): `in_progress_no_selected_research_baseline`

Run50AH(실행50AH)는 run50AG(실행50AG)의 threshold relaxation saturation(임계값 완화 포화) 뒤 C value(C 값), non-flat sample weight(비평탄 표본 가중), recent-2023 balanced training(2023 이후 균형 학습)을 actual MT5 validation/OOS(실제 메타트레이더5 검증/표본외)로 시험했다. 효과(effect, 효과): model-axis perturbation(모델 축 교란)이 OOS density(표본외 밀도)를 새로 열 수 있는지 확인했다.

- closest intermediate variant(가장 가까운 중간 변형): `nf200s25b`
- A+B actual routed total(A+B 실제 라우팅 전체) validation(검증): 5.513661 trades/day(일 거래 수), net(순손익) 459.98, PF(수익 팩터) 1.18
- A+B actual routed total(A+B 실제 라우팅 전체) OOS(표본외): 3.789744 trades/day(일 거래 수), net(순손익) 428.88, PF(수익 팩터) 1.24
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

Run50AG(실행50AG)는 `s25c8a` quality branch(품질 가지)의 OOS density(표본외 밀도)를 단순 threshold relaxation(임계값 완화)으로 회복할 수 있는지 실제 MT5 validation/OOS(메타트레이더5 검증/표본외)로 시험했다. 효과(effect, 효과): 같은 신호 집합이 반복되는 포화 여부를 확인했다.

- closest intermediate variant(가장 가까운 중간 변형): `s24l15a`
- A+B actual routed total(A+B 실제 라우팅 전체) validation(검증): 5.349727 trades/day(일 거래 수), net(순손익) 466.64, PF(수익 팩터) 1.19, max DD(최대 손실) 255.14
- A+B actual routed total(A+B 실제 라우팅 전체) OOS(표본외): 3.646154 trades/day(일 거래 수), net(순손익) 417.57, PF(수익 팩터) 1.23, max DD(최대 손실) 159.26
- Tier A only(Tier A 단독) OOS(표본외): net(순손익) 417.57, PF(수익 팩터) 1.23
- Tier B fallback-only OOS(Tier B 대체 전용 표본외): net(순손익) -10.43, PF(수익 팩터) 0.69로 damaging(손상)했다.
- MFE capture read(MFE 포착 판독): OOS MFE capture ratio(표본외 MFE 포착 비율)는 0.588858이다.
- same-move read(동일 이동 판독): OOS same-move re-entry ratio(표본외 동일 이동 재진입 비율)는 0.594937이고 12-bar cooldown(12봉 쿨다운) 뒤 OOS density(표본외 밀도)는 1.476923 trades/day(일 거래 수)라 density gain(밀도 증가)이 기준까지 생존하지 못했다.
- threshold read(임계값 판독): 0.240/0.150부터 0.200/0.130까지 validation/OOS(검증/표본외) 거래 집합이 s25c8a와 같아 threshold relaxation(임계값 완화)이 포화됐다.
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

Run50AF(실행50AF)는 sell ADX20-25 repair(매도 평균 방향 지수 20-25 수리)를 실제 MT5 validation/OOS(메타트레이더5 검증/표본외)로 시험했다. 효과(effect, 효과): run50AE(실행50AE)의 validation(검증) 손상이 수리되는지, 그리고 그 밀도가 same-move split trading(동일 이동 분할 거래) 없이 살아나는지 확인했다.

- closest intermediate variant(가장 가까운 중간 변형): `s25c8a`
- A+B actual routed total(A+B 실제 라우팅 전체) validation(검증): 5.349727 trades/day(일 거래 수), net(순손익) 466.64, PF(수익 팩터) 1.19, max DD(최대 손실) 255.14
- A+B actual routed total(A+B 실제 라우팅 전체) OOS(표본외): 3.646154 trades/day(일 거래 수), net(순손익) 417.57, PF(수익 팩터) 1.23, max DD(최대 손실) 159.26
- Tier A only(Tier A 단독) OOS(표본외): net(순손익) 417.57, PF(수익 팩터) 1.23
- Tier B fallback-only OOS(Tier B 대체 전용 표본외): net(순손익) -10.43, PF(수익 팩터) 0.69로 damaging(손상)했다.
- MFE capture read(MFE 포착 판독): OOS MFE capture ratio(표본외 MFE 포착 비율)는 0.588858이다.
- same-move read(동일 이동 판독): OOS same-move re-entry ratio(표본외 동일 이동 재진입 비율)는 0.594937이고 12-bar cooldown(12봉 쿨다운) 뒤 OOS density(표본외 밀도)는 1.476923 trades/day(일 거래 수)라 density gain(밀도 증가)이 기준까지 생존하지 못했다.
- attribution read(귀속 판독): validation(검증)은 ADX20-25(평균 방향 지수 20-25) 손상이 수리됐지만 OOS(표본외)는 buy vol_low(매수 저변동성) -42.92와 mid session(중반 세션) 약세가 남았다.
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

Run50AE(실행50AE)는 buy vol_low firewall(매수 저변동성 방화벽)을 유지하고 cooldown(쿨다운) 6/8/10봉 및 early_mid session(초반+중반 세션)을 실제 MT5 validation/OOS(메타트레이더5 검증/표본외)로 시험했다. 효과(effect, 효과): density recovery(밀도 회복)가 real density(실제 밀도)인지 same-move split trading(동일 이동 분할 거래)인지 확인했다.

- closest intermediate variant(가장 가까운 중간 변형): `c08b`
- A+B actual routed total(A+B 실제 라우팅 전체) validation(검증): 4.322404 trades/day(일 거래 수), net(순손익) 118.68, PF(수익 팩터) 1.05, max DD(최대 손실) 217.41
- A+B actual routed total(A+B 실제 라우팅 전체) OOS(표본외): 3.153846 trades/day(일 거래 수), net(순손익) 330.59, PF(수익 팩터) 1.19, max DD(최대 손실) 133.17
- Tier A only(Tier A 단독) OOS(표본외): net(순손익) 288.55, PF(수익 팩터) 1.17
- Tier B fallback-only OOS(Tier B 대체 전용 표본외): net(순손익) 4.41, PF(수익 팩터) 1.24지만 validation(검증)은 net(순손익) -495.18, PF(수익 팩터) 0.01로 damaging(손상)했다.
- MFE capture read(MFE 포착 판독): OOS MFE capture ratio(표본외 MFE 포착 비율)는 0.598210이다.
- same-move read(동일 이동 판독): OOS same-move re-entry ratio(표본외 동일 이동 재진입 비율)는 0.539837이고 12-bar cooldown(12봉 쿨다운) 뒤 OOS density(표본외 밀도)는 1.451282 trades/day(일 거래 수)라 density gain(밀도 증가)이 기준까지 생존하지 못했다.
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

Run50AC(실행50AC)는 Windows path length(윈도우 경로 길이) 문제로 blocked(차단)됐고 run50AD(실행50AD)가 같은 hypothesis family(가설군)를 짧은 ID(식별자)로 수리해 실제 MT5 validation/OOS(메타트레이더5 검증/표본외)를 완료했다. 효과(effect, 효과): 실패 시도는 중간 근거로 남기고 Stage56(56단계)을 닫지 않았다.

- closest intermediate variant(가장 가까운 중간 변형): `lv26b`
- A+B actual routed total(A+B 실제 라우팅 전체) validation(검증): 3.836066 trades/day(일 거래 수), net(순손익) 23.40, PF(수익 팩터) 1.01, max DD(최대 손실) 381.69
- A+B actual routed total(A+B 실제 라우팅 전체) OOS(표본외): 2.533333 trades/day(일 거래 수), net(순손익) 312.41, PF(수익 팩터) 1.23, max DD(최대 손실) 118.77
- Tier A only(Tier A 단독) OOS(표본외): net(순손익) 414.56, PF(수익 팩터) 1.31
- Tier B fallback-only OOS(Tier B 대체 전용 표본외): net(순손익) 4.41, PF(수익 팩터) 1.24지만 validation(검증)은 net(순손익) -495.38, PF(수익 팩터) 0.01로 damaging(손상)했다.
- MFE capture read(MFE 포착 판독): OOS MFE capture ratio(표본외 MFE 포착 비율)는 0.613230으로 d390h10 reference(d390h10 참조) 대비 materially worse(중대 악화)는 아니다.
- same-move read(동일 이동 판독): OOS same-move re-entry ratio(표본외 동일 이동 재진입 비율)는 0.242915지만 12-bar cooldown(12봉 쿨다운) 뒤 OOS density(표본외 밀도)는 1.917949 trades/day(일 거래 수)라 density gain(밀도 증가)이 기준까지 생존하지 못했다.
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

Run50AB(실행50AB)는 actual 12-bar cooldown(실제 12봉 쿨다운), hold10/hold8/hold6(10봉/8봉/6봉 보유), lower threshold(낮은 임계값), matched Tier B comparison(대응 Tier B 비교)을 실제 MT5 validation/OOS(검증/표본외)로 시험했다. 효과(effect, 효과): shorter hold(짧은 보유)가 same-move split trading(동일 이동 분할 거래)으로 밀도를 만든 것인지 확인했다.

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

Run50AA(실행50AA)는 cooldown6(6봉 쿨다운), buy ADX below 30/35(매수 평균 방향 지수 30/35 미만 허용), 낮은 threshold(임계값), matched Tier B comparison(대응 Tier B 비교)을 실제 MT5 validation/OOS(검증/표본외)로 시험했다. 효과(effect, 효과): run50Z(실행50Z)에서 cost-stressed expectancy(비용 압박 기대값)가 양수로 돌아선 가지의 density(밀도)를 회복할 수 있는지 확인했다.

- closest intermediate variant(가장 가까운 중간 변형): `nfaa_s23l13_c6_l30_b`
- A+B actual routed total(A+B 실제 라우팅 전체) validation(검증): 4.464481 trades/day(일 거래 수), net(순손익) 288.34, PF(수익 팩터) 1.14, max DD(최대 손실) 171.39
- A+B actual routed total(A+B 실제 라우팅 전체) OOS(표본외): 3.020513 trades/day(일 거래 수), net(순손익) 308.82, PF(수익 팩터) 1.21, max DD(최대 손실) 168.45
- Tier A only(Tier A 단독) OOS(표본외): net(순손익) 305.18, PF(수익 팩터) 1.20
- Tier B fallback-only OOS(Tier B 대체 전용 표본외): net(순손익) -10.26, PF(수익 팩터) 0.66으로 negative(음수)다.
- MFE capture read(MFE 포착 판독): OOS MFE capture ratio(표본외 MFE 포착 비율)는 0.607286이다.
- same-move read(동일 이동 판독): OOS same-move re-entry ratio(표본외 동일 이동 재진입 비율)는 0.504244이고, 12-bar cooldown(12봉 쿨다운) 뒤 OOS density(표본외 밀도)는 1.497436 trades/day(일 거래 수)다.
- attribution read(귀속 판독): validation early session(검증 초반 세션) -78.95, validation vol_mid(검증 중간 변동성) -127.14, validation ADX 20-25(검증 평균 방향 지수 20-25) -69.41이 약했다. OOS(표본외)는 mid session(중반 세션) -12.41, vol_low(저변동성) -2.19, ADX 20-25(평균 방향 지수 20-25) -11.27만 약하고 나머지는 양수였다.
- selected_research_baseline(선택 연구 기준선)으로 올리지 않는 이유: validation/OOS density(검증/표본외 밀도) 5.0 미만, same-move density audit(동일 이동 밀도 감사) 실패, Tier B fallback-only OOS(Tier B 대체 전용 표본외) 음수다.
- next_hypothesis_branch(다음 가설 가지): `recover_density_from_run50AA_quality_branch_without_reopening_same_move_split`

## Latest Run50Z Intermediate Evidence(최신 50Z 중간 근거)

- packet(묶음): `stage56_run50Z_partial_buy_adx_reintro_v1`
- report(보고서): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50Z_reopen_batch.md`
- summary_csv(요약 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50Z_summary.csv`
- audit_csv(감사 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50Z_audit.csv`
- aggregate_summary(합산 요약): `docs/agent_control/packets/stage56_run50Z_partial_buy_adx_reintro_v1/aggregate_summary.json`
- selected_research_baseline(선택 연구 기준선): `none`
- current_judgment(현재 판정): `in_progress_no_selected_research_baseline`

Run50Z(실행50Z)는 partial buy ADX reintroduction(부분 매수 평균 방향 지수 재도입), Tier A only(Tier A 단독), matched Tier B comparison(대응 Tier B 비교)을 실제 MT5 validation/OOS(검증/표본외)로 시험했다. 효과(effect, 효과): run50Y(실행50Y)의 strict buy ADX 20+ block(강한 매수 평균 방향 지수 20 이상 차단)이 버린 density(밀도)를 되살리면서 품질을 보존할 수 있는지 확인했다.

- closest intermediate variant(가장 가까운 중간 변형): `nfz_s31l18_c3_s2030_b`
- A+B actual routed total(A+B 실제 라우팅 전체) validation(검증): 7.196721 trades/day(일 거래 수), net(순손익) 451.99, PF(수익 팩터) 1.15, max DD(최대 손실) 249.56
- A+B actual routed total(A+B 실제 라우팅 전체) OOS(표본외): 5.056410 trades/day(일 거래 수), net(순손익) 251.32, PF(수익 팩터) 1.10, max DD(최대 손실) 142.59
- Tier A only(Tier A 단독) OOS(표본외): net(순손익) 201.81, PF(수익 팩터) 1.08
- Tier B fallback-only OOS(Tier B 대체 전용 표본외): net(순손익) -2.52, PF(수익 팩터) 0.91로 negative(음수)다.
- MFE capture read(MFE 포착 판독): best OOS MFE capture ratio(최선 표본외 MFE 포착 비율)는 0.605995다.
- same-move read(동일 이동 판독): OOS same-move re-entry ratio(표본외 동일 이동 재진입 비율)는 0.748479이고 12-bar cooldown(12봉 쿨다운) 뒤 OOS density(표본외 밀도)는 1.271795 trades/day(일 거래 수)로 떨어진다.
- branch read(가지 판독): partial buy ADX block(부분 매수 평균 방향 지수 차단)은 same-move ratio(동일 이동 비율)를 0.564945~0.669939까지 낮췄지만 OOS density(표본외 밀도)가 5 미만이었다. cooldown6(6봉 쿨다운) 변형 `nfz_s27l15_c6_l30_a`는 OOS cost-stressed expectancy(표본외 비용 압박 기대값) 0.025267과 OOS PF(표본외 수익 팩터) 1.20을 만들었지만 OOS density(표본외 밀도)는 2.979487에 그쳤다.
- selected_research_baseline(선택 연구 기준선)으로 올리지 않는 이유: cost-stressed expectancy(비용 압박 기대값) 음수 또는 density(밀도) 부족, same-move density audit(동일 이동 밀도 감사) 실패, Tier B fallback-only OOS(Tier B 대체 전용 표본외) 음수다.
- next_hypothesis_branch(다음 가설 가지): `same_move_density_survival_and_cost_stress_repair_after_run50Z`

## Latest Run50Y Intermediate Evidence(최신 50Y 중간 근거)

- packet(묶음): `stage56_run50Y_buy_side_firewall_tierb_v1`
- report(보고서): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50Y_reopen_batch.md`
- summary_csv(요약 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50Y_summary.csv`
- audit_csv(감사 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50Y_audit.csv`
- aggregate_summary(합산 요약): `docs/agent_control/packets/stage56_run50Y_buy_side_firewall_tierb_v1/aggregate_summary.json`
- attribution_report(귀속 보고서): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50Y_nfy_s31l18_c3_adx_b_market_weather_attribution.md`
- selected_research_baseline(선택 연구 기준선): `none`
- current_judgment(현재 판정): `in_progress_no_selected_research_baseline`

Run50Y(실행50Y)는 buy ADX 20+(매수 평균 방향 지수 20 이상) firewall(방화벽), buy vol_low(매수 저변동성) firewall(방화벽), Tier B disabled/A+B routed comparison(Tier B 비활성화/A+B 실제 라우팅 비교)을 실제 MT5 validation/OOS(검증/표본외)로 시험했다. 효과(effect, 효과): run50X(실행50X)의 손상 원인이 buy-side(매수 방향) 필터인지, Tier B(티어 B)인지, same-move split(동일 이동 분할)인지 분리했다.

- closest intermediate variant(가장 가까운 중간 변형): `nfy_s31l18_c3_adx_b`
- A+B actual routed total(A+B 실제 라우팅 전체) validation(검증): 3.868852 trades/day(일 거래 수), net(순손익) 166.36, PF(수익 팩터) 1.09, max DD(최대 손실) 159.92
- A+B actual routed total(A+B 실제 라우팅 전체) OOS(표본외): 2.625641 trades/day(일 거래 수), net(순손익) 378.86, PF(수익 팩터) 1.29, max DD(최대 손실) 137.04
- Tier A only(Tier A 단독) OOS(표본외): net(순손익) 420.75, PF(수익 팩터) 1.33
- Tier B fallback-only OOS(Tier B 대체 전용 표본외): net(순손익) -6.61, PF(수익 팩터) 0.59로 negative(음수)다.
- MFE capture read(MFE 포착 판독): OOS MFE capture ratio(표본외 MFE 포착 비율)는 0.628193으로 run50X(실행50X)보다 높다.
- same-move read(동일 이동 판독): OOS same-move re-entry ratio(표본외 동일 이동 재진입 비율)는 0.474609로 내려갔지만, 12-bar cooldown(12봉 쿨다운) 뒤 OOS density(표본외 밀도)는 1.379487 trades/day(일 거래 수)라 5+ 기준을 살리지 못한다.
- attribution read(귀속 판독): strict buy ADX 20+ block(강한 매수 평균 방향 지수 20 이상 차단) 뒤 OOS(표본외)는 early/mid/late session(초반/중반/후반 세션)이 모두 양수였지만 validation early session(검증 초반 세션)은 -133.52로 약했다. 효과(effect, 효과): 품질은 좋아졌으나 너무 많은 매수 기회를 제거해 density(밀도)가 부족해졌다.
- alternate reads(대안 판독): buy vol_low firewall(매수 저변동성 방화벽)은 validation/OOS density(검증/표본외 밀도) 6.180328/4.410256까지 남겼지만 validation net/PF(검증 순손익/수익 팩터)가 -79.97/0.97로 실패했다.
- selected_research_baseline(선택 연구 기준선)으로 올리지 않는 이유: validation/OOS density(검증/표본외 밀도) 5.0 미만, validation PF(검증 수익 팩터) 1.10 미만, same-move density audit(동일 이동 밀도 감사) 실패, Tier B fallback-only OOS(Tier B 대체 전용 표본외) 음수다.
- next_hypothesis_branch(다음 가설 가지): `partial_buy_adx_reintroduction_aonly_density_repair_after_run50Y`

## Latest Run50X Intermediate Evidence(최신 50X 중간 근거)

- packet(묶음): `stage56_run50X_nonflat_adx_soft_firewall_v1`
- report(보고서): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50X_reopen_batch.md`
- summary_csv(요약 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50X_summary.csv`
- audit_csv(감사 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50X_audit.csv`
- aggregate_summary(합산 요약): `docs/agent_control/packets/stage56_run50X_nonflat_adx_soft_firewall_v1/aggregate_summary.json`
- attribution_report(귀속 보고서): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50X_nfx_s33l20_c3_s2030_market_weather_attribution.md`
- selected_research_baseline(선택 연구 기준선): `none`
- current_judgment(현재 판정): `in_progress_no_selected_research_baseline`

Run50X(실행50X)는 short ADX 20-30 firewall(숏 평균 방향 지수 20-30 방화벽), soft long ADX block(완만한 롱 평균 방향 지수 차단), 2~3 bar reentry cooldown(2~3봉 재진입 쿨다운), core/mixed Tier B fallback(핵심/혼합 Tier B 대체)을 실제 MT5 validation/OOS(검증/표본외)로 시험했다. 효과(effect, 효과): run50W(실행50W)에서 보인 OOS buy ADX damage(표본외 매수 평균 방향 지수 손상)를 줄이면서 5+ trades/day(일 거래 수) 밀도가 남는지 확인했다.

- closest intermediate variant(가장 가까운 중간 변형): `nfx_s33l20_c3_s2030`
- A+B actual routed total(A+B 실제 라우팅 전체) validation(검증): 7.196721 trades/day(일 거래 수), net(순손익) 451.99, PF(수익 팩터) 1.15, max DD(최대 손실) 249.56
- A+B actual routed total(A+B 실제 라우팅 전체) OOS(표본외): 5.056410 trades/day(일 거래 수), net(순손익) 251.32, PF(수익 팩터) 1.10, max DD(최대 손실) 142.59
- Tier A only(Tier A 단독) OOS(표본외): net(순손익) 201.81, PF(수익 팩터) 1.08
- Tier B fallback-only OOS(Tier B 대체 전용 표본외): net(순손익) -2.52, PF(수익 팩터) 0.91로 negative(음수)다.
- MFE capture read(MFE 포착 판독): best OOS MFE capture ratio(최선 표본외 MFE 포착 비율)는 0.605995다.
- same-move read(동일 이동 판독): OOS same-move re-entry ratio(표본외 동일 이동 재진입 비율)는 0.748479이고 12-bar cooldown(12봉 쿨다운) 뒤 OOS density(표본외 밀도)는 1.271795 trades/day(일 거래 수)로 떨어진다. 효과(effect, 효과): density gain(밀도 증가)은 아직 real density(실제 밀도)가 아니라 same-move split trading(동일 이동 분할 거래)에 크게 기대고 있다.
- attribution read(귀속 판독): OOS buy vol_low(표본외 매수 저변동성) -285.35, buy ADX 20-25(매수 평균 방향 지수 20-25) -111.11, buy ADX >25(매수 평균 방향 지수 25 초과) -116.97이 약했고, sell ADX >25(매도 평균 방향 지수 25 초과)는 +281.21로 강했다. 효과(effect, 효과): 다음 가지는 sell-side(매도 방향) 강점을 보존하고 buy-side(매수 방향) 저변동성/ADX 손상을 차단하는 방향으로 좁힌다.
- alternate reads(대안 판독): `nfx_s35l22_c2_s2030`와 `nfx_s35l22_c2_s2030l40`은 Tier B fallback-only OOS(Tier B 대체 전용 표본외)가 non-negative(비음수)이지만 OOS PF(표본외 수익 팩터)가 1.10 미만이다. `nfx_s33l20_c3_s2030l40`은 OOS PF(표본외 수익 팩터) 1.14와 net(순손익) 318.73이지만 OOS density(표본외 밀도) 4.641026이고 Tier B fallback-only OOS(Tier B 대체 전용 표본외)가 negative(음수)다.
- selected_research_baseline(선택 연구 기준선)으로 올리지 않는 이유: cost-stressed expectancy(비용 압박 기대값) 음수, same-move audit(동일 이동 감사) 실패, Tier B fallback-only OOS(Tier B 대체 전용 표본외) 음수다.
- next_hypothesis_branch(다음 가설 가지): `buy_side_vol_low_adx_firewall_plus_tier_b_disablement_aonly_comparison`

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

- packet(묶음): `stage56_run50S_nonflat_vol_low_block_v1`
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

Run50Q(실행50Q)는 one-bar cooldown interpolation(1봉 쿨다운 보간)을 실제 MT5 validation/OOS(검증/표본외)로 시험했다. 효과(effect, 효과): run50P(실행50P)의 0봉 density(밀도)와 2봉 quality recovery(품질 회복) 사이를 확인했다.

- best intermediate variant(최선 중간 변형): `nf_h10c1_s390l280_b_sadx`
- A+B actual routed total(A+B 실제 라우팅 전체) validation(검증): 7.530055 trades/day(일 거래 수), net(순손익) -8.43, PF(수익 팩터) 1.00, max DD(최대 손실) 288.32
- A+B actual routed total(A+B 실제 라우팅 전체) OOS(표본외): 5.102564 trades/day(일 거래 수), net(순손익) 99.37, PF(수익 팩터) 1.03, max DD(최대 손실) 278.00
- Tier A only(Tier A 단독) OOS(표본외): net(순손익) -4.22, PF(수익 팩터) 1.00
- Tier B fallback-only OOS(Tier B 대체 전용 표본외): net(순손익) -36.33, PF(수익 팩터) 0.88로 damaging(손상)했다.
- MFE capture read(MFE 포착 판독): best OOS MFE capture ratio(최선 표본외 MFE 포착 비율)는 0.607672로 d390h10 reference(d390h10 참조)보다 낮지만 materially worse(중대 악화)로만 볼 정도는 아니다.
- same-move read(동일 이동 판독): best OOS same-move re-entry ratio(최선 표본외 동일 이동 재진입 비율)는 0.767839이고 12-bar re-entry count(12봉 재진입 수)는 764다.
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
- Tier A only(Tier A 단독) OOS(표본외): net(순손익) 71.67, PF(수익 팩터) 1.03
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

Run50O(실행50O)은 hold6(6봉 보유) density recovery(밀도 회복)와 short ADX 20~25 side filter(숏 ADX 20~25 방향 필터)를 결합했다. 효과(effect, 효과): run50N(실행50N)의 품질 필터를 밀도 회복 축에 붙여도 selected_research_baseline(선택 연구 기준선) 조건이 살아나는지 확인했다.

- best intermediate variant(최선 중간 변형): `d320h06_sadx_c0_b045`
- A+B actual routed total(A+B 실제 라우팅 전체) validation(검증): 6.398907 trades/day(일 거래 수), net(순손익) 143.47, PF(수익 팩터) 1.04, max DD(최대 손실) 285.05
- A+B actual routed total(A+B 실제 라우팅 전체) OOS(표본외): 4.882051 trades/day(일 거래 수), net(순손익) 60.50, PF(수익 팩터) 1.02, max DD(최대 손실) 240.54
- Tier B fallback-only OOS(Tier B 대체 전용 표본외): net(순손익) -44.61, PF(수익 팩터) 0.82로 damaging(손상)했다.
- MFE capture read(MFE 포착 판독): best OOS MFE capture ratio(최선 표본외 MFE 포착 비율)는 0.605966이다.
- same-move read(동일 이동 판독): best OOS same-move re-entry ratio(최선 표본외 동일 이동 재진입 비율)는 0.742647이고 12-bar re-entry count(12봉 재진입 수)는 707이라 density gain(밀도 증가)이 생존하지 못했다.
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

Run50N(실행50N)은 run50M(실행50M) attribution(귀속)에서 숏 ADX 20~25(short ADX 20~25, 숏 ADX 20~25)가 validation/OOS(검증/표본외)를 동시에 깎는다는 판독을 실제 EA side filter(방향 필터)로 시험했다. 효과(effect, 효과): 후처리 필터가 아니라 실제 MT5 routed run(라우팅 실행)에서 숏 ADX 20~25 차단이 품질과 밀도를 같이 회복하는지 확인했다.

- best intermediate variant(최선 중간 변형): `c6s330l235_b_sadx`
- A+B actual routed total(A+B 실제 라우팅 전체) validation(검증): 6.196721 trades/day(일 거래 수), net(순손익) 256.42, PF(수익 팩터) 1.09, max DD(최대 손실) 237.16
- A+B actual routed total(A+B 실제 라우팅 전체) OOS(표본외): 4.005128 trades/day(일 거래 수), net(순손익) 508.97, PF(수익 팩터) 1.25, max DD(최대 손실) 171.29
- Tier A only(Tier A 단독) OOS(표본외): net(순손익) 536.95, PF(수익 팩터) 1.27
- Tier B fallback-only(Tier B 대체 전용) OOS(표본외): net(순손익) 18.42, PF(수익 팩터) 1.08로 non-negative(비음수)이지만 A+B routed total(A+B 실제 라우팅 전체)을 충분히 개선하지 못했다.
- MFE capture read(MFE 포착 판독): best OOS MFE capture ratio(최선 표본외 MFE 포착 비율)는 0.619893이고 d390h10 reference(d390h10 참조) 대비 약 -0.008372라 materially worse(중대 악화)는 아니다.
- same-move read(동일 이동 판독): best OOS same-move re-entry ratio(최선 표본외 동일 이동 재진입 비율)는 0.661972이고 12-bar re-entry count(12봉 재진입 수)는 517이다. 효과(effect, 효과): ADX 숏 차단은 품질을 개선했지만 density gain(밀도 증가)이 cooldown(쿨다운) 뒤 생존하지 못했다.
- selected_research_baseline(선택 연구 기준선)으로 올리지 않는 이유: OOS density(표본외 밀도) 5.0 미만, validation PF(검증 수익 팩터) 1.10 미만, validation cost-stressed expectancy(검증 비용 압박 기대값) 음수, same-move audit(동일 이동 감사) 실패다.

## Latest Run50M Intermediate Evidence(최신 50M 중간 근거)

- packet(묶음): `stage56_run50M_cooldown_threshold_interpolation_v1`
- report(보고서): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50M_reopen_batch.md`
- summary_csv(요약 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50M_summary.csv`
- audit_csv(감사 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50M_audit.csv`
- aggregate_summary(합산 요약): `docs/agent_control/packets/stage56_run50M_cooldown_threshold_interpolation_v1/aggregate_summary.json`
- selected_research_baseline(선택 연구 기준선): `none`
- current_judgment(현재 판정): `in_progress_no_selected_research_baseline`

Run50M(실행50M)은 cooldown/threshold interpolation(쿨다운/임계값 보간)으로 run50L(실행50L)의 6봉/12봉 사이를 실제 MT5 validation/OOS(검증/표본외)로 시험했다. 효과(effect, 효과): OOS quality(표본외 품질)가 살아나는 낮은 임계값이 density(밀도)와 same-move audit(동일 이동 감사)까지 통과하는지 확인했다.

- best intermediate variant(최선 중간 변형): `nf150_c8_h10_s340l240_b045`
- A+B actual routed total(A+B 실제 라우팅 전체) validation(검증): 6.415301 trades/day(일 거래 수), net(순손익) 91.64, PF(수익 팩터) 1.03, max DD(최대 손실) 254.78
- A+B actual routed total(A+B 실제 라우팅 전체) OOS(표본외): 4.066667 trades/day(일 거래 수), net(순손익) 233.06, PF(수익 팩터) 1.11, max DD(최대 손실) 188.43
- closest OOS quality read(가장 가까운 표본외 품질 판독): `nf150_c6_h10_s350l250_b045`는 OOS(표본외) net(순손익) 590.30, PF(수익 팩터) 1.28, cost-stressed expectancy(비용 압박 기대값) 0.183218였지만 OOS density(표본외 밀도)는 4.430769였다.
- Tier B fallback-only OOS(Tier B 대체 전용 표본외): net(순손익) 15.82~16.67, PF(수익 팩터) 1.07로 non-negative(비음수)다.
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

Run50K(실행50K)는 model-axis density repair(모델 축 밀도 수리)로 non-flat sample weighting(비무포지션 표본 가중)과 recent-train model(최근 학습 모델)을 실제 MT5 validation/OOS(검증/표본외)로 시험했다. 효과(effect, 효과): density(밀도)를 모델 자체에서 늘릴 수 있는지 확인하고, Tier B(티어 B)가 보험 역할을 실제로 돕는지 비교했다.

- best intermediate variant(최선 중간 변형): `nf150_h10_s420l360_b045`
- A+B actual routed total(A+B 실제 라우팅 전체) validation(검증): 7.704918 trades/day(일 거래 수), net(순손익) 120.56, PF(수익 팩터) 1.03, max DD(최대 손실) 284.39
- A+B actual routed total(A+B 실제 라우팅 전체) OOS(표본외): 5.323077 trades/day(일 거래 수), net(순손익) -53.42, PF(수익 팩터) 0.98, max DD(최대 손실) 365.34
- density-pass quality-fail variants(밀도 통과 품질 실패 변형): `nf150_h10_s420l360_b045`와 `nf150_h10_s400l300_aonly`는 validation/OOS(검증/표본외) 모두 5+ trades/day(일 거래 수)에 도달했지만 OOS net/PF(표본외 순손익/수익 팩터), cost-stressed expectancy(비용 압박 기대값), same-move audit(동일 이동 감사)를 통과하지 못했다.
- Tier B fallback-only OOS(Tier B 대체 전용 표본외): net(순손익) -38.17, PF(수익 팩터) 0.87로 negative(음수)다.
- MFE capture read(MFE 포착 판독): best OOS MFE capture ratio(최선 표본외 MFE 포착 비율)는 0.619826이고 d390h10 reference(d390h10 참조) 대비 -0.008439라 materially worse(중대 악화)는 아니다.
- same-move read(동일 이동 판독): best OOS same-move re-entry ratio(최선 표본외 동일 이동 재진입 비율)는 0.786127이고 12-bar cooldown(12봉 쿨다운) 뒤 1.138462 trades/day(일 거래 수)로 떨어져 density gain(밀도 증가)이 생존하지 못했다.
- selected_research_baseline(선택 연구 기준선)으로 올리지 않는 이유: OOS net(표본외 순손익) 음수, validation/OOS PF(검증/표본외 수익 팩터) 1.10 미만, cost-stressed expectancy(비용 압박 기대값) 음수, same-move audit(동일 이동 감사) 실패, Tier B fallback-only OOS(Tier B 대체 전용 표본외) 음수다.

## Latest Run50J Intermediate Evidence(최신 50J 중간 근거)

- packet(묶음): `stage56_run50J_hold_extension_direction_v1`
- report(보고서): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50J_reopen_batch.md`
- summary_csv(요약 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50J_summary.csv`
- audit_csv(감사 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50J_audit.csv`
- aggregate_summary(합산 요약): `docs/agent_control/packets/stage56_run50J_hold_extension_direction_v1/aggregate_summary.json`
- selected_research_baseline(선택 연구 기준선): `none`
- current_judgment(현재 판정): `in_progress_no_selected_research_baseline`

Run50J(실행50J)는 hold extension(보유 연장) 10봉과 long-density/short-filter(롱 밀도/숏 필터) 변형을 실제 MT5 validation/OOS(검증/표본외)로 시험했다. 효과(effect, 효과): hold compression(보유 압축)이 만든 same-move split(동일 이동 분할)을 반대로 압박했다.

- best intermediate variant(최선 중간 변형): `h10_s400l295_aonly`
- A-only actual routed total(A 단독 실제 라우팅 전체) validation(검증): 4.360656 trades/day(일 거래 수), net(순손익) 397.72, PF(수익 팩터) 1.14, max DD(최대 손실) 243.44
- A-only actual routed total(A 단독 실제 라우팅 전체) OOS(표본외): 3.071795 trades/day(일 거래 수), net(순손익) 157.34, PF(수익 팩터) 1.07, max DD(최대 손실) 176.68
- Tier B fallback-only OOS(Tier B 대체 전용 표본외): net(순손익) -37.69, PF(수익 팩터) 0.87로 negative(음수)다.
- hold/re-entry audit(보유/재진입 감사): best OOS same-move re-entry ratio(최선 표본외 동일 이동 재진입 비율)는 0.636060이고 12-bar cooldown read(12봉 쿨다운 판독)는 1.138462 trades/day(일 거래 수)라 density gain(밀도 증가)이 생존하지 못했다.
- selected_research_baseline(선택 연구 기준선)으로 올리지 않는 이유: validation/OOS density(검증/표본외 밀도) 5.0 미만, OOS PF(표본외 수익 팩터) 1.10 미만, cost-stressed expectancy(비용 압박 기대값) 음수, same-move audit(동일 이동 감사) 실패다.

## Latest Run50I Intermediate Evidence(최신 50I 중간 근거)

- packet(묶음): `stage56_run50I_early_mid_session_direction_v1`
- report(보고서): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50I_reopen_batch.md`
- summary_csv(요약 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50I_summary.csv`
- audit_csv(감사 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50I_audit.csv`
- aggregate_summary(합산 요약): `docs/agent_control/packets/stage56_run50I_early_mid_session_direction_v1/aggregate_summary.json`
- selected_research_baseline(선택 연구 기준선): `none`
- current_judgment(현재 판정): `in_progress_no_selected_research_baseline`

Run50I(실행50I)는 run50H attribution(run50H 귀속)에서 late session(후반 세션)이 OOS(표본외)를 깎는 판독을 바탕으로 early+mid session(초반+중반 세션) 변형과 matched A-only/A+B comparison(맞춘 A 단독/A+B 비교)을 실제 MT5 validation/OOS(검증/표본외)로 시험했다. 효과(effect, 효과): session/weather instability(세션/시장 상태 불안정성)가 기준선 후보를 개선하는지 확인했다.

- best intermediate variant(최선 중간 변형): `em_s390l300h06_aonly`
- A-only actual routed total(A 단독 실제 라우팅 전체) validation(검증): 4.502732 trades/day(일 거래 수), net(순손익) 21.61, PF(수익 팩터) 1.01, max DD(최대 손실) 358.41
- A-only actual routed total(A 단독 실제 라우팅 전체) OOS(표본외): 3.512821 trades/day(일 거래 수), net(순손익) 471.91, PF(수익 팩터) 1.22, max DD(최대 손실) 167.58
- Tier B fallback-only OOS(Tier B 대체 전용 표본외): net(순손익) -40.84, PF(수익 팩터) 0.85로 negative(음수)다.
- hold/re-entry audit(보유/재진입 감사): best OOS same-move re-entry ratio(최선 표본외 동일 이동 재진입 비율)는 0.740146이고 12-bar cooldown read(12봉 쿨다운 판독)는 0.958974 trades/day(일 거래 수)라 density gain(밀도 증가)이 생존하지 못했다.
- selected_research_baseline(선택 연구 기준선)으로 올리지 않는 이유: validation/OOS density(검증/표본외 밀도) 5.0 미만, validation PF(검증 수익 팩터) 1.10 미만, validation cost-stressed expectancy(검증 비용 압박 기대값) 음수, same-move audit(동일 이동 감사) 실패다.

## Latest Run50H Intermediate Evidence(최신 50H 중간 근거)

- packet(묶음): `stage56_run50H_long_density_short_filter_v1`
- report(보고서): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50H_reopen_batch.md`
- summary_csv(요약 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50H_summary.csv`
- audit_csv(감사 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50H_audit.csv`
- aggregate_summary(합산 요약): `docs/agent_control/packets/stage56_run50H_long_density_short_filter_v1/aggregate_summary.json`
- selected_research_baseline(선택 연구 기준선): `none`
- current_judgment(현재 판정): `in_progress_no_selected_research_baseline`

Run50H(실행50H)는 long-density/short-filter(롱 밀도/숏 필터) 변형과 matched A-only/A+B comparison(맞춘 A 단독/A+B 비교)을 실제 MT5 validation/OOS(검증/표본외)로 시험했다. 효과(effect, 효과): short threshold(숏 임계값)을 더 높이고 long threshold(롱 임계값)을 더 낮춰 품질 보존 밀도가 가능한지 확인했다.

- best intermediate variant(최선 중간 변형): `s410l315h06_b045`
- A+B actual routed total(A+B 실제 라우팅 전체) validation(검증): 5.644809 trades/day(일 거래 수), net(순손익) 240.62, PF(수익 팩터) 1.08, max DD(최대 손실) 259.16
- A+B actual routed total(A+B 실제 라우팅 전체) OOS(표본외): 4.276923 trades/day(일 거래 수), net(순손익) 145.24, PF(수익 팩터) 1.06, max DD(최대 손실) 235.07
- Tier B fallback-only OOS(Tier B 대체 전용 표본외): net(순손익) -49.70, PF(수익 팩터) 0.80으로 negative(음수)다.
- hold/re-entry audit(보유/재진입 감사): best OOS same-move re-entry ratio(최선 표본외 동일 이동 재진입 비율)는 0.738609이고 12-bar cooldown read(12봉 쿨다운 판독)는 1.117949 trades/day(일 거래 수)라 density gain(밀도 증가)이 생존하지 못했다.
- selected_research_baseline(선택 연구 기준선)으로 올리지 않는 이유: OOS density(표본외 밀도) 5.0 미만, PF(수익 팩터) 1.10 미만, cost-stressed expectancy(비용 압박 기대값) 음수, same-move audit(동일 이동 감사) 실패, Tier B fallback-only OOS(Tier B 대체 전용 표본외) 음수다.

## Latest Run50G Intermediate Evidence(최신 50G 중간 근거)

- packet(묶음): `stage56_run50G_direction_threshold_tier_b_disablement_v1`
- report(보고서): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50G_reopen_batch.md`
- summary_csv(요약 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50G_summary.csv`
- audit_csv(감사 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50G_audit.csv`
- aggregate_summary(합산 요약): `docs/agent_control/packets/stage56_run50G_direction_threshold_tier_b_disablement_v1/aggregate_summary.json`
- failed_attempt_record(실패 시도 기록): `docs/agent_control/packets/stage56_run50G_direction_threshold_tier_b_disablement_v1/failed_attempt_metaeditor_path.json`
- selected_research_baseline(선택 연구 기준선): `none`
- current_judgment(현재 판정): `in_progress_no_selected_research_baseline`

Run50G(실행50G)는 short threshold(숏 임계값)을 높이고 long threshold(롱 임계값)을 낮춘 direction-threshold(방향 임계값) 변형과 matched A-only/A+B comparison(맞춘 A 단독/A+B 비교)을 실제 MT5 validation/OOS(검증/표본외)로 시험했다. 효과(effect, 효과): Tier B disablement(티어 B 비활성화) 근거와 방향별 밀도 보정 가능성을 함께 확인했다.

- first attempt(첫 시도): MetaEditor path(메타에디터 경로) 오류로 blocked(차단)됐고, 경로 수정 뒤 force rerun(강제 재실행)으로 실제 MT5 근거를 만들었다.
- best intermediate variant(최선 중간 변형): `s390l330h06_b045`
- A+B actual routed total(A+B 실제 라우팅 전체) validation(검증): 6.005464 trades/day(일 거래 수), net(순손익) 274.44, PF(수익 팩터) 1.08, max DD(최대 손실) 257.48
- A+B actual routed total(A+B 실제 라우팅 전체) OOS(표본외): 4.594872 trades/day(일 거래 수), net(순손익) 109.52, PF(수익 팩터) 1.04, max DD(최대 손실) 312.34
- Tier B fallback-only OOS(Tier B 대체 전용 표본외): net(순손익) -49.70, PF(수익 팩터) 0.80으로 negative(음수)다.
- hold/re-entry audit(보유/재진입 감사): best OOS same-move re-entry ratio(최선 표본외 동일 이동 재진입 비율)는 0.742188이고 12-bar cooldown read(12봉 쿨다운 판독)는 1.184615 trades/day(일 거래 수)라 density gain(밀도 증가)이 생존하지 못했다.
- selected_research_baseline(선택 연구 기준선)으로 올리지 않는 이유: OOS density(표본외 밀도) 5.0 미만, PF(수익 팩터) 1.10 미만, cost-stressed expectancy(비용 압박 기대값) 음수, same-move audit(동일 이동 감사) 실패, Tier B fallback-only OOS(Tier B 대체 전용 표본외) 음수다.

## Latest Run50F Intermediate Evidence(최신 50F 중간 근거)

- packet(묶음): `stage56_run50F_cooldown_b_tight_repair_v1`
- report(보고서): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50F_reopen_batch.md`
- summary_csv(요약 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50F_summary.csv`
- audit_csv(감사 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50F_audit.csv`
- aggregate_summary(합산 요약): `docs/agent_control/packets/stage56_run50F_cooldown_b_tight_repair_v1/aggregate_summary.json`
- selected_research_baseline(선택 연구 기준선): `none`
- current_judgment(현재 판정): `in_progress_no_selected_research_baseline`

Run50F(실행50F)는 reentry cooldown(재진입 쿨다운) 1~2봉과 stricter Tier B(더 엄격한 Tier B) 0.42~0.45를 실제 MT5 validation/OOS(검증/표본외)로 시험했다. 효과(effect, 효과): run50E(실행50E)에서 보인 same-move split trading(동일 이동 분할 거래) 위험을 실제 실행 규칙으로 압박했다.

- best intermediate variant(최선 중간 변형): `d330h06_b045_c1`
- A+B actual routed total(A+B 실제 라우팅 전체) validation(검증): 6.333333 trades/day(일 거래 수), net(순손익) 53.40, PF(수익 팩터) 1.02, max DD(최대 손실) 279.72
- A+B actual routed total(A+B 실제 라우팅 전체) OOS(표본외): 4.728205 trades/day(일 거래 수), net(순손익) 114.76, PF(수익 팩터) 1.04, max DD(최대 손실) 241.93
- Tier B fallback-only OOS(Tier B 대체 전용 표본외): best nearby reads(근접 판독)는 B045에서 net(순손익) -62.55 또는 -10.06, PF(수익 팩터) 0.75~0.95로 여전히 negative(음수)다.
- hold/re-entry audit(보유/재진입 감사): 12-bar cooldown read(12봉 쿨다운 판독) 뒤 OOS trades/day(표본외 일 거래 수)는 약 1.35~1.36이고 same-move re-entry ratio(동일 이동 재진입 비율)는 약 0.68~0.71이다.
- selected_research_baseline(선택 연구 기준선)으로 올리지 않는 이유: OOS density(표본외 밀도) 5.0 미만, PF(수익 팩터) 1.10 미만, cost-stressed expectancy(비용 압박 기대값) 음수, Tier B fallback-only OOS(Tier B 대체 전용 표본외) 음수다.
- prior_candidate(이전 후보): `d38h10`
- preserved_density_frontier(보존 밀도 경계): `d35h07_routed_density_failed_quality`
- preserved_quality_frontier(보존 품질 경계): `d390h10_stronger_quality_net_candidate`
- current_operating_reference(현재 운영 참조): `none`
- runtime_authority(런타임 권위): `none`
- live_readiness(실거래 준비): `none`
- operating_promotion(운영 승격): `none`
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Latest Run50E Intermediate Evidence(최신 50E 중간 근거)

- packet(묶음): `stage56_run50E_density_reentry_tier_b_disablement_v1`
- report(보고서): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50E_reopen_batch.md`
- summary_csv(요약 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50E_summary.csv`
- audit_csv(감사 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50E_audit.csv`
- aggregate_summary(합산 요약): `docs/agent_control/packets/stage56_run50E_density_reentry_tier_b_disablement_v1/aggregate_summary.json`
- selected_research_baseline(선택 연구 기준선): `none`
- current_judgment(현재 판정): `in_progress_no_selected_research_baseline`

Run50E(실행50E)는 actual MT5 validation/OOS(실제 MT5 검증/표본외) 9개 variant(변형)를 완료했다. 효과(effect, 효과): Stage56(56단계)을 닫지 않고, 다음 hypothesis branch(가설 가지)를 좁힌다.

- d390h10_aonly(변형): validation/OOS(검증/표본외) 3.775956/2.794872 trades/day(일 거래 수), PF(수익 팩터) 1.19/1.09, net(순손익) 488.03/204.48. quality(품질)는 비교적 좋지만 density(밀도) 기준을 통과하지 못했다.
- d340h06_ab_b040(변형): validation/OOS(검증/표본외) 6.934426/5.282051 trades/day(일 거래 수), PF(수익 팩터) 1.06/1.03, net(순손익) 202.83/99.77. density(밀도)는 통과했지만 PF(수익 팩터), cost-stressed expectancy(비용 압박 기대값), same-move audit(동일 이동 감사)를 통과하지 못했다.
- d350h06_ab_b040(변형): validation/OOS(검증/표본외) 6.732240/5.148718 trades/day(일 거래 수), PF(수익 팩터) 1.06/1.03, net(순손익) 199.14/95.60. density(밀도)는 통과했지만 PF(수익 팩터), cost-stressed expectancy(비용 압박 기대값), same-move audit(동일 이동 감사)를 통과하지 못했다.
- hold/re-entry audit(보유/재진입 감사): dense variants(고밀도 변형)의 same-move re-entry ratio(동일 이동 재진입 비율)는 약 0.72~0.75였고, 12-bar cooldown(12봉 쿨다운) 뒤 trades/day(일 거래 수)는 대략 1.3~1.9로 떨어졌다. 효과(effect, 효과): 이번 density gain(밀도 증가)은 selected_research_baseline(선택 연구 기준선) 근거가 아니다.
- Tier B read(Tier B 판독): B040 fallback-only OOS(B040 대체 전용 표본외)는 net(순손익) -171.98, PF(수익 팩터) 0.70으로 damaging(손상)했다. A+B routed total(A+B 실제 라우팅 전체)은 OOS density(표본외 밀도)를 올렸지만 PF/net(수익 팩터/순손익)을 기준선 조건까지 끌어올리지 못했다.

## Prior Intermediate Evidence(이전 중간 근거)

- status_note(상태 메모): this section is non-final intermediate evidence(이 구간은 비최종 중간 근거)이다.
- run50D(실행50D) deep repair suite(조밀 보정 묶음)는 18개 variant(변형)를 실제 MT5 strategy tester(메타트레이더5 전략 테스터) closed trades(청산 거래) 기준으로 비교했다.
- best stronger candidate(최선 강화 후보): `d390h10`
- A+B actual routed total(A+B 실제 라우팅 전체) validation(검증): 748 trades(거래), 4.087432 trades/day(일 거래 수), net(순손익) 341.54, PF(수익 팩터) 1.13, max DD(최대 손실) 229.20
- A+B actual routed total(A+B 실제 라우팅 전체) OOS(표본외): 594 trades(거래), 3.046154 trades/day(일 거래 수), net(순손익) 273.20, PF(수익 팩터) 1.12, max DD(최대 손실) 179.28
- comparison reference(비교 기준): prior d38h10(이전 d38h10)는 validation/OOS(검증/표본외) density(밀도) 4.464481/3.446154, PF(수익 팩터) 1.07/1.13, total net(총 순손익) 492.48였다.
- selected_research_baseline(선택 연구 기준선)으로 올리지 않는 이유: OOS density(표본외 밀도)가 preferred density target(선호 밀도 목표) 5~10 trades/day(거래/일)에 못 미친다.
- closeout packet(종료 묶음): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/stage56_closeout_packet.md`
- run50D report(실행50D 보고서): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50D_deep_repair_suite.md`
- run50D summary(실행50D 요약): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50D_deep_repair_suite_summary.csv`
- market-weather attribution(시장 상태 귀속): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/stage56_run50D_d390h10_market_weather_attribution.md`

## Terminal Condition(종료 조건)

Stage56(56단계)은 selected_research_baseline(선택 연구 기준선)이 발견될 때만 닫는다. 효과(effect, 효과): d390h10은 연구 후보로 d38h10보다 강하게 보존하지만, Stage56(56단계)을 닫거나 selected_research_baseline(선택 연구 기준선), live readiness(실거래 준비), runtime authority(런타임 권위), operating promotion(운영 승격), operating reference(운영 참조)를 만들지 않는다.
