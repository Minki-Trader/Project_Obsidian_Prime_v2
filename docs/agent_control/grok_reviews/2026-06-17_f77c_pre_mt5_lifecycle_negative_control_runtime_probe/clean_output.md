## Grok Review Classification(그록 검토 분류)

**`accepted_with_conditions` (조건부 수용)**

F77D는 **lifecycle execution path(생명주기 실행 경로)** 를 좁게 보려는 **negative-control style probe(부정 대조형 탐침)** 로 방향은 맞다. 다만 **그대로 실행하면 안 되고**, materialization(물질화)을 먼저 조정·고정한 뒤에만 진행해야 한다.

핵심 이유:
- F77B **best proxy(최선 프록시)** `f77b_08051`(HistGBM)과 F77D **실제 probe target(탐침 대상)** `f77b_07979`(ExtraTrees)가 **다른 후보**다. export constraint(보내기 제약)만으로 rank-3로 바꾸는 건 허용 가능하지만, **“best proxy MT5 check”가 아니라 “exportable surrogate probe”** 로 claim boundary(주장 경계)를 낮춰야 한다.
- `selected-entry runtime veto tape(선택 진입 런타임 거부 테이프)` 는 **signal-count parity(신호 수 일치)** 를 강제하므로, 이번 probe는 **model inference parity(모델 추론 동등성)** 검증이 아니라 **lifecycle trade mechanics parity(생명주기 거래 메커니즘 동등성)** 검증에 가깝다. 그건 F77C pre-MT5 review(사전 MT5 검토) 범위 안에서는 타당하다.
- F77B에서 **meaningful signal count = 0(의미 신호 0)** 인 상태라, F77D 성공·실패 모두 **exploratory negative control(탐색용 부정 대조)** 로만 읽어야 한다.

---

## 1. Top Proxy/Runtime Gap Risks(최상위 프록시/런타임 간극 위험)

1. **Candidate substitution gap(후보 대체 간극)**
   HistGBM → ExtraTrees 전환으로 val/OOS profile(검증/표본외 프로필)이 크게 달라진다. val DD 0.53→1.48, OOS net 127→61, trades 29→34 축. **gap cause(간극 원인)** 이 lifecycle label(생명주기 라벨)인지 **model-family swap(모델군 교체)** 인지 분리되지 않는다.

2. **Forced-timestamp masking(강제 시각 마스킹)**
   veto tape(거부 테이프)가 ONNX threshold drift(온엑스 임계값 드리프트), feature lag(피처 지연), rank-threshold mismatch(순위 임계값 불일치)를 가린다. MT5가 좋아도 **inference works(추론 동작)** 를 말할 수 없고, 나빠도 **execution-only failure(실행만 실패)** 인지 **label/path mismatch(라벨/경로 불일치)** 인지 구분이 어렵다.

3. **Entry timing semantics(진입 시각 의미)**
   `closed-bar key + next-bar open entry(닫힌 봉 키 + 다음 봉 시가 진입)` 는 proxy(프록시)와 MT5 bar indexing(봉 인덱싱), tick vs open fill(틱 vs 시가 체결), spread at open(시가 스프레드)에서 어긋나기 쉽다.

4. **Trade-shape clamps(거래 형태 고정)**
   `h12 / TP18 / SL12 / short-only` 는 축과 맞지만, ATR min=max clamp(최소=최대 고정), max-hold bar count(최대 보유 봉 수), partial fill, SL/TP touch order(손절/익절 접촉 순서)가 Python lifecycle simulator(파이썬 생명주기 시뮬레이터)와 tester modeling(테스터 모델링)에서 다르면 KPI gap(핵심 성과 지표 간극) 이 커진다.

5. **Threshold-margin with synthetic long column(합성 롱 열 + 임계값-마진)**
   `[p_short, p_flat, p_long=0]` + `long_threshold=1.1`, `min_margin=-1.0` 는 short-only(숏 전용) 의도는 분명하지만, EA decision path(전문가자문 결정 경로)가 training-time quantile rank(학습 시점 분위수 순위)와 다른 **absolute score scale(절대 점수 스케일)** 을 쓰면 proxy threshold(프록시 임계값) 이식이 깨진다.

6. **Low OOS sample(표본외 표본 부족)**
   `f77b_07979` OOS trades=34 는 F77B meaningful gate(의미 신호 게이트) 아래다. MT5 mismatch(불일치) 하나가 통계적으로 과대해석되기 쉽다.

---

## 2. Required Local Verification Before Execution(실행 전 필수 로컬 검증)

Codex가 Grok 답변 후 **로컬에서** 반드시 확인해야 할 것:

| Priority | Check | Pass criterion |
|----------|-------|----------------|
| P0 | **Retrained model ONNX export(재학습 모델 온엑스보내기)** | smoke test(연기 테스트)가 아니라 **f77b_07979 동일 축 재학습 가중치** export OK |
| P0 | **Probe identity receipt(탐침 정체성 영수증)** | F77D 문서에 `surrogate_of=f77b_07979`, `not_equal_to=f77b_08051`, `reason=hist_gbm_onnx_export_failed` 명시 |
| P0 | **Veto tape audit(거부 테이프 감사)** | proxy selected timestamps(프록시 선택 시각) count/hash == MT5 post-threshold admitted entries(임계값 적용 후 허용 진입) |
| P1 | **Feature parity(피처 동등성)** | closed-bar feature timestamp(닫힌 봉 피처 시각) EA 계산 == Python materialization hash(파이썬 물질화 해시) |
| P1 | **ONNX I/O contract(온엑스 입출력 계약)** | 3-column order, dtype, opset, EA loader interpretation 일치 |
| P1 | **Threshold transplant(임계값 이식)** | `short_threshold=proxy_threshold-epsilon` 의 epsilon 고정값·근거 기록; rank vs probability 혼동 없음 |
| P1 | **Tester forensics preset(테스터 포렌식 프리셋)** | US100 M5 spread/commission/slippage/modeling mode가 proxy assumptions(프록시 가정)와 boundary-labeled compare(경계 라벨 비교) 가능 |
| P2 | **HistGBM export failure scope(히스토그램 부스팅보내기 실패 범위)** | 환경 고정 이슈인지, tree count/depth 이슈인지 분류. F77D blocker(차단 요소)는 아니지만 repair log(수리 기록) 남김 |

**실행 go/no-go(진행 여부):** P0 전부 통과 시에만 F77D 실행. P1 하나라도 fail이면 **adjust materialization(물질화 조정)** 후 재시도.

---

## 3. Forbidden Claim Risks(금지 주장 위험)

| Risk | Why forbidden under current boundary |
|------|--------------------------------------|
| **“F77B best proxy validated in MT5”** | 실제 probe는 rank-3 ExtraTrees surrogate(대리 후보) |
| **“Lifecycle labels reduce proxy/runtime gap”** | veto tape가 gap의 상당 부분을 인위적으로 제거 |
| **“Meaningful signal found”** | F77B meaningful=0; OOS n=34 still below gate |
| **promotion_candidate / runtime_probe success** | single negative-control attempt(단일 부정 대조 시도) 는 승격·런타임 권위 근거가 아님 |
| **baseline / operating promotion** | explicit forbidden in claim boundary |
| **probability-calibrated edge(확률 보정 엣지)** | calibration risk already `selection ranks only(순위 선택만)` |
| **Goal Achieve / live readiness** | MT5 val+oos 한 번으로 금지 |

안전한 allowed claim(허용 주장) 예:
> “Under forced signal parity, lifecycle short trade mechanics showed [aligned / partial gap / clear divergence] between proxy and MT5 on f77b_07979 axes.”

---

## 4. Smallest Useful MT5 Probe Scope(가장 작은 유용한 MT5 탐침 범위)

**Minimum sufficient packet(최소 충분 묶음):**

- **One candidate only:** `f77b_07979`
- **One direction only:** short-only
- **One bundle only:** retrained ExtraTrees ONNX + one `run_manifest.json` / `.set`
- **One parity mode only:** veto tape ON (이번 probe의 negative control 핵심)
- **One period first:** **validation window only**
  - OOS는 val에서 **directional gap sign(간극 방향 부호)** 이 보일 때만追加
- **One tier:** 가장 좁은 usable tier 하나 (가능하면 Tier A; blocked면 boundary-labeled Tier B, combined는 이번 probe에 불필요)
- **KPI compare set(비교 지표 묶음):** trades count, net, PF, max DD, avg hold bars, TP-first vs SL-first ratio
  - proxy lifecycle trades **on same vetoed timestamps only(동일 거부 시각만)**

**Explicitly out of scope for smallest probe(최소 탐침에서 제외):**
- multi-candidate sweep(다중 후보 스윕)
- HistGBM retry unless export path fixed in same packet
- veto tape OFF ablation (두 번째 packet으로 미룸)
- Tier A+B combined promotion read

---

## Final Codex Direction(최종 Codex 방향)

**Proceed F77D, but not “as proposed” verbatim(제안 그대로가 아니라 조건부 진행).**

필수 조정:
1. Probe label을 **“exportable surrogate lifecycle execution probe”** 로 rename/clarify
2. P0 local verification 완료 후 실행
3. 결과는 **gap taxonomy(간극 분류)** 로만 보고: `execution_aligned`, `execution_diverged`, `inconclusive_low_n`
4. HistGBM export failure는 **parallel repair track(병렬 수리 트랙)** 으로 남기되 F77D blocker로 승격하지 말 것

**Advice classification(조언 분류): `accepted_with_conditions` (조건부 수용)**
