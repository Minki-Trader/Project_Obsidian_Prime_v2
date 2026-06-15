# F63A Stage Open Report(F63A 단계 개방 보고)

Action(행동): F53~F62 failure memory(실패 기억)를 확인하고 F63을 inverse event-compressed side allocation(역전 이벤트 압축 방향 배분) 가설로 열었다.

Effect(효과): F62가 density(밀도)는 목표 근처로 옮겼지만 PF(수익 팩터)가 실패했으므로, 같은 handoff path(인계 경로)에서 signal polarity(신호 극성)만 뒤집어 PF source(수익 팩터 원천) 가능성을 좁게 확인한다.

- Grok stage-open(그록 단계 개방): `accepted`
- Grok local check demand(그록 로컬 검증 요구): completed(완료)
- failure audit read(실패 감사 판독): `F62 moved runtime density into the target neighborhood with feature_ready_diff=0, but PF failed on validation and OOS; this supports one bounded signal-polarity test before widening the PF-source search.`
- feature contract(피처 계약): `{'feature_count': 58, 'feature_order_hash': 'fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2', 'expected_feature_hash': 'fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2', 'feature_contract_match': True, 'raw_rows': 261345, 'missing_entry_positions': 0, 'missing_future_positions': 0}`
- proxy grid rows(프록시 격자 행): `252`
- inverse protocol(역전 절차): `{'definition': 'true polarity inversion is applied before entry-transition-only plus close-on-flat plus same-direction reentry cooldown; proxy trade events are counted after these gates, while raw signal counts remain separately recorded', 'invert_signal': True, 'density_band_penalty_formula': 'sum(max(5-density,0,density-10) for train, validation, oos trades_per_day)', 'retrain_gate': 'train a fresh F63 model because F62 artifacts are stage-local and F63 tests inverse signal polarity as a new PF-source hypothesis; no F62 winner/baseline/authority is inherited', 'bounded_repair_note': 'no post-MT5 repair is allowed; if proxy density is unusable, only a pre-MT5 Grok-reviewed bounded grid repair may occur', 'runtime_probe_freeze': 'one selected proxy candidate only after pre-MT5 Grok review; no threshold or cooldown expansion after seeing MT5 output', 'claim_boundary': 'runtime_probe_observation_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve'}`
- Tier B/combined(티어 B/합산): `missing_required` declared at stage open(단계 개방에서 선언)
