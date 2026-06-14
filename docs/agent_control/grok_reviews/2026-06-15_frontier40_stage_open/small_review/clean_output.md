## Grok small review — Frontier40 stage open

**verdict:** `accepted`

**novelty_ok:** `yes`
F39가 score + regime gate(점수·레짐 게이트) 쪽을 `preserved_clue_negative_memory`로 닫았고, F40은 **entry-known raw feature state pocket(진입 시점 알려진 원시 피처 상태 포켓)**으로 source family(소스 계열)를 바꿉니다. F39 best를 baseline(기준선)으로 물려받지 않는 것도 맞습니다.

**leakage_guard_ok:** `needs_local_verification`
설계상 train-only fitting(학습 구간만 적합)과 read-only validation/OOS(검증·OOS 읽기 전용)는 맞지만, 58-feature × threshold × AND/OR(조합) 탐색은 **multiple-testing leakage(다중검정 누수)** 위험이 큽니다. Codex가 로컬에서 “선택이 train에서만 닫혔는지”를 확인하기 전에는 leakage-safe(누수 방지)로 닫지 마세요.

**runtime_claim_boundary_ok:** `yes`
Exploration only(탐색 전용), no runtime authority(런타임 권위 없음), F39 `runtime_probe_ineligible`(런타임 탐침 부적격)을 이어받지 않음, seed/runtime 전 pre-expensive Grok review(비용 큰 작업 전 그록 검토) — 경계가 적절합니다.

**mandatory_guardrail:**
Codex는 **WFO/MT5/runtime(워크포워드/메타트레이더5/런타임) 전에** 아래를 강제하세요.

1. **Train-only selection freeze(학습 구간 선택 고정):** pocket threshold(포켓 임계값), AND/OR union(조합 합집합), stop/take(손절·익절) 전부 train split(학습 분할)에서만 선택·고정하고, validation/OOS는 **평가만**.
2. **Search budget cap(탐색 예산 상한):** single / two-feature AND / one capped OR-repair(1회 한정 OR 수리)만 허용; validation/OOS metric으로 feature·threshold·union을 고르는 것 금지.
3. **Matched-comparison gate(동일 조건 비교 게이트):** B의 scout/seed/runtime 주장은 반드시 **같은 train-derived stop/take family(동일 학습 유래 손익절 계열)**의 A 대비, **density-matched(밀도 맞춤)** lift(개선)로만 판정 — F39 negative memory(부정 기억)와 같은 밀도 착시 방지.
4. **F39 parity guardrail(39단계 동등 가드레일):** `ablation pass rows > 0` 및 seed/runtime ledger rows(장부 행) 없으면 runtime probe packaging(런타임 탐침 패키징) 금지.
5. **Entry-known audit(진입 시점 알려진 감사):** 58-feature contract(피처 계약) 전부 closed-bar entry-known(봉 마감 후 진입 시점 알려짐) 로컬 증명 없으면 후보 폐기.

**biggest_risk:**
Broad raw-feature pocket mining(넓은 원시 피처 포켓 채굴)이 train에서 우연한 scout clue(정찰 단서)를 만들고, validation/OOS에서 **A 대비 PF lift 없이 density/DD만 좋아 보이는** F39형 false pocket(가짜 포켓)을 재현할 가능성.

**suggested_stop_rule:**
- **No scout vs A, or no density-matched PF lift vs A** → `negative_memory`로 즉시 close(마감).
- **Scout 있으나 seed surface(씨드 표면) 미달** → proposed one capped OR-repair 1회만; 이후에도 seed 없으면 close.
- **Seed surface 충족** → WFO/MT5/runtime 전에 stop하고 pre-expensive Grok review(비용 큰 작업 전 그록 검토) 필수.
- **Runtime candidate(런타임 후보) 없음** → exploration close(탐색 마감)만; runtime authority 주장 금지.

---

**요약:** Frontier40 stage-open direction(전선 40단계 개방 방향)은 F39 이후 **valid exploration pivot(유효한 탐색 전환)**으로 **accepted(수용)**. 다만 Codex는 위 **mandatory guardrail(필수 가드레일)**을 로컬 검증·시행한 뒤에만 실험 실행을 열어야 합니다.
