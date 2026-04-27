# run03D Stage 12 standalone batch-20 plan(단독 20개 묶음 계획)

## Scope(범위)

- stage(단계): `12_model_family_challenge__extratrees_training_effect`
- run(실행): `run03D_et_standalone_batch20_v1`
- exploration label(탐색 라벨): `stage12_Model__ExtraTreesStandaloneBatch20`
- intent(의도): Stage12 단독 ExtraTrees(엑스트라 트리) 계열 안에서 20개 가설을 한 번에 선점하고 Python structural scout(파이썬 구조 탐색)로 돌린다.
- exclusion(제외): Stage10/11(10/11단계) 모델, 임계값, 기준선, 승격 이력, 런타임 권위는 사용하지 않는다.
- effect(효과): 단독 실험 경계를 고정하면서 모델 구조, 피처 묶음, 임계값, 방향 규칙의 약점과 가능성을 같이 본다.

## Inputs(입력)

- dataset(데이터셋): `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime_v2\data\processed\model_inputs\label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58\model_input_dataset.parquet`
- dataset sha256(데이터셋 해시): `c30eb033f104f0b1682964b546593e8b18125760c37ce2b945f7ab0f447ae38f`
- feature order(피처 순서): `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime_v2\data\processed\model_inputs\label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58\model_input_feature_order.txt`
- feature order sha256(피처 순서 해시): `18c83876fe3c3a9f74d2a207cd236b1d746447af43108a5b554f2d54eea264cb`

## Hypotheses(가설)

| # | variant(변형) | idea(아이디어) | hypothesis(가설) |
|---:|---|---|---|
| 1 | `v01_base_leaf20_q90` | `IDEA-ST12-ET-BATCH20-V01` | 기본 잎 20 구조가 단독 Stage12 신호를 만든다. |
| 2 | `v02_dense_leaf10_q90` | `IDEA-ST12-ET-BATCH20-V02` | 잎 10의 촘촘한 구조가 약한 방향 신호를 더 잘 잡는다. |
| 3 | `v03_smooth_leaf40_q90` | `IDEA-ST12-ET-BATCH20-V03` | 잎 40의 부드러운 구조가 잡음을 줄인다. |
| 4 | `v04_log2_features_leaf20_q90` | `IDEA-ST12-ET-BATCH20-V04` | 분기마다 더 적은 피처를 보면 과적합이 줄어든다. |
| 5 | `v05_half_features_leaf20_q90` | `IDEA-ST12-ET-BATCH20-V05` | 절반 피처 샘플링이 방향 신호 다양성을 만든다. |
| 6 | `v06_entropy_leaf20_q90` | `IDEA-ST12-ET-BATCH20-V06` | 엔트로피 분할 기준이 비대칭 라벨 구조를 더 잘 본다. |
| 7 | `v07_balanced_subsample_leaf20_q90` | `IDEA-ST12-ET-BATCH20-V07` | 부트스트랩 균형 가중치가 클래스 불균형을 완화한다. |
| 8 | `v08_depth12_leaf20_q90` | `IDEA-ST12-ET-BATCH20-V08` | 깊이 12 제한이 표본외 흔들림을 줄인다. |
| 9 | `v09_depth8_leaf10_q90` | `IDEA-ST12-ET-BATCH20-V09` | 얕은 깊이와 촘촘한 잎 조합이 안정 신호를 만든다. |
| 10 | `v10_bootstrap70_leaf20_q90` | `IDEA-ST12-ET-BATCH20-V10` | 70% 부트스트랩 표본이 모델 분산을 낮춘다. |
| 11 | `v11_base_leaf20_q85` | `IDEA-ST12-ET-BATCH20-V11` | 더 낮은 임계값이 신호 밀도를 회복한다. |
| 12 | `v12_base_leaf20_q95` | `IDEA-ST12-ET-BATCH20-V12` | 더 높은 임계값이 신호 품질을 선별한다. |
| 13 | `v13_base_margin002_q90` | `IDEA-ST12-ET-BATCH20-V13` | 0.02 마진 요구가 애매한 예측을 걸러낸다. |
| 14 | `v14_base_margin005_q90` | `IDEA-ST12-ET-BATCH20-V14` | 0.05 마진 요구가 강한 예측만 남긴다. |
| 15 | `v15_base_short_only_q90` | `IDEA-ST12-ET-BATCH20-V15` | 숏 방향만 남기면 비대칭 수익 신호가 보인다. |
| 16 | `v16_base_long_only_q90` | `IDEA-ST12-ET-BATCH20-V16` | 롱 방향만 남기면 비대칭 수익 신호가 보인다. |
| 17 | `v17_top30_features_q90` | `IDEA-ST12-ET-BATCH20-V17` | 훈련 중요도 상위 30개 피처가 약한 피처 잡음을 줄인다. |
| 18 | `v18_core42_features_q90` | `IDEA-ST12-ET-BATCH20-V18` | 핵심 42개 피처만으로도 단독 Stage12 신호가 유지된다. |
| 19 | `v19_context16_features_q90` | `IDEA-ST12-ET-BATCH20-V19` | 보조 문맥 16개 피처만으로 독립 신호가 있는지 본다. |
| 20 | `v20_base_inverse_q90` | `IDEA-ST12-ET-BATCH20-V20` | 확률 방향을 반대로 쓰면 구조적 역방향성이 드러난다. |

## Judgment Boundary(판정 경계)

- 이 패키지는 Python structural scout(파이썬 구조 탐색)다.
- MT5(`MetaTrader 5`, 메타트레이더5) external verification(외부 검증)은 이번 주장 범위 밖(out_of_scope_by_claim, 주장 범위 밖)이다.
- effect(효과): 결과가 좋아 보여도 runtime authority(런타임 권위)나 operating promotion(운영 승격)으로 말하지 않는다.
