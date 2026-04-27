# RUN02T~RUN02V Priority Probe Packet

## Scope

`run02T_run02V_priority_probe_packet_v1`은 Stage 11(11단계)의 다음 우선순위 1/2/3을 구조 탐침(structural probe, 구조 탐침)으로 정리한다.

- Priority 1(우선순위 1): label/horizon sensitivity(라벨/예측수평선 민감도)
- Priority 2(우선순위 2): WFO-lite(가벼운 워크포워드 최적화) 가능성
- Priority 3(우선순위 3): short-specific(숏 전용) 구조 판독

## Result Table

| Run(실행) | Question(질문) | Primary read(핵심 판독) | Judgment(판정) |
|---|---|---|---|
| RUN02T | label/horizon(라벨/예측수평선) | best OOS horizon `18`, hit `0.714286` vs fwd12 `0.285714` | `horizon_shift_worth_retraining_probe` |
| RUN02U | WFO-lite(WFO-lite) | OOS signals `10`, nonzero windows `3` | `wfo_lite_density_insufficient_for_full_wfo` |
| RUN02V | short-specific(숏 전용) | P hit `0.1`, Q hit `0.190476`, density x `2.1` | `short_specific_probe_inconclusive` |

## Boundary

이 packet(묶음)은 Python structural probe(파이썬 구조 탐침)이다. 재학습(retraining, 재학습), MT5 runtime(런타임), operating promotion(운영 승격)을 주장하지 않는다.

Effect(효과): 다음 작업에서 전체 WFO(워크포워드 최적화)를 바로 태우기 전에, 비용 대비 정보량이 큰 방향을 먼저 고른다.
