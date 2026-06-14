# Frontier20 Experiment Design(전선20 실험 설계)

- primary_family(주 작업군): `experiment_design(실험 설계)`
- primary_skill(주 스킬): `obsidian-experiment-design`
- support_skills(보조 스킬): `obsidian-reentry-read, obsidian-exploration-mandate, obsidian-model-validation, obsidian-grok-collaboration, obsidian-result-judgment`
- required_gates(필수 게이트): `external_review_packet`, `train_only_leakage_guard`, `rule_atlas_lock_gate`, `tier_paired_record_gate`, `runtime_probe_obligation_gate`, `required_gate_coverage_audit`, `final_claim_guard`

hypothesis(가설): Sparse closed-bar feature-state conjunctions(희소 확정봉 피처 상태 결합)를 train split(학습 분할)에서만 선택하면 validation/OOS(검증/표본외)에서 5~10 trades/day(일 5~10회), PF improvement(수익 팩터 개선), lower DD(낮은 손실폭), smoother curve(더 매끄러운 곡선)에 가까워지는 seed surface(씨앗 표면)를 찾을 수 있다.

decision_use(결정 용도): Open F20A stage(전선20A 단계)를 계획/잠금 상태로 열고 F20B proxy scout(전선20B 프록시 탐색) 범위를 고정합니다. Completion/baseline/promotion/runtime authority(완성/기준선/승격/런타임 권위)는 만들지 않습니다.

comparison_baseline(비교 기준): Recent negative memories(최근 부정 기억) F05/F15/F16/F18/F19 and reference-only Stage12~364 archive(참조 전용 12~364단계 보관소).

control_variables(통제 변수): US100 M5 FPMarkets v2 dataset(US100 5분봉 FPMarkets v2 데이터셋), label_v1 fwd12 split(라벨 v1 12봉 전방 분할), 58 feature order hash(58 피처 순서 해시), closed-bar only inference boundary(확정봉 전용 추론 경계), no validation/OOS rule selection(검증/표본외 규칙 선택 없음)

changed_variables(변경 변수): feature-state rule definitions(피처 상태 규칙 정의), train-only rule side(학습 전용 규칙 방향), rule atlas ranking on train only(학습 전용 규칙 지도 순위)

sample_scope(표본 범위): Tier A separate(티어 A 분리) is materialized from the 58-feature model input. Tier B separate(티어 B 분리) and Tier A+B combined(티어 A+B 합산) are required record views and may be missing_required/out_of_scope_by_claim(필수 누락/주장 범위 밖) if no Tier B source exists.

success_criteria(성공 기준): scout clue(탐색 단서): validation/OOS PF(검증/표본외 수익 팩터)가 1.5+ toward target(목표 방향)으로 움직이고 density(빈도)가 5~10/day 근처입니다., seed surface(씨앗 표면): PF/density/DD/smoothness(수익 팩터/빈도/손실폭/매끄러움) 중 하나 이상이 악화 없이 의미 있게 좋아집니다., runtime probe observation(런타임 탐침 관찰): handoff candidate(인계 후보)가 생기면 MT5 runtime probe(MT5 런타임 탐침)를 시도합니다.

failure_criteria(실패 기준): Train-only rules(학습 전용 규칙)이 validation/OOS(검증/표본외)에서 PF 1.1~1.3, high DD(높은 손실폭)에 머물러 F19와 같은 no-forward-clue(전진 단서 없음)로 끝납니다., Useful-looking surface(좋아 보이는 표면)가 validation/OOS guided filtering(검증/표본외 유도 필터링)을 요구합니다., No strict/seed/preserved/handoff row(엄격/씨앗/보존/인계 행)가 남지 않습니다.

invalid_conditions(무효 조건): New feature engineering(새 피처 설계), Probability threshold search(확률 임계값 탐색), Validation/OOS selection(검증/표본외 선택), Boosted backbone rerun(부스팅 백본 재실행), Lifecycle/quota/firewall/veto repair inside F20B(F20B 내부 생명주기/할당량/방화벽/배제 수리)

stop_conditions(중단 조건): strict/seed/handoff surface(엄격/씨앗/인계 표면)가 생기면 Grok pre-expensive review(비싼 실행 전 그록 검토)로 멈춥니다., locked atlas(고정 지도)에서 0/0/0/0이면 repair_or_closeout decision(수리/마감 결정)으로 넘깁니다., MT5 claim(MT5 주장)이 필요하면 runtime probe(런타임 탐침) 또는 exact blocker(정확한 차단 사유)를 남깁니다.

evidence_plan(근거 계획): stage_open_summary.json(단계 개방 요약), rule_atlas_lock.json(규칙 지도 잠금), grok_stage_open_receipt.md(그록 단계 개방 영수증), F20B metrics by split(F20B 분할별 지표), Tier A/Tier B/Tier A+B ledger rows(티어 A/B/합산 장부 행), runtime probe report or blocker(런타임 탐침 보고 또는 차단 사유)
