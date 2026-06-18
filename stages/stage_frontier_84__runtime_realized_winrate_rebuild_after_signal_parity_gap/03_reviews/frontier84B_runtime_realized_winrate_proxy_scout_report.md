# F84B Runtime-Realized Winrate Proxy Scout Report(F84B 런타임 실현 승률 프록시 탐색 보고서)

Updated(갱신): 2026-06-18T09:41:32Z

Run(실행): `frontier84B_runtime_realized_winrate_proxy_scout_v1`

## Result(결과)

Action(행동): runtime-realized winrate labels(런타임 실현 승률 라벨), stop-touch/fill-path labels(손절·익절 터치/체결 경로 라벨), risk/session splits(위험/세션 분할)을 bounded representative-axis scout(상한 있는 대표 축 탐색)로 실행했다.

Effect(효과): F83의 signal parity after win-rate erosion(신호 동등성 뒤 승률 침식)을 같은 threshold repair(임계값 수리)로 반복하지 않고, label semantics(라벨 의미)를 runtime outcome(런타임 결과)에 맞춰 다시 세웠다.

## KPI Summary(KPI 요약)

- candidate rows(후보 행): `1280`
- scout clue(탐색 단서): `579`
- materialization candidate(물질화 후보): `269`
- meaningful signal(의미 신호): `127`
- final-like reference(최종 유사 참고): `0`
- winrate preserved vs F83E OOS(F83E 표본외 대비 승률 보존): `1189`
- 5-10 trades/day proxy density(일 5~10회 프록시 밀도): `128`
- best candidate(최선 후보): `f84b_01151` `reversal_balance` `long` val(검증) `344.4161/1.3957/2.8653/8.3653/2267`; OOS(표본외) `291.8095/1.4199/2.4484/9.5103/1845`

## Top Candidates(상위 후보)

| candidate(후보) | side(방향) | surface(표면) | model(모델) | feature(피처) | regime/risk/cooldown(장세/위험/쿨다운) | val net/PF/DD/tpd/trades/win%(검증) | OOS net/PF/DD/tpd/trades/win%(표본외) | scout/material/meaningful/final-like(탐색/물질/의미/최종유사) |
|---|---:|---|---|---|---|---:|---:|---:|
| `f84b_01151` | `long` | `reversal_balance` | `histgbm_density_shallow` | `compact_exportable_30` | `high_vol/intent_release/0` | `344.4161/1.3957/2.8653/8.3653/2267/47.1548` | `291.8095/1.4199/2.4484/9.5103/1845/45.6911` | `1/1/1/0` |
| `f84b_00319` | `long` | `stop_touch_asymmetry` | `histgbm_density_shallow` | `density_core` | `high_vol/intent_release/0` | `332.0128/1.3657/4.4736/8.6347/2340/46.6239` | `298.3607/1.4367/2.1752/9.4072/1825/45.9178` | `1/1/1/0` |
| `f84b_00287` | `long` | `stop_touch_asymmetry` | `extra_trees_d7_l120` | `density_core` | `high_vol/intent_release/0` | `341.6369/1.3779/4.5254/8.6347/2340/46.8376` | `288.0970/1.4246/2.9310/9.3041/1805/45.7064` | `1/1/1/0` |
| `f84b_00383` | `long` | `stop_touch_asymmetry` | `histgbm_density_shallow` | `compact_exportable_30` | `high_vol/intent_release/0` | `294.5116/1.3476/3.8642/8.0111/2171/46.2920` | `254.9329/1.3926/2.6755/8.8041/1708/45.2576` | `1/1/1/0` |
| `f84b_01131` | `long` | `reversal_balance` | `histgbm_density_shallow` | `compact_exportable_30` | `trend/intent_release/0` | `267.3248/1.3517/2.7243/7.1956/1950/46.3590` | `247.5656/1.3346/2.2261/9.8557/1912/44.0900` | `1/1/1/0` |
| `f84b_01071` | `long` | `reversal_balance` | `histgbm_density_shallow` | `density_core` | `high_vol/intent_release/0` | `340.5803/1.3545/4.4878/9.1033/2467/46.4126` | `288.0101/1.4018/2.0581/9.7577/1893/45.3249` | `1/1/1/0` |
| `f84b_01087` | `long` | `reversal_balance` | `histgbm_density_shallow` | `density_core` | `high_vol/intent_release/0` | `313.9302/1.3699/3.7302/8.0849/2191/46.6910` | `246.1285/1.3727/2.0332/8.9072/1728/44.7917` | `1/1/1/0` |
| `f84b_01115` | `long` | `reversal_balance` | `extra_trees_d7_l120` | `compact_exportable_30` | `trend/intent_release/0` | `244.5379/1.3169/3.1268/7.2177/1956/45.7055` | `244.2239/1.3334/2.9452/9.7629/1894/44.0338` | `1/1/1/0` |
| `f84b_00367` | `long` | `stop_touch_asymmetry` | `histgbm_density_shallow` | `compact_exportable_30` | `high_vol/intent_release/0` | `314.3471/1.3304/4.5765/8.9410/2423/45.9761` | `282.0781/1.3887/2.7926/9.8299/1907/45.1494` | `1/1/1/0` |
| `f84b_01147` | `long` | `reversal_balance` | `histgbm_density_shallow` | `compact_exportable_30` | `trend/intent_release/0` | `250.8000/1.3995/3.8190/6.0406/1637/47.2205` | `226.3356/1.3598/1.7494/8.4485/1639/44.5394` | `1/1/1/0` |
| `f84b_00351` | `long` | `stop_touch_asymmetry` | `extra_trees_d7_l120` | `compact_exportable_30` | `high_vol/intent_release/0` | `266.7979/1.3040/5.1248/8.1734/2215/45.4628` | `268.7699/1.4209/4.7637/8.7423/1696/45.6368` | `1/1/1/0` |
| `f84b_00303` | `long` | `stop_touch_asymmetry` | `histgbm_density_shallow` | `density_core` | `high_vol/intent_release/0` | `361.2825/1.3613/5.3217/9.4982/2574/46.5423` | `297.0833/1.4036/2.5761/10.0258/1945/45.3470` | `1/1/1/0` |
| `f84b_01055` | `long` | `reversal_balance` | `extra_trees_d7_l120` | `density_core` | `high_vol/intent_release/0` | `357.9275/1.3821/3.8331/8.9594/2428/46.9110` | `290.3015/1.3882/4.3876/10.1289/1965/45.0891` | `1/1/1/0` |
| `f84b_00335` | `long` | `stop_touch_asymmetry` | `extra_trees_d7_l120` | `compact_exportable_30` | `high_vol/intent_release/0` | `309.0467/1.3144/6.2549/9.1882/2490/45.6627` | `298.7892/1.4161/4.0221/9.8144/1904/45.5882` | `1/1/1/0` |
| `f84b_01119` | `long` | `reversal_balance` | `extra_trees_d7_l120` | `compact_exportable_30` | `high_vol/intent_release/0` | `336.4731/1.3451/3.2069/9.2103/2496/46.2340` | `317.2337/1.4218/1.7458/10.3041/1999/45.6728` | `1/1/1/0` |
| `f84b_00315` | `long` | `stop_touch_asymmetry` | `histgbm_density_shallow` | `density_core` | `trend/intent_release/0` | `212.1190/1.3073/6.0908/6.4354/1744/45.5275` | `213.3769/1.3244/2.3419/8.7371/1695/43.8348` | `1/1/1/0` |
| `f84b_01083` | `long` | `reversal_balance` | `histgbm_density_shallow` | `density_core` | `trend/intent_release/0` | `235.0362/1.3671/4.8302/6.0923/1651/46.6384` | `202.9979/1.3228/2.1530/8.3505/1620/43.8272` | `1/1/1/0` |
| `f84b_01051` | `long` | `reversal_balance` | `extra_trees_d7_l120` | `density_core` | `trend/intent_release/0` | `267.9466/1.3687/5.4124/6.9188/1875/46.6667` | `221.0591/1.3190/3.2432/9.1856/1782/43.7710` | `1/1/1/0` |
| `f84b_01067` | `long` | `reversal_balance` | `histgbm_density_shallow` | `density_core` | `trend/intent_release/0` | `251.4138/1.3307/5.5701/7.1439/1936/45.9711` | `227.2085/1.3199/2.2106/9.4175/1827/43.7876` | `1/1/1/0` |
| `f84b_01135` | `long` | `reversal_balance` | `histgbm_density_shallow` | `compact_exportable_30` | `high_vol/intent_release/0` | `363.7132/1.3722/2.7766/9.3173/2525/46.7327` | `316.8718/1.4113/2.4484/10.5155/2040/45.5392` | `1/1/1/0` |

## Interpretation(해석)

This is proxy evidence only(프록시 근거 전용). Meaningful candidate(의미 후보)나 materialization candidate(물질화 후보)가 있으면 next action(다음 행동)은 MT5 Strategy Tester materialization(MT5 전략 테스터 물질화)다.

Signal count(신호 수)는 diagnostic only(진단 전용)이며 runtime economics(런타임 경제성)를 대체하지 않는다.

## Tier Record(티어 기록)

Tier A separate(티어 A 분리)는 proxy scout(프록시 탐색)로 기록했다. Tier B separate(티어 B 분리)는 `missing_required(필수 누락)`, Tier A+B combined(티어 A+B 합산)는 `out_of_scope_by_claim(주장 범위 밖)`로 기록했다.

Boundary(경계): `proxy_scout_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`.
