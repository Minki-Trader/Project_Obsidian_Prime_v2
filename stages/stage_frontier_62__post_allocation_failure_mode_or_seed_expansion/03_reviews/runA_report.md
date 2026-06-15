# F62A Stage Open Report(F62A 단계 개방 보고)

Action(행동): F53~F61 failure memory(실패 기억)를 확인하고 F62를 event-compressed side allocation(이벤트 압축 방향 배분) 가설로 열었다.

Effect(효과): F61의 raw signal(원신호) 기반 과잉 거래를 같은 신호 동등성 문제로 오해하지 않고, trade event(거래 이벤트) 압축이 PF/DD/density(PF/DD/밀도)를 같이 개선하는지 직접 관찰한다.

- Grok stage-open(그록 단계 개방): `accepted`
- Grok local check demand(그록 로컬 검증 요구): completed(완료)
- failure audit read(실패 감사 판독): `F53-F59 have completed MT5 rows and mostly signal_diff=0, so repeated failure is treated as alpha/economics failure more than handoff failure; F60 separately records intentional admission suppression; F61 records signal_diff=0 but MT5 density above the 5-10/day target.`
- feature contract(피처 계약): `{'feature_count': 58, 'feature_order_hash': 'fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2', 'expected_feature_hash': 'fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2', 'feature_contract_match': True, 'raw_rows': 261345, 'missing_entry_positions': 0, 'missing_future_positions': 0}`
- proxy grid rows(프록시 격자 행): `252`
- event protocol(이벤트 절차): `{'definition': 'entry-transition-only plus close-on-flat plus same-direction reentry cooldown; proxy trade events are counted after these gates, while raw signal counts remain separately recorded', 'density_band_penalty_formula': 'sum(max(5-density,0,density-10) for train, validation, oos trades_per_day)', 'retrain_gate': 'train a fresh F62 model because F61 artifacts are stage-local and F62 changes the selection target to event-compressed proxy metrics; no F61 winner/baseline/authority is inherited', 'bounded_repair_note': 'first proxy grid was 0.35/day and pre-MT5 Grok accepted exactly one threshold/margin/cooldown repair before MT5', 'runtime_probe_freeze': 'one selected proxy candidate only after the bounded proxy repair; no threshold or cooldown expansion after seeing MT5 output', 'claim_boundary': 'runtime_probe_observation_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve'}`
- Tier B/combined(티어 B/합산): `missing_required` declared at stage open(단계 개방에서 선언)
