# run04H_mlp_direction_collision_attribution_v1 결과 요약(Result Summary, 결과 요약)

- status(상태): `completed(완료)`
- judgment(판정): `inconclusive_collision_attribution_completed(충돌 기여도 분해 완료, 판단은 불충분)`
- source run(원천 실행): `run04F_mlp_direction_asymmetry_runtime_probe_v1`
- boundary(경계): `collision_attribution_only_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`

## 핵심 판독(Core Read, 핵심 판독)

- direct same-bar collision(같은 봉 직접 충돌): validation/OOS(검증/표본외) 모두 `0`이었다.
- OOS(표본외) opposite position signal(반대 포지션 신호): `27`개였다.
- OOS(표본외) reverse open(반전 진입): long(매수) `19`, short(매도) `6`였다.
- OOS(표본외) short(매도) same-open(같은 진입 시각) 중 close changed(청산 시각 변경): `18`개, delta(차이) `-66.57`였다.

효과(effect, 효과): both(양방향) 손상은 신호가 같은 봉에서 long/short(매수/매도)로 동시에 난 문제가 아니라, 단일 계좌 경로에서 reverse(반전)와 early close(조기 청산)가 거래 정체성을 바꾼 문제로 좁혀진다.

## Telemetry Collision(원격측정 충돌)

| split(분할) | long candidates(매수 후보) | short candidates(매도 후보) | same-bar collision(같은 봉 충돌) | opposite signals(반대 포지션 신호) | reverse long(반전 매수) | reverse short(반전 매도) | net damage(순손상) |
|---|---:|---:|---:|---:|---:|---:|---:|
| validation_is | 903 | 82 | 0 | 30 | 16 | 13 | -42.03 |
| oos | 557 | 103 | 0 | 27 | 19 | 6 | -130.62 |

## Trade Identity(거래 정체성)

| split(분할) | side(방향) | separate/both count(분리/양방향 거래 수) | same exact(완전 동일) | same open(같은 진입) | changed close(청산 변경) | net delta(순차이) | changed close delta(청산 변경 차이) |
|---|---|---:|---:|---:|---:|---:|---:|
| validation_is | long | 212/216 | 179 | 190 | 11 | -43.84 | -101.27 |
| validation_is | short | 47/49 | 32 | 47 | 15 | 1.81 | 8.20 |
| oos | long | 159/159 | 150 | 156 | 6 | -14.49 | -19.65 |
| oos | short | 49/49 | 27 | 45 | 18 | -116.13 | -66.57 |

## OOS Close Action(표본외 청산 행동)

| side(방향) | open action(진입 행동) | close action(청산 행동) | trades(거래 수) | net(순수익) | avg(평균) |
|---|---|---|---:|---:|---:|
| long | open_long | close_max_hold | 137 | 208.66 | 1.52 |
| long | open_long | reverse_open_short | 3 | -12.59 | -4.20 |
| long | reverse_open_long | close_max_hold | 16 | -56.69 | -3.54 |
| long | reverse_open_long | reverse_open_short | 3 | -70.51 | -23.50 |
| short | open_short | close_max_hold | 27 | 20.43 | 0.76 |
| short | open_short | reverse_open_long | 16 | -44.46 | -2.78 |
| short | reverse_open_short | close_max_hold | 3 | 31.27 | 10.42 |
| short | reverse_open_short | reverse_open_long | 3 | -19.44 | -6.48 |

효과(effect, 효과): short-only(매도 전용) OOS(표본외) 49 trades(49개 거래)는 여전히 얇은 clue(단서)이고, both(양방향)에서는 특히 short(매도) 청산 시각이 바뀌며 수익이 훼손됐다.
