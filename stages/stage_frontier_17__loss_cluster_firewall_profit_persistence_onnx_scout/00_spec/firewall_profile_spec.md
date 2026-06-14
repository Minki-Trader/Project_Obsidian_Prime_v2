# Frontier17 Firewall Profile Spec(전선17 방화벽 프로필 명세)

Action(행동): 3 profiles(프로필 3개)를 Frontier17B(전선17B) 전에 고정합니다.

Effect(효과): bounded exploration(제한 탐색)은 허용하되, 결과를 본 뒤 profile/quantile(프로필/분위수)을 추가하는 repair ladder(수리 사다리)를 막습니다.

- `f17b_firewall_h8_ddq70_contq60`: hold_bars(보유 봉수) `8`, adverse_cluster_quantile(불리 군집 분위수) `0.7`, continuation_quantile(지속 분위수) `0.6`; soft firewall with moderate continuation trigger(완만한 방화벽과 중간 지속 트리거)
- `f17b_firewall_h10_ddq75_contq65`: hold_bars(보유 봉수) `10`, adverse_cluster_quantile(불리 군집 분위수) `0.75`, continuation_quantile(지속 분위수) `0.65`; balanced firewall with stricter loss-cluster veto(균형 방화벽과 더 엄격한 손실 군집 배제)
- `f17b_firewall_h12_ddq80_contq70`: hold_bars(보유 봉수) `12`, adverse_cluster_quantile(불리 군집 분위수) `0.8`, continuation_quantile(지속 분위수) `0.7`; strict firewall with strict continuation trigger(강한 방화벽과 강한 지속 트리거)
