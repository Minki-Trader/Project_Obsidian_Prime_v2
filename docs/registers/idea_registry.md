# Idea Registry

| idea_id | stage_id | hypothesis | tier_scope | status | notes |
|---|---|---|---|---|---|
| `IDEA-ST11-LGBM-DIRECTION-LONG-ONLY` | `11_alpha_robustness__wfo_label_horizon_sensitivity` | LGBM(`LightGBM`, 라이트GBM) 실패가 direction-asymmetric(방향 비대칭)일 수 있고, long-only(롱만) 라우팅이 short(숏) 손상을 제거할 수 있다 | `Tier A + Tier B mixed(Tier A + Tier B 혼합)` | `runtime_probe_completed_inconclusive` | RUN02C(실행 02C); validation/OOS(검증/표본외) `-154.01/82.69` net profit(순수익); salvage value(회수 가치) 있음 |
| `IDEA-ST11-LGBM-DIRECTION-SHORT-ONLY` | `11_alpha_robustness__wfo_label_horizon_sensitivity` | LGBM(라이트GBM) 실패가 direction-asymmetric(방향 비대칭)일 수 있고, short-only(숏만) 라우팅이 long(롱) 손상을 제거할 수 있다 | `Tier A + Tier B mixed(Tier A + Tier B 혼합)` | `runtime_probe_completed_weak` | RUN02D(실행 02D); OOS(표본외) `-211.48 / 0.31`로 약함 |
| `IDEA-ST11-LGBM-EXTREME-CONFIDENCE` | `11_alpha_robustness__wfo_label_horizon_sensitivity` | LGBM(라이트GBM)은 extreme probability and margin(극단 확률과 마진)에서만 쓸 수 있을 수 있다 | `Tier A + Tier B mixed(Tier A + Tier B 혼합)` | `runtime_probe_completed_inconclusive` | RUN02E(실행 02E); OOS(표본외)는 `-6.35 / 0.96`로 거의 본전이나 validation(검증)이 약함 |
| `IDEA-ST11-LGBM-CALM-TREND-GATE` | `11_alpha_robustness__wfo_label_horizon_sensitivity` | calm trend context(차분한 추세 문맥)에서만 LGBM(라이트GBM) 신호가 깨끗할 수 있다 | `Tier A + Tier B mixed(Tier A + Tier B 혼합)` | `runtime_probe_completed_weak` | RUN02F(실행 02F); validation/OOS(검증/표본외) 모두 약함 |

## Rule

Register ideas when they become durable work, not for every passing thought.
