# Frontier32 stage open small review(전선32 단계 개방 소규모 검토)

You are Grok(그록) as external second opinion(외부 2차 의견). Codex(코덱스) owns final judgment(최종 판정), and your answer is advisory(조언) only.

Please answer with these exact ASCII keys first:

verdict: accepted / rejected / needs_local_verification
novelty_ok: yes / no
leakage_risk: low / medium / high
frontier_boundary_ok: yes / no
hypothesis_scope_ok: yes / no
runtime_claim_boundary_ok: yes / no

Current truth(현재 진실):
- F31(전선31) closed as preserved clue + negative memory(보존 단서+부정 기억).
- F31B return-space proxy(수익률 공간 프록시): density/scout/seed/handoff(밀도/탐색/씨앗/인계) = 85/78/62/16.
- F31B realistic/executable handoff rows(현실적/실행 가능 인계 행) = 16/0.
- Best F31 read-only forward candidate(읽기 전용 전진 후보): `f31b_0013`, validation PF/density/DD(검증 수익 팩터/밀도/손실폭) 2.450/5.962/4.708, OOS(표본외) 2.268/6.687/4.812.
- F31D runtime probe status(런타임 탐침 상태): `runtime_probe_out_of_scope_by_claim_return_space_proxy_only_executable_mapping_not_validated`.
- F31 negative memory(부정 기억): return-space clip(수익률 공간 클립) without intrabar or MT5 SL/TP probe(봉내 또는 MT5 손절/익절 탐침) cannot claim runtime or ONNX(런타임 또는 온엑스).

Proposed Frontier32(제안 전선32):
- Stage id(단계 ID): `stage_frontier_32__executable_sl_tp_mapping_for_return_space_exit_shape_handoff_surface_onnx_scout`
- Hypothesis(가설): F31 return-space stop/take log caps(수익률 공간 손절/익절 로그 상한)을 fixed price-path SL/TP rules(고정 가격 경로 손절/익절 규칙)로 mapped(매핑)하면, some F31 handoff surface(일부 F31 인계 표면)는 intrabar high/low path proxy(봉내 고가/저가 경로 프록시)에서도 5~10 trades/day(일 5~10회), PF lift(수익 팩터 상승), DD reduction(손실폭 감소)을 보존할 수 있다.
- Changed variable(변경 변수): executable SL/TP path representation(실행 가능한 손절/익절 경로 표현).
- Fixed controls(고정 통제): F31 top 16 mapping queue(전선31 상위 16개 매핑 큐), F30/F31 entry masks(진입 마스크), fwd12 horizon(12봉 구간), train-only parameter source(학습 전용 파라미터 원천).
- Raw path source(원천 경로): `data/raw/mt5_bars/m5/US100/bars_us100_m5_mt5api_raw.csv`, Bid open/high/low/close(매수호가 시가/고가/저가/종가).
- Alignment check(정렬 점검): dataset future return(데이터셋 미래 수익률) matches raw open-to-open(원천 시가-시가) basis, not close-to-close(종가-종가).

Success criteria(성공 기준):
- Scout clue(탐색 단서): path-proxy validation/OOS(경로 프록시 검증/표본외) both positive, density 5~10/day, forward PF >= 1.05, DD <= 20.
- Seed surface(씨앗 표면): forward PF >= 1.20, DD <= 15, density 5~10/day, smoothness proxy(매끄러움 프록시) acceptable.
- Runtime probe candidate(런타임 탐침 후보): forward PF >= 1.50, DD <= 10~12, density 5~10/day, executable representation available(실행 가능 표현 있음), but still no runtime authority(런타임 권위 없음).

Forbidden claims(금지 주장):
- Do not claim completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성).
- Do not run MT5(엠티5) before executable path proxy(실행 경로 프록시), local verification(로컬 검증), and pre-expensive Grok review(비싼 실행 전 그록 검토) if a candidate survives.

Question(질문): Is this a valid new frontier hypothesis(새 전선 가설) rather than a F31 inheritance(전선31 상속), and are the runtime claim boundaries(런타임 주장 경계) correct?
