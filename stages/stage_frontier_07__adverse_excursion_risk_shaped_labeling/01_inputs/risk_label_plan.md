# Risk-Shaped Label Plan(위험 형성 라벨 계획)

Frontier07B(전선07B)는 raw path(원천 경로)에서 아래 broad variants(넓은 변형)를 먼저 만듭니다.

- MAE cap(최대 불리 이동 상한): entry 후 허용되는 adverse excursion(불리한 이동)을 제한합니다.
- MFE target(최대 유리 이동 목표): favorable excursion(유리한 이동)이 비용과 스프레드를 넘는지 봅니다.
- recovery window(회복 창): 초반 불리한 이동 후 회복되는 표본과 계속 손실나는 표본을 분리합니다.
- time-to-adverse penalty(불리 이동까지 시간 벌점): 빠른 손실 진입을 더 강하게 벌점화합니다.
- side-asymmetric risk(방향 비대칭 위험): long/short(롱/숏) 손실 구조가 다른지 분리합니다.

Action(행동): label(라벨)은 미래 경로를 쓸 수 있지만 feature(피처)는 현재/과거 확정 입력만 씁니다. Effect(효과): 학습 목표와 런타임 입력 경계를 분리해 leakage(누수)를 막습니다.

Frontier07B required bounds(전선07B 필수 경계):

- fixed feature_set_v2 input(고정 피처 세트 v2 입력)과 small ONNX-exportable model family(작은 온엑스 내보내기 가능 모델군)를 쓴다.
- scout signal(탐색 신호)은 argmax-only(최대확률 전용)로 시작하고, F06-style abstention threshold search(전선06식 기권 임계값 탐색)는 하지 않는다.
- comparison references(비교 참조)는 label_v1 argmax(label_v1 최대확률), F04 locked path trainable reference(F04 고정 경로 학습 참조), F06 best selective reference(F06 최선 선택 참조)로 둔다.
- each label family(각 라벨군)는 F04 event-label semantics(F04 이벤트 라벨 의미)와 다른 점을 한 줄로 적는다.
- report learnability first(학습 가능성 우선 보고): class balance(클래스 균형), train-to-validation separability(학습-검증 분리도), ONNX parity(온엑스 동등성), transfer gap(전달 격차).
- DD-only improvement(손실폭만 개선)는 strict scout clue(엄격 탐색 단서)가 아니라 preserved clue(보존 단서)로만 둔다.
