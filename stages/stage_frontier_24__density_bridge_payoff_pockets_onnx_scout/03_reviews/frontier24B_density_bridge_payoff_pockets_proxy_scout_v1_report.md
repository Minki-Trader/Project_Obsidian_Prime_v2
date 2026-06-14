# Frontier24B Density Bridge Payoff Pockets Proxy Scout Report(전선24B 빈도 연결 보상 구간 프록시 탐색 보고서)

Updated(갱신): 2026-06-14T08:02:58Z

Status(상태): `density_bridge_frequency_only_proxy_no_authority`

Judgment(판정): `density_clue_pf_or_dd_shortfall_requires_repair_or_closeout_no_authority`

Action(행동): F23C(전선23C)에서 파생한 micro-pocket(미세 구간)을 같은 방향 OR-union bridge(OR 합집합 연결)로 조립했습니다.

Effect(효과): timestamp(타임스탬프) 중복 신호는 한 거래로 세고, validation/OOS(검증/표본외)는 read-only diagnostic(읽기 전용 진단)으로만 사용해 density bridge(빈도 연결)가 실제 고유 빈도를 만드는지 확인했습니다.

Micro/bridge/metric rows(미세 구간/연결/지표 행): `80` / `180` / `540`

Density/scout/seed/handoff rows(빈도/탐색/씨앗/인계 행): `105` / `0` / `0` / `0`

Best bridge(최상 연결): `f24b_0174`

Best validation PF/density/DD(최상 검증 수익 팩터/빈도/손실폭): `1.2395` / `8.53552/day` / `30.5553%`

Best OOS PF/density/DD(최상 표본외 수익 팩터/빈도/손실폭): `1.14229` / `9.54962/day` / `21.154%`

Runtime probe status(런타임 탐침 상태): `out_of_scope_by_claim_no_handoff_candidate(인계 후보 없어 주장 범위 밖)`

## Top Readonly Forward Rows(상위 읽기 전용 전진 행)

| bridge(연결) | type(유형) | pockets(구간 수) | side(방향) | val PF | val density | val DD | OOS PF | OOS density | OOS DD | train overlap | scout | seed |
|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `f24b_0174` | pair | 2 | long(롱) | 1.2395 | 8.53552 | 30.5553 | 1.14229 | 9.54962 | 21.154 | 0.158287 | False | False |
| `f24b_0110` | pair | 2 | long(롱) | 1.23523 | 9 | 31.6094 | 1.12399 | 9.76336 | 21.2141 | 0.126776 | False | False |
| `f24b_0053` | triple | 3 | long(롱) | 1.19358 | 8.55738 | 35.3467 | 0.934521 | 9.77863 | 36.1036 | 0.166755 | False | False |
| `f24b_0054` | triple | 3 | long(롱) | 1.19358 | 8.55738 | 35.3467 | 0.934521 | 9.77863 | 36.1036 | 0.166755 | False | False |
| `f24b_0074` | pair | 2 | long(롱) | 1.14521 | 7.18033 | 28.0131 | 1.0842 | 7.20611 | 15.1349 | 0.187013 | False | False |
| `f24b_0046` | triple | 3 | long(롱) | 1.18403 | 8.38798 | 35.9058 | 0.938536 | 9.64122 | 35.4981 | 0.152275 | False | False |
| `f24b_0047` | triple | 3 | long(롱) | 1.18403 | 8.38798 | 35.9058 | 0.938536 | 9.64122 | 35.4981 | 0.152275 | False | False |
| `f24b_0093` | pair | 2 | long(롱) | 1.31729 | 8.3388 | 29.8761 | 1.07853 | 8.9084 | 21.1465 | 0.23269 | False | False |
| `f24b_0094` | pair | 2 | long(롱) | 1.31729 | 8.3388 | 29.8761 | 1.07853 | 8.9084 | 21.1465 | 0.23269 | False | False |
| `f24b_0018` | triple | 3 | long(롱) | 1.18494 | 7.55738 | 25.7004 | 0.955245 | 9.35115 | 30.6553 | 0.185052 | False | False |
| `f24b_0122` | pair | 2 | long(롱) | 1.24569 | 6.25683 | 30.6436 | 1.1515 | 7.0229 | 19.8846 | 0.0206646 | False | False |
| `f24b_0019` | triple | 3 | long(롱) | 1.20237 | 8.53552 | 32.3913 | 0.997784 | 9.48855 | 31.6983 | 0.189759 | False | False |

Next action(다음 행동): `frontier24C_density_bridge_repair_or_closeout_decision_v1`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
