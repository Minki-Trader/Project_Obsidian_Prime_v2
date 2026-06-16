# F69D Pre-MT5 Runtime Probe Review(F69D MT5 런타임 탐침 전 검토)

You are Grok(Grok, 그록), external second opinion(외부 2차 의견). Answer only from this bounded snapshot(제한 스냅샷). Do not inspect files(파일 확인 금지), run tools(도구 실행 금지), browse(브라우징 금지), or claim local verification(로컬 검증 금지).

## Current State(현재 상태)

- Stage(단계): `stage_frontier_69__axis_rotation_after_lifecycle_risk_only_negative_memory`.
- Boundary(경계): proxy/runtime probe observation only(프록시/런타임 탐침 관찰 전용). No completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
- F69B proxy sweep(프록시 탐색): 3240 candidates(후보), scout candidates(탐색 후보) 0, meaningful with control(통제 포함 의미 후보) 0.
- F69C density repair(밀도 수리): 216 candidates(후보), meaningful candidates(의미 후보) 0.
- Mandatory stage rule(필수 단계 규칙): each frontier stage(전선 단계)는 MT5 Runtime Probe(MT5 런타임 탐침)를 실행하거나 true bridge impossibility(진짜 연결 불가능)를 기록해야 한다.

## Key Proxy Evidence(핵심 프록시 근거)

1. Best high-PF proxy clue(최고 고PF 프록시 단서), but HGB export risk(HGB 내보내기 위험):
   - candidate(후보): `f69b_c059a1429316`
   - model(모델): `small_hist_gradient_v1`
   - validation(검증): net 771.326973, PF 2.653945, DD 0.818416%, trades/day 0.132731
   - OOS(표본외): net 655.919283, PF 3.561207, DD 0.761477%, trades/day 0.144162
   - local bridge memory(로컬 연결 기억): HistGradientBoosting(HGB, 히스토그램 그래디언트 부스팅) previously had skl2onnx converter failure(변환 실패) in F68C, so Codex does not want to make this the MT5 probe axis unless export proves otherwise.

2. Proposed exportable PF axis(제안 내보내기 가능 PF 축):
   - candidate(후보): `f69b_9dd9ed423f5f`
   - model(모델): `shallow_extra_trees_v1`
   - feature set(피처 묶음): `price_path_core_v1`
   - target(목표): `fh_h3_sl09_tp135_edge10`
   - event(이벤트): `event_session_edges`
   - side policy(방향 정책): `long_only`
   - validation(검증): net 255.095477, PF 2.393653, DD 0.530873%, trades/day 0.062678, trades 17
   - OOS(표본외): net 127.575040, PF 2.964008, DD 0.513565%, trades/day 0.036041, trades 7
   - purpose(목적): high-PF sparse clue(고PF 희박 단서)를 MT5로 물질화해 proxy/runtime gap(프록시/런타임 간극)을 관찰한다.

3. Proposed exportable density repair axis(제안 내보내기 가능 밀도 수리 축):
   - candidate(후보): `f69b_968cfd55b728`
   - model(모델): `shallow_extra_trees_v1`
   - feature set(피처 묶음): `morph_session_core_v1`
   - target(목표): `fh_h3_sl09_tp135_edge10`
   - event(이벤트): `event_bb_squeeze_release`
   - side policy(방향 정책): `long_only`
   - validation(검증): net 495.026329, PF 1.184987, DD 2.990793%, trades/day 1.021290, trades 277
   - OOS(표본외): net 319.831953, PF 1.159850, DD 4.345634%, trades/day 1.060622, trades 206
   - purpose(목적): denser but weak-PF clue(더 촘촘하지만 약한 PF 단서)를 MT5로 물질화해 density/economics gap(밀도/경제성 간극)을 관찰한다.

## Proposed Codex Direction(Codex 제안 방향)

Codex proposes to proceed to F69D ONNX export and MT5 Runtime Probe(F69D ONNX 내보내기와 MT5 런타임 탐침) for the two ExtraTrees axes above.

Bridge mapping(연결 매핑):

- ONNX export(ONNX 내보내기): existing `export_sklearn_to_onnx_zipmap_disabled` path(기존 경로).
- Probability parity(확률 동등성): sklearn vs onnxruntime(사이킷런 대 온엑스런타임) on train/validation/OOS samples.
- Signal parity(신호 동등성): reproduce F69 proxy signal(프록시 신호) with ONNX probabilities.
- Event mask(이벤트 마스크): materialize as RuntimeVetoTape(런타임 차단 테이프), with `entry_veto=1` outside event rows(이벤트 밖 봉).
- Side policy(방향 정책): `long_only` represented by `short_threshold=1.1`, `long_threshold=0.0`, `min_margin=edge_threshold`, `decision_mode=threshold_margin`.
- Runtime test(런타임 테스트): validation and OOS Strategy Tester(전략 테스터) attempts with RuntimeProbeEA(런타임 탐침 EA).

Success criteria(성공 기준):

- ONNX export succeeds and probability/signal parity is recorded.
- MT5 Runtime Probe runs or records exact blocker(정확한 차단 사유).
- Required KPI(필수 KPI): period, net profit, gross profit/loss, PF, DD, trade count, trades/day, signal count parity, feature readiness parity, proxy/runtime gap cause.

Failure/block criteria(실패/차단 기준):

- ExtraTrees ONNX export fails.
- RuntimeVetoTape cannot represent event mask exactly.
- RuntimeProbeEA compile or tester output is blocked.
- Feature timestamp parity or signal parity fails before MT5 execution.

## Question(질문)

Is this a disciplined next action(규율 있는 다음 행동) for F69, despite neither axis being a completion candidate(완성 후보 아님)? Identify accepted points(수용 지점), rejected/risky points(거절/위험 지점), needs_local_verification(로컬 검증 필요), and any tighter guardrail(더 좁은 보호 장치). Do not propose promotion/runtime authority/live readiness/baseline/Goal Achieve(승격/런타임 권위/실거래 준비/기준선/목표 달성 제안 금지).
