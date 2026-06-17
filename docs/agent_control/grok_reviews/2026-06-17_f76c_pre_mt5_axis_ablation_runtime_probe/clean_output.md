## Advice Classification(조언 분류)

**`accepted_with_conditions` (조건부 수용)**

방향은 맞다. F76D는 **좁은 parity probe(좁은 동등성 탐침)** 로 설계됐고, 프록시 거래 형태(max hold 12, long-only, 초기 SL/TP 없음)와 맞추려는 의도도 일관된다.
다만 이 스냅샷만으로는 **재학습 모델 ↔ 스카우트 후보(f76b_06637) ↔ ONNX ↔ EA threshold_margin ↔ veto tape(거부 테이프)** 연결이 실제로 닫혔다고 말할 수 없다. **이름 붙인 로컬 검증(named local checks, 이름 붙인 로컬 검증)** 없이 바로 실행하면 프록시/런타임 간극을 MT5 결과로 오해할 위험이 크다.

**`rejected`(거절)는 아님** — 제안 매핑이 논리적으로 불가능해 보이지는 않는다.
**`accepted`(수용)도 아님** — materialization(물질화) 쪽 확인 공백이 크다.

---

## 1. Top Proxy/Runtime Gap Risks(최상위 프록시/런타임 간극 위험)

1. **Re-train drift(재학습 드리프트)**
   제안은 train split(학습 분할)에서 ExtraTrees를 **다시 학습**한다. 스냅샷의 최선 후보는 `80/80 fit completed` 그리드의 `f76b_06637`이다. 재학습이 동일 가중치/확률 분포를 재현하지 않으면 `threshold=0.5144632153473251`이 무의미해지고, val/OOS 거래 수(`194`/`154`)와도 어긋날 수 있다.

2. **Single-candidate axis illusion(단일 후보 축 착시)**
   `f76b_06637`이 `mega_cap_removed`, `long_fwd12_q60`, `extra_trees_d7_l60`, `cash_open`, `trend_aligned`에서 모두 best(최선)로 보인다. 이건 **다축 독립 확인(multi-axis independent confirmation, 다축 독립 확인)** 이 아니라 **한 설정이 여러 축 라벨에 반복 등장**한 형태일 수 있다. MT5에서 한 번만 맞아도 “축 발견 성공”으로 읽기 쉽다.

3. **Veto tape completeness(거부 테이프 완전성)**
   `cash_open` + `trend_aligned` + 확률 임계값을 veto tape(거부 테이프)로 맞추겠다는 설계는 맞다. 다만 스냅샷은 tape가 **프록시의 trend_aligned 정의**와 **세션 경계**를 1:1로 담는지 증명하지 않는다. 여기서 어긋나면 “신호 수 일치” 주장 자체가 깨진다.

4. **ONNX 3-column semantics(3열 의미)**
   `[p_short=0, p_flat=P(non-long), p_long=P(long)]`는 long-only(롱 전용) 표면으로는 합리적이다. 그러나 EA의 `threshold_margin`이 **어느 열/조합**을 쓰는지, `P(non-long)`이 proxy의 “롱 아님” 정의와 같은지 스냅샷에 없다. 열 해석 하나만 틀려도 진입 타이밍이 바뀐다.

5. **Threshold_margin epsilon(임계값 마진 엡실론)**
   `long_threshold = proxy_prob_threshold - epsilon`은 거래 수를 민감하게 움직인다. proxy는 `quantile 0.8` 기반 임계값인데, MT5에서 epsilon이 proxy 분위수 선택과 동등한지 불명확하다. **tpd(일거래 수)** 가 `~1.06` / `~1.18`에서 크게 벗어나면 probe는 실패에 가깝다.

6. **Friction and tester economics(마찰/테스터 경제성)**
   Proxy KPI는 PF 1.59/1.69, DD ~6–8%로 괜찮아 보인다. MT5 Strategy Tester(전략 테스터)의 spread/commission/slippage(스프레드/수수료/슬리피지)가 proxy에 없으면, **경제성 병목 검증 전에 마찰 병목**으로 false negative(거짓 음성)가 날 수 있다.

7. **Sparse “meaningful” signal(희소 의미 신호)**
   `meaningful signal count = 10` / `scout clue count = 2091` / `7680 candidates`다. 통계적으로 얇은 후보라서, MT5에서 약간의 parity miss도 “경제성 없음”처럼 보이기 쉽다.

---

## 2. Required Local Verification Before Execution(실행 전 필수 로컬 검증)

Codex가 MT5를 돌리기 **직전**에 아래를 통과해야 한다.

| Check(검증) | Pass criterion(통과 기준) |
|---|---|
| **Feature parity(피처 동등성)** | `mega_cap_removed` 48-feature manifest(목록)의 **순서·이름·해시**가 재학습/ONNX/EA 입력과 동일 |
| **Label parity(라벨 동등성)** | `future_log_return_12 > train_q60`의 **train_q60 값**이 f76b_06637 scout와 동일 소스/동일 split에서 계산됨 |
| **Model replay(모델 재현)** | 재학습 모델로 proxy replay 시 val/OOS **거래 수·진입 시각**이 `194`/`154`에 근접(사전 정의 허용 오차 내) |
| **Probability threshold(확률 임계값)** | `0.5144632153473251`이 **재학습 모델 출력**에서 재현되는 분위수 임계값임을 확인 |
| **ONNX contract(ONNX 계약)** | 3열 출력 순서·스케일·합/정규화 규칙이 EA 문서와 일치; 샘플 바 spot check(점검) |
| **Veto tape count(거부 테이프 건수)** | val/OOS 각각 proxy selected timestamps(선택 시각) 수 = runtime veto 통과 후 예상 진입 수 |
| **Session `cash_open`(세션)** | proxy `cash_open` 시간창 = MT5/session filter 정의 일치 |
| **`trend_aligned` risk filter** | tape 또는 runtime gate가 proxy 정의와 동일; 별도 축 요약 수치와 모순 없음 |
| **EA decision mode(판단 모드)** | `threshold_margin`에서 `short_threshold=1.1`, `min_margin=-1.0`이 **long-only 차단** 의도와 실제 동작 일치 |
| **Trade shape(거래 형태)** | max hold 12 M5, no ATR SL/TP, long-only가 tester 설정/EA 로직에 반영됨 |
| **Friction disclosure(마찰 공개)** | tester spread/commission/slippage가 기록되고 proxy 비교 시 분리 해석 가능 |

**하나라도 실패하면:** MT5 실행은 **parity repair(동등성 수리)** 후로 미루고, 결과로 axis/economics 주장하지 말 것.

---

## 3. Forbidden Claim Risks(금지 주장 위험)

claim boundary(주장 경계)가 `pre_mt5_review_only...`이므로, 아래는 **F76D에서도 금지**다.

1. **Runtime authority / live readiness(런타임 권위/실거래 준비)**
   OOS PF 1.69, win 61.7%는 proxy 증거일 뿐이다. MT5 1회 probe로 실거래 준비 주장하면 바로 경계 위반.

2. **Baseline / promotion(기준선/승격)**
   `f76b_06637`이 여러 축 best라도 **selected baseline(선택 기준선)** 이나 **promotion candidate(승격 후보)** 로 올리면 안 된다. meaningful=10은 탐색 단서지 승격 근거가 아니다.

3. **“Axis discovery validated”(축 발견 검증됨)**
   MT5가 PF>1이면 “source axis 식별 성공”처럼 말하기 쉽다. F76 가설은 **식별 가능성 테스트**이지 **식별 완료**가 아니다.

4. **Completion / Goal Achieve(완성/목표 달성)**
   val+OOS tester run을 끝냈다고 stage completion(단계 완성)이나 Goal Achieve로 닫으면 안 된다.

5. **Negative overreach(부정 과장)**
   반대로 MT5 mismatch 시 “mega_cap_removed / cash_open / trend_aligned 축 실패”처럼 **단일 축 사망**으로 쓰면 안 된다. 먼저 materialization failure(물질화 실패) vs economics failure(경제성 실패)를 분리해야 한다.

---

## 4. Smallest Useful MT5 Probe Scope(가장 작은 유용한 MT5 탐침 범위)

**최소 유용 범위(minimal useful scope, 최소 유용 범위):**

- **Single candidate only(단일 후보만):** `f76b_06637` 하나
- **Single window first(단일 구간 우선):** **validation split만** 먼저
  - 이유: 거래 수 `194`, tpd `~1.06`으로 **신호 수 parity(신호 수 동등성)** 판정이 더 빠름
- **Single direction/model surface(단일 방향/모델 표면):** long-only ExtraTrees, `mega_cap_removed` 48f
- **Single trade shape(단일 거래 형태):** max hold 12, no ATR SL/TP
- **No MT5 ablation grid( MT5 축 제거 그리드 없음):** 축 비교는 F76B proxy에서 이미 했음
- **Success criterion for this micro-probe(이 미세 탐침의 성공 기준):**
  - runtime selected entry count(런타임 선택 진입 수) ≈ proxy val count
  - direction/hold semantics(방향/보유 의미) 불일치 없음
  - PF/net은 **2차 지표(secondary KPI, 2차 지표)** — parity 먼저, 경제성은 그다음

**validation parity가 닫힌 뒤에만** OOS window(표본외 구간)를 같은 설정으로 한 번 더 돌릴 것.

---

## Direct Answer to Focus Question(집중 질문에 대한 직접 답)

**Proceed(진행):** 예, **조건부로** F76D narrow MT5 Runtime Probe(좁은 MT5 런타임 탐침)를 진행해도 된다.
**Adjust before execution(실행 전 조정):** 예, materialization(물질화)을 아래처럼 좁혀라.

1. **Two-phase execution(2단계 실행):** val-only parity probe → 통과 시 OOS
2. **Freeze parity contract(동등성 계약 고정):** 재학습 모델이 proxy replay를 통과하기 전에는 ONNX/MT5 금지
3. **Explicit failure taxonomy(실패 분류 명시):** mismatch 시 `materialization_fail` vs `economics_fail` 라벨 분리
4. **Do not widen scope(범위 확장 금지):** 다른 feature_set, session, model, 또는 short 축을 이번 MT5에 넣지 말 것

**Bottom line(요약):** 제안된 F76D는 **올바른 다음 단계**이지만, **“as proposed full val+OOS 즉시 실행”** 보다 **“val-only parity-closed materialization 후 OOS”** 가 이 스냅샷에 더 맞다.
Grok 조언은 **조건부 수용**이며, 최종 실행 여부와 주장 강도는 Codex 로컬 검증이 결정한다.
