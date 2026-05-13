# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `stage56_run50AT_extratrees_leaf_granularity_transition_density_source_v1`
- current run(현재 실행): `run50AT_stage56_extratrees_leaf_granularity_transition_density_source_v1`
- active stage(활성 단계): `56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection`
- selected_research_baseline(선택 연구 기준선): `none`
- status(상태): active_in_progress(활성 진행 중)
- terminal_condition(종료 조건): useful BaselineAdapter(유용한 기준선 어댑터) hard condition(강한 완료 조건) satisfied(충족)

Stage56(56단계)은 unfinished optimization campaign(미완 최적화 캠페인)으로 계속 열려 있다. Effect(효과): run50AT(실행50AT)는 ExtraTrees(엑스트라트리스) leaf granularity/source(잎 세분도/원천) 변경을 실제 MT5 validation/OOS(검증/표본외)로 확인한 중간 근거다.

## Latest Evidence(최신 근거)

- latest_batch(최신 묶음): `run50AT_stage56_extratrees_leaf_granularity_transition_density_source_v1`
- selected_research_baseline(선택 연구 기준선): `none`
- best_variant(현재 최선 변형): `et20h6_r030_b`
- stage56_remains_open(56단계 계속 열림): `True`
- forbidden claims(금지 주장): live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(운영 기준선), reviewed_closed(검토 종료)

## Current Bottleneck(현재 병목)

- OOS density(표본외 밀도), cost-stressed expectancy(비용 압박 기대값), same-move split re-entry(동일 이동 분할 재진입), and source replacement(원천 교체).
- run50AT judgment(실행50AT 판정): best_variant(현재 최선 변형) `et20h6_r030_b`는 validation/OOS(검증/표본외) trades/day(일 거래 수) `5.983607` / `4.271795`, net(순손익) `346.02` / `249.83`, PF(수익 팩터) `1.13` / `1.13`이다. 하지만 OOS density(표본외 밀도)가 5/day(일 5회) 미만이고, cost-stressed expectancy(비용 압박 기대값)는 validation/OOS(검증/표본외) `-0.184000` / `-0.200084`, same-move ratio(동일 이동 비율)는 `0.581735` / `0.596639`, 12-bar cooldown after density(12봉 쿨다운 후 밀도)는 `2.502732` / `1.723077`로 실패했다. Effect(효과): leaf granularity(잎 세분도) 변경도 실제 독립 밀도를 충분히 만들지 못했다.
- closest_density_variant(밀도 최접근 변형): `et20h6_r015_b`는 validation/OOS(검증/표본외) trades/day(일 거래 수) `6.584699` / `4.748718`, PF(수익 팩터) `1.07` / `1.14`, net(순손익) `220.66` / `312.02`이나 OOS density(표본외 밀도), cost stress(비용 압박), same-move/cooldown survival(동일 이동/쿨다운 생존)이 부족하다.
- run50AT attribution(실행50AT 기여도): `et20h6_r030_b`는 OOS(표본외) late session(후반 세션) `-1.81`, vol_high(고변동) `-15.91`, adx_gt25(ADX 25 초과) `-95.21`이 약하고, `et20h6_r015_b`는 OOS late session(후반 세션) `-79.22`, vol_high(고변동) `-14.53`이 약하다. Effect(효과): market-state filter(시장 상태 필터)만 붙이면 밀도가 더 줄 가능성이 높으므로 ExtraTrees(엑스트라트리스) branch(분기)는 reference/failure memory(참조/실패 기억)로 낮추고 QDA composite route(QDA 합성 라우트) 쪽으로 이동한다.
- next_hypothesis_branch(다음 가설 분기): `run50AU_composite_qda_route_density_repair`
