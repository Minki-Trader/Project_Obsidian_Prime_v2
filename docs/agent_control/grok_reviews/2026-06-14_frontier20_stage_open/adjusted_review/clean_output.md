**decision:** `adjust` — F20(전선20) stage-open(단계 개방)은 **탐색용 가설 생명주기(exploration hypothesis lifecycle, 탐색 가설 생명주기)** 로는 허용하되, 완성·승격·런타임 주장 경계는 열지 말 것.

**why(이유):**
- F19(전선19) negative_memory(부정 기억)은 ONNX(온엑스) 유효성이 아니라 **strict/seed/preserved/handoff(엄격/씨앗/보존/인계) 생명주기 행 전멸**이 핵심 실패라, F20의 train-only rule atlas(학습 전용 규칙 지도) + no-threshold(무임계값) + no-boosted-backbone(부스팅 백본 없음) 축은 **반복 금지(do-not-repeat, 반복 금지)를 피한 의미 있는 축 전환**이다.
- pre-open probe(개방 전 탐침)의 validation/OOS PF(검증/표본외 수익 팩터)는 **seed surface(씨앗 표면)** 수준의 탐색 동기만 주며, high DD(큰 손실폭) 때문에 **accept-as-completion(완성으로 수용)** 근거는 아니다.
- F18 lifecycle repair(생명주기 수리) 실패 이력과 맞게, F20이 repair(수리) 없이 scout(정찰)만 한다는 설계는 맞지만, 그래서 **운영 생명주기(operating lifecycle, 운영 생명주기) 개방 주장은 금지**해야 한다.

**mandatory locks(필수 잠금):**
- **58 contract features only(58 계약 피처만)**, fixed train quantiles(고정 학습 분위수), **max depth 2(결합 깊이 2)**, **train-only side(방향 학습 전용)**, **validation/OOS read-only(검증/표본외 읽기 전용)** — 범위 밖 확장 금지.
- **no new feature engineering(새 피처 설계 없음)**, **no probability thresholds(확률 임계값 없음)**, **no boosted backbone(부스팅 백본 없음)**, **no lifecycle/quota/firewall repair(생명주기/할당량/방화벽 수리 없음)** — F05/F15/F16/F18/F19 재시도 금지.
- ONNX encode/distill(온엑스 인코딩/증류)는 **surviving surface(생존 표면) 이후 후행 단계**로만; F20 open(개방) 자체를 ONNX 성공으로 해석 금지.
- probe 결과는 **in-memory only(메모리 내 전용)**; F20A 첫 run(첫 실행) 전 **재현 가능한 stage-local evidence(단계 로컬 근거)** 없이 carry-forward(이월) 금지.

**local verification before F20A(전선20A 전 로컬 검증):**
- F20 packet(작업 묶음)에 **Tier A separate / Tier B separate / Tier A+B combined(티어 A 분리·티어 B 분리·합산)** 기록 슬롯이 실제로 열려 있는지 확인.
- train-only quantile fitting(학습 전용 분위수 적합)이 **validation/OOS leakage-free(검증/표본외 누수 없음)** 인지, side selection(방향 선택)이 train partition(학습 구간)에만 묶였는지 확인.
- rule atlas(규칙 지도)에 **density(빈도), PF, DD, trade count(거래 수)** 를 validation/OOS 각각 분리 기록하고, probe의 `vix_zscore_20 <= q30` + momentum pairs(모멘텀 쌍)를 **첫 재현 대조선(replication control, 재현 대조선)** 으로만 사용.
- F20A closeout(종료 기록)은 **strict/seed/preserved/handoff row counts(엄격/씨앗/보존/인계 행 수)** 를 F19와 동일 기준으로 먼저 집계; 0/0/0/0이면 **negative_memory continuation(부정 기억 연속)** 으로 닫기.

**forbidden claims(금지 주장):**
- completion / baseline / promotion / runtime authority / live readiness / Goal Achieve(완성·기준선·승격·런타임 권위·실거래 준비·목표 달성).
- probe PF 1.2~1.4를 **positive alpha(긍정 알파)** 또는 **promotion candidate(승격 후보)** 로 승격.
- valid ONNX 4/4 또는 later ONNX scout(추후 온엑스 정찰)를 **handoff-ready(인계 준비 완료)** 로 해석.
- high DD(큰 손실폭)를 “나중에 threshold/repair로 해결” 전제로 **F15/F16/F18 재개 명분**으로 사용.
