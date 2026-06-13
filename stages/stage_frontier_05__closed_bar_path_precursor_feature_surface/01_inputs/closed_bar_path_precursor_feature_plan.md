# Closed-Bar Path Precursor Feature Plan(확정봉 경로 선행 피처 계획)

Frontier05B(전선05B)는 current closed bar(현재 확정봉)와 prior closed bars(과거 확정봉)에서만 stage-local features(단계 로컬 피처)를 만듭니다.

Candidate families(후보군):

- wick/body pressure(꼬리/몸통 압력): upper/lower wick share(위/아래 꼬리 비중), body direction persistence(몸통 방향 지속).
- excursion asymmetry(진폭 비대칭): recent high-side versus low-side reach(최근 상방/하방 도달 비대칭).
- volatility compression/expansion(변동성 수축/확장): rolling range percentile(롤링 범위 분위), ATR-relative range(ATR 대비 범위).
- impulse decay(충격 감쇠): recent impulse follow-through versus fade(최근 충격 추종 대비 소멸).
- adverse-tail clustering(불리한 꼬리 군집): repeated opposite-tail pressure(반대 꼬리 압력 반복).

Action(행동): build baseline and augmented feature matrices on identical rows(동일 행에서 기준/증강 피처 행렬 생성). Effect(효과): any improvement(개선)이 label/split drift(라벨/분할 드리프트)가 아니라 feature surface(피처 표면) 변화에서 나온 것인지 확인합니다.

Boundary(경계): these features are stage-local exploratory features(단계 로컬 탐색 피처) and are not foundation/features reusable logic(재사용 피처 로직) until separately promoted by architecture decision(구조 결정).
