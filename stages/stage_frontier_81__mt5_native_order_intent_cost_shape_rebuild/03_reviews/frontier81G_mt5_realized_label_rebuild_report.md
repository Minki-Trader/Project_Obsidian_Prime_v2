# F81G MT5-Realized Label Rebuild(F81G MT5 실현 손익 라벨 재구축)

Updated(갱신): 2026-06-18T04:33:29Z

- run id(실행 ID): `frontier81G_mt5_realized_label_rebuild_v1`
- parent run(부모 실행): `frontier81F_deal_reconciled_runtime_label_preflight_v1`
- status(상태): `f81g_realized_label_rebuild_low_density_seed_no_materialization_ready_no_authority`
- judgment(판정): `realized_label_filter_found_low_density_seed_repair_cap_consumed_rotation_decision_required_no_authority`
- next run(다음 실행): `frontier81H_capped_repair_closeout_or_f82_rotation_decision_v1`
- claim boundary(주장 경계): `realized_label_diagnostic_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`

## Action And Effect(행동과 효과)

Action(행동): F81F trade rows(거래 행)를 F81C runtime feature rows(런타임 피처 행)에 붙이고, MT5 realized win/loss label(MT5 실현 승/패 라벨)로 diagnostic filter models(진단 필터 모델)를 학습했다.

Effect(효과): 기존 F81C의 손실 거래를 사후 라벨로 분석해 repair value(수리 가치)를 확인했다. 단, validation-as-train/OOS-holdout(검증 훈련/표본외 보류) 진단이므로 runtime authority(런타임 권위)나 baseline(기준선)이 아니다.

## Label Dataset(라벨 데이터셋)

- matched trade rows(매칭 거래 행): `1365`
- unmatched trade rows(미매칭 거래 행): `2`
- validation label rows(검증 라벨 행): `695`
- OOS label rows(표본외 라벨 행): `670`
- validation/OOS win rate(검증/표본외 승률): `0.2403/0.2537`

## Best Diagnostic Candidate(최선 진단 후보)

- candidate(후보): `f81g_0006`
- model(모델): `histgbm_realized_label_diagnostic`
- exportability(내보내기 가능성): `not_exportable_current_path_or_not_attempted(현재 경로 내보내기 불가 또는 미시도)`
- OOS net/PF/DD/trades/day(표본외 순손익/수익 팩터/손실폭/일 거래): `8.9100/1.4313/0.6831/40/0.2051`
- validation net/PF/DD/trades/day(검증 순손익/수익 팩터/손실폭/일 거래): `168.0300/18.9519/0.2698/105/0.3860`

## Counts(개수)

- candidates(후보): `24`
- positive low-density seeds(양수 저밀도 씨앗): `4`
- materialization candidates(물질화 후보): `0`
- final-like references(최종 유사 참고): `0`

Interpretation(해석): F81G found a low-density seed(F81G는 저밀도 씨앗을 찾음) but no exportable density-sufficient candidate(내보내기 가능하고 밀도 충분한 후보 없음). Effect(효과): F81 repair cap(수리 상한)은 소모됐고 F81H(전선81H)는 closeout or rotation decision(마감 또는 회전 결정)을 해야 한다.

Forbidden claims(금지 주장): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
