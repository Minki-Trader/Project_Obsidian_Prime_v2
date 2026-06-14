## Classification: accepted

Codex가 제안한 Frontier15 `negative_memory` 마감은 제한 근거와 맞습니다. 엄격 통과 행이 0이고, PF/DD/하위기간 안정성이 동시에 맞지 않았으며, 빈도 전이만은 좁은 보존 단서로 남길 수 있습니다.

---

## Answers:

**1. `negative_memory` closeout(부정 기억 마감)이 적절한가?**
**예, 적절합니다.**
- 후보 81행 중 primary strict(1순위 엄격) 0, secondary strict-like(보조 엄격 유사) 0, preserved clue rows(보존 단서 행) 0입니다.
- 전체 최고 행도 validation PF(검증 수익 팩터)가 1.006 수준이고 negative subperiod fraction(음수 하위기간 비율)이 0.364로, “엣지 품질 + PF/DD + 안정성”을 같이 만족하지 못합니다.
- 1순위 칸 `edge_margin__target8` 최고 행은 validation PF 0.895, negative subperiod 0.50으로 더 약합니다.
- “확률 점수 임계값 + density target(빈도 목표)만으로는 품질·리스크·안정성을 동시에 만들지 못했다”는 부정 기억 문장이 근거와 일치합니다.

**2. density-transfer clue(빈도 전이 단서)를 preserved clue(보존 단서)로 좁게 보존해도 되는가?**
**예, 좁게 보존해도 됩니다.**
- train threshold density(학습 임계값 빈도)는 모든 칸에서 5/8/10 per day(일 5/8/10회) 목표에 정확히 맞습니다.
- validation/OOS density(검증/표본밖 빈도)는 목표 주변으로 전이됩니다. 예: `edge_margin__target8` validation 8.629/day, OOS 8.063/day.
- 이건 **빈도 보정 메커니즘**에 대한 관찰이지, edge quality(엣지 품질)나 PF/DD 승격 주장이 아닙니다.
- preserved clue rows가 0인 것은 “행 단위 엄격 통과” 기준이고, **칸/메커니즘 수준의 좁은 단서**는 별도로 남겨도 과장이 아닙니다.
- 단, “density transfer = edge”나 “target8 = 운영 후보”로 확장하면 안 됩니다.

**3. 필수 수리가 F15 내부에 남아 있는가, 아니면 다음 프론티어로 가야 하는가?**
**다음 프론티어 단계로 가야 합니다. F15 내부 추가 수리는 필요하지 않습니다.**
- 고정 9칸 격자에서 후보를 충분히 봤고, 엄격 통과가 0이면 같은 가설 안 threshold/density 튜닝만으로는 수리 경로가 좁습니다.
- 남은 실패는 PF/DD/smoothness(수익 팩터/손실폭/매끄러움) 동시 통과이므로, score contract(점수 계약) 변경, 다른 신호/리스크 결합, 또는 다른 선택 기준 같은 **새 가설**이 필요합니다.
- density transfer(빈도 전이)는 다음 단계의 **입력 단서**로 쓰고, F15 안에서 “한 번 더 고쳐서 통과시키기”는 하지 않는 것이 맞습니다.

---

## Required local checks:

- `stages/stage_frontier_15*/03_reviews/stage_run_ledger.csv`에서 strict/preserved clue 행 수가 **0/0/0**인지 확인
- `docs/registers/alpha_run_ledger.csv`와 stage closeout 문서의 **81 candidates / 9 cells / primary cell** 숫자 일치 확인
- closeout 문서에 **density-transfer preserved clue**가 PF/DD/승격 주장 없이 **메커니즘 관찰**로만 적혀 있는지 확인
- `docs/workspace/workspace_state.yaml`에 active stage가 Frontier15에서 **closed negative_memory**로 바뀌었는지 확인
- forbidden claims(금지 주장)가 문서/레지스터에 실수로 들어가지 않았는지 확인

---

## Forbidden claims:

| Claim | Status |
|---|---|
| completion(완성) | `not_claimed` |
| baseline(기준선) | `not_claimed` |
| promotion(승격) | `not_claimed` |
| runtime authority(런타임 권위) | `not_claimed` |
| live readiness(실거래 준비) | `not_claimed` |
| Goal Achieve(목표 달성) | `not_claimed` |

**모두 `not_claimed` — 이번 마감 제안 범위 안에서는 금지 주장이 없습니다.**
