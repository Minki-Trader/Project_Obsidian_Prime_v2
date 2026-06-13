Frontier09 stage-open 검토를 위해 프로젝트 규칙·스킬과 Frontier07/08 맥락을 먼저 확인합니다.
## Grok Stage-Open Review(그록 단계 개방 검토)

**Review size(검토 크기):** medium review(중간 검토)
**Primary classification(주 분류):** **accepted(수용)**
**Claim boundary(주장 경계):** stage-open design only(단계 개방 설계만) — completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) 없음

---

### Conclusion(결론)

Frontier09(전선09) `stage_frontier_09__drawdown_normalized_clean_path_labeling` 개방을 **수용**합니다.

이유는 Frontier08(전선08) 마감 방향(“표본 가중 단독으로는 validation DD(검증 손실폭)를 못 고침 → DD/curve quality(손실폭/곡선 품질)를 직접 다루는 새 가설”)과 맞고, **target representation(목표 표현)** 축을 바꾸므로 Frontier08 반복이 아니기 때문입니다. Frontier07(전선07)과 겹치는 부분은 있지만, 대조군·참조 전용 설계와 “drawdown-normalized clean path(손실폭 정규화 깨끗한 경로)” 계약으로 **정교화된 재시험**으로 볼 수 있습니다.

---

### 1. Novelty delta(신규성 차이)

| Axis(축) | Frontier07 | Frontier08 | Frontier09 (proposed) |
|---|---|---|---|
| What changes(무엇이 바뀌나) | risk-shaped labels(위험 형성 라벨) | same labels + sample weights(동일 라벨 + 표본 가중) | **new label contract(새 라벨 계약)** |
| DD intent(손실폭 의도) | adverse excursion scoring(불리 이동 점수화) | train loss reweighting(학습 손실 재가중) | **bad-path rows → flat(나쁜 경로 행 → 관망)** |
| Runtime(런타임) | fixed probs3 argmax(고정 3확률 최대확률) | same | same |

**Plain meaning(쉬운 설명):** Frontier08은 “같은 정답지, 다른 공부 비중”이었고, Frontier09는 “정답지 자체를 더 까다롭게 만든다”는 차이입니다.

**Frontier07 overlap(전선07 겹침) — acknowledged, not blocking:**

로컬 `frontier07b` 구현을 보면 제안 3 family(가족)가 F07 family와 대응됩니다.

- `payoff_adverse_ratio` ≈ F07 `mae_mfe_balance` (MFE가 MAE를 압도해야 함)
- `underwater_burden` ≈ F07 `time_to_adverse_penalty` (불리 이동 부담) — 단, F09는 **bar count(봉 수)** 명시가 잠재 차이점
- `clean_recovery` ≈ F07 `recovery_close_survival` (종가 회복 + 경로 제한)

**Effect(효과):** F07을 그대로 다시 여는 것은 아니지만, scout(탐색) 전에 family별 `difference_from_f07(전선07 대비 차이)`를 stage brief(단계 개요)에 적어야 “이름만 바꾼 반복” 논쟁을 막을 수 있습니다.

**Archive note(보관소 메모):** Stage281 `drawdown-normalized directional`(손실폭 정규화 방향)은 **negative memory(부정 기억)** 로 reference only(참조 전용)만 씁니다. F09는 Python oracle-label scout(오라클 라벨 탐색)이므로 같은 실패를 그대로 상속하지 않지만, `do_not_repeat(반복 금지)`에 “Stage281 MT5 directional rebuild(방향 MT5 재구성) 재시도 금지”를 넣는 것이 좋습니다.

---

### 2. Leakage boundary(누수 경계)

**Accepted design elements(수용 설계 요소):**

- train-only thresholds(학습 전용 임계값) from future path diagnostics(미래 경로 진단) — F07 `base_scale = train quantile`(학습 분위수) 패턴과 동일하면 안전
- oracle labels for supervised learning only(지도학습 전용 오라클 라벨) — runtime signal(런타임 신호) 아님 주장 적절
- unchanged split(분할 불변) + same 58-feature Tier A(동일 58피처 티어 A)

**Needs local verification at implementation(구현 시 로컬 검증 필요):**

1. 모든 threshold/scale(임계값/스케일)이 **train split(학습 분할)** 에서만 fit(적합)되는지 코드·리포트로 확인
2. validation/OOS(검증/표본밖)는 evaluation-only(평가 전용)인지 확인
3. “drawdown-normalized(손실폭 정규화)”가 전체 샘플·검증 구간 통계를 쓰지 않는지 확인 — 이게 섞이면 leakage(누수) 위험

F07 `path_arrays` + `build_risk_labels`는 이미 horizon-future path(수평선 미래 경로)를 라벨에 쓰되, feature(피처)에는 넣지 않습니다. F09도 같은 경계를 유지하면 scout lane(탐색 레인)에서는 허용됩니다.

---

### 3. Controls(대조군)

**Strong enough(충분함):**

- `label_v1` reference(참조) — “기존 3분류 기준선이 아니라 비교 축”
- Frontier07 risk label reference(전선07 위험 라벨 참조) — **가장 중요한 대조군** (F07 vs F09 차이를 직접 측정)
- matched sklearn specs(동일 sklearn 스펙): logistic plain/balanced, small RF balanced
- ONNX parity per model(모델별 온엑스 동등성)
- same scout gates(동일 탐색 게이트): density 5–10/day, PF≥1.2, DD≤15%

**Effect(효과):** F09가 F07보다 나은지 “같은 모델·같은 split”에서 paired axis(짝 축)로 판정할 수 있습니다. winner/baseline(승자/기준선) 상속 없이도 비교는 가능합니다.

---

### 4. Does this avoid merely repeating Frontier07/08?(전선07/08 단순 반복 회피?)

| Frontier | Repeat risk(반복 위험) | Verdict(판정) |
|---|---|---|
| **F08** | Low(낮음) — weight axis(가중 축), not labels(라벨 아님) | **Avoided(회피됨)** |
| **F07** | Medium(중간) — 3 family가 F07 subset에 가깝음 | **Avoided if** family mechanics differ + F07 is explicit control(가족 기계가 다르고 F07이 명시 대조군이면 회피) |

**Not a blocked retry(차단 재시도 아님)** because:

- F08 negative memory(부정 기억): “sample weighting alone(표본 가중 단독)은 validation DD 58–60% 미해결” → F09는 weight(가중)이 아닌 label(라벨) 축
- F08 closeout(마감)이 다음을 “DD/curve quality new hypothesis(손실폭/곡선 품질 새 가설)”로 지정
- F07 preserved clue(보존 단서)(OOS DD 개선, density bridge)는 **reference only(참조 전용)** 로 carry(운반) 가능

**Stop criteria(중단 기준)** 도 적절합니다: class collapse(분류 붕괴), density-only gain with PF/DD worsening(밀도만 개선), validation DD still far above 15% with no paired improvement(짝 개선 없음).

---

### Accepted for stage open(단계 개방 수용 항목)

- Open `stage_frontier_09__drawdown_normalized_clean_path_labeling`
- Run `frontier09A_stage_open_drawdown_clean_path_labeling_v1` (workspace의 `frontier09A_stage_open_new_hypothesis_design_v1`와 정렬 가능)
- Next scout: `frontier09B_drawdown_clean_path_label_proxy_scout_v1` (이름은 Codex가 패턴에 맞게)
- Keep fixed probs3 ONNX contract(고정 3확률 온엑스 계약), argmax-only(최대확률 전용), no threshold search in first scout(첫 탐색에서 임계값 탐색 없음)
- WFO/MT5 only after strict scout clue + Grok pre-expensive review(엄격 탐색 단서 + 그록 비싼 검증 전 검토)

### Needs local verification before/during materialization(개방 물질화 전·중 로컬 검증)

1. Stage brief에 family별 `difference_from_f07` 1줄씩
2. `do_not_repeat`: F08 weight-only repair(가중 단독 수리), F07 family rename without mechanical delta(기계적 차이 없는 이름 변경), Stage281 MT5 directional rebuild
3. Train-only threshold audit(학습 전용 임계값 감사) in frontier09A report
4. Tier B / combined: `missing_required` if unavailable(불가 시 필수 누락 명시)

### Rejected(거절)

- Opening에 completion/baseline/promotion/runtime authority 주장 — 금지, 제안도 없음 ✓
- F07 best row를 seed/winner로 상속 — 금지, 제안도 control only ✓

---

### Receipt(영수증)

| Field(필드) | Value(값) |
|---|---|
| trigger_reason(트리거 이유) | User-requested Frontier09 stage-open review |
| review_size(검토 크기) | medium |
| bounded_evidence(제한 근거) | `workspace_state.yaml`, F07B label code, F08D closeout, frontier_governance |
| advice_classification(조언 분류) | **accepted** |
| forbidden_claim_check(금지 주장 확인) | pass — no authority claims proposed |
| final_codex_direction(최종 Codex 방향) | Proceed to materialize Frontier09A; enforce F07-as-control and train-only leakage guards at scout |

---

**한 줄 요약:** Frontier09 개방은 **수용**합니다. F08 반복은 피하고, F07과의 겹침은 **대조군 + family별 mechanical delta 문서화**로 관리하면 됩니다. 개방은 설계 단계이며, scout 결과가 나오기 전까지 어떤 성능 주장도 할 수 없습니다.

원하시면 다음 턴에서 Codex가 `materialize_frontier09a_stage_open` 패턴으로 stage folder(단계 폴더)·decision memo(결정 메모)·workspace sync(작업공간 동기화)까지 진행할 수 있습니다.
