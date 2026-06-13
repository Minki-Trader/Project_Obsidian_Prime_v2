# Decision: Open Frontier08(결정: 전선08 개방)

Date(날짜): 2026-06-14

Decision(결정): open `stage_frontier_08__sample_weighted_objective` with `frontier08A_stage_open_sample_weight_objective_v1`.

Reason(이유): Frontier07(전선07)의 risk label/class-prior repair(위험 라벨/클래스 사전분포 수리)는 strict clue(엄격 단서)를 만들지 못했으므로, 다음 axis(축)는 train loss weighting(학습 손실 가중)으로 둡니다.

Effect(효과): 새 hypothesis lifecycle(가설 생명주기)을 열고, 이전 frontier(전선)는 reference only(참조 전용)로 유지합니다.
