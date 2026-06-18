# F82B Density-First Proxy Scout Report(F82B 밀도 우선 프록시 탐색 보고서)

Updated(갱신): 2026-06-18T05:39:10Z

Run(실행): `frontier82B_density_first_runtime_economic_mechanism_proxy_scout_v1`

## Result(결과)

Action(행동): density-first runtime economic mechanism(밀도 우선 런타임 경제 메커니즘) proxy scout(프록시 탐색)를 실행했다.

Effect(효과): F81G low-density seed(F81G 저밀도 씨앗)보다 높은 trade density(거래 밀도)를 우선 보상하면서 net/PF/DD(순수익/수익 팩터/손실폭)를 같이 본 후보 표면을 만들었다.

## KPI Summary(KPI 요약)

- candidate rows(후보 행): `10800`
- scout clue(탐색 단서): `1919`
- materialization candidate(물질화 후보): `717`
- meaningful signal(의미 신호): `160`
- final-like reference(최종 유사 참고): `0`
- density beats F81G seed(밀도 F81G 씨앗 초과): `7136`
- best candidate(최선 후보): `f82b_07295` `side_session_release` `long` val(검증) `234.9537/1.2529/3.9148/7.2989/1978`; OOS(표본외) `190.9750/1.3121/2.4484/6.9072/1340`

## Top Candidates(상위 후보)

| candidate(후보) | side(방향) | surface(표면) | model(모델) | feature(피처) | regime/risk/cooldown(장세/위험/쿨다운) | val net/PF/DD/tpd/trades(검증) | OOS net/PF/DD/tpd/trades(표본외) | scout/material/meaningful/final-like(탐색/물질/의미/최종유사) |
|---|---:|---|---|---|---|---:|---:|---:|
| `f82b_07295` | `long` | `side_session_release` | `extra_trees_d7_l120` | `trend_density` | `all/intent_release/0` | `234.9537/1.2529/3.9148/7.2989/1978` | `190.9750/1.3121/2.4484/6.9072/1340` | `1/1/1/0` |
| `f82b_07319` | `long` | `side_session_release` | `extra_trees_d7_l120` | `trend_density` | `trend/intent_release/0` | `191.2243/1.2695/4.0638/5.6089/1520` | `152.7589/1.2891/2.2994/5.9175/1148` | `1/1/1/0` |
| `f82b_09485` | `long` | `smooth_trade_supply` | `histgbm_density_shallow` | `trend_density` | `all/intent_release/0` | `371.0042/1.2664/7.9067/9.0775/2460` | `307.7817/1.3047/4.1303/9.4175/1827` | `1/1/1/0` |
| `f82b_09425` | `long` | `smooth_trade_supply` | `extra_trees_d7_l120` | `trend_density` | `all/intent_release/0` | `372.9123/1.2993/5.6641/8.2103/2225` | `360.6589/1.3938/3.4384/8.7887/1705` | `1/1/1/0` |
| `f82b_09443` | `long` | `smooth_trade_supply` | `extra_trees_d7_l120` | `trend_density` | `high_vol/intent_release/0` | `361.2816/1.2951/5.4654/8.0554/2183` | `350.9540/1.3922/3.7826/8.5825/1665` | `1/1/1/0` |
| `f82b_09455` | `long` | `smooth_trade_supply` | `extra_trees_d7_l120` | `trend_density` | `all/intent_release/0` | `362.9458/1.3533/5.9196/6.8930/1868` | `316.2153/1.4156/2.4200/7.3505/1426` | `1/1/1/0` |
| `f82b_09473` | `long` | `smooth_trade_supply` | `extra_trees_d7_l120` | `trend_density` | `high_vol/intent_release/0` | `351.3506/1.3477/5.7209/6.7675/1834` | `304.9847/1.4085/2.7642/7.1959/1396` | `1/1/1/0` |
| `f82b_09605` | `long` | `smooth_trade_supply` | `extra_trees_d7_l120` | `compact_exportable_30` | `all/intent_release/0` | `371.1914/1.2704/6.3880/8.9594/2428` | `355.4144/1.3376/3.5306/9.9278/1926` | `1/1/1/0` |
| `f82b_09623` | `long` | `smooth_trade_supply` | `extra_trees_d7_l120` | `compact_exportable_30` | `high_vol/intent_release/0` | `360.5542/1.2671/6.2035/8.8007/2385` | `340.2450/1.3313/3.8748/9.6649/1875` | `1/1/1/0` |
| `f82b_09635` | `long` | `smooth_trade_supply` | `extra_trees_d7_l120` | `compact_exportable_30` | `all/intent_release/0` | `320.5976/1.2858/5.6002/7.3579/1994` | `301.5321/1.3334/4.1552/8.5206/1653` | `1/1/1/0` |
| `f82b_09395` | `long` | `smooth_trade_supply` | `logistic_l2_balanced` | `trend_density` | `all/intent_release/0` | `329.1359/1.3116/4.6209/6.9889/1894` | `238.3779/1.3156/3.7826/7.0670/1371` | `1/1/1/0` |
| `f82b_09413` | `long` | `smooth_trade_supply` | `logistic_l2_balanced` | `trend_density` | `high_vol/intent_release/0` | `324.5310/1.3128/4.4222/6.8672/1861` | `227.8570/1.3136/3.3994/6.7938/1318` | `1/1/1/0` |
| `f82b_09653` | `long` | `smooth_trade_supply` | `extra_trees_d7_l120` | `compact_exportable_30` | `high_vol/intent_release/0` | `313.0120/1.2831/5.4796/7.2472/1964` | `281.5902/1.3163/4.4994/8.3402/1618` | `1/1/1/0` |
| `f82b_09449` | `long` | `smooth_trade_supply` | `extra_trees_d7_l120` | `trend_density` | `trend/intent_release/0` | `314.8377/1.3273/5.8699/6.3985/1734` | `283.5702/1.3609/3.5945/7.4639/1448` | `1/1/1/0` |
| `f82b_09275` | `long` | `smooth_trade_supply` | `extra_trees_d7_l120` | `density_core` | `all/intent_release/0` | `372.7207/1.3103/6.6177/7.9446/2153` | `314.7676/1.3505/4.3432/8.5052/1650` | `1/1/1/0` |
| `f82b_09293` | `long` | `smooth_trade_supply` | `extra_trees_d7_l120` | `density_core` | `high_vol/intent_release/0` | `364.8158/1.3072/6.6177/7.8450/2126` | `297.0612/1.3344/4.6874/8.3711/1624` | `1/1/1/0` |
| `f82b_09479` | `long` | `smooth_trade_supply` | `extra_trees_d7_l120` | `trend_density` | `trend/intent_release/0` | `306.0288/1.3783/6.2602/5.4723/1483` | `256.9218/1.3930/2.5229/6.2732/1217` | `1/1/1/0` |
| `f82b_09269` | `long` | `smooth_trade_supply` | `extra_trees_d7_l120` | `density_core` | `trend/intent_release/0` | `285.9813/1.2700/6.5752/6.9114/1873` | `293.1091/1.3244/3.5590/8.4845/1646` | `1/1/1/0` |
| `f82b_09659` | `long` | `smooth_trade_supply` | `extra_trees_d7_l120` | `compact_exportable_30` | `trend/intent_release/0` | `241.2220/1.2803/5.8060/5.6347/1527` | `236.7031/1.3170/3.6832/7.0000/1358` | `1/1/1/0` |
| `f82b_09629` | `long` | `smooth_trade_supply` | `extra_trees_d7_l120` | `compact_exportable_30` | `trend/intent_release/0` | `274.3577/1.2615/6.3951/6.8266/1850` | `265.9418/1.3026/3.7471/8.1959/1590` | `1/1/1/0` |

## Interpretation(해석)

This is proxy evidence only(프록시 근거 전용). Meaningful candidate(의미 후보)나 materialization candidate(물질화 후보)가 있으면 next action(다음 행동)은 MT5 Strategy Tester materialization(MT5 전략 테스터 물질화)다.

Signal count(신호 수)는 diagnostic only(진단 전용)이며 runtime economics(런타임 경제성)를 대체하지 않는다.

## Tier Record(티어 기록)

Tier A separate(티어 A 분리)는 proxy scout(프록시 탐색)로 기록했다. Tier B separate(티어 B 분리)는 `missing_required(필수 누락)`, Tier A+B combined(티어 A+B 합산)는 `out_of_scope_by_claim(주장 범위 밖)`로 기록했다.

Boundary(경계): `proxy_scout_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve_no_parity_only_economics`.
