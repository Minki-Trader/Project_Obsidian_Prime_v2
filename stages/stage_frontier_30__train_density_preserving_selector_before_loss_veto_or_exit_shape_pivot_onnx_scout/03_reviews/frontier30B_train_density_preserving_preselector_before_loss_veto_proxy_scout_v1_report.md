# Frontier30B Train Density Preserving Preselector Proxy Report(전선30B 학습 밀도 보존 사전 선택기 프록시 보고서)

Updated(갱신): 2026-06-14T12:18:37Z

Status(상태): `density_preserving_preselector_scout_clue_proxy_no_authority`

Judgment(판정): `scout_clue_requires_repair_or_closeout_no_authority`

Action(행동): F30A lock(전선30A 잠금)의 `top_160` train-only preselector(학습 전용 사전 선택기)를 F28/F29 reference surface(참조 표면)에 적용했습니다.

Effect(효과): selection(선택)은 train-only preselector score(학습 전용 사전 선택기 점수)만 사용했고, validation/OOS(검증/표본외)는 read-only(읽기 전용)로만 scout/seed/handoff(탐색/씨앗/인계)를 판독했습니다.

Source/preselected/candidate rows(원천/사전 선택/후보 행): `234` / `160` / `245`

Branch rows(분기 행): source no-veto(원천 무차단) `160`, density-preserving veto(밀도 보존 차단) `85`

Density/scout/seed/handoff rows(밀도/탐색/씨앗/인계 행): `188` / `5` / `0` / `0`

Scout split(탐색 분해): source branch(원천 분기) `5`, veto branch(차단 분기) `0`

Best forward read-only candidate(최상 전진 읽기 전용 후보): `f30b_0214` from source(원천) `f28b_0079` branch(분기) `source_no_veto_density_preservation_branch`

Best validation PF/density/DD(최상 검증 수익 팩터/밀도/손실폭): `1.310` / `5.962` / `17.839`

Best OOS PF/density/DD(최상 표본외 수익 팩터/밀도/손실폭): `1.151` / `6.687` / `13.416`

Runtime probe status(런타임 탐침 상태): `runtime_probe_out_of_scope_by_claim_scout_only_no_handoff`

## Top Read-Only Forward Rows(상위 읽기 전용 전진 행)

| candidate(후보) | branch(분기) | source(원천) | train score(학습 점수) | val PF | val density | val DD | OOS PF | OOS density | OOS DD | scout | seed | handoff |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `f30b_0214` | `source_no_veto_density_preservation_branch` | `f28b_0079` | 1.627 | 1.310 | 5.962 | 17.839 | 1.151 | 6.687 | 13.416 | True | False | False |
| `f30b_0213` | `source_no_veto_density_preservation_branch` | `f28b_0080` | 1.627 | 1.310 | 5.962 | 17.839 | 1.151 | 6.687 | 13.416 | True | False | False |
| `f30b_0003` | `source_no_veto_density_preservation_branch` | `f28b_0002` | 2.563 | 1.119 | 6.934 | 19.874 | 1.183 | 7.802 | 18.024 | True | False | False |
| `f30b_0174` | `source_no_veto_density_preservation_branch` | `f28b_0026` | 1.785 | 1.064 | 6.208 | 18.643 | 1.189 | 6.947 | 18.221 | False | False | False |
| `f30b_0173` | `source_no_veto_density_preservation_branch` | `f28b_0025` | 1.785 | 1.064 | 6.208 | 18.643 | 1.189 | 6.947 | 18.221 | False | False | False |
| `f30b_0185` | `source_no_veto_density_preservation_branch` | `f28b_0054` | 1.683 | 1.177 | 5.710 | 20.050 | 1.173 | 6.344 | 13.175 | True | False | False |
| `f30b_0175` | `source_no_veto_density_preservation_branch` | `f28b_0040` | 1.764 | 1.069 | 5.951 | 19.874 | 1.255 | 6.733 | 17.491 | False | False | False |
| `f30b_0140` | `top_density_preserving_loss_veto_variant_per_source` | `f28b_0197` | 2.279 | 1.073 | 4.781 | 11.821 | 1.207 | 5.084 | 12.748 | False | False | False |
| `f30b_0133` | `source_no_veto_density_preservation_branch` | `f28b_0076` | 2.297 | 1.232 | 8.388 | 25.079 | 0.947 | 10.115 | 28.884 | False | False | False |
| `f30b_0149` | `source_no_veto_density_preservation_branch` | `f28b_0212` | 2.258 | 1.231 | 9.694 | 31.871 | 1.088 | 11.275 | 26.523 | False | False | False |
| `f30b_0131` | `source_no_veto_density_preservation_branch` | `f28b_0069` | 2.321 | 1.249 | 7.514 | 25.079 | 0.980 | 8.351 | 21.844 | False | False | False |
| `f30b_0057` | `source_no_veto_density_preservation_branch` | `f28b_0089` | 2.501 | 1.052 | 6.169 | 12.679 | 1.016 | 6.977 | 19.489 | False | False | False |

Next action(다음 행동): `frontier30C_density_preserving_preselector_repair_or_closeout_decision_v1`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
