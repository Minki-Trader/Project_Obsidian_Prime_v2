# Frontier17 Definition Locks(전선17 정의 고정)

Action(행동): Frontier17B(전선17B) 물질화 전에 adverse cluster(불리 군집), continuation quality(지속 품질), decision gate(결정 게이트)의 의미를 고정합니다.

Effect(효과): F16 risk-quality label(전선16 위험 품질 라벨)을 이름만 바꿔 반복하는 일을 막습니다.

- `adverse_cluster_state_contract`: Use train-only adverse-cluster score from closed-bar market state and path-risk diagnostics; do not reuse F16 edge_margin label columns(종료봉 시장 상태와 경로 위험 진단으로 학습 전용 불리 군집 점수를 만들고 F16 엣지 마진 라벨 열은 재사용하지 않음).
- `continuation_quality_contract`: Use realized continuation quality as a separate target axis; no future-edge label rename(실현 지속 품질을 별도 목표 축으로 쓰며 미래 엣지 라벨 이름 변경 금지).
- `decision_and_gate_contract`: Runtime decision meaning is NOT adverse_veto AND continuation_trigger; no score-rank density calibration(런타임 결정 의미는 불리 배제 아님 AND 지속 트리거이며 점수 순위 빈도 보정 금지).
