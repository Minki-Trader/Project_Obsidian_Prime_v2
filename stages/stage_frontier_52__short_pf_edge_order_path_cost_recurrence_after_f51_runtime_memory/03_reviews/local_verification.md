# Local Verification(로컬 검증)

- git_scope(깃 범위): F52 stage-local adapter(단계 전용 어댑터), stage artifacts(단계 산출물), ledgers(장부), Grok receipts(그록 영수증).
- EA boundary(EA 경계): `foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5` unchanged(변경 없음); `.set` parameter(설정 파라미터) only.
- reference_boundary(참조 경계): F51 candidate(전선51 후보)는 reference-only(참조 전용), no inherited winner/baseline(승자/기준선 상속 없음).
- runtime_policy(런타임 정책): `{"InpAtrMaxStopPoints": 180.0, "InpAtrMaxTakeProfitPoints": 260.0, "InpAtrMinStopPoints": 40.0, "InpAtrMinTakeProfitPoints": 60.0, "InpAtrPeriod": 14, "InpAtrSltpEnabled": true, "InpAtrStopMultiplier": 0.8, "InpAtrTakeProfitMultiplier": 1.2, "InpCloseOnFlatSignal": true, "InpEntryTransitionOnly": true, "InpEntryTransitionRearmMinConfidenceDelta": 0.02, "InpMaxHoldBars": 6, "InpReentryCooldownBars": 3, "InpSameDirectionReentryCooldownBars": 6}`
- signal_diff_boundary(신호 차이 경계): negative signal_diff(음수 신호 차이)는 entry policy suppression(진입 정책 억제)로 해석하며, feature_ready_diff(피처 준비 차이) `0`이 핵심 로컬 확인값이다.
- judgment(판정): `preserved_clue_negative_memory_dd_compressed_but_pf_failed(보존 단서+부정 기억, 손실폭은 압축됐지만 수익 팩터 실패)`
