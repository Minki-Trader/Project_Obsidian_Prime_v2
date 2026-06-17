# F77H Stage Closeout Grok Review Prompt(F77H 단계 마감 Grok 검토 프롬프트)

You are Grok(Grok, 그록), external second-opinion reviewer(외부 2차 의견 검토자).
Answer only from this bounded evidence snapshot(제한 근거 스냅샷).
Do not inspect files(파일 확인 금지), run tools(도구 실행 금지), browse(브라우징 금지), or perform local verification(로컬 검증 금지).

## Codex Proposed Closeout(Codex 제안 마감)

- stage(단계): `stage_frontier_77__runtime_lifecycle_label_density_rebuild`
- closeout label(마감 라벨): `preserved_clue(보존 단서)`
- claim boundary(주장 경계): `stage_closeout_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`
- forbidden claims(금지 주장): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)

## Evidence(근거)

- proxy candidates(프록시 후보): `10368`
- meaningful proxy candidates(의미 프록시 후보): `0`
- final-like references(완성 유사 참조): `0`
- proxy best OOS net/PF/DD/tpd(프록시 최선 표본외 순수익/수익 팩터/손실폭/일 거래 수): `127.2/1.8030303030303034/0.6239999999999963/2.230769230769231`
- runtime best OOS net/PF/DD/tpd(런타임 최선 표본외 순수익/수익 팩터/손실폭/일 거래 수): `4.48/1.23/1.41/0.14871794871794872`
- MT5 runtime probe(MT5 런타임 탐침): F77D and F77F both executed(실행), F77F completed 2/2(2/2 완료)
- signal/feature parity(신호/피처 동등성): pass(통과)

## Required F77G Conditions(F77G 필수 조건)

1. gap causes(간극 원인)를 bookkeeping only(장부), hypothesis-negative(가설 부정), preserved mechanic(보존 메커니즘)으로 분리한다.
2. negative memory(부정 기억)에 zero meaningful proxy candidates(의미 프록시 후보 0), density metric misalignment(밀도 지표 불일치), money scale not contract-calibrated(금액 배율 계약 미보정), exportability distorted target selection(내보내기 가능성의 대상 선택 왜곡)을 포함한다.
3. preserved clues(보존 단서)에 point-unit repair pattern(포인트 단위 수리 패턴), ONNX/EA signal parity path(ONNX/EA 신호 동등성 경로), runtime bridge mechanics(런타임 연결 메커니즘)을 포함한다.
4. next frontier(다음 전선)는 F77 continuation(F77 연속)이 아니라 new hypothesis(새 가설)여야 한다.

## Codex Closeout Contents(Codex 마감 내용)

Gap mapping(간극 매핑):
[
  {
    "gap_cause": "money_scale_gap_after_point_unit_repair",
    "bucket": "bookkeeping/measurement(장부/측정)",
    "meaning": "proxy P/L(프록시 손익)이 broker contract P/L(브로커 계약 손익)로 보정되지 않았다."
  },
  {
    "gap_cause": "trade_density_denominator_gap_proxy_active_dates_vs_runtime_calendar_days",
    "bucket": "bookkeeping/measurement(장부/측정)",
    "meaning": "proxy trades/day(프록시 일 거래 수)는 selected active dates(선택 활성 날짜)를 분모로 썼고 runtime(런타임)은 calendar days(달력일)를 썼다."
  },
  {
    "gap_cause": "minor_fill_count_gap_from_hold_same_direction_after_realized_runtime_holds",
    "bucket": "preserved mechanic(보존 메커니즘)",
    "meaning": "runtime realized holds(런타임 실제 보유)가 proxy selected entries(프록시 선택 진입) 중 일부를 same-direction hold(동방향 보유)로 압축했다."
  },
  {
    "gap_cause": "weak_alpha_gap_pf_and_density_below_goal_after_runtime_materialization",
    "bucket": "hypothesis-negative(가설 부정)",
    "meaning": "F77F runtime PF/density(런타임 수익 팩터/밀도)가 목표권과 거리가 멀고 F77B meaningful signal(의미 신호)이 0이었다."
  }
]

Negative memory(부정 기억):
[
  "zero meaningful proxy candidates(의미 프록시 후보 0): F77B 10,368 후보 중 meaningful signal(의미 신호)과 final-like reference(완성 유사 참조)가 모두 0이었다.",
  "density metric misalignment(밀도 지표 불일치): proxy trades/day(프록시 일 거래 수)는 selected active dates(선택 활성 날짜) 기준이라 final review(최종 검토)의 일 거래 수와 다르다.",
  "money scale not contract-calibrated(금액 배율 계약 미보정): proxy money(프록시 금액)는 MT5 realized P/L(실현 손익)보다 약 12배 크게 보였다.",
  "exportability distorted target selection(내보내기 가능성이 대상 선택 왜곡): best HistGBM(최선 히스토그램 GBM)은 ONNX export(ONNX 내보내기)가 실패해 weaker ExtraTrees(더 약한 엑스트라트리)를 런타임 대상으로 썼다."
]

Preserved clues(보존 단서):
[
  "point-unit repair pattern(포인트 단위 수리 패턴): TP18/SL12 price units(가격 단위)을 TP1800/SL1200 broker points(브로커 포인트)로 변환하면 MT5 Invalid stops(잘못된 손절/익절)가 사라진다.",
  "ONNX/EA signal parity path(ONNX/EA 신호 동등성 경로): three-column short schema(3열 숏 스키마)와 selected-entry veto tape(선택 진입 거부 테이프)가 signal count parity(신호 수 동등성)를 유지했다.",
  "runtime bridge mechanics(런타임 연결 메커니즘): point-unit repair(포인트 단위 수리) 후 Strategy Tester(전략 테스터)에서 validation/OOS(검증/표본외) 주문이 체결됐다."
]

Next frontier hypothesis(다음 전선 가설):
Execution-calibrated labels(실행 보정 라벨)이 broker contract P/L(브로커 계약 손익), final-review density denominator(최종 검토 밀도 분모), fill semantics(체결 의미), and lifecycle risk(생명주기 위험)를 proxy 단계부터 내장하면 PF/density/DD(수익 팩터/밀도/손실폭)를 동시에 더 잘 맞출 수 있는지 본다.

## Focus Question(집중 질문)

Does this satisfy stage closeout(단계 마감) as preserved clue(보존 단서) with negative memory(부정 기억), without granting forbidden claims(금지 주장)?

Classify at top as one of:
- accepted(수용)
- accepted_with_conditions(조건부 수용)
- needs_local_verification(로컬 검증 필요)
- rejected(거절)
