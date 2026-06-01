# run354C Expanded Proxy Filter Sweep(354C 확장 프록시 필터 스윕)

- run_id(실행 ID): `run354C_expand_proxy_filter_sweep_without_db_v1`
- status(상태): `completed_stage354C_expanded_sweep_no_density_edge_queue_model_family_pivot_opened`
- judgment(판정): `negative_proxy_scout_existing_surface_no_density_edge_queue_no_operating_claim`
- decision(결정): `stage354C_open_run355A_design_density_recovery_label_model_source_without_db_v1`
- sweep_rows(스윕 행): `6912`
- density_valid_queue_rows(밀도 유효 대기열 행): `0`
- next_stage_id(다음 단계 ID): `355_density_recovery_model_family__new_label_source_probe`
- next_run_id(다음 실행 ID): `run355A_design_density_recovery_label_model_source_without_db_v1`

## Action(행동)

Stage351B(351B 실행)의 probability tape(확률 테이프)와 runtime features(런타임 피처)를 유지하고, raw US100 close(원시 US100 종가)에서 `4/6/8/12` bar future return(봉 미래 수익률)을 새 proxy label(프록시 라벨)로 계산했다. 그 다음 filter/threshold/margin(필터/임계값/마진) 조합을 non-overlap trade shape(비중첩 거래 형태)로 다시 검사했다.

## Effect(효과)

trade splitting(거래 쪼개기) 없이 trade/day(일별 거래수) `3+` 조건을 지키면서, 기존 surface(표면)가 작은 보유기간이나 넓은 필터에서 살아나는지 확인했다.

## Best Read(최상 판독)

- candidate_id(후보 ID): `b03_1d_logreg_cashopen_c050__h6__adx25__s0.380__l0.320__m0.020`
- model_variant_id(모델 변형 ID): `b03_1d_logreg_cashopen_c050`
- hold_bars(보유 봉): `6`
- filter_name(필터 이름): `adx25`
- validation net(검증 순 로그수익): `-0.001025910034607766`
- validation PF(검증 수익 팩터): `0.9986716739396042`
- validation trade/day(검증 일별 거래수): `3.8785714285714286`
- oos net(표본외 순 로그수익): `0.010006124178335699`
- oos PF(표본외 수익 팩터): `1.020167550935205`
- oos trade/day(표본외 일별 거래수): `4.009174311926605`
- validation stress net(검증 비용 압박 순 로그수익): `-0.08247591003460776`
- oos stress net(표본외 비용 압박 순 로그수익): `-0.0555438758216643`

## Boundary(경계)

이 결과는 proxy scout(프록시 탐색)이다. MT5 KPI(MT5 핵심 성과 지표), candidate selection(후보 선정), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 주장하지 않는다.

## Next Action(다음 행동)

`run355A_design_density_recovery_label_model_source_without_db_v1`.

Effect(효과): 같은 기존 surface(표면)의 micro threshold search(임계값 미세 탐색)를 반복하지 않고, 다음 단계에서 더 맞는 수익 원천을 찾는다.
