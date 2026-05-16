# Known Weaknesses(알려진 약점)

- Tier B fallback(Tier B 대체)은 disabled(비활성)이다. Effect(효과): actual routed total(실제 라우팅 전체)은 Tier A(티어 A) 중심이며, Tier B(티어 B) 재활성은 별도 연구가 필요하다.
- validation mid segment(검증 중간 구간) PF(수익 팩터)는 1.1007 근처다. Effect(효과): 연구 패키지는 통과하지만 여유 폭은 크지 않다.
- MFE/MAE telemetry(MFE/MAE 텔레메트리)는 존재하지만 정의별 ratio(비율)가 다르다. Effect(효과): 추후 비교에서는 같은 정의만 비교해야 한다.
- Stage61(61단계)은 live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위)를 주장하지 않는다. Effect(효과): 이 패키지는 연구 기록으로만 닫힌다.
- 사용자 로컬 동기화(user-local sync, 사용자 로컬 동기화)는 확인하지 않았다. Effect(효과): 확인 가능한 것은 origin/main(원격 main)에 push(푸시)된 commit(커밋)뿐이다.
