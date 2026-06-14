Grok 외부 2차 검토로 답하기 전에, 협업 스킬과 F18·F19 관련 제한 근거를 먼저 확인합니다.
**Classification:** `needs_local_verification`

F19는 **모델 계열(model family, 모델 계열) 축**으로는 새 전선 가설 생명주기(frontier hypothesis lifecycle, 전선 가설 생명주기)에 가깝습니다. F15–F18(전선15–18)은 모두 `lr_plain` 위에 threshold/veto/firewall/lifecycle 수리(repair, 수리)를 쌓았고, F18은 lifecycle 수리까지 0/0/0으로 닫혔습니다. 그래서 “얕은 모델 한계”를 다음 1차 변수로 바꾸는 건 방향 자체는 타당합니다.

다만 **“boosted tree + temporal stability selection(시간 안정성 선택)”**을 한 묶음으로 열면, 이미 실패한 수리 축을 다시 섞는 형태에 가깝습니다. F11(전선11)은 subperiod stability-first selection(하위기간 안정성 우선 선택)이 aggregate top(합계 최상위)을 바꾸지 못했고 DD floor(손실폭 바닥)도 못 깼다는 negative memory(부정 기억)로 닫혔습니다. Archive Stage17/18(17/18단계)도 XGBoost/CatBoost를 이미 시험했습니다. 그래서 “새 가설”이라기보다 **실패한 선택기 + 실패한 스캐폴드(ONNX scout ladder, ONNX 탐색 사다리) + 다른 백본** 조합으로 보일 수 있고, F19A stage-open 전에 novelty_delta(신규성 차이)와 do_not_repeat(반복 금지)를 문서로 고정하지 않으면 F19B는 invalid setup(무효 설정) 위험이 큽니다.

또 F17/F18 실패는 shallow-model(얕은 모델) 단독 실패로 읽기 어렵습니다. F17 proxy는 validation PF ~1.30까지 갔지만 MT5 DD가 붕괴했고, F18은 DD는 낮지만 OOS PF ~1.0입니다. 즉 bottleneck(병목)이 **신호 품질·실행 경제성(signal quality / execution economics, 신호 품질·실행 경제성)** 쪽일 수 있어, boosted tree만으로 PF/density/DD/smoothness를 동시에 올린다는 가설은 아직 검증 전 주장입니다.

**Key risks:**
- **Repair stacking(수리 중첩):** F11 stability selection 실패 + F15–F18 execution-overlay 실패를 한 패킷에 다시 넣으면, novelty 없는 repair loop(수리 반복)로 보일 수 있음.
- **Misread failure mode(실패 원인 오독):** F17/F18은 proxy PF ceiling(프록시 PF 상한)과 MT5/OOS 지속성 문제가 핵심인데, shallow→boosted 전환만으로는 같은 0/0/0 마감이 반복될 수 있음.
- **Hidden tuning surface(숨은 튜닝 면):** “train-only temporal stability selection”이 사전 등록 없이 들어가면 validation/OOS threshold fishing(검증·표본외 임계값 낚시) 변형이 될 수 있음.

**Required locks before F19B:**
- **Primary-variable lock(1차 변수 고정):** 작은 XGBoost/CatBoost variant grid(변형 격자)를 hyperparam cap(하이퍼파라미터 상한)과 후보 수 상한까지 **metrics 전에** 고정하고, F11 + Stage17/18 + F15–F18을 `prior_stage_scan` / `do_not_repeat`에 명시.
- **Stability contract lock(안정성 계약 고정):** subperiod 정의, stability score(안정성 점수), tie-break, train-only selection rule(학습 전용 선택 규칙)을 고정. validation/OOS로 selector를 바꾸지 않음. F11처럼 “기존 후보 재선택만”이면 1차 가설이 아니라는 점을 문서에 적을 것.
- **Execution-surface lock(실행 표면 고정):** F18식 3-profile lifecycle sweep(생명주기 스윕) 금지. 단일 entry/exit policy(단일 진입·청산 정책), fixed 58-feature order(고정 58피처 순서), `[p_short,p_flat,p_long]` ONNX parity gate(ONNX 동등성 게이트), Tier A / Tier B / Tier A+B 또는 `missing_required` 기록 의무를 F19B 전에 박아 둘 것.

**Codex follow-up:** F19A stage-open 문서에 `novelty_delta = model-family backbone change only` vs `stability selector = bounded tie-break only`를 분리해 적고, 그다음 Grok small review(소규모 검토)를 한 번 더 받는 편이 안전합니다.
