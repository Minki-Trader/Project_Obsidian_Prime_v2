# run328B cp318 Outcome Source Audit(328B cp318 결과 원천 감사)

- run_id(실행 ID): `run328B_deep_audit_cp318_outcome_source_and_live_feature_rebuild_options_v1`
- status(상태): `completed_cp318_outcome_source_audit_rebuild_required`
- judgment(판정): `blocked_repair_required_no_goal_achieve`
- decision(결정): `cp318_outcome_source_not_forward_authority_live_feature_rebuild_required`
- goal_achieve(목표 달성): `not_claimed`

## Core Finding(핵심 발견)

cp318A(318A 후보)는 Stage317 validation+OOS(검증+표본외) 실제 MT5 손익을 학습한 outcome distillation(결과 증류) 표면이다. 학습 행은 `24320`개, positive_rate(양수 비율)는 `0.3241`, in_sample_auc(표본내 AUC)는 `0.8606`다.

Effect(효과): 이 수치는 과거 조각을 잘 분류했다는 근거이지, 새 forward(전진) 구간에서 신호를 만들 권한은 아니다.

## Feature Authority(피처 권한)

- model_feature_count(모델 피처 수): `66`
- market_live_computable(시장 기반 재구축 가능): `45`
- upstream_research_dependency(상류 연구 의존): `19`
- surface_signal_dependency(표면/신호 의존): `2`

Effect(효과): raw market(원천 시장) 피처만 다시 계산해서 cp318A/cp322A를 forward(전진)에 옮길 수 없다. `source_code`와 `hyp_signal`은 upstream source surface(상류 원천 표면)를 요구한다.

## Estimated vs Actual Gap(추정 대 실제 차이)

| split(구간) | estimated net(추정 순수익) | actual MT5 net(실제 MT5 순수익) | scale ratio(규모 비율) | estimated PF(추정 수익 팩터) | actual PF(실제 수익 팩터) | actual DD%(실제 손실폭) |
|---|---:|---:|---:|---:|---:|---:|
| validation(검증) | 2749.30 | 392856.96 | 142.89 | 3.16 | 1.24 | 35.48 |
| OOS(표본외) | 1731.30 | 254199.30 | 146.83 | 2.48 | 1.23 | 17.54 |

Effect(효과): estimated replay(추정 재생)와 actual MT5(실제 MT5) 사이의 규모가 140배 이상 벌어져, 이 점수판을 forward calibration(전진 보정)으로 쓸 수 없다.

## Decision(결정)

cp322A(322A 후보)는 계속 frozen research artifact(고정 연구 산출물)로 보존한다. 그러나 cp318A outcome source(결과 원천)는 forward authority(전진 권한)가 아니며, cp322A forward generator(전진 생성기)는 아직 없다.

Next action(다음 행동): `run328C_design_live_feature_rebuild_control_or_stage329_standalone_onnx_packet`

`research_development_only_no_new_data_tuning_no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve`
