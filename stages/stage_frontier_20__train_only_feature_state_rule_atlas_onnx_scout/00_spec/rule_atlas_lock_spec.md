# Frontier20 Rule Atlas Lock Spec(전선20 규칙 지도 잠금 명세)

Action(행동): F20B proxy scout(F20B 프록시 탐색) 전에 rule atlas(규칙 지도)의 허용 범위를 고정합니다.

Effect(효과): validation/OOS(검증/표본외) 숫자를 본 뒤 규칙을 바꾸는 leakage(누수)와 F15/F19 반복을 막습니다.

## Locks(잠금)

- `existing_58_contract_features_only`: Use only existing 58 contract features(기존 58개 계약 피처만 사용). No new feature engineering(새 피처 설계 없음).
- `fixed_train_quantile_grid`: Fit q10/q20/q30/q70/q80/q90 only on train split(학습 분할에서만 고정 분위수 적합).
- `max_conjunction_depth_two`: Rule atlas(규칙 지도)는 single or pair conjunction(단일 또는 쌍 결합)까지만 허용합니다.
- `train_only_side_selection`: Long/short side(롱/숏 방향)는 train split(학습 분할) 성과로만 고릅니다.
- `validation_oos_read_only`: Validation/OOS(검증/표본외)는 평가 전용이며 rule selection(규칙 선택)에 쓰지 않습니다.
- `no_probability_threshold_or_backbone`: No probability threshold(확률 임계값 없음), no boosted backbone(부스팅 백본 없음).
- `no_overlay_repair_stack`: No lifecycle/quota/firewall/veto repair(생명주기/할당량/방화벽/배제 수리 없음).
- `tier_paired_record_slots`: Stage run ledger(단계 실행 장부)는 Tier A/Tier B/Tier A+B 기록 슬롯을 반드시 엽니다.
- `runtime_probe_obligation`: If a handoff candidate(인계 후보)가 있으면 MT5 runtime probe(MT5 런타임 탐침)를 시도하고, 없으면 exact blocker(정확한 차단 사유)를 기록합니다.
- `claim_boundary_lock`: Only scout clue/seed surface/runtime probe observation/preserved clue/negative memory/invalid setup/blocked(탐색 단서/씨앗 표면/런타임 탐침 관찰/보존 단서/부정 기억/무효 설정/차단) language is allowed.

## Required Record Views(필수 기록 보기)

- Tier A separate(티어 A 분리)
- Tier B separate(티어 B 분리)
- Tier A+B combined(티어 A+B 합산)
