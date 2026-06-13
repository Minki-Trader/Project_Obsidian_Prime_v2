# Proxy Score Plan(프록시 점수 계획)

This plan(이 계획)은 first scout(첫 탐색)가 final target(최종 목표)을 hard gate(강제 게이트)로 오해하지 않게 하는 score contract(점수 계약)이다.

## Design Rule(설계 규칙)

Frontier 02(전선 02)의 novelty_delta(신규성 차이)는 evaluation-time joint gate(평가 시점 동시 게이트)가 아니라 proxy/training/selection-time joint objective(프록시/학습/선택 시점 동시 목적)다.

Effect(효과): 후보를 나중에 걸러내기만 하는 것이 아니라, 처음부터 density/PF/DD/smoothness(밀도/수익 팩터/손실폭/매끄러움)를 동시에 덜 망가뜨리는 표면을 찾는다.

## Four Axes(네 축)

1. Density distance(밀도 거리): 5~10 trades/day(일 5~10회 거래)에 가까운지 본다. Scout(탐색)에서는 미달을 invalid(무효)로 보지 않고 distance penalty(거리 벌점)로 둔다.
2. PF distance(수익 팩터 거리): PF 2~3+(수익 팩터 2~3 이상)에 가까운지 본다. Tiny trade count(얇은 거래 수)에서 생긴 PF999(PF999)는 sparse penalty(희소 벌점)를 받는다.
3. DD distance(손실폭 거리): full split(전체 분할)과 zoomed segment(확대 구간)의 max drawdown(최대 손실폭)을 함께 벌점화한다.
4. Curve smoothness distance(곡선 매끄러움 거리): equity curve(자산 곡선)의 long flatline(긴 정체), loss cluster(손실 군집), time under water(회복 전 체류 시간)를 벌점화한다.

## Scout Score(탐색 점수)

`aspiration_distance_score(목표 거리 점수)`는 네 축 벌점을 합친다.

Allowed use(허용 사용): compare scout surfaces(탐색 표면 비교), choose what to inspect next(다음 점검 대상 선택), detect DNR breach(반복 금지 위반 탐지).

Forbidden use(금지 사용): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성) 주장.

## Strict Sample Floor(엄격 표본 바닥)

Scout row(탐색 행)는 아래를 반드시 표시한다.

- split(분할): train/validation/OOS(학습/검증/표본외) 또는 not_applicable(해당 없음)
- trade_count(거래 수)
- days_in_scope(범위 일수)
- trades_per_day(일 거래 수)
- sparse_flag(희소 표식)
- pf999_sparse_flag(희소 PF999 표식)

Effect(효과): high PF(높은 수익 팩터)가 얇은 거래 수를 가리는 일을 막는다.

## Joint Pass Count(동시 통과 수)

`joint_pass_count(동시 통과 수)`는 네 축을 모두 기록한 row(행)에서만 계산한다.

Scout pass(탐색 통과)는 final pass(최종 통과)가 아니다. It only means(의미) the surface(표면)가 next inspection(다음 점검)을 받을 만큼 네 축을 동시에 덜 망가뜨렸다는 뜻이다.

## Scout Vs Serious Boundary(탐색과 진지 검증 경계)

Scout(탐색):

- single-window or cheap replay(단일 구간 또는 저비용 재생) 가능
- missing Tier B(티어 B 누락)는 `missing_required(필수 누락)`로 기록 가능
- result word(결과 표현)는 scout clue(탐색 단서) 또는 seed surface(씨앗 표면)까지만 허용

Serious validation(진지 검증):

- WFO(`walk-forward optimization`, 워크포워드 최적화), stress(스트레스), and MT5(메타트레이더5) before stronger claim(강한 주장 전 필요)
- Tier A separate/Tier B separate/Tier A+B combined(티어 A 분리/티어 B 분리/티어 A+B 합산) 기록 필요
- Grok pre-expensive review(비싼 검증 전 그록 검토) 필요

## First Implementation Boundary(첫 구현 경계)

The next packet(다음 작업 묶음)은 `frontier02B_proxy_scout_execution_v1`로 열 수 있다.

That packet(그 작업 묶음)은 actual data artifact(실제 데이터 산출물), script(스크립트), run manifest(실행 목록), and ledger rows(장부 행)를 따로 만들어야 한다.
