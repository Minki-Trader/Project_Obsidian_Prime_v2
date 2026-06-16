# F70 Stage Open Review(F70 단계 개방 검토)

You are Grok(Grok, 그록), external second opinion(외부 2차 의견). Answer only from this bounded snapshot(제한 스냅샷). Do not inspect files(파일 확인 금지), run tools(도구 실행 금지), browse(브라우징 금지), or claim local verification(로컬 검증 주장 금지).

## Current Truth(현재 진실)

- Project(프로젝트): Project Obsidian Prime v2, FPMarkets US100 M5(US100 5분봉).
- Goal(목표): eventually build one strong ONNX(온엑스) with 5-10 trades/day(일 5-10회 거래), PF 2-3+(수익 팩터 2-3 이상), DD <10%(손실폭 10% 미만), smooth upward equity(매끄러운 우상향 자산 곡선).
- Final gates(최종 게이트)는 final completion review(최종 완성 검토)에서만 hard gate(강제 게이트)다. Stage open(단계 개방)은 exploration only(탐색 전용)다.
- F69 closeout label(마감 라벨): preserved clue + negative memory, no authority(보존 단서 + 부정 기억, 권위 없음).
- F69 preserved clue(보존 단서): ONNX/probability/signal/feature parity(온엑스/확률/신호/피처 동등성)는 exact(정확)했고 RuntimeVetoTape(런타임 차단 테이프)는 observation bridge(관찰 연결)로 유효했다.
- F69 negative memory(부정 기억): event-first ExtraTrees trade-shape-only repair(이벤트 우선 엑스트라트리스 거래 형태 단독 수리)는 density/PF/DD(밀도/수익 팩터/손실폭)를 동시에 맞추지 못했다.
- F69D runtime observation(런타임 관찰): sparse OOS(희박 표본외) PF 2.94, DD 1.52%, trades/day 0.0359; dense OOS(조밀 표본외) PF 1.19, DD 7.49%, trades/day 1.3385.
- F69E repair sweep(수리 탐색): 650 rows(650행), final-like rows(최종 조건 유사 행) 0, joint-soft rows(완화 공동 행) 0.
- Five-stage retrospective(5단계 중간 검토): not due(아직 아님), 4/5 after F69 closeout(F69 마감 후 4/5).

## Codex Proposed Direction(Codex 제안 방향)

Open `stage_frontier_70__regime_specific_asymmetric_value_exit_model_rotation`.

Hypothesis(가설): regime/session-specific asymmetric value and exit labels(장세/세션별 비대칭 가치 및 청산 라벨)이 density objective(밀도 목표)를 label/selection(라벨/선택)에 내장하고 model family(모델 계열)를 linear/EBM-like/small NN/ExtraTrees-light(선형/EBM 유사/작은 신경망/가벼운 엑스트라트리스)로 회전하면, F69의 sparse-PF vs dense-weak split(희박 고PF 대 조밀 저PF 분리)을 넘는 new PF source(새 수익 팩터 원천)를 만들 수 있다.

Planned changed variables(변경 변수):

- feature set(피처 묶음): regime/session compact features(장세/세션 압축 피처), exit-path features(청산 경로 피처), and ablations(소거).
- label/target(라벨/목표): asymmetric value labels(비대칭 가치 라벨), exit-survival labels(청산 생존 라벨), density-aware labels(밀도 인식 라벨).
- model family(모델 계열): regularized linear(정규화 선형), EBM-like additive trees(EBM 유사 가법 트리), small NN(작은 신경망), shallow ExtraTrees as reference only(얕은 엑스트라트리스 참조 전용).
- trade shape(거래 형태): fixed-hold vs exit-triggered hold(고정 보유 대 청산 트리거 보유), long/short asymmetric routing(롱/숏 비대칭 라우팅).
- risk logic(위험 로직): fixed SL/TP envelope(고정 손절/익절 봉투) only as runtime-compatible envelope(런타임 호환 봉투), not post-hoc rescue(사후 구제 아님).
- regime/session split(장세/세션 분할): cash open/mid/late/outside(정규장 초반/중반/후반/외부), trend/chop/vol expansion/squeeze(추세/횡보/변동성 확장/압축).

Controls(고정 조건):

- US100 M5(US100 5분봉), split_v1(분할 v1), no inherited winner/baseline/promotion/runtime authority(승자/기준선/승격/런타임 권위 상속 없음).
- If proxy signal(프록시 신호)이 meaningful(의미 있음)이면 mandatory MT5 Runtime Probe(필수 MT5 런타임 탐침)로 materialize(물질화).
- Do not repeat F69 threshold/cooldown/daily quota repair loop(F69 임계값/쿨다운/일별 할당 수리 반복 금지).

## Review Questions(검토 질문)

1. Is this F70 hypothesis(가설) genuinely new enough after F69, or is it disguised trade-shape-only repair(거래 형태 단독 수리 위장) again?
2. Which axis should be the first proxy scout(첫 프록시 탐색) priority: label/target(라벨/목표), model family(모델 계열), regime/session split(장세/세션 분할), or exit shape(청산 형태)?
3. What failure condition(실패 조건) should force Codex to close F70 as negative memory(부정 기억) rather than keep repairing?

Allowed claims(허용 주장): scout clue(탐색 단서), seed surface(씨앗 표면), runtime probe observation(런타임 탐침 관찰).

Forbidden claims(금지 주장): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성).
