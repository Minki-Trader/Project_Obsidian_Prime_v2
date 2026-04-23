# Stage 06 Tier B-Safe Feature Schema Draft (Stage 06 Tier B 안전 피처 스키마 초안)

## Status (상태)
- this file is a `draft-only local input (드래프트 전용 로컬 입력)` for the first shared `Tier B reduced-context model (Tier B 공용 축약 문맥 모델)` discussion
- it does not update `workspace_state (워크스페이스 상태)`, `current_working_state (현재 작업 상태)`, or the active `selection_status (선정 상태)`
- it does not authorize any `simulated execution (가상 실행)`, `MT5 path (MT5 경로)`, or `operating promotion (운영 승격)` work
- the current `strict Tier A runtime rule (엄격 Tier A 런타임 규칙)` remains unchanged

## Purpose (목적)
- convert the current `draft-only anchor (드래프트 전용 앵커)` into one feature-level `schema draft (스키마 초안)` so later Stage 06 work does not reopen the same keep/drop debate from scratch
- define the narrowest first shared feature surface (공용 피처 표면) for a future `Tier B reduced-context model` without claiming a new official readiness boundary
- keep the first reduced-context pass inside the current `offline-only (오프라인 전용)` Stage 06 boundary

## Evidence Basis (근거 기반)
- `report_fpmarkets_v2_tier_b_robustness_0001.md` shows the dominant `Tier B` holdout missing pattern is `g4_leader_equity|g5_breadth_extension` with `row_share=0.905440`, while the smaller distinct pattern is `g3_macro_proxy` with `row_share=0.094504`
- `report_fpmarkets_v2_tier_b_calibration_fit_0001.md` shows `tier_b_exploration_temperature_fit` improves the `Tier B` holdout probabilistic read over the reused `strict_tier_a` temperature fit, so a separate reduced-context read is worth continuing
- `report_fpmarkets_v2_tier_b_weight_verdict_0001.md` keeps placeholder weights acceptable for `offline screening (오프라인 선별)` only, but still requires a real-weight rerun before any later simulated or `MT5` meaning
- the current anchor note under `note_fpmarkets_v2_tier_b_reduced_context_model_anchor_0001.md` already prefers one shared `Tier B` model first and uses subtype tags for reporting only

## Classification Rules (분류 규칙)
- `keep (유지)`: feature stays in the first shared `Tier B` schema when it depends only on `g1_contract_base (g1 계약 기반)` or `g2_session_semantics (g2 세션 의미)` and therefore remains defined on every `Tier B` row by construction
- `conditional (조건부)`: feature is excluded from the first shared active set, but may return later if a narrower reduced-context contract proves that optional macro context can be handled without reopening the current Stage 06 boundary
- `drop (제외)`: feature leaves the first shared `Tier B` schema because it depends directly on the dominant missing external context or on aggregate paths that inherit the same missing-path instability

## First Shared Active Set (첫 공용 활성 세트)
- active feature count for the first shared `Tier B reduced-context model`: `42`
- deferred feature count: `16`
- rule: the first shared model uses `keep` features only; `conditional` features remain out of the first training surface until a later explicit follow-up says otherwise

### `keep (유지)` — `g1_contract_base` feature family
- `log_return_1`
- `log_return_3`
- `hl_range`
- `close_open_ratio`
- `gap_percent`
- `close_prev_close_ratio`
- `return_zscore_20`
- `hl_zscore_50`
- `return_1_over_atr_14`
- `close_ema20_ratio`
- `close_ema50_ratio`
- `ema9_ema20_diff`
- `ema20_ema50_diff`
- `ema50_ema200_diff`
- `ema20_ema50_spread_zscore_50`
- `sma50_sma200_ratio`
- `rsi_14`
- `rsi_50`
- `rsi_14_slope_3`
- `rsi_14_minus_50`
- `stoch_kd_diff`
- `stochrsi_kd_diff`
- `ppo_hist_12_26_9`
- `roc_12`
- `trix_15`
- `atr_14`
- `atr_50`
- `atr_14_over_atr_50`
- `bollinger_width_20`
- `bb_position_20`
- `bb_squeeze`
- `historical_vol_20`
- `historical_vol_5_over_20`
- `adx_14`
- `di_spread_14`
- `supertrend_10_3`
- `vortex_indicator`

### `keep (유지)` — `g2_session_semantics` feature family
- `overnight_return`
- `is_us_cash_open`
- `minutes_from_cash_open`
- `is_first_30m_after_open`
- `is_last_30m_before_cash_close`

### `conditional (조건부)` — `g3_macro_proxy` feature family
- `vix_change_1`
- `vix_zscore_20`
- `us10yr_change_1`
- `us10yr_zscore_20`
- `usdx_change_1`
- `usdx_zscore_20`
- rationale (근거): the `g3_macro_proxy` missing family is real but minority-sized, so these features are not safe for the first shared active set; they remain candidates only for a later `macro-aware optional schema (매크로 인지 선택 스키마)` if that later pass stays separate from current official state

### `drop (제외)` — `g4_leader_equity` feature family
- `nvda_xnas_log_return_1`
- `aapl_xnas_log_return_1`
- `msft_xnas_log_return_1`
- `amzn_xnas_log_return_1`
- rationale (근거): the dominant current `Tier B` holdout pattern already concentrates in `g4_leader_equity|g5_breadth_extension`, so the first shared reduced-context model should not rely on leader-equity raw features that disappear on the dominant missing path

### `drop (제외)` — `g5_breadth_extension` aggregate family
- `mega8_equal_return_1`
- `top3_weighted_return_1`
- `mega8_pos_breadth_1`
- `mega8_dispersion_5`
- `us100_minus_mega8_equal_return_1`
- `us100_minus_top3_weighted_return_1`
- rationale (근거): these aggregates depend on the same external-symbol surface that dominates current `Tier B` missingness, and the top-3 weighted branch additionally stays tied to `placeholder weights (임시 가중치)` that remain `offline-only` by policy

## Subtype Tag Guidance (하위유형 태그 지침)
- `b_eq_dark (주식문맥 전면결손형)`: use the first shared `keep` set only
- `b_macro_late (매크로문맥 후반결손형)`: use the same first shared `keep` set only; do not activate `conditional` macro features in the first shared pass
- `b_residual_sparse (희소 예외형)`: treat as the same shared-schema family unless a later explicit evidence pass proves a narrower second family is worth opening
- these tags remain `reporting-only (보고 전용)` in this draft and do not become an official readiness boundary

## Explicit Non-Goals (명시적 비목표)
- do not describe this draft as a `materialized model artifact (물질화된 모델 산출물)` or as a completed Stage 06 decision
- do not treat the `conditional` list as permission to use missing-value fabrication, forward-fill, or relaxed contract semantics
- do not reopen `Stage 05 (05단계)` parity questions or imply that reduced-context exploration is contract-equivalent to the current `strict Tier A` line

## Next Use (다음 사용 방식)
- the next narrow implementation pass should materialize one shared `Tier B reduced-context model` using the `42` `keep` features only
- a later pass may compare that shared reduced-context model against one optional `macro-aware` variant only after the first shared-schema result exists as a separate artifact
