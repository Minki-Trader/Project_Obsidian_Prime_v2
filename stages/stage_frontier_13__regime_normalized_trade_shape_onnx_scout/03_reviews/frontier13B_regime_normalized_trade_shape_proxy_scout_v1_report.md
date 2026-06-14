# Frontier13B Regime-Normalized Trade Shape Proxy Scout(프론티어13B 레짐 정규화 거래 형상 프록시 탐색)

Updated(갱신): 2026-06-14T00:52:20Z

Status(상태): `regime_normalized_no_strict_clue_no_authority`

Judgment(판정): `negative_memory_candidate(부정 기억 후보)`

Action(행동): train-only regime bucket scales(학습 전용 레짐 버킷 척도)로 3개 label variants(라벨 변형)를 만들고 fixed argmax ONNX models(고정 최대확률 온엑스 모델)을 학습했습니다.

Effect(효과): F12(프론티어12)의 sparse low-DD surface(희소한 낮은 손실폭 표면)가 regime scale(레짐 척도)로 density/PF/DD(빈도/수익 팩터/손실폭)를 동시에 개선하는지 측정했습니다.

## Result Summary(결과 요약)

- candidate rows(후보 행): `9`
- strict scout clue rows(엄격 탐색 단서 행): `0`
- preserved clue rows(보존 단서 행): `0`
- best candidate(최고 후보): `f13b_vol_squeeze_h12_t1p00_cap0p62_ecap0p36_rec0p12__lr_plain`
- validation PF/density/DD(검증 수익 팩터/빈도/손실폭): `1.03969` / `2.25683` / `54.3762%`
- OOS PF/density/DD(표본밖 수익 팩터/빈도/손실폭): `2.02765` / `0.412214` / `5.5735%`
- worst subperiod DD(최악 하위기간 손실폭): `54.3762%`

## Artifacts(산출물)

- candidate summary(후보 요약): `stages/stage_frontier_13__regime_normalized_trade_shape_onnx_scout/02_runs/frontier13B_regime_normalized_trade_shape_proxy_scout_v1/candidate_summary.csv`
- bucket scales(버킷 척도): `stages/stage_frontier_13__regime_normalized_trade_shape_onnx_scout/02_runs/frontier13B_regime_normalized_trade_shape_proxy_scout_v1/bucket_scales.csv`
- ONNX parity(온엑스 동등성): `stages/stage_frontier_13__regime_normalized_trade_shape_onnx_scout/02_runs/frontier13B_regime_normalized_trade_shape_proxy_scout_v1/onnx_parity.csv`
- run manifest(실행 목록): `stages/stage_frontier_13__regime_normalized_trade_shape_onnx_scout/02_runs/frontier13B_regime_normalized_trade_shape_proxy_scout_v1/run_manifest.json`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
