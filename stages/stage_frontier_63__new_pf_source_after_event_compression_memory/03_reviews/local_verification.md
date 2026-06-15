# F63 Local Verification(F63 로컬 검증)

Action(행동): Grok stage-open review(그록 단계 개방 검토)의 local checks(로컬 확인)를 파일/장부/계약으로 확인했다.

Effect(효과): F63 구현이 true polarity inversion(진짜 극성 역전)을 시험하는지, F62 winner/baseline/authority(승자/기준선/권위)를 상속하지 않는지 고정한다.

- failure_mode_audit(실패 모드 감사): `F62 moved runtime density into the target neighborhood with feature_ready_diff=0, but PF failed on validation and OOS; this supports one bounded signal-polarity test before widening the PF-source search.`
- f62_proxy_check(F62 프록시 확인): validation/OOS(검증/표본외) proxy PF(프록시 수익 팩터)가 1.10/0.98이고 MT5 PF(메타트레이더5 수익 팩터)가 0.36/0.61이라, inversion(역전)은 runtime-only inference(런타임 단독 추론)가 아니다.
- inverse_materialization(역전 구현): Python signal(파이썬 신호)은 `-signal`로 반전되고 MT5 set(MT5 설정)은 `InpInvertSignal=True`를 기록한다.
- label_contract(라벨 계약): `balanced_margin_q45_opp_q55`, flat/tie rule(무거래/동점 규칙) recorded(기록됨)
- feature_contract(피처 계약): feature_count(피처 수) `58`, hash `fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2`
- proxy_grid_freeze(프록시 격자 동결): `{'thresholds': (0.2, 0.24, 0.28, 0.32, 0.36, 0.4, 0.42), 'min_margins': (0.0, 0.01, 0.02, 0.04), 'max_hold_options': (2, 4, 6), 'same_direction_cooldown_options': (0, 1, 2), 'close_on_flat_options': (True,), 'grid_rows': 252, 'selection_metric': 'density_band_penalty(train+validation+oos), then read-only validation/OOS PF-DD-density balance', 'one_candidate_freeze': 'exactly one selected_proxy_candidate is materialized for MT5 only after pre-MT5 Grok review', 'posthoc_expansion': 'no expansion after MT5 output; any proxy repair must be pre-MT5 and Grok-reviewed'}`
- runtime_parity_checklist(런타임 동등성 체크리스트): ONNX parity(온엑스 동등성) `{'passed': True, 'max_abs_diff': 1.4164066713950874e-07, 'mean_abs_diff': 3.0875702206434505e-08, 'rows': 1024, 'output_count': 2, 'input_name': 'float_input'}`, hash(해시) `56d8c2d04adc6f79684d5e567d5d78ae01b18c0000d2653efc7dce1ca7fae549`
- Tier plan(티어 계획): `{'tier_a': 'validation_is and oos MT5 runtime probe rows are Tier A separate', 'tier_b': 'missing_required at stage open because no Tier B runtime payload is materialized in this packet', 'tier_ab_combined': 'missing_required at stage open because no routed Tier A+B payload is materialized in this packet', 'boundary': 'Tier B absence cannot support completion or authority claims'}`
- stop criteria(중단 기준): runtime PF(런타임 수익 팩터)<1 or DD(손실폭)>=10 or density(밀도) outside 5~10/day(일 5~10회)이면 concrete preserved clue(구체 보존 단서)가 없는 한 negative memory(부정 기억)로 닫는다.
- stage scaffold(단계 뼈대): `00_spec/01_inputs/02_runs/03_reviews/04_selected` present(존재)
