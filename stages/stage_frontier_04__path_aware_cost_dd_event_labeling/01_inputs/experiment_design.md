# Frontier04 Experiment Design(전선04 실험 설계)

- hypothesis(가설): Path-aware cost/DD event labels may train an ONNX that avoids close-only validation drawdown failure(경로 인식 비용/손실폭 이벤트 라벨은 종가 전용 검증 손실폭 실패를 피하는 온엑스를 학습시킬 수 있음).
- decision_use(결정 사용): Controls whether Frontier04B proxy scout should run(Frontier04B 프록시 탐색 실행 여부 결정).
- comparison_baseline(비교 기준): Frontier03 preserved clue and negative memory as reference only(전선03 보존 단서와 부정 기억은 참조 전용).
- control_variables(고정 변수): ["US100 M5 FPMarkets dataset(US100 M5 FPMarkets 데이터셋)", "feature_set_v2 fixed 58 feature order(고정 58개 피처 순서)", "time-ordered train/validation/OOS split(시간순 학습/검증/표본밖 분할)", "no ONNX/WFO/MT5 in first proxy scout(첫 프록시 탐색에서 ONNX/WFO/MT5 없음)"]
- changed_variables(변경 변수): ["forward path label using high/low event path(고가/저가 이벤트 경로를 쓰는 전방 경로 라벨)", "target/stop/time-out label variants(목표/손절/시간만료 라벨 변형)", "cost/DD-aware proxy scoring(비용/손실폭 인식 프록시 점수화)"]
- sample_scope(표본 범위): Tier A model input rows plus raw US100 M5 OHLC; Tier B missing_required until a paired source is materialized(Tier A 모델 입력 행과 원천 US100 5분봉 OHLC; Tier B는 쌍 원천 물질화 전 필수 누락).
- success_criteria(성공 기준): ["Grok stage-open accepts or only narrows the direction(그록 단계 개방이 방향을 수용하거나 좁히기만 함)", "Raw OHLC alignment is locally verifiable(원천 OHLC 정렬이 로컬에서 검증 가능)", "Frontier04B has clear proxy-only criteria(Frontier04B에 명확한 프록시 전용 기준 존재)"]
- failure_criteria(실패 기준): ["Grok says direction repeats Frontier03 threshold repair(그록이 전선03 임계값 수리 반복이라고 판단)", "Raw OHLC cannot align to model input timestamps(원천 OHLC가 모델 입력 타임스탬프와 정렬 불가)"]
- invalid_conditions(무효 조건): ["event label uses current/future features as model inputs(이벤트 라벨이 현재/미래 피처를 모델 입력으로 사용)", "timestamp semantics are treated as direct UTC against policy(타임스탬프를 정책과 달리 직접 UTC로 취급)"]
- stop_conditions(중지 조건): ["Frontier04B proxy has zero rows improving density/PF/DD jointly(Frontier04B 프록시에서 밀도/PF/DD 동시 개선 행 0개)", "path labels collapse into sparse PF999 tiny samples(경로 라벨이 희소 PF999 작은 표본으로 접힘)"]
- evidence_plan(근거 계획): ["Grok prompt/output/metadata(그록 프롬프트/출력/메타데이터)", "stage brief, experiment design, input refs(단계 요약/실험 설계/입력 참조)", "run registry and alpha ledgers(실행 등록부와 알파 장부)", "Frontier04B proxy report and manifest(Frontier04B 프록시 보고서와 실행 목록)"]
