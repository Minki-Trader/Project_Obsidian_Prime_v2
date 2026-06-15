# Frontier57 Stage-Open Review — External Second Opinion

**Review size:** medium review (제한 스냅샷 + 집중 질문 3개)
**Claim boundary:** 방향 타당성·사전 점검·마감 기억만 논함. F57 실행·승격·런타임 권위 주장 없음.

---

## 1. F57 방향 — 의미 있는 신규인가, 수리 반복인가?

**분류: `accepted` (부분 수용)** — 둘 다 맞고, “수리만”은 아님.

| 축 | F56 | F57 | 판단 |
|---|---|---|---|
| **Label/source (라벨/원천)** | 불리 이동(adverse excursion) 손절 회피 | 빠른 청산(fast-exit) 수익 거래 | **새 알파 가설** |
| **Proxy ranking (프록시 순위)** | 순차 비중복 필터 거래 | 전체 원신호 = 실행 거래 | **F56 마감 단서에 맞춘 수리** |
| **고정 인프라** | US100 M5, Tier A, 58-feature, ExtraTrees, short-only 등 | 동일 | 탐색 프레임 유지 |

**근거**

- F56 마감은 “동등성(parity) 차단”이 아니라 **“MT5 거래 빈도가 프록시 필터 빈도가 아니라 원신호 빈도를 따름”** 이었다. F57의 all-signal proxy는 그 단서에 **직접 대응**한다 → 수리 루프(repair loop) 성격이 분명함.
- 동시에 라벨/원천을 **회피(avoidance) → 양수 실행(positive execution)** 으로 바꾸는 것은 단순 프록시 패치가 아니라 **별도 가설**이다. 스테이지명 `after_adverse_excursion_memory`도 F56을 상속(inheritance)이 아니라 **참조(reference)** 로 쓰는 전선 규칙과 맞다.

**리스크 (claim boundary 낮춤)**

- 두 축을 한 번에 바꾸면, MT5 실패 시 **원천 실패 vs 프록시 정렬 실패** 분리가 어렵다.
- 탐색 단계에서는 허용 가능하나, closeout(마감)에서는 **어느 축이 실패했는지**를 반드시 쪼개 기록해야 한다.

**한 줄 요약:** F57 = **(A) 실행 정렬 프록시 수리** + **(B) fast-exit short 원천 신규 가설**. 수리만이 아니지만, 프록시 변경만으로 F56을 “고친 것”이라고 말하면 과장이다.

---

## 2. MT5 전 Codex가 해야 할 로컬 점검

**분류: `accepted`** — F56 단서에서 필수 항목이 거의 정해져 있음. 아래는 스냅샷 기준 **필수 최소 집합**이다.

### A. Proxy 경제성 (MT5 전 게이트)

1. **Validation + OOS** 모두에서 all-signal proxy PF·DD·trades/day(거래/일) 기록.
2. **원신호 밀도**가 대략 **5~10/day** 인지 확인 (F57 성공 기준과 F56 MT5 실측 ~7.6~7.8/day 정합).
3. F56 대비 **순차 필터 proxy (~3.2~3.5/day)** 와 **all-signal proxy** 밀도·PF 차이를 **같은 표에서** 남김 — “프록시만 바꿨을 때 경제성이 살아나는지”를 MT5 전에 먼저 본다.

### B. Handoff / parity (인계·동등성)

4. Pre-MT5에서 **signal_diff=0**, **feature_ready_diff=0** 목표 정렬 확인 (F56에서 parity는 blocker가 아니었지만, 정렬 여부는 **실패 원인 분리**에 필요).
5. **Short-only**, **58-feature order**, **direct ONNX threshold**, **no sparse admission**, **no RuntimeVetoTape** 고정 변수가 학습→보내기→EA 인계 경로에서 일관한지 점검.

### C. Label/source 정의 (신규 가설 축)

6. **Fast-exit profitable trade** 라벨 정의가 leakage(누수) 없이 Tier A validation/OOS split과 맞는지 확인 — 스냅샷만으로는 정의 검증 불가 → **`needs_local_verification`** (라벨 경계·누수·집계 규칙).
7. 학습 표본에서 short 원천의 **표본 수·양성 비율·기간별 안정성** — proxy가 좋아도 원천이 희소/불안정하면 MT5 반복 실패 가능.

### D. Proxy–runtime gap 사전 문서화

8. F56 교훈대로 **proxy trades/day vs 기대 raw signal rate** 갭을 probe **전**에 기록 (probe 후 “또 밀도만 맞고 PF는 무너짐” 패턴인지 바로 비교).

### E. Mandatory probe 준비

9. Probe 1회: PF, DD, density, **proxy-runtime gap**, signal_diff, feature_ready_diff를 **한 줄 receipt(영수증)** 로 남길 필드 확정.

**MT5 전 go/no-go (스냅샷 기준)**

- **Go:** all-signal proxy가 val+OOS에서 경제성이 “약하지만 추적 가능”하고, 밀도 ~5~10/day, handoff 정렬 점검 통과.
- **No-go (MT5 연기):** proxy 경제성이 여전히 약하거나 불안정 — F57 실패 기준 1번에 해당; MT5는 “밀도 정렬 실험”만 반복할 위험.

---

## 3. MT5가 또 실패할 때 required closeout memory (필수 마감 기억)

**분류: `accepted`**

F56이 이미 **“parity ≠ blocker, density misalignment ≠ 유일 원인”** 을 남겼으므로, F57 재실패 시에는 **패턴 이름을 더 쪼개**야 한다.

### 필수 기록 (최소)

| 항목 | 기록 내용 |
|---|---|
| **Failure mode (실패 유형)** | `parity_fail` / `density_align_economics_collapse` / `source_no_transfer` / `proxy_still_misaligned` 중 **하나 이상 명시** |
| **Parity row** | signal_diff, feature_ready_diff — F56처럼 0이면 “동등성 차단 아님”을 다시 명시 |
| **Density row** | proxy all-signal trades/day vs MT5 trades/day — F56의 3.2~3.5 vs 7.6~7.8 비교를 **F57 숫자로 갱신** |
| **Economics row** | proxy PF (val/OOS) vs MT5 PF (val/OOS), DD — “밀도 맞췄는데 경제성 붕괴” 반복 여부 |
| **Source axis** | fast-exit positive label이 MT5로 **전이(transfer) 안 됨** vs **전이됐으나 PF<1** 구분 |
| **Negative memory 한 줄** | 예: `negative_memory_fast_exit_short_source_did_not_transfer_despite_all_signal_proxy` 또는 `negative_memory_density_aligned_proxy_runtime_gap_closed_but_pf_below_one` |

### 분기별 마감 문장 (템플릿)

1. **Parity 깨짐:** handoff/정렬 문제로 MT5 실패 — economics 주장 금지.
2. **Parity 유지 + 밀도 정렬 + PF<1:** F56 후속 — **“실행 정렬 all-signal proxy로 밀도 갭은 닫혔으나 short fast-exit 원천 경제성은 MT5에서 재현 안 됨”**.
3. **Parity 유지 + 밀도 여전히 어긋남:** all-signal proxy 수리 **불충분** — sequential 필터 말고도 다른 실행 레이어가 빈도를 지배.
4. **Proxy 자체가 val/OOS에서 이미 약함:** MT5 실패는 확인용 — **probe 없이도 탐색 종료 가능**했는지 retrospective(사후) 기록.

### 금지 주장 (F57 closeout)

- completion / baseline / promotion / runtime authority / live readiness / Goal Achieve — 사용자 성공 기준과 동일하게 **금지**.

### 다음 전선에 넘길 clue (do-not-repeat)

- **“원신호 밀도로 proxy를 고르되, 평가는 sequential filtered trades/day로 하지 말 것”** — F56에서 이미 나온 clue; F57에서 all-signal로 바꿨는데도 실패하면 **“밀도 정렬만으로는 short 원천 승격 불가”** 를 negative memory로 격상.

---

## Advice Classification Summary

| 질문 | 분류 | 요약 |
|---|---|---|
| Q1 신규 vs 수리 | **accepted** | 신규 가설 + 프록시 수리 병행; 둘 다 해당 |
| Q2 MT5 전 점검 | **accepted** + 일부 **needs_local_verification** (라벨 정의·누수) | proxy val/OOS, 밀도 5~10/day, parity, gap 사전 기록 |
| Q3 실패 시 마감 기억 | **accepted** | parity/density/economics/source 4축 분리 negative memory |

---

**Codex action (방향만):** F57 개방은 **타당**하다. 다만 MT5 probe 전에 **all-signal proxy가 val+OOS에서 먼저 살아 있는지**를 hard gate로 두고, 재실패 시 F56의 “parity 아님” 기억을 **더 세분화된 실패 유형**으로 이어갈 것.
