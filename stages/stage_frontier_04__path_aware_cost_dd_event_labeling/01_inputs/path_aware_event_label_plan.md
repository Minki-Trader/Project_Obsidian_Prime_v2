# Frontier04 Path-Aware Event Label Plan(전선04 경로 인식 이벤트 라벨 계획)

Frontier04B(전선04B)는 model input timestamp(모델 입력 타임스탬프)를 raw US100 M5 OHLC(원천 US100 5분봉 시가/고가/저가/종가)에 맞춘 뒤, 현재 봉 이후 forward horizon(전방 수평선) 안에서 favorable excursion(유리한 움직임)과 adverse excursion(불리한 움직임)을 계산합니다.

Label variants(라벨 변형)는 target/stop/time-out(목표/손절/시간만료)을 바꾸되, 첫 실행에서는 proxy-only(프록시 전용)로 둡니다.

Effect(효과): close-only future return(종가 전용 미래 수익률)이 숨긴 intra-horizon pain(수평선 내부 고통)을 라벨 단계에서 먼저 제거할 수 있는지 확인합니다.
