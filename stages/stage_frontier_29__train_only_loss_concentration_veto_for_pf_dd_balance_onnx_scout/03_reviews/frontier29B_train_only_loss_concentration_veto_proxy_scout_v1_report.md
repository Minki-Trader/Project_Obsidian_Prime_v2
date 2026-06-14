# Frontier29B Train-Only Loss Concentration Veto Proxy Report(전선29B 학습 전용 손실 집중 차단 프록시 보고서)

Updated(갱신): 2026-06-14T11:44:03Z

Status(상태): `loss_concentration_veto_no_scout_no_seed_no_handoff_proxy_no_authority`

Judgment(판정): `negative_memory_candidate_requires_closeout_or_capped_repair_no_authority`

Action(행동): F28 reference union surface(F28 참조 합집합 표면) `234`개에 train-only loss concentration veto(학습 전용 손실 집중 차단)를 적용했습니다.

Effect(효과): selection(선택)은 train loss capture(학습 손실 포착), removed fraction(제거 비율), train PF/DD(학습 수익 팩터/손실폭)만 사용했고 validation/OOS(검증/표본외)는 read-only(읽기 전용)로 기록했습니다.

Screened/selected rows(선별/선택 행): `36108` / `1438`

Density/scout/seed/handoff rows(밀도/탐색/씨앗/인계 행): `287` / `0` / `0` / `0`

Best forward read-only candidate(최상 전진 읽기 전용 후보): `f29b_0274` from `f28b_0197`

Best validation PF/density/DD(최상 검증 수익 팩터/밀도/손실폭): `1.073` / `4.781/day` / `11.821%`

Best OOS PF/density/DD(최상 표본외 수익 팩터/밀도/손실폭): `1.207` / `5.084/day` / `12.748%`

Runtime probe status(런타임 탐침 상태): `runtime_probe_ineligible_no_handoff_candidate_after_f29b_proxy`

## Top Read-Only Forward Rows(상위 읽기 전용 전진 행)

| veto(차단) | source(F28 원천) | train score(학습 점수) | removed frac(제거 비율) | loss capture(손실 포착) | val PF | val density | val DD | OOS PF | OOS density | OOS DD | scout | seed | handoff |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `f29b_0274` | `f28b_0197` | 1.124 | 0.223 | 0.347 | 1.073 | 4.781 | 11.821 | 1.207 | 5.084 | 12.748 | False | False | False |
| `f29b_1221` | `f28b_0061` | 0.772 | 0.234 | 0.377 | 1.135 | 4.169 | 8.528 | 1.186 | 4.229 | 9.362 | False | False | False |
| `f29b_1220` | `f28b_0060` | 0.772 | 0.234 | 0.377 | 1.135 | 4.169 | 8.528 | 1.186 | 4.229 | 9.362 | False | False | False |
| `f29b_1320` | `f28b_0221` | 0.733 | 0.234 | 0.343 | 1.456 | 6.055 | 20.151 | 0.928 | 8.359 | 21.378 | False | False | False |
| `f29b_1321` | `f28b_0222` | 0.733 | 0.234 | 0.343 | 1.456 | 6.055 | 20.151 | 0.928 | 8.359 | 21.378 | False | False | False |
| `f29b_0973` | `f28b_0191` | 0.863 | 0.231 | 0.348 | 1.425 | 6.809 | 19.995 | 0.908 | 9.718 | 27.429 | False | False | False |
| `f29b_0972` | `f28b_0190` | 0.863 | 0.231 | 0.348 | 1.425 | 6.809 | 19.995 | 0.908 | 9.718 | 27.429 | False | False | False |
| `f29b_0626` | `f28b_0197` | 0.972 | 0.309 | 0.423 | 1.086 | 4.333 | 9.632 | 1.216 | 4.573 | 12.978 | False | False | False |
| `f29b_1024` | `f28b_0225` | 0.843 | 0.233 | 0.339 | 1.474 | 5.820 | 17.295 | 0.858 | 7.328 | 27.025 | False | False | False |
| `f29b_1281` | `f28b_0210` | 0.751 | 0.253 | 0.332 | 1.185 | 3.760 | 9.102 | 1.196 | 4.435 | 10.437 | False | False | False |
| `f29b_1282` | `f28b_0211` | 0.751 | 0.253 | 0.332 | 1.185 | 3.760 | 9.102 | 1.196 | 4.435 | 10.437 | False | False | False |
| `f29b_1182` | `f28b_0120` | 0.784 | 0.239 | 0.335 | 1.089 | 4.257 | 12.379 | 1.142 | 5.221 | 10.525 | False | False | False |

Next action(다음 행동): `frontier29C_loss_concentration_veto_repair_or_closeout_decision_v1`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
