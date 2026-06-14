# Frontier21 Lifecycle Lock Spec(전선21 생명주기 잠금 명세)

Entry lock(진입 잠금): `vix_zscore_20 <= q30 & close_ema50_ratio >= q70`, `long(롱)`

Rules(규칙):

- F20 entry surface is fixed(F20 진입 표면 고정)
- No new rule-atlas rerank(새 규칙 지도 재순위 없음)
- No side flip(방향 전환 없음)
- No boosted backbone(부스팅 백본 없음)
- No probability threshold search(확률 임계값 탐색 없음)
- No new feature engineering(새 피처 설계 없음)
- Lifecycle grid is capped and pre-registered(생명주기 격자는 상한 있고 사전 등록됨)
- Validation/OOS are read-only diagnostics(검증/표본외는 읽기 전용 진단)
- Pre-expensive Grok review before any MT5/runtime work(비싼 MT5/런타임 전 그록 검토)

| profile_id(프로필 ID) | role(역할) | max_hold(최대 보유) | stop ATR(손절 ATR) | take ATR(익절 ATR) | cooldown(쿨다운) | early exit(초기 청산) |
|---|---:|---:|---:|---:|---:|---|
| `f21b_sim_baseline_hold12_no_stop` | parity_baseline_row(동등성 비교 행) | 12 | 0.0 | 0.0 | 0 | False |
| `f21b_hold4_atr0p8_tp1p6_cd2_early` | dd_containment_profile(손실폭 억제 프로필) | 4 | 0.8 | 1.6 | 2 | True |
| `f21b_hold6_atr1p0_tp2p0_cd3` | balanced_profile(균형 프로필) | 6 | 1.0 | 2.0 | 3 | False |
| `f21b_hold8_atr1p2_tp2p4_cd4_early` | wide_profile_with_early_exit(넓은 프로필+초기 청산) | 8 | 1.2 | 2.4 | 4 | True |
| `f21b_hold10_atr1p5_tp3p0_cd6` | loose_profile(느슨한 프로필) | 10 | 1.5 | 3.0 | 6 | False |
