# Frontier28B Train-Only Stability Gap Proxy Report(전선28B 학습 전용 안정성 격차 프록시 보고서)

Updated(갱신): 2026-06-14T11:02:05Z

Status(상태): `stability_gap_scout_clue_proxy_no_authority`

Judgment(판정): `scout_clue_requires_repair_or_closeout_no_authority`

Action(행동): F27B reference union surface(F27B 참조 합집합 표면) `234`개를 재구성하고, train-only four-chunk stability gap rank(학습 전용 4조각 안정성 격차 순위)로 다시 정렬했습니다.

Effect(효과): validation/OOS(검증/표본외)를 선택에 쓰지 않고, 학습 내부의 PF/DD instability(수익 팩터/손실폭 불안정성)가 전진 균형을 더 잘 예고하는지 확인했습니다.

Reference/stability/chunk rows(참조/안정성/조각 행): `234` / `234` / `936`

Density/scout/seed/handoff rows(빈도/탐색/씨앗/인계 행): `189` / `19` / `0` / `0`

Best stability union(최상 안정성 합집합): `f28b_0001` from `f27b_0003`

Best validation PF/density/DD(최상 검증 수익 팩터/빈도/손실폭): `1.044` / `5.749/day` / `20.604%`

Best OOS PF/density/DD(최상 표본외 수익 팩터/빈도/손실폭): `1.044` / `6.679/day` / `16.198%`

Runtime probe status(런타임 탐침 상태): `out_of_scope_by_claim_no_handoff_candidate(인계 후보 없어 주장 범위 밖)`

## Top Stability Rows(상위 안정성 행)

| F28 union(F28 합집합) | source(F27 원천) | micro ids(미세 ID) | stability score(안정성 점수) | chunk PF floor(조각 PF 바닥) | chunk DD max(조각 DD 최대) | density CV(빈도 변동계수) | net+ chunks(양수 조각) | val PF | val density | val DD | OOS PF | OOS density | OOS DD | scout | seed |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `f28b_0001` | `f27b_0003` | `f24p_0045|f24p_0064` | 4.765 | 1.316 | 13.985 | 0.157 | 4.000 | 1.044 | 5.749 | 20.604 | 1.044 | 6.679 | 16.198 | False | False |
| `f28b_0002` | `f27b_0082` | `f24p_0056|f24p_0064|f24p_0067` | 4.482 | 1.337 | 16.916 | 0.169 | 4.000 | 1.119 | 6.934 | 19.874 | 1.183 | 7.802 | 18.024 | True | False |
| `f28b_0003` | `f27b_0002` | `f24p_0056|f24p_0064` | 4.471 | 1.383 | 14.375 | 0.197 | 4.000 | 0.997 | 4.699 | 12.216 | 1.124 | 4.374 | 10.189 | False | False |
| `f28b_0004` | `f27b_0007` | `f24p_0056|f24p_0036` | 4.450 | 1.301 | 15.456 | 0.162 | 4.000 | 1.014 | 5.705 | 15.434 | 1.122 | 5.435 | 18.721 | False | False |
| `f28b_0005` | `f27b_0017` | `f24p_0060|f24p_0064|f24p_0001` | 4.396 | 1.353 | 18.082 | 0.160 | 4.000 | 1.053 | 7.306 | 14.450 | 0.982 | 8.931 | 22.112 | False | False |
| `f28b_0006` | `f27b_0020` | `f24p_0064|f24p_0011|f24p_0015` | 4.328 | 1.334 | 18.026 | 0.159 | 4.000 | 1.091 | 6.607 | 31.467 | 1.129 | 7.649 | 21.748 | False | False |
| `f28b_0007` | `f27b_0021` | `f24p_0045|f24p_0064|f24p_0038` | 4.218 | 1.294 | 17.030 | 0.166 | 4.000 | 1.003 | 6.557 | 20.741 | 1.044 | 7.786 | 16.893 | False | False |
| `f28b_0008` | `f27b_0078` | `f24p_0015|f24p_0064|f24p_0005` | 4.201 | 1.332 | 17.759 | 0.170 | 4.000 | 1.121 | 6.240 | 29.250 | 1.152 | 7.359 | 20.363 | False | False |
| `f28b_0009` | `f27b_0014` | `f24p_0012|f24p_0064|f24p_0062` | 4.161 | 1.325 | 18.333 | 0.187 | 4.000 | 1.155 | 7.197 | 29.395 | 1.067 | 8.466 | 23.249 | False | False |
| `f28b_0010` | `f27b_0050` | `f24p_0064|f24p_0016|f24p_0010` | 4.148 | 1.431 | 18.659 | 0.199 | 4.000 | 1.304 | 6.923 | 22.959 | 1.074 | 8.634 | 20.953 | False | False |
| `f28b_0011` | `f27b_0051` | `f24p_0064|f24p_0017|f24p_0010` | 4.148 | 1.431 | 18.659 | 0.199 | 4.000 | 1.304 | 6.923 | 22.959 | 1.074 | 8.634 | 20.953 | False | False |
| `f28b_0012` | `f27b_0013` | `f24p_0056|f24p_0064|f24p_0036` | 4.147 | 1.283 | 17.357 | 0.192 | 4.000 | 1.021 | 6.749 | 15.398 | 1.134 | 6.641 | 17.485 | False | False |

Next action(다음 행동): `frontier28C_stability_gap_repair_or_closeout_decision_v1`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
