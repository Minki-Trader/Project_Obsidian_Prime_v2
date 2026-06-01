# run355B Density Recovery Label Materialization(355B 밀도 회복 라벨 물질화)

- run_id(실행 ID): `run355B_materialize_density_recovery_label_inputs_without_db_v1`
- status(상태): `completed_stage355B_timestamp_safe_label_inputs_materialized_training_queue_ready_no_selection`
- judgment(판정): `timestamp_safe_label_materialization_positive_training_queue_no_operating_claim`
- decision(결정): `stage355B_open_run355C_train_density_recovery_proxy_models_without_db_v1`
- label_table_rows(라벨 표 행): `186600`
- label_variant_count(라벨 변형 수): `4`
- training_queue_rows(학습 대기열 행): `4`
- next_run_id(다음 실행 ID): `run355C_train_density_recovery_proxy_models_without_db_v1`

## Action(행동)

Stage355A(355A 실행)의 materialization queue(물질화 대기열)를 받아, raw US100 M5 bars(원시 US100 M5 봉)와 runtime features(런타임 피처)를 timestamp-safe(시점 안전) 방식으로 결합했다.

## Effect(효과)

세 가지 새 label family(라벨 계열)를 실제 학습 입력으로 만들었다. 이 결과는 model training(모델 학습)이나 MT5 KPI(MT5 핵심 성과 지표)가 아니라 다음 학습 실행의 입력이다.

## Density Read(밀도 판독)

- `d02_tb12_path_quality` `oos` projected_nonflat/day(예상 비중립 일별): `48.70992366412214` balance(균형): `0.6129929221435794`
- `d02_tb12_path_quality` `validation` projected_nonflat/day(예상 비중립 일별): `45.94535519125683` balance(균형): `0.6765702891326022`
- `d01_h8_cost_buffer` `oos` projected_nonflat/day(예상 비중립 일별): `33.541984732824424` balance(균형): `0.9801712483100495`

## Boundary(경계)

training(학습), proxy KPI(프록시 핵심 성과 지표), MT5 runtime probe(MT5 런타임 탐침), candidate selection(후보 선정), runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성)는 주장하지 않는다.
