## Grok Review — Frontier39 Stage Open (small review)

**verdict(판정):** `needs_local_verification` (로컬 검증 필요)

**novelty_ok(신규성 적합):** `yes` (예) — *conditional(조건부)*
F39는 F38의 “얕은 점수 + path-quality 분위수 확장만”이 아니라, **train-only regime gate(학습 전용 체제 게이트)를 thresholding(임계값) 앞에 둔다**는 한 가지 변경 변수가 분명합니다. 다만 여전히 **model-score source family(모델 점수 소스 패밀리)** 안에 있으므로, 설계는 유효하지만 “새 패밀리”라고 말하면 과장입니다.

**leakage_guard_ok(누수 방지 적합):** `yes` (예) — *on paper(문서상)*
`fit only train split(학습 분할만 적합)` + `validation/OOS read-only(검증/표본밖 읽기 전용)` + `train quantiles only(학습 분위수만)` 조합은 방향이 맞습니다.
로컬에서 반드시 확인할 것: val/OOS regime bucket(체제 버킷) 경계가 **train-derived only(학습에서만 도출)** 인지, 그리고 score + regime가 **같은 train window(같은 학습 구간)** 에서만 joint-fit(공동 적합)되지 않았는지.

**runtime_claim_boundary_ok(런타임 주장 경계 적합):** `yes` (예)
`proxy/repair exploration(프록시/수리 탐색)` 한정, seed/runtime candidate(씨앗/런타임 후보) 없으면 MT5 probe(탐침) 금지 — F38 negative memory(부정 기억)와도 맞습니다.

---

### biggest_risk(가장 큰 위험)

**Regime conditioning(체제 조건화)이 PF를 올리는 척하지만, 실제로는 같은 shallow score(얕은 점수)를 train에서 과적합 분할한 것**일 수 있습니다.
F38이 이미 density/DD(밀도/손실폭)는 회복했는데 PF(수익 팩터)만 seed 미만이었다는 점은, **signal weakness(신호 약함)** 또는 **short PF edge(숏 PF 우위) 부재** 쪽 신호입니다. regime bucket(체제 버킷)을 더 얹어도 **matched-density(밀도 맞춤) 비교에서 PF lift(수익 팩터 상승)가 없으면** F38 반복으로 끝납니다.

---

### must_not_repeat(반복 금지)

1. **F38 shallow model-score source family(얕은 모델 점수 소스 패밀리)를 regime label만 바꿔 재실행**
2. **path-quality quantile expansion alone(경로 품질 분위수 확장 단독)** 또는 score threshold sweep(점수 임계값 스윕)만으로 scout row(탐색 행)量産
3. **F38 repair numbers(수리 수치)를 baseline(기준선)처럼 읽기** — reference clue(참조 단서)만 허용
4. **scout row(탐색 행)만으로 seed/runtime narrative(씨앗/런타임 서사) 시작** — F38에서 이미 0이었음
5. **validation/OOS에서 regime boundary refit(체제 경계 재적합)** 또는 feature-derived regime(피처 유래 체제)의 implicit peek(암묵적 엿보기)

---

### suggested_guardrail(제안 가드레일) — smallest before proxy execution(프록시 실행 전 최소 가드레일)

**One mandatory paired ablation(필수 1회 쌍대 소거 실험), same split/hash/replay(동일 분할·해시·재생):**

| Arm | What |
|-----|------|
| **A** | F38-equivalent ungated high-score short mask(게이트 없는 고점수 숏 마스크) |
| **B** | Same score cut + train-only regime gate(동일 점수 컷 + 학습 전용 체제 게이트) |

**Proceed to full scout grid(전체 탐색 그리드) only if(다음을 만족할 때만):**

- **B beats A** on **validation AND OOS(검증·표본밖 모두)**
- **PF(수익 팩터) ≥ +0.05 absolute(절대 +0.05 이상)** vs A
- **density(밀도)** stays in **4–12/day(일 4–12회)** band
- **DD(손실폭)** does not worsen **>1.0% absolute(절대 1.0%p 초과 악화)** vs A

**If fail(실패 시):** close as `regime_gate_did_not_lift_pf_over_ungated_score_at_matched_density(체제 게이트가 동일 밀도에서 무게이트 점수 대비 PF를 끌어올리지 못함)` — **no further regime bucket expansion(추가 체제 버킷 확장 금지)** in F39.

---

### Direct answer to the question(질문에 대한 직접 답)

**Valid F39 hypothesis lifecycle(가설 생명주기)?**
**Yes, as a bounded next pivot(예, 제한된 다음 전환으로서)** — F38 failure mode(PF shortfall despite density/DD recovery, 씨앗/런타임 0)를 직접 겨냥하고, 변경 변수가 하나로 고정되어 있으며, claim boundary(주장 경계)가 낮습니다.

**Still risks same shallow repetition(얕은 반복 위험)?**
**Yes(예)** — 패밀리는 같기 때문입니다. 위 **paired ablation gate(쌍대 소거 게이트)** 없이 proxy를 돌리면, F38c의 “scout는 있으나 seed 0” 패턴이 그대로 반복될 가능성이 큽니다.

**Codex local verification before execution(실행 전 코덱스 로컬 검증):** regime bucket definition(체제 버킷 정의)이 58-feature train quantile(58피처 학습 분위수)만 쓰는지, ablation A/B wiring(배선)이 동일 replay path(동일 재생 경로)인지 확인 후 `frontier39A` proxy를 열면 됩니다.
