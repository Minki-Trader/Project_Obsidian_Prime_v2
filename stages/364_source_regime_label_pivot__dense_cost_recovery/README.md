# Stage364(364단계): Source Regime Label Pivot(원천 국면 라벨 전환)

Action(행동): Stage363C(363C 실행)의 lower-floor/rank failure(낮은 하한/순위 실패)에서 timestamp-safe context(시점 안전 문맥) 탐색으로 분기했다.

Effect(효과): q05 dense trade count(q05 고밀도 거래수)를 쪼개지 않고 cost drag(비용 끌림)를 줄일 수 있는 새 설명 축을 확인한다.

## run364B Materialization(364B 구체화)

Action(행동): timestamp-safe context(시점 안전 문맥)를 q05 long-only MT5 report-derived trades(q05 롱 단독 MT5 보고서 파생 거래)에 적용했다.

Effect(효과): 비용 양수와 trade density(거래 밀도)를 동시에 보는 Stage364C(364C 실행) review(검토) 대기열을 열었다.

## run364C Review(364C 검토)

Action(행동): Stage364B(364B) positive scout(긍정 스카우트)를 월별 안정성과 과적합 위험으로 검토했다.

Effect(효과): 다음 실행은 `run364D_materialize_timestamp_context_training_seed_without_db_v1`이고, 운영 주장은 없다.

## run364D Training Seed(364D 학습 씨앗)

Action(행동): q05 trade table(q05 거래표)를 model training seed(모델 학습 씨앗)로 구체화했다.

Effect(효과): 다음 실행은 `run364E_train_timestamp_context_cost_filter_model_without_db_v1`이고, 운영 주장은 없다.

## run364E Model Training(364E 모델 학습)

Action(행동): timestamp context(시점 문맥) 학습 씨앗으로 ONNX-exportable cost filter(ONNX 변환 가능 비용 필터)를 만들었다.

Effect(효과): 다음 실행은 `run364F_prepare_timestamp_context_onnx_runtime_probe_without_db_v1`이고, 운영 주장은 없다.

## run364F Runtime Probe Package(364F 런타임 탐침 패키지)

Action(행동): timestamp context cost-filter(시점 문맥 비용 필터)를 MT5 runtime package(MT5 런타임 패키지)로 만들었다.

Effect(효과): proxy expected tape(프록시 예상 테이프)와 MT5 telemetry(MT5 런타임 기록)를 비교할 준비가 끝났다.

## run364G MT5 Runtime Probe(MT5 런타임 탐침)

- run_id(실행 ID): `run364G_execute_timestamp_context_onnx_mt5_runtime_probe_without_db_v1`
- summary(요약): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364G/timestamp_context_onnx_mt5_probe_summary.csv`
- effect(효과): Stage364(364단계)의 proxy(프록시)를 MT5 runtime evidence(MT5 런타임 근거)로 대조한다.
