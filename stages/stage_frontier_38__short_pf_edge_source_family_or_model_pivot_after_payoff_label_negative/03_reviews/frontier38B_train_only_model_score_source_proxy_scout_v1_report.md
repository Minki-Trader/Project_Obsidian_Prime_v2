# frontier38B_train_only_model_score_source_proxy_scout_v1 Report(frontier38B_train_only_model_score_source_proxy_scout_v1 보고)

Updated(갱신): 2026-06-14T17:55:16Z

Status(상태): `model_score_source_proxy_scout_complete_no_runtime_authority`

Judgment(판정): `scout_surface_only_no_seed_runtime`

Action(행동): model score source(모델 점수 소스) candidate(후보)를 train-only(학습 전용)로 만들고 path-native first-hit replay(경로 네이티브 최초 터치 재생)로 평가했다.

Effect(효과): feature/source pivot(피처/소스 전환)이 forward PF-density-DD(전진 수익 팩터-밀도-손실폭)에 실제 단서를 주는지 확인한다.

Candidate/scout/near-seed/seed/runtime rows(후보/탐색/근접 씨앗/씨앗/런타임 행): `22` / `5` / `0` / `0` / `0`

Best read-only candidate(최상 읽기 전용 후보): `f38b_0013`

Best validation PF-density-DD(최상 검증 수익 팩터-밀도-손실폭): `1.040` / `8.525/day` / `9.973%`

Best OOS PF-density-DD(최상 표본밖 수익 팩터-밀도-손실폭): `1.050` / `10.015/day` / `7.786%`

Runtime probe status(런타임 탐침 상태): `runtime_probe_out_of_scope_by_claim_proxy_no_seed_or_runtime_candidate`

| candidate(후보) | label(라벨) | model(모델) | side(방향) | val PF | val density | val DD | OOS PF | OOS density | OOS DD | scout | near seed | seed |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `f38b_0013` | `path_quality_mfe60_mae40` | `extratrees_d5_leaf120` | `high` | 1.040 | 8.525 | 9.973 | 1.050 | 10.015 | 7.786 | True | False | False |
| `f38b_0010` | `path_quality_mfe60_mae40` | `logreg_C0.3` | `high` | 1.079 | 7.311 | 10.113 | 1.141 | 9.557 | 8.855 | True | False | False |
| `f38b_0006` | `path_quality_mfe60_mae40` | `logreg_C0.1` | `high` | 1.077 | 7.257 | 10.008 | 1.142 | 9.420 | 8.300 | True | False | False |
| `f38b_0017` | `path_quality_mfe60_mae40` | `logreg_C0.3` | `high` | 1.080 | 7.311 | 12.663 | 1.186 | 9.557 | 9.121 | True | False | False |
| `f38b_0016` | `path_quality_mfe60_mae40` | `logreg_C0.1` | `high` | 1.085 | 7.257 | 12.962 | 1.192 | 9.420 | 9.480 | True | False | False |
| `f38b_0020` | `horizon_positive` | `logreg_C0.3` | `high` | 0.981 | 12.421 | 14.697 | 1.068 | 14.763 | 15.024 | False | False | False |
| `f38b_0015` | `path_quality_mfe60_mae40` | `extratrees_d5_leaf120` | `high` | 0.999 | 8.525 | 12.824 | 1.079 | 10.015 | 8.960 | False | False | False |
| `f38b_0019` | `horizon_positive` | `logreg_C0.3` | `high` | 0.976 | 12.421 | 16.123 | 1.016 | 14.763 | 16.629 | False | False | False |
| `f38b_0021` | `horizon_positive` | `logreg_C0.1` | `high` | 0.967 | 12.596 | 16.971 | 1.068 | 14.802 | 15.947 | False | False | False |
| `f38b_0022` | `horizon_positive` | `logreg_C0.1` | `high` | 0.941 | 12.596 | 22.547 | 1.023 | 14.802 | 20.489 | False | False | False |
| `f38b_0008` | `horizon_positive` | `logreg_C0.3` | `high` | 0.964 | 7.470 | 15.308 | 1.055 | 9.313 | 11.532 | False | False | False |
| `f38b_0012` | `horizon_positive` | `logreg_C0.1` | `high` | 0.953 | 7.470 | 16.190 | 1.052 | 9.183 | 11.745 | False | False | False |

Next action(다음 행동): `frontier38C_model_score_quantile_capped_repair_or_closeout_decision_v1`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)이다.
