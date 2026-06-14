Frontier31 단계 개방 검토입니다. Grok 협업 스킬과 로컬 근거를 먼저 확인한 뒤, 요청하신 형식으로 답하겠습니다.
## Frontier31 Stage-Open Review (전선31 단계 개방 검토)

로컬 검증 완료: `final_closeout_summary.json`, `workspace_state.yaml`, `preserved_clue.md`, `negative_memory.md`, `density_preserving_preselector_lock_spec.md`의 수치·라벨이 제시 근거와 일치합니다. F30D는 `next_stage_id` / `next_run_id`로 F31을 이미 예약했고, F30C 진단의 `would_require_exit_shape_pivot_rows: 5`가 exit-shape pivot(청산 형태 전환)을 다음 전선 단계로 넘기는 근거와 맞습니다.

---

- **verdict:** accepted
- **novelty_ok:** yes
- **leakage_risk:** low
- **frontier_boundary_ok:** yes
- **hypothesis_scope_ok:** yes
- **runtime_claim_boundary_ok:** yes

**must_watch:**
- F30에서 exit-shape는 `reference_fallback_only`였고, F31에서만 `active_changed_variable`로 승격 — F30B 안에서 켜면 안 됨
- 고정 대상은 F30B source no-veto scout 5행뿐 — entry mask(진입 마스크)·진입 규칙·scout 재순위화 금지
- `future_log_return_12`만 있으므로 return-space clipping(수익률 공간 클리핑)은 탐색 프록시일 뿐, MT5 실행 표현이 아님
- 5개 scout 전부 `scout_pf_blocked_seed`였음 — train-only exit 선택이 PF lift를 만들어도 forward read-only PF(`~1.31`/`~1.15`)가 seed floor를 넘는지 별도 확인
- transform family(변환군)가 크면 train tail overfit(학습 꼬리 과적합) 위험 — 파라미터 수·선택 규칙을 F31A에 명시
- 비현실적으로 tight한 clipping만 통과하면 `invalid setup` 또는 `negative memory`로 닫기
- MT5/ONNX/WFO는 `handoff_candidate_rows > 0` + executable exit representation + pre-expensive Grok review 전부 충족 전 금지

**advice_classification:**

- **accepted**
  - F31을 exit-shape pivot 전용 새 frontier stage로 여는 것 — F30D `next_hypothesis_clue`와 frontier repair rule(수리 규칙)의 정상 격상(escalation, 격상)
  - `train_only_return_space_exit_shape_transform`을 단일 active changed variable로 두는 것 — F30 preselector(사전 선택기)와 분리된 novelty delta(신규성 차이)
  - F30B 5개 scout + mask/entry 고정 — invalid boundary(무효 경계)와 일치
  - train split PnL만으로 exit parameter 선택, validation/OOS는 read-only — leakage guard(누수 방어)로 타당
  - return-space proxy를 scout/seed surface 탐색용으로만 쓰고 MT5 executability(실행 가능성)를 주장하지 않는 것
  - F30 identity를 reference-only로 두고 winner/baseline/promotion/runtime authority를 상속하지 않는 것
  - 실패 경계(validation/OOS 선택, entry 변경, forward re-rank, clipping-only MT5 claim)가 명확한 것
  - forbidden claims(금지 주장) 전부 `not_claimed` 유지

- **rejected**
  - F30 안에서 exit-shape pivot을 active로 켜서 scout를 seed/handoff로 구제하려는 시도
  - validation/OOS PF/DD로 stop/take 파라미터를 고르거나 scout를 재순위화하는 것
  - return-space clipping만으로 MT5/ONNX 실행 가능성·runtime authority를 주장하는 것
  - `f30b_0214` forward read-only 수치를 baseline/promotion/handoff 근거로 승격하는 것
  - handoff 후보 없이 MT5/ONNX/WFO를 실행하는 것

- **needs_local_verification**
  - F31A stage-open 시 F30B 5개 scout row identity를 `density_preselector_candidate_summary.csv`(또는 동등 산출물) 경로·해시로 고정했는지
  - F31B proxy 구현 시 transform family·parameter grid·train-only selection audit trail(감사 흔적)이 실제로 기록되는지
  - (stage-open verdict 자체는 이번 bounded evidence 범위에서 로컬 재검증 완료)

---

### Specific checks (구체 확인)

**1. F30이 exit-shape를 reference-only로 둔 뒤, F31을 exit-shape pivot 전용 새 frontier로 여는 것이 타당한가?**

**예.** F30은 “F30 안에서 exit-shape를 켜지 말라”는 뜻이지 “다음 전선에서 시험하지 말라”는 뜻이 아닙니다. F30C는 5개 scout 모두 `would_require_exit_shape_pivot_rows`로 분류했고, F30D는 `exit_shape_pivot_for_density_preserved_source_scout_pf_lift_reference_only`를 다음 단서로 보존했습니다. active changed variable(활성 변경 변수)이 preselector → exit-shape transform으로 바뀌므로 frontier governance의 새 전선 개방 조건을 만족합니다.

**2. MT5 실행 가능성을 주장하지 않는다면 return-space exit-shape proxy가 탐색에 충분히 유용한가?**

**예, 범위 안에서는.** `future_log_return_12`만 있을 때 intrabar MFE/MAE(봉내 최대유리/불리 이동) 없이도 “고정 진입 위에 청산 형태가 PF/DD를 얼마나 바꿀 수 있는지”를 저비용으로 볼 수 있습니다. 다만 이는 scout clue/seed surface(탐색 단서/씨앗 표면)용 프록시이며, executable exit representation(실행 가능한 청산 표현)이 생기기 전까지는 handoff 근거가 될 수 없습니다.

**3. exit parameter를 train만 쓰고 validation/OOS는 read-only면 leakage risk(누수 위험)가 낮은가?**

**낮음 — 계약이 지켜지면.** 선택이 train PnL distribution(학습 손익 분포)에만 묶이고 validation/OOS가 진단 전용이면 전형적인 forward leakage(전진 누수)는 막힙니다. 다만 scout가 5개뿐이고 transform family가 넓으면 train-tail overfit(학습 꼬리 과적합)은 남으므로, F31A에 파라미터 수·선택 규칙·감사 흔적을 적어 두는 것이 좋습니다.

**4. F31B proxy 전·비싼 MT5/ONNX/WFO 전에 Codex가 지켜볼 것**

| 시점 | 필수 감시 |
|------|-----------|
| **F31A (hypothesis design)** | 5 scout row 고정 경로·해시, transform family 정의, train-only selection contract, data limitation 명시, failure/invalid boundary 문서화 |
| **F31B (proxy)** | entry/mask 불변, train-only exit 선택 audit, forward metric은 read-only only, unrealistic clipping 탐지, seed/handoff gate 정의 |
| **MT5/ONNX/WFO 전** | `handoff_candidate_rows > 0`, executable exit representation 존재, proxy→executable gap(프록시↔실행 간극) 기록, pre-expensive Grok review, runtime probe status 기록 |

---

**Plain read (쉬운 해석):** F30은 “밀도는 맞는 진입 후보 5개를 찾았지만, 수익 팩터·손실폭 때문에 씨앗/인계까지는 못 갔다”로 닫혔습니다. F31은 그 5개 진입을 그대로 두고, **청산 형태만** 바꿔서 PF가 오르고 DD가 줄 수 있는지 보는 다음 가설입니다. 탐색용 수익률 프록시로는 타당하고, 누수 방어·런타임 주장 경계도 잘 잡혀 있어 **stage-open은 수용(accepted)** 합니다.
