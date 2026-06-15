# Grok Receipt(그록 영수증): stage_open(단계 개방)

- path(경로): `docs/agent_control/grok_reviews/2026-06-16_frontier58_stage_open_snapshot`
- classification(분류): `needs_local_verification(로컬 검증 필요)`
- metadata_success(메타데이터 성공): `True`
- metadata_timed_out(메타데이터 시간초과): `False`
- local_action(로컬 행동): Codex(코덱스)가 repo files(저장소 파일), EA parameters(EA 파라미터), MT5 output(MT5 출력)으로 다시 검증했다.
- effect(효과): Grok(그록) output(출력)은 authority(권위)를 만들지 않고 review boundary(검토 경계)만 제공한다.

## Clean Output(정리 출력)
## Grok verdict (그록 판정)

**Novelty under F50~F57:** **conditionally novel at the label axis (라벨 축), not novel at the transfer mechanism (전이 메커니즘).**
**Sharpest pre-MT5 failure risk:** **Python order-path survivability proxy (파이썬 주문경로 생존 프록시) will again look good on density/PF while hiding the same MT5 single-position fill/compression gap (단일 포지션 체결·압축 격차) that killed F50~F57.**

---

### 1) Is F58 materially novel enough?

**Partially — but only as a research pivot, not as a new risk class.**

| What changed | What did not change |
|---|---|
| Axis moved from **exit memory** (F57 fast exit, F56 adverse excursion) toward **entry survivability under immediate friction (즉시 마찰 아래 진입 생존성)** | Still an **execution-shaped microstructure source (실행형 미시구조 원천)** trained in Python, ranked by proxy PF/density/DD, then sent to MT5 |
| Explicitly rejects “fast-exit label tweak only” and “lifecycle as main lever” | Same historical failure chain: **parity can pass, PF source still does not transfer (동등성 통과, PF 원천 미전이)** |

**Why this is not enough novelty by itself**

- F50 already says **first-touch / order-path proxies (첫 터치·주문경로 프록시)** understate MT5 DD and trade-count compression.
- F53~F57 say **path quality, payoff shape, sparse veto, adverse excursion, fast exit** all failed transfer despite different label stories.
- F58’s “early favorable vs early adverse + ATR-buffered survival (초기 유리/불리 이동 + ATR 완충 생존)” is **adjacent reframing**, not a new validation contract. It still predicts “this entry survives friction on the research path,” which is very close to what F50/F53/F56 already probed from different angles.

**Classification**

- **Accepted:** axis shift from exit-label iteration to entry-survivability hypothesis is a **legitimate stage pivot (정당한 단계 전환)** and better than another F57-like tweak.
- **Rejected:** claim that this is **materially novel enough to raise prior on MT5 transfer (MT5 전이 사전확률을 올릴 만큼 충분히 신규)**. Recent memory says the blocker is likely **representation/fill/path semantics (표현·체결·경로 의미)**, not missing one more execution label variant.
- **Needs local verification:** whether “entry survivability” is **empirically orthogonal (경험적으로 직교)** to F56/F57 labels, or mostly the same information with entry timing instead of exit timing.

**Bottom line:** Open F58 as a **bounded scout stage (제한 탐색 단계)** is reasonable. Treat it as **novel question, familiar failure mode (새 질문, 익숙한 실패 양상)** — not a break from the F50~F57 pattern.

---

### 2) Sharpest failure risk before expensive MT5 probe

**#1 risk: optimistic survivability labeling on a non-MT5 order path (비-MT5 주문경로에서 낙관적 생존 라벨링).**

Codex should guard this **before** MT5:

1. **Survivability label uses research fill assumptions MT5 cannot reproduce (연구용 체결 가정이 MT5에서 재현 불가)**
   - Early favorable/adverse windows + ATR buffer can bake in **partial fills, queue, spread timing, single-position sequencing (부분체결, 대기열, 스프레드 타이밍, 단일포지션 순서)** that Python simplifies.
   - Expected symptom: **good proxy density/PF (프록시 밀도·PF 양호)**, then MT5 shows **DD/trade-count compression or PF collapse (손실폭·거래수 압축 또는 PF 붕괴)** even with `feature_ready_diff=0`, `signal_diff=0` — the F50/F51 pattern.

2. **Density target (5~10/day) selects the wrong candidates (밀도 목표가 잘못된 후보를 고름)**
   - For friction-survivability ideas, higher signal density often means **more marginal entries that survive only in proxy (프록시에서만 생존하는 주변 진입)**.
   - F55/F51 warn: parity without runtime edge, DD blowout.
   - Sharpest pre-MT5 guard: rank candidates first on **transfer-sensitive diagnostics (전이 민감 진단)**, not on hitting 5~10/day.

3. **Novelty is nominal; feature space is old (신규성은 이름뿐, 피처 공간은 기존)**
   - If survivability features are mostly transforms of path quality / adverse excursion / early move stats, ONNX parity passes while **mechanism is not new**.
   - Guard: require explicit **orthogonality check vs F56/F57 negative memory (F56/F57 부정기억 대비 직교성 검사)** in proxy stage, not just better PF.

4. **F52-inspired DD policy masks weak PF pre-probe (F52식 손실폭 정책이 약한 PF를 가림)**
   - Even “modest” lifecycle compression can make a bad source look scout-worthy.
   - Guard: evaluate **raw ONNX-threshold PF/DD first (원시 ONNX 임계값 PF/DD 우선)**; add DD compression only in a **separate ablation arm (별도 ablation 팔)**.

---

### 3) What Codex should require before MT5 (cheap gates)

These are **accepted** from the snapshot; they do not need repo inspection to state:

| Pre-MT5 gate | Pass intent | Fail means |
|---|---|---|
| **Transfer-sensitive proxy audit (전이 민감 프록시 감사)** | Recompute survivability under **MT5-like single-position constraints (MT5 유사 단일포지션 제약)** in Python | Stop: likely F50 repeat |
| **Orthogonality to F56/F57 (F56/F57 대비 직교성)** | Show label/source adds signal beyond adverse-excursion / fast-exit memories | Stop: rename, not new source |
| **Density-last ranking (밀도 후순위 랭킹)** | Choose by PF under DD cap, then check density | Stop: F51/F55 density trap |
| **No-DD-policy scout winner (무손실폭정책 탐색 우승자)** | Promote only a candidate with acceptable PF **without** lifecycle compression | Stop: F52 false clue |
| **Explicit proxy-runtime gap hypothesis (프록시-런타임 격차 가설 명시)** | Write which MT5 semantics could break transfer before running tester | Otherwise MT5 is fishing |

If the first gate fails, MT5 is not “validation”; it is **expensive confirmation of a known negative memory (비싼 부정기억 확인)**.

---

### 4) Advice classification (조언 분류)

| Item | Class |
|---|---|
| Open F58 with entry-survivability axis | **accepted** |
| Treat F58 as materially new transfer strategy | **rejected** |
| Mandatory MT5 runtime probe remains correct closeout | **accepted** |
| Orthogonality + MT5-like proxy compression before tester | **needs_local_verification** (Codex must run locally; Grok cannot) |
| F58 likely fails on same proxy-runtime gap if pre-gates skipped | **accepted** (from F50~F57 pattern in prompt) |

---

### 5) One-line answer to your question

**F58 is novel enough to open as the next honest scout question, but not novel enough to expect MT5 transfer unless Codex first proves the survivability source is orthogonal to F56/F57 and still holds under MT5-like single-position path compression; the sharpest pre-MT5 failure risk is another optimistic Python order-path survivability proxy that passes ONNX parity and fails on runtime PF/DD semantics — the same failure family as F50~F57.**
