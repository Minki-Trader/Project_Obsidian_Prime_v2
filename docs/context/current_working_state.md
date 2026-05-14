# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `stage56_run50AU_composite_qda_route_density_repair_v1`
- current run(현재 실행): `run50AU_stage56_composite_qda_route_density_repair_v1`
- active stage(활성 단계): `56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection`
- selected_research_baseline(선택 연구 기준선): `none`
- status(상태): active_in_progress(활성 진행 중)
- terminal_condition(종료 조건): useful BaselineAdapter(유용한 기준선 어댑터) hard condition(강한 완료 조건) satisfied(충족)

Stage56(56단계)은 unfinished optimization campaign(미완 최적화 캠페인)으로 계속 열려 있다. Effect(효과): run50AU(실행50AU)는 QDA composite route density repair(QDA 합성 라우트 밀도 수정)를 실제 MT5 validation/OOS(검증/표본외)로 확인하는 중간 근거다.

## Latest Evidence(최신 근거)

- latest_batch(최신 묶음): `run50AU_stage56_composite_qda_route_density_repair_v1`
- best_variant(현재 최선 변형): `qda85_s800_flat_trans_r060_h8`
- selected_research_baseline(선택 연구 기준선): `none`
- validation/OOS trades/day(검증/표본외 일 거래): `5.262295` / `3.389744`
- validation/OOS PF(검증/표본외 수익 팩터): `1.11` / `1.12`
- validation/OOS net(검증/표본외 순손익): `277.91` / `213.64`

## Current Bottleneck(현재 병목)

- run50AU judgment(실행50AU 판정): best quality(최선 품질) `qda85_s800_flat_trans_r060_h8`은 validation/OOS(검증/표본외) trades/day(일 거래 수) `5.262295` / `3.389744`, PF(수익 팩터) `1.11` / `1.12`, net(순손익) `277.91` / `213.64`이지만 OOS density(표본외 밀도), cost-stressed expectancy(비용 압박 기대값) `-0.211412` / `-0.176793`, same-move/cooldown survival(동일 이동/쿨다운 생존)을 통과하지 못했다.
- closest_density_variant(밀도 최접근 변형): `qda85_s800_flat_trans_r030_h6`은 validation/OOS(검증/표본외) trades/day(일 거래 수) `6.726776` / `4.405128`, PF(수익 팩터) `1.06` / `1.07`, net(순손익) `165.43` / `142.01`이다. Effect(효과): lifecycle compression(생명주기 압축)은 OOS density(표본외 밀도)를 조금 올렸지만 품질과 비용 압박을 망가뜨렸다.
- attribution_read(기여도 판독): `qda85_s800_flat_trans_r060_h8` OOS(표본외)는 range/adx_lt20(횡보/ADX 20 미만) `233.75`와 early session(초반 세션) `199.72`가 강하지만 mid session(중간 세션) `-50.26`과 adx_20_25(ADX 20-25) `-40.03`이 약하다. `qda85_s800_flat_trans_r030_h6` OOS(표본외)는 early session(초반 세션) `332.74`와 adx_20_25(ADX 20-25) `100.58`이 강하지만 late/mid session(후반/중간 세션) `-124.88` / `-65.85`, adx_gt25(ADX 25 초과) `-94.45`가 약하다.
- next_hypothesis_branch(다음 가설 분기): `run50AV_new_source_density_survival_branch`

Forbidden claims(금지 주장): live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(운영 기준선), reviewed_closed(검토 종료).
