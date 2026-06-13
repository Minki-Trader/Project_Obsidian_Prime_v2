# Sample Weight Plan(표본 가중 계획)

- utility_emphasis(효용 강조): train split(학습 분할)의 favorable excursion(유리 이동)과 realized forward return(전방 수익)을 이용해 깨끗한 방향 행을 더 크게 배웁니다.
- adverse_downweight(불리 이동 하향 가중): label direction(라벨 방향)과 반대되는 MAE(max adverse excursion, 최대 불리 이동)가 큰 행의 가중치를 낮춥니다.
- flat_ambiguity_shaping(평탄 애매함 형성): flat(평탄)이어야 하는 저효용/고위험 행은 더 강하게 flat으로 학습합니다.
- side_balance_path_quality(방향 균형+경로 품질): long/short(롱/숏) 균형은 전역 클래스 사전분포가 아니라 경로 품질 조건부 행 가중으로 맞춥니다.
- local verification(로컬 검증): weight parameters(가중 파라미터)는 train split(학습 분할)에서만 계산하고, validation/OOS(검증/표본밖)는 평가 전용으로 둡니다.
