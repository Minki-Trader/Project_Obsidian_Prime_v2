Bounded Grok review(제한 그록 검토)를 위해 협업 스킬과 Frontier21·유사 선행 작업 근거를 먼저 확인합니다.
## Bounded Grok Review — Frontier22 Stage Open

**Review size:** small review(소규모 검토)
**Decision:** **adjust** (조정 후 진행; pure accept 아님, reject 아님)

---

### Plain read (쉬운 요약)

Frontier21(전선21)은 “청산·빈도·손실폭 수리”만으로는 PF edge(수익 팩터 우위)가 안 나온다고 닫혔습니다. 그래서 Frontier22에서 **진입 품질(entry quality, 진입 품질)** 쪽을 새로 보자는 방향은 맞습니다.

다만 지금 문장 그대로 열면, Frontier20(전선20)이 이미 한 **58피처 전체 규칙 지도(rule atlas, 규칙 지도)** 와 너무 가깝습니다. F20 최상 씨앗이 `vix_zscore_20 + close_ema50_ratio`(변동성 + 추세/위치)였고, F22가 말하는 volatility/trend/chop/session/breadth는 그 안에 이미 들어 있습니다.

그래서 **가설 방향은 유효**하지만, **열기 전에 잠금(lock, 잠금) 6~8개**를 넣어야 F20 재탐색이 아닌 새 전선이 됩니다.

---

### Local verification (로컬 검증)

| Check | Result |
|---|---|
| F21 closed as stated | **pass** — `workspace_state.yaml`, F21D closeout report 일치 |
| F20 rule-atlas negative memory | **pass** — depth-2 train-only atlas, 533 candidates, best `f20b_pair_0359` |
| F22 stage folder exists | **pass (none yet)** — 아직 미개방, 설계 단계 적합 |
| Forbidden claims in proposal | **pass** — scout-only, no promotion/runtime authority |

---

### Answer to the narrow question

**Is this a valid new Frontier22 hypothesis?**
**Yes, directionally** — F21이 “lifecycle alone(생명주기 단독)”을 부정했으니, PF source(수익 팩터 원천)를 entry-state(진입 상태)로 옮기는 건 논리적으로 맞습니다. Stage308의 `session/breadth/volatility/trend` 축과도 맞습니다.

**Is it too close to F20 feature-state rule atlas / threshold search?**
**Yes, unless adjusted** — 같은 `feature_set_v2` 58피처, 같은 train quantile thresholds(학습 분위 임계값), 같은 `future_log_return_12` 고정 프록시를 쓰면 **F20의 부분 재실행**이 됩니다. 특히 F20이 이미 volatility+trend 조합에서 PF≈1.2 seed를 냈기 때문에, “context만 바꿔 다시 훑기”는 novelty(신규성)가 약합니다.

**What must change before Codex opens and runs proxy scout?**
아래 **Required adjustments(필수 조정)** 를 stage-open contract(단계 개방 계약)에 박아 넣어야 합니다.

---

### Required adjustments before open (필수 조정)

1. **Novelty delta contract (신규성 차이 계약)**
   - Changed variable(변경 변수) = **shock-anchored entry states(충격 고정 진입 상태)**
   - Fixed variable(고정 변수) = `fwd12` horizon proxy, no lifecycle, no F20 seed inheritance
   - Do-not-repeat(반복 금지): F20 global depth-2 atlas, F21 lifecycle/density repair, F05/F15/F19 threshold-backbone loops

2. **Operational “return shock” definition (충격 정의)**
   최소 1개 shock family를 명시적으로 고정하세요. 예:
   - `return_zscore_20`, `log_return_1`, `return_1_over_atr_14`, `gap_percent`, `close_prev_close_ratio`
   효과: “충격”이 추상 문구가 아니라 검색/판정 가능한 피처 집합이 됩니다.

3. **Thematic bucket map (주제 버킷 지도)** — F20 전체 58 sweep 금지
   | Bucket | Example features |
   |---|---|
   | shock | `return_zscore_20`, `log_return_1`, `gap_percent` |
   | volatility | `atr_14_over_atr_50`, `historical_vol_5_over_20`, `vix_zscore_20` |
   | trend/chop | `adx_14`, `ema20_ema50_diff`, `bb_squeeze` |
   | session age | `minutes_from_cash_open`, `is_first_30m_after_open` |
   | breadth | `mega8_pos_breadth_1`, `us100_minus_mega8_equal_return_1` |

4. **Mandatory cross-family rule shape (교차군 규칙 형태)**
   모든 후보는 **shock 1개 이상 + context 1개 이상**을 포함해야 합니다.
   효과: F20식 “vol+trend 재발견”만으로 scout clue를 주장하지 못하게 합니다.

5. **Search breadth cap (탐색 폭 상한)**
   - condition pool per family 상한 (예: family당 ≤8)
   - pair depth = 2 고정, 3-depth 금지
   - max candidates ≤200 (F20 533 재현 금지)
   - train-only rank, validation/OOS read-only 유지

6. **F20 duplicate guard (F20 중복 가드)**
   best rule이 다시 `vix_zscore_20 + close_ema50_ratio` 류면:
   - judgment = `f20_duplicate_pressure_not_novel_pf_source`
   - scout clue 주장 금지, reference contrast only
   효과: “새 전선”이 “F20 재확인”으로 닫히는 걸 막습니다.

7. **Side hypothesis lock (방향 가설 잠금)**
   shock continuation vs shock fade/mean-reversion 중 **어느 쪽을 먼저 시험하는지** stage-open에 적으세요. train-only side pick은 허용하되, 양쪽 무제한 혼합 탐색은 금지하는 편이 낫습니다.

8. **Exit proxy lock (청산 프록시 잠금)**
   “simple next-bar/horizon proxy”를 `future_log_return_12 + scout.ROUGH_COST_LOG_RETURN` 로 고정 명시. lifecycle repair는 **PF source가 validation+OOS 양수일 때만** 후속 run으로 분리.

9. **Tier labeling (티어 라벨링)**
   Tier A separate only; Tier B = `missing_required`; Tier A+B = `out_of_scope_by_claim` — 제안대로 유지 OK.

10. **Success criteria tweak (성공 기준 미세 조정)**
    scout clue에 **“shock feature present + not F20-duplicate”** 를 추가하세요.
    seed/handoff PF·DD·density 기준은 그대로 써도 됩니다.

---

### Advice classification (조언 분류)

| Item | Class |
|---|---|
| Open new PF-edge-source frontier after F21 close | **accepted** |
| Thematic session/shock/breadth hypothesis direction | **accepted** |
| Run as-is without locks | **rejected** — F20 partial rerun risk |
| Inherit F20 seed or F21 lifecycle in first proxy | **rejected** |
| Exact bucket sizes / side choice | **needs_local_verification** — stage-open doc에서 확정 |

**Forbidden claim check:** pass — Grok review does not create promotion, runtime authority, baseline, or Goal Achieve.

---

### Grok receipt (영수증)

- **trigger_reason:** user-requested bounded Grok review before Frontier22 open
- **review_size:** small
- **direction_before_grok:** open `stage_frontier_22__session_return_shock_pf_source_onnx_scout` as scout-only PF-source hypothesis
- **bounded_evidence:** F21D closeout, F20C closeout, F20B methodology (`build_condition_pool` on all 58 features), `feature_set_v2` 58 order, `workspace_state.yaml`
- **prompt_identity:** conversation-only (no new `docs/agent_control/grok_reviews/` packet unless Codex materializes stage open)
- **grok_output_identity:** this response
- **final_codex_direction:** proceed with **adjust** — materialize `frontier22A_stage_open_...` only after novelty delta + shock definition + cross-family rule shape + F20 duplicate guard are written into locks; then run `frontier22B_..._proxy_scout_v1`

---

### Bottom line

**Decision = adjust.**

방향은 맞지만, 지금은 “F20 규칙 지도의 테마 필터 버전”에 가깝습니다. **shock-anchored cross-family contract(충격 고정 교차군 계약)** 와 **F20 duplicate guard** 를 stage-open에 넣으면, Codex가 proxy scout를 열어도 됩니다. 그 전에는 scout run을 시작하지 마세요.
