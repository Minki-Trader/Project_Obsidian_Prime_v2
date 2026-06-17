# F74B Required Gate Coverage Audit(F74B 필수 게이트 커버리지 감사)

Updated(갱신): 2026-06-17T03:31:07Z

| gate(게이트) | status(상태) | evidence/effect(근거/효과) |
|---|---|---|
| raw label density gate(원시 라벨 밀도 게이트) | `pass(통과)` | pass axes(통과 축) `6` |
| proxy KPI measurement(프록시 KPI 측정) | `pass(통과)` | candidate rows(후보 행) recorded(기록됨). |
| data integrity boundary(데이터 무결성 경계) | `pass_with_boundary(경계 포함 통과)` | next-bar entry and declared horizon(다음 봉 진입과 선언 수평선). |
| model validation boundary(모델 검증 경계) | `pass_scout_only(탐색 전용 통과)` | scores are rank signals, not calibrated probability(점수는 순위 신호이지 보정 확률 아님). |
| next action routing(다음 행동 배치) | `raw_density_passed_but_proxy_needs_repair(원시 밀도는 통과했지만 프록시 수리 필요)` | MT5 is not claimed yet(MT5는 아직 주장하지 않음). |
| final claim guard(최종 주장 보호) | `pass(통과)` | no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음). |
