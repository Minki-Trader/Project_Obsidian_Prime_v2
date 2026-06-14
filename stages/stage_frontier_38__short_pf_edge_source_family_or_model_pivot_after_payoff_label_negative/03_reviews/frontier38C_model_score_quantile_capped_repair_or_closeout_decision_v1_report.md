# frontier38C_model_score_quantile_capped_repair_or_closeout_decision_v1 Report(frontier38C_model_score_quantile_capped_repair_or_closeout_decision_v1 보고)

Updated(갱신): 2026-06-14T17:55:16Z

Status(상태): `capped_model_score_quantile_repair_complete_no_runtime_authority`

Judgment(판정): `scout_surface_only_no_seed_runtime`

Action(행동): model score source(모델 점수 소스) candidate(후보)를 train-only(학습 전용)로 만들고 path-native first-hit replay(경로 네이티브 최초 터치 재생)로 평가했다.

Effect(효과): feature/source pivot(피처/소스 전환)이 forward PF-density-DD(전진 수익 팩터-밀도-손실폭)에 실제 단서를 주는지 확인한다.

Candidate/scout/near-seed/seed/runtime rows(후보/탐색/근접 씨앗/씨앗/런타임 행): `64` / `16` / `1` / `0` / `0`

Best read-only candidate(최상 읽기 전용 후보): `f38c_0058`

Best validation PF-density-DD(최상 검증 수익 팩터-밀도-손실폭): `1.121` / `8.475/day` / `7.791%`

Best OOS PF-density-DD(최상 표본밖 수익 팩터-밀도-손실폭): `1.138` / `10.733/day` / `8.290%`

Runtime probe status(런타임 탐침 상태): `runtime_probe_out_of_scope_by_claim_repair_no_seed_or_runtime_candidate`

| candidate(후보) | label(라벨) | model(모델) | side(방향) | val PF | val density | val DD | OOS PF | OOS density | OOS DD | scout | near seed | seed |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `f38c_0058` | `path_quality_mfe60_mae40` | `logreg_C0.03` | `high` | 1.121 | 8.475 | 7.791 | 1.138 | 10.733 | 8.290 | True | True | False |
| `f38c_0057` | `path_quality_mfe60_mae40` | `logreg_C0.1` | `high` | 1.110 | 8.689 | 7.392 | 1.094 | 10.847 | 8.852 | True | False | False |
| `f38c_0050` | `path_quality_mfe60_mae40` | `logreg_C0.03` | `high` | 1.089 | 8.475 | 7.681 | 1.165 | 10.733 | 8.430 | True | False | False |
| `f38c_0055` | `path_quality_mfe60_mae40` | `logreg_C0.3` | `high` | 1.089 | 8.639 | 7.135 | 1.109 | 11.053 | 9.488 | True | False | False |
| `f38c_0054` | `path_quality_mfe60_mae40` | `logreg_C0.1` | `high` | 1.080 | 8.689 | 7.809 | 1.128 | 10.847 | 8.995 | True | False | False |
| `f38c_0056` | `path_quality_mfe60_mae40` | `logreg_C0.3` | `high` | 1.115 | 8.639 | 7.128 | 1.074 | 11.053 | 9.359 | True | False | False |
| `f38c_0043` | `path_quality_mfe60_mae40` | `logreg_C0.03` | `high` | 1.057 | 7.246 | 8.039 | 1.206 | 9.344 | 6.813 | True | False | False |
| `f38c_0040` | `path_quality_mfe60_mae40` | `logreg_C0.3` | `high` | 1.089 | 7.311 | 8.896 | 1.188 | 9.557 | 7.323 | True | False | False |
| `f38c_0026` | `path_quality_mfe60_mae40` | `logreg_C0.03` | `high` | 1.058 | 7.246 | 8.120 | 1.160 | 9.344 | 6.491 | True | False | False |
| `f38c_0032` | `path_quality_mfe60_mae40` | `logreg_C0.1` | `high` | 1.070 | 7.257 | 8.465 | 1.228 | 9.420 | 7.036 | True | False | False |
| `f38c_0012` | `path_quality_mfe60_mae40` | `logreg_C0.1` | `high` | 1.074 | 7.257 | 8.794 | 1.172 | 9.420 | 6.709 | True | False | False |
| `f38c_0052` | `path_quality_mfe60_mae40` | `logreg_C0.3` | `high` | 1.079 | 7.311 | 10.113 | 1.141 | 9.557 | 8.855 | True | False | False |

Next action(다음 행동): `frontier38D_stage_closeout_model_score_source_pivot_v1`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)이다.
