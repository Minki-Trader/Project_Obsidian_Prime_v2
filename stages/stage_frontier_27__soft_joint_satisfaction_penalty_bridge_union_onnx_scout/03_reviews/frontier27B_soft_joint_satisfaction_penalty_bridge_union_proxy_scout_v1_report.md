# Frontier27B Soft Joint Satisfaction Penalty Proxy Report(전선27B 연성 합동 충족 페널티 프록시 보고서)

Updated(갱신): 2026-06-14T10:18:14Z

Status(상태): `soft_penalty_scout_clue_proxy_no_authority`

Judgment(판정): `scout_clue_requires_repair_or_closeout_no_authority`

Action(행동): F24 full micro pool(F24 전체 미세 풀) `80`개를 train-only soft penalty(학습 전용 연성 페널티)로 점수화하고, 같은 방향 pair/triple OR-union(2/3중 OR 합집합)을 순위화했습니다.

Effect(효과): F26 hard gate relaxation(F26 경성 게이트 완화)을 주 경로로 쓰지 않고, union surface(합집합 표면)가 연성 순위에서 살아나는지 확인했습니다.

Soft micro/construction/union rows(연성 미세/구성/합집합 행): `80` / `60` / `234`

Broad envelope/density/scout/seed/handoff rows(넓은 외피/빈도/탐색/씨앗/인계 행): `205` / `189` / `19` / `0` / `0`

Top10 overlap F24/F25/F26(상위10 중복 F24/F25/F26): `0` / `0` / `0`

Best soft union(최상 연성 합집합): `f27b_0181`

Best validation PF/density/DD(최상 검증 수익 팩터/빈도/손실폭): `1.310` / `5.962/day` / `17.839%`

Best OOS PF/density/DD(최상 OOS 수익 팩터/빈도/손실폭): `1.151` / `6.687/day` / `13.416%`

Runtime probe status(런타임 탐침 상태): `out_of_scope_by_claim_no_handoff_candidate(인계 후보 없어 주장 범위 밖)`

## Top Soft Union Rows(상위 연성 합집합 행)

| union(합집합) | micro ids(미세 ID) | soft score(연성 점수) | train PF | train density | train DD | val PF | val density | val DD | OOS PF | OOS density | OOS DD | scout | seed |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `f27b_0181` | `f24p_0045|f24p_0027` | 14.687 | 1.299 | 5.742 | 18.187 | 1.310 | 5.962 | 17.839 | 1.151 | 6.687 | 13.416 | True | False |
| `f27b_0182` | `f24p_0045|f24p_0028` | 14.687 | 1.299 | 5.742 | 18.187 | 1.310 | 5.962 | 17.839 | 1.151 | 6.687 | 13.416 | True | False |
| `f27b_0187` | `f24p_0056|f24p_0027` | 14.635 | 1.292 | 5.646 | 19.500 | 1.381 | 5.650 | 14.495 | 1.152 | 5.656 | 12.439 | True | False |
| `f27b_0188` | `f24p_0056|f24p_0028` | 14.635 | 1.292 | 5.646 | 19.500 | 1.381 | 5.650 | 14.495 | 1.152 | 5.656 | 12.439 | True | False |
| `f27b_0132` | `f24p_0062|f24p_0027` | 16.158 | 1.292 | 5.065 | 16.524 | 1.289 | 5.404 | 19.786 | 1.216 | 5.550 | 13.045 | True | False |
| `f27b_0133` | `f24p_0062|f24p_0028` | 16.158 | 1.292 | 5.065 | 16.524 | 1.289 | 5.404 | 19.786 | 1.216 | 5.550 | 13.045 | True | False |
| `f27b_0082` | `f24p_0056|f24p_0064|f24p_0067` | 18.866 | 1.365 | 7.246 | 16.916 | 1.119 | 6.934 | 19.874 | 1.183 | 7.802 | 18.024 | True | False |
| `f27b_0111` | `f24p_0056|f24p_0067` | 17.639 | 1.299 | 5.693 | 16.151 | 1.177 | 5.710 | 20.050 | 1.173 | 6.344 | 13.175 | True | False |
| `f27b_0134` | `f24p_0027|f24p_0064` | 16.137 | 1.396 | 4.780 | 17.419 | 1.350 | 5.131 | 15.098 | 1.181 | 5.458 | 17.390 | True | False |
| `f27b_0135` | `f24p_0028|f24p_0064` | 16.137 | 1.396 | 4.780 | 17.419 | 1.350 | 5.131 | 15.098 | 1.181 | 5.458 | 17.390 | True | False |
| `f27b_0164` | `f24p_0027|f24p_0041` | 15.128 | 1.335 | 5.215 | 17.051 | 1.277 | 5.432 | 18.476 | 1.113 | 6.168 | 13.113 | True | False |
| `f27b_0165` | `f24p_0028|f24p_0041` | 15.128 | 1.335 | 5.215 | 17.051 | 1.277 | 5.432 | 18.476 | 1.113 | 6.168 | 13.113 | True | False |

Next action(다음 행동): `frontier27C_soft_joint_satisfaction_penalty_repair_or_closeout_decision_v1`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
