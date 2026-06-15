# F62 Local Verification(F62 로컬 검증)

Action(행동): Grok stage-open review(그록 단계 개방 검토)의 `needs_local_verification(로컬 검증 필요)` 항목 1~8을 파일/장부/계약으로 확인했다.

Effect(효과): F62 구현이 event-compressed representation(이벤트 압축 표현)이라는 새 가설을 시험하는지, F52 lifecycle-only(생명주기 전용) 수리 반복이나 런타임 권위 주장으로 drift(드리프트)하지 않는지 고정한다.

- failure_mode_audit(실패 모드 감사): `F53-F59 have completed MT5 rows and mostly signal_diff=0, so repeated failure is treated as alpha/economics failure more than handoff failure; F60 separately records intentional admission suppression; F61 records signal_diff=0 but MT5 density above the 5-10/day target.`
- label_contract(라벨 계약): `balanced_margin_q45_opp_q55`, flat/tie rule(무거래/동점 규칙) recorded(기록됨)
- feature_contract(피처 계약): feature_count(피처 수) `58`, hash `fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2`
- proxy_grid_freeze(프록시 격자 동결): `{'thresholds': (0.2, 0.24, 0.28, 0.32, 0.36, 0.4, 0.42), 'min_margins': (0.0, 0.01, 0.02, 0.04), 'max_hold_options': (2, 4, 6), 'same_direction_cooldown_options': (0, 1, 2), 'close_on_flat_options': (True,), 'grid_rows': 252, 'selection_metric': 'density_band_penalty(train+validation+oos), then read-only validation/OOS PF-DD-density balance', 'one_candidate_freeze': 'exactly one selected_proxy_candidate is materialized for MT5 after the pre-MT5 bounded density repair', 'posthoc_expansion': 'one bounded grid repair accepted by pre-MT5 Grok because first proxy density was too sparse; no expansion after MT5 output'}`
- runtime_parity_checklist(런타임 동등성 체크리스트): ONNX parity(온엑스 동등성) `{'passed': True, 'max_abs_diff': 1.4164066713950874e-07, 'mean_abs_diff': 3.087570220733801e-08, 'rows': 1024, 'output_count': 2, 'input_name': 'float_input'}`, hash(해시) `1df987c1198c6846e194e1c952f3e7b81f2fb8638acb15919c3191bccd3532bd`
- Tier plan(티어 계획): `{'tier_a': 'validation_is and oos MT5 runtime probe rows are Tier A separate', 'tier_b': 'missing_required at stage open because no Tier B runtime payload is materialized in this packet', 'tier_ab_combined': 'missing_required at stage open because no routed Tier A+B payload is materialized in this packet', 'boundary': 'Tier B absence cannot support completion or authority claims'}`
- stop criteria(중단 기준): runtime PF<1 or DD>=10 or density outside 5~10/day closes as negative memory unless a concrete preserved clue appears.
- stage scaffold(단계 뼈대): `00_spec/01_inputs/02_runs/03_reviews/04_selected` present(존재)
