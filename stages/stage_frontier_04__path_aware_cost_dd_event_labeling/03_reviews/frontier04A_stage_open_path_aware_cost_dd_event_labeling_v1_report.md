# Frontier04A Stage Open Report(전선04A 단계 개방 보고서)

Updated(갱신): 2026-06-13T18:51:31Z

Status(상태): `opened_frontier04_path_aware_cost_dd_event_labeling_no_authority`

Judgment(판정): `stage_opened_after_grok_review_no_authority`

## Thesis(가설)

Path-aware cost/DD event labels may train an ONNX that avoids close-only validation drawdown failure(경로 인식 비용/손실폭 이벤트 라벨은 종가 전용 검증 손실폭 실패를 피하는 온엑스를 학습시킬 수 있음).

## Novelty Delta(신규성 차이)

Label target changes from close-return class to high/low path event outcome(라벨 목표가 종가 수익률 분류에서 고가/저가 경로 이벤트 결과로 바뀜).

## Grok Review(그록 검토)

Recommendation(권고): `open_frontier04(전선04 개방)`

Accepted(수용):
- open Frontier04 as a new hypothesis lifecycle(전선04를 새 가설 생명주기로 개방)
- keep Frontier04B proxy-first before ONNX/WFO/MT5(전선04B를 ONNX/WFO/MT5 전 프록시 우선으로 제한)
- keep Frontier03 clue reference-only(전선03 단서는 참조 전용 유지)
- cite Stage355 first_barrier_labels as reusable archive precedent(Stage355 first_barrier_labels를 재사용 보관소 선례로 인용)

Needs local verification(로컬 검증 필요):
- raw OHLC alignment manifest before path labels(경로 라벨 전 원천 OHLC 정렬 목록)
- leakage audit: labels use future OHLC only and features stay closed-bar(누수 감사: 라벨은 미래 OHLC만 쓰고 피처는 종료봉만 사용)
- Stage355 first_barrier_labels citation and Frontier04 semantic diff(Stage355 first_barrier_labels 인용과 전선04 의미 차이)
- paired close-return versus path-label comparison on identical rows/splits(동일 행/분할의 종가 수익률 대비 경로 라벨 쌍 비교)
- fixed grid: 3 target/stop pairs times 2 horizons only(고정 격자: 목표/손절 3쌍 곱하기 2개 수평선만)
- same-bar ambiguity, timeout, event-first, and cost semantics fixed in manifest(동일 봉 모호/시간 만료/이벤트 우선/비용 의미를 실행 목록에 고정)

## Next Action(다음 행동)

`frontier04B_path_aware_label_proxy_scout_v1`. Action(행동)은 path-aware label proxy scout(경로 인식 라벨 프록시 탐색)를 실행하는 것입니다. Effect(효과)는 ONNX(온엑스) 학습 전에 비용·손실폭 라벨 축이 실제로 가치가 있는지 확인하는 것입니다.

## Claim Boundary(주장 경계)

No completion(완성 없음), no baseline(기준선 없음), no promotion(승격 없음), no runtime authority(런타임 권위 없음), no live readiness(실거래 준비 없음), no Goal Achieve(목표 달성 없음).
