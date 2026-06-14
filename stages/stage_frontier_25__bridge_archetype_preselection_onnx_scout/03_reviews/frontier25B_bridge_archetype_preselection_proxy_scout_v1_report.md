# Frontier25B Bridge Archetype Preselection Proxy Report(전선25B 연결 원형 사전 선택 프록시 보고서)

Updated(갱신): 2026-06-14T08:45:40Z

Status(상태): `bridge_archetype_scout_clue_proxy_no_authority`

Judgment(판정): `scout_clue_requires_repair_or_closeout_no_authority`

Action(행동): F24 micro pockets(F24 미세 구간)를 재구성하고 train-only DD-headroom-first archetype score(학습 전용 손실폭 여유 우선 원형 점수)로 pair/triple OR-union(쌍/삼중 OR 합집합)을 선택했습니다.

Effect(효과): post-hoc repair(사후 수리) 없이 구조 선택만으로 PF/density/DD/smoothness(수익 팩터/빈도/손실폭/매끄러움)가 forward(전진)에서 좋아지는지 확인했습니다.

Micro/eligible/archetype/metric rows(미세/적격/원형/지표 행): `80` / `16` / `26` / `78`

Density/scout/seed/handoff rows(빈도/탐색/씨앗/인계 행): `24` / `17` / `0` / `0`

F24B top10 overlap(F24B 상위10 중복): `0`

Best archetype(최상 원형): `f25b_0022`

Best validation PF/density/DD(최상 검증 수익 팩터/빈도/손실폭): `1.23272` / `5.60656/day` / `20.1588%`

Best OOS PF/density/DD(최상 표본외 수익 팩터/빈도/손실폭): `1.24574` / `6.16031/day` / `14.2862%`

Runtime probe status(런타임 탐침 상태): `out_of_scope_by_claim_no_handoff_candidate(인계 후보 없어 주장 범위 밖)`

## Top Archetype Rows(상위 원형 행)

| archetype(원형) | micro ids(미세 ID) | train DD | train DD headroom | val PF | val density | val DD | OOS PF | OOS density | OOS DD | scout | seed |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `f25b_0022` | `f24p_0027|f24p_0067` | 17.532 | 0.468015 | 1.23272 | 5.60656 | 20.1588 | 1.24574 | 6.16031 | 14.2862 | True | False |
| `f25b_0023` | `f24p_0028|f24p_0067` | 17.532 | 0.468015 | 1.23272 | 5.60656 | 20.1588 | 1.24574 | 6.16031 | 14.2862 | True | False |
| `f25b_0001` | `f24p_0027|f24p_0062` | 16.5244 | 1.47561 | 1.28922 | 5.40437 | 19.7857 | 1.21646 | 5.54962 | 13.0449 | True | False |
| `f25b_0002` | `f24p_0028|f24p_0062` | 16.5244 | 1.47561 | 1.28922 | 5.40437 | 19.7857 | 1.21646 | 5.54962 | 13.0449 | True | False |
| `f25b_0007` | `f24p_0056|f24p_0067` | 16.1508 | 1.84918 | 1.17696 | 5.71038 | 20.0505 | 1.17335 | 6.34351 | 13.1747 | True | False |
| `f25b_0012` | `f24p_0062|f24p_0067` | 15.0384 | 2.96164 | 1.10908 | 5.12022 | 20.0714 | 1.22555 | 5.67939 | 13.8272 | True | False |
| `f25b_0003` | `f24p_0027|f24p_0041` | 17.0507 | 0.94926 | 1.27676 | 5.43169 | 18.4756 | 1.11275 | 6.16794 | 13.1126 | True | False |
| `f25b_0004` | `f24p_0028|f24p_0041` | 17.0507 | 0.94926 | 1.27676 | 5.43169 | 18.4756 | 1.11275 | 6.16794 | 13.1126 | True | False |
| `f25b_0014` | `f24p_0045|f24p_0073` | 15.5756 | 2.42437 | 1.1175 | 5.21858 | 18.8221 | 1.16605 | 5.94656 | 12.8111 | True | False |
| `f25b_0015` | `f24p_0045|f24p_0074` | 15.5756 | 2.42437 | 1.1175 | 5.21858 | 18.8221 | 1.16605 | 5.94656 | 12.8111 | True | False |
| `f25b_0011` | `f24p_0045|f24p_0067` | 16.09 | 1.90996 | 1.10269 | 5.43716 | 20.7562 | 1.17983 | 6.09924 | 13.4652 | True | False |
| `f25b_0005` | `f24p_0027|f24p_0075` | 17.0576 | 0.942372 | 1.28437 | 5.36612 | 18.4756 | 1.10892 | 6.0458 | 13.4065 | True | False |

Next action(다음 행동): `frontier25C_bridge_archetype_repair_or_closeout_decision_v1`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
