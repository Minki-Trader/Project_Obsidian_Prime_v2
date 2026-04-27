# RUN03B Standalone ExtraTrees Result Summary

RUN03B(실행 03B)는 Stage 10/11(10/11단계)을 계승하지 않는 standalone(단독) ExtraTrees(엑스트라 트리) 학습 효과 탐침이다.

| split(분할) | macro F1(매크로 F1) | signals(신호) | hit rate(적중률) |
|---|---:|---:|---:|
| validation(검증) | `0.4246068031038796` | `604` | `0.3526490066225166` |
| OOS(표본외) | `0.44655366112413875` | `463` | `0.42764578833693306` |

판정(judgment, 판정): `inconclusive_standalone_extratrees_training_effect`

효과(effect, 효과): 모델은 학습됐고 독립 신호 규칙도 만들어졌지만, MT5 runtime_probe(MT5 런타임 탐침)나 운영 의미(operational meaning, 운영 의미)는 아직 없다.
