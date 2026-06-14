Frontier32 개방 검토입니다. Grok 협업 스킬과 전선 거버넌스·F31 맥락을 먼저 확인합니다.
**Grok advisory (조언 전용)** — Codex가 최종 판정을 소유합니다.

---

```
verdict: accepted
novelty_ok: yes
leakage_risk: medium
frontier_boundary_ok: yes
hypothesis_scope_ok: yes
runtime_claim_boundary_ok: yes
```

---

## 1. Valid new frontier vs F31 inheritance(새 전선 vs 전선31 상속)

**Accepted(수용).** F32는 F31 **상속(inheritance, 상속)** 이 아니라 F31이 스스로 남긴 **다음 전선 제안(next frontier proposal, 다음 전선 제안)** 에 해당합니다.

근거(로컬 대조):

| F31 마감 기록 | F32 제안과의 관계 |
|---|---|
| `executable handoff = 0`, `runtime_probe_out_of_scope_by_claim` | 변경 변수가 바로 이 gap(공백)을 겨냥 |
| negative memory: intrabar/MT5 SL/TP 없이는 runtime/ONNX 주장 불가 | intrabar H/L path proxy(봉내 고저가 경로 프록시)를 **새 검증 축**으로 도입 |
| next hypothesis clue: `executable_sl_tp_mapping...` | stage id·가설이 그 단서와 직접 정렬 |
| `top_executable_mapping_queue.csv` 16행, `executable_gap=requires_intrabar_or_mt5_sl_tp_probe` | 고정 통제 큐로 **참조(reference, 참조)** 만 사용 |

`frontier_governance.md`의 **reference, not inheritance(참조이지 상속 아님)** 와 **runtime representation change(런타임 표현 변경)** 조건을 충족합니다.

- **가져오는 것(허용)**: preserved clue(보존 단서), negative memory(부정 기억), top-16 mapping queue(매핑 큐), entry masks(진입 마스크) — 모두 **고정 통제(fixed control, 고정 통제)** 로 라벨됨.
- **가져오지 않는 것(금지 반입 준수)**: F31 PF 2.45/OOS 2.27을 baseline(기준선)·promotion(승격)·runtime authority(런타임 권위)로 승격하지 않음. F32 success criteria(성공 기준)는 scout PF ≥ 1.05부터 **재측정(re-measurement, 재측정)** 을 요구.

F31B의 16/0 (realistic/executable) 수치도 로컬 CSV와 일치합니다. F31이 “닫힌 뒤 같은 수리 반복”이 아니라 **표현 계층 전환(representation-layer pivot, 표현 계층 전환)** 으로 격상된 케이스입니다.

---

## 2. Runtime claim boundaries(런타임 주장 경계)

**Correct(올바름).** 계층이 F31 negative memory와 정합합니다.

| 단계 | 주장 수준 | F32 설계 |
|---|---|---|
| Scout clue | path-proxy 탐색 단서 | PF ≥ 1.05, DD ≤ 20 — **탐색 라벨** |
| Seed surface | 씨앗 표면 | PF ≥ 1.20 — 여전히 exploration(탐색) |
| Runtime probe **candidate** | 후보 라벨만 | PF ≥ 1.50 + executable representation — **명시적 no runtime authority** |
| MT5 | 금지 게이트 | path proxy → local verification → pre-expensive Grok **이후에만** |

특히 다음 두 줄이 핵심 방어막입니다.

1. F31 negative memory를 F32 **전제(precondition, 전제)** 로 씀 — “intrabar proxy 통과 전 ONNX/runtime 주장 금지”를 반복하지 않고 **실행 순서**로 고정.
2. `runtime_probe_candidate`와 `runtime_authority`를 **이름·임계값·금지 주장** 세 축에서 분리.

Stage id의 `onnx_scout`는 **탐색 라벨(exploration label, 탐색 라벨)** 로만 읽어야 합니다. ONNX readiness(온엑스 준비)는 F32 closeout 전까지 주장 범위 밖으로 유지하는 것이 맞습니다.

---

## 3. Leakage risk(누수 위험) — medium(중간)

경계 설계는 맞지만, **구현·검증 전**에는 medium이 적절합니다.

| 위험 축 | 이유 | 완화 조건 |
|---|---|---|
| Intrabar ordering(봉내 순서) | 동일 봉에서 SL·TP 동시 터치 시 long/short·시가 근접 규칙에 PF/DD가 민감 | 규칙을 spec에 고정·문서화 |
| Train caps → price SL/TP(학습 상한 → 가격 손절익절) | entry 시점 가격 기준 변환만 허용; forward 재튜닝 시 누수 | **train-only parameter source** 고정 유지 |
| Open-to-open alignment(시가-시가 정렬) | 주장은 있으나 아직 실행 전 | F32A 첫 패킷에서 수치 대조 필수 |
| Top-16 queue 재사용 | F31 val/OOS로 선별된 표면 — **매핑 대상 고정**은 OK, forward에서 queue 재랭킹은 누수 | queue frozen(큐 동결) 명시 유지 |

`leakage_risk: low`로 올리려면 alignment check(정렬 점검)와 intrabar tie-break rule(동시 터치 규칙)이 로컬 spec에 박혀 있어야 합니다. Stage **open** 시점에는 medium이 보수적으로 맞습니다.

---

## 4. Hypothesis scope(가설 범위)

**OK.** 한 문장 가설이 명확합니다.

- **Changed variable(변경 변수)**: return-space log caps → fixed price-path SL/TP — 단일 축.
- **Fixed controls(고정 통제)**: top-16 queue, entry masks, fwd12, train-only source — 범위 제한 적절.
- **Success criteria(성공 기준)**: scout / seed / runtime-probe-candidate 3단 — progressive hardening(점진적 경화) 패턴과 일치.

Minor scope note(소규모 범위 주의): 가설 본문은 “some handoff surface(일부 인계 표면)”인데 stage id는 `onnx_scout`까지 담음. F32A spec 작성 시 **primary question = executable SL/TP mapping**, ONNX는 downstream optional branch(하류 선택 분기)로 적어 scope creep(범위 팽창)을 막으면 좋습니다.

---

## 5. Codex local verification checklist(코덱스 로컬 검증 체크리스트)

Stage open(단계 개방)은 **accepted** 가능. 아래는 F32A 첫 work packet(작업 묶음) 전 Codex가 확인할 항목입니다.

1. `bars_us100_m5_mt5api_raw.csv` Bid OHLC vs dataset future return이 **open-to-open** basis로 일치하는지 수치 대조.
2. Intrabar path proxy: long은 low→high 순, short는 high→low 순 등 **tie-break rule** spec 고정.
3. Top-16 queue **frozen** — forward 구간에서 재선별·재튜닝 없음을 ledger에 명시.
4. F31 `f31b_0013` PF 2.45는 **reference anchor(참조 앵커)** 로만 인용; F32 scout threshold(PF ≥ 1.05)와 혼동 금지.

---

## Summary(요약)

F32는 F31 승자·기준선·런타임 권위를 물려받는 **상속이 아니라**, F31이 남긴 executable-gap(실행 가능 공백)을 **runtime representation change(런타임 표현 변경)** 로 격상한 **유효한 새 전선 가설**입니다. Runtime claim boundaries(런타임 주장 경계)는 F31 negative memory와 정합하고, MT5 지연 게이트도 적절합니다. `leakage_risk: medium`은 설계 결함이 아니라 **아직 미검증인 alignment·intrabar 구현 세부**에 대한 보수적 라벨입니다.

**Classification for Codex receipt(코덱스 영수증 분류)**: `accepted` — stage open(단계 개방) 진행 가능; 위 4항목은 F32A 실행 전 `needs_local_verification` 항목으로 closeout에 연결.
