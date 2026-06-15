Review size(검토 크기): small review(소규모 검토)

Snapshot-only rule(스냅샷 전용 규칙): answer only from this prompt(이 프롬프트). Do not inspect files(파일 확인 금지), run tools(도구 실행 금지), browse(브라우징 금지), or perform local verification(로컬 검증 금지). If evidence is insufficient, say needs_local_verification(로컬 검증 필요).

Project(프로젝트): Project Obsidian Prime v2, FPMarkets US100 M5.

Stage(단계): F55 sparse admission source(희소 진입 허용 원천) after F54 negative memory(부정 기억). Claim boundary(주장 경계): runtime probe observation only(런타임 탐침 관찰 전용); no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 주장 없음).

Stage-open Grok(단계 개방 그록): accepted(수용) with caveats(주의점): run identical sparse admission in proxy before MT5, watch density alignment vs economics, and avoid forward-looking daily ranking leakage(미래정보 누수).

Local verification(로컬 검증) already done by Codex: F54 did not test sparse admission; F54 used raw score threshold export(원시 점수 문턱값 내보내기). EA(전문가 자문) has RuntimeVetoTape(런타임 차단 테이프), so F55 keeps all feature rows(피처 행) and vetoes raw threshold hits(원시 문턱값 신호) that are not admitted(허용되지 않음). This preserves feature_ready(피처 준비) and maxhold/ATR runtime path(최대 보유/평균진폭 런타임 경로) better than exporting sparse feature rows only.

Proxy-first result(프록시 우선 결과): selected candidate `f55b_sparse_admission_extratrees_d6_l80_short_runtimepay_q65_b10_gap4`.
- ONNX parity(온엑스 동등성): passed, max_abs_diff about 1.98e-7, feature_count=58.
- Admission(진입 허용): score_q=0.65, daily_budget=10, min_gap_bars=4, forward-only daily quota(전진 전용 일일 쿼터), runtime veto tape(런타임 차단 테이프).
- validation proxy(검증 프록시): PF=1.131947, DD=4.467872, proxy trades/day=4.306011, admitted signals/day=5.229508, raw signals/day=17.885246.
- OOS proxy(표본외 프록시): PF=1.127362, DD=5.624917, proxy trades/day=4.618321, admitted signals/day=5.442748, raw signals/day=19.091603.
- Density caveat(밀도 주의): no proxy-surface candidate reached proxy trades/day 5 in both validation/OOS, but admitted signals/day is in the 5~10 target band. F54 MT5 previously filled nearly every expected signal: validation expected signals=2788 vs trades=2781; OOS expected signals=2178 vs trades=2163.

Proposed MT5 action(제안 MT5 행동): run one MT5 runtime probe(런타임 탐침) for validation_is and OOS using the selected sparse admission candidate, not a wider MT5 sweep(넓은 MT5 탐색 아님). Record PF/DD/trades/day, signal_diff, feature_ready_diff, and proxy-runtime gap(프록시-런타임 차이). If MT5 density remains under 5 or PF/DD fails, close as preserved clue or negative memory(보존 단서 또는 부정 기억), not completion(완성).

Question(질문): Is it reasonable to spend MT5 Strategy Tester time(MT5 전략 테스터 시간) on this one candidate now? Classify advice as accepted/rejected/needs_local_verification(수용/거절/로컬 검증 필요), and name the top failure risk.
