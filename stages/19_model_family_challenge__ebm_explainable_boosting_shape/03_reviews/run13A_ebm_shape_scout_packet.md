# RUN13A EBM Shape Scout Packet(실행13A EBM 모양 탐색 묶음)

## Judgment(판정)

- run(실행): `run13A_ebm_main_effect_shape_scout_v1`
- status(상태): `reviewed_structural_scout_completed`
- judgment(판정): `inconclusive_ebm_shape_structural_scout_completed`
- selected variant(선택 변형): `v01_main_effects_broad_bins`
- boundary(경계): `ebm_shape_structural_scout_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`
- external verification(외부 검증): `out_of_scope_by_claim_python_structural_scout(주장 범위 밖, 파이썬 구조 탐색)`

효과(effect, 효과): EBM(설명가능 부스팅 머신) shape(모양)는 확인했지만 MT5(`MetaTrader 5`, 메타트레이더5) runtime_probe(런타임 탐침)나 운영 의미(operating meaning, 운영 의미)는 주장하지 않는다.

## Evidence(근거)

- variants(변형 수): `3`
- Tier A rows(Tier A 행): `46650`
- Tier B fallback rows(Tier B 대체 행): `12398`
- validation signal coverage(검증 신호 커버리지): `0.10006095083299472`
- OOS signal coverage(표본외 신호 커버리지): `0.0981012658227848`
- validation directional hit(검증 방향 적중): `0.4152284263959391`
- OOS directional hit(표본외 방향 적중): `0.4018817204301075`

## Top Shape Terms(상위 모양 항)

- `hl_range`: gain_share(기여 비중) `0.0591`, degree(차수) `1`
- `historical_vol_20`: gain_share(기여 비중) `0.0545`, degree(차수) `1`
- `ema20_ema50_diff`: gain_share(기여 비중) `0.0540`, degree(차수) `1`
- `overnight_return`: gain_share(기여 비중) `0.0482`, degree(차수) `1`
- `sma50_sma200_ratio`: gain_share(기여 비중) `0.0469`, degree(차수) `1`

## Claim Boundary(주장 경계)

allowed(허용): EBM(설명가능 부스팅 머신) Python structural scout(파이썬 구조 탐색), Tier A/B paired records(Tier A/B 쌍 기록), top term clue(상위 항 단서).

forbidden(금지): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion_candidate(승격 후보), operating_promotion(운영 승격), runtime_authority(런타임 권위).
