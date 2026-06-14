# Frontier11 Selection Metric Spec(전선11 선택 지표 명세)

## Slice Definitions(구간 정의)

- monthly validation slices(월별 검증 구간)
- quarterly validation slices(분기별 검증 구간)
- matching OOS slices(대응 표본밖 구간)

Slice boundaries(구간 경계)는 timestamp calendar(타임스탬프 달력)로 고정하고 결과를 본 뒤 바꾸지 않습니다.

## Metrics(지표)

- aggregate PF/density/DD(합계 수익 팩터/밀도/손실폭)
- worst-slice DD(최악 구간 손실폭)
- worst-slice PF(최악 구간 수익 팩터)
- time-under-water proxy(회복 전 체류 시간 프록시)
- equity smoothness proxy(자산곡선 매끄러움 프록시)
- trade distribution entropy(거래 분포 엔트로피)

## Control Arm(대조군)

The same candidate pool(같은 후보 풀)을 aggregate-only selector(합계 전용 선택기)와 stability-first selector(안정성 우선 선택기)로 동시에 평가합니다.

Effect(효과): 새 selection philosophy(선택 철학)의 효과를 candidate pool change(후보 풀 변화)와 분리합니다.

## Claim Boundary(주장 경계)

This metric(이 지표)은 scout ranking(탐색 순위)입니다. It does not create baseline(기준선), promotion(승격), runtime authority(런타임 권위), or live readiness(실거래 준비).
