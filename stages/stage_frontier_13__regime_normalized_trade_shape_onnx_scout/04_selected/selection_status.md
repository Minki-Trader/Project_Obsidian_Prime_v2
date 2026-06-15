# Frontier13 Selection Status(프론티어13 선택 상태)

Updated(갱신): 2026-06-14T00:59:45Z

Status(상태): `closed_negative_memory_no_authority`

Judgment(판정): `negative_memory(부정 기억)`

Closeout run(마감 실행): `frontier13C_stage_closeout_regime_normalized_trade_shape_onnx_scout_v1`

Selection(선택): no selected baseline/completion candidate/promotion/runtime authority(선택 기준선/완성 후보/승격/런타임 권위 없음).

Negative memory(부정 기억): Regime-normalized trade-shape labels(국면 정규화 거래 형상 라벨)은 PF/density/DD(수익 팩터/빈도/손실폭)를 동시에 맞추지 못했습니다. Sparse LR plain(희소 로지스틱 평범) 표면은 OOS PF/DD(표본밖 수익 팩터/손실폭)가 좋아 보여도 OOS density(표본밖 빈도)가 너무 낮고, balanced variants(균형 변형)는 density(빈도)를 키웠지만 DD(손실폭)를 크게 악화했습니다.

Reference-only carry(참조 전용 이월): The vol-squeeze h12 LR plain surface(변동성 압축 h12 로지스틱 평범 표면)는 sparse seed surface(희소 씨앗 표면)로만 보관합니다.

Next action(다음 행동): `frontier14A_stage_open_new_hypothesis_design_v1`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) 없음.

<!-- runtime_probe_backfill_status -->

# Runtime Probe Backfill Status(런타임 탐침 소급 상태)

Updated(갱신): 2026-06-15T14:16:13Z

Status(상태): `runtime_probe_backfill_observation_no_authority`

Judgment(판정): `runtime_probe_observation(런타임 탐침 관찰)`

Action(행동): omitted MT5 runtime probe(누락된 MT5 런타임 탐침)를 소급 점검했습니다.

Effect(효과): 실행 가능 후보는 실제 tester KPI(테스터 지표)로 보강하고, 불가능한 후보는 blocker(차단 사유)를 남깁니다.

Reason(사유): `runtime_probe_observation(런타임 탐침 관찰)`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
