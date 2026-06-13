# Stage355 Barrier Precedent(Stage355 장벽 선례)

Archive citation(보관소 인용):
- `stage_pipelines/stage355/materialize_density_recovery_label_inputs_without_db.py`
- Function(함수): `first_barrier_labels`
- Archived design(보관 설계): `d02_triple_barrier_path_quality_fwd12`

Reusable artifact(재사용 산출물): Stage355 already tested barrier/path style labeling(장벽/경로형 라벨링). Frontier04(전선04)는 이 선례를 novelty claim(신규성 주장)의 한계로 인용합니다.

Frontier04 semantic diff(전선04 의미 차이):
- Action(행동): reuse the barrier idea as a reference, not inheritance(장벽 아이디어를 상속이 아닌 참조로 사용). Effect(효과): 과거 winner/baseline/promotion(승자/기준선/승격)을 가져오지 않습니다.
- Action(행동): require OHLC alignment manifest before label materialization(라벨 물질화 전 OHLC 정렬 목록 요구). Effect(효과): timezone/alignment failure(시간대/정렬 실패)를 invalid setup(무효 설정)으로 분리할 수 있습니다.
- Action(행동): compare each path label against a close-return proxy on identical rows/splits(각 경로 라벨을 동일 행/분할의 종가 수익률 프록시와 비교). Effect(효과): DD(drawdown, 손실폭) 개선이 고립 지표가 아니라 paired delta(쌍 비교 차이)로 남습니다.
- Action(행동): keep Frontier04B proxy-only(전선04B 프록시 전용 유지). Effect(효과): ONNX/WFO/MT5 주장으로 너무 빨리 넘어가지 않습니다.

Claim boundary(주장 경계): this is archive-aware path labeling(보관소 인식 경로 라벨링) exploration(탐색) only, not a completion candidate(완성 후보), baseline(기준선), promotion(승격), runtime authority(런타임 권위), or live readiness(실거래 준비).
