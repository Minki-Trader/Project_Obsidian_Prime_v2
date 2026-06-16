# F64 Input References(F64 입력 참조)

Action(행동): F64 stage-open(단계 개방)에 사용한 bounded evidence(제한 근거)를 고정했다.

Effect(효과): Stage12~364(12~364단계)와 F53~F63은 reference-only(참조 전용)로만 읽히고, authority(권위)는 상속되지 않는다.

## Current Truth(현재 진실)

- workspace_state_before_open(개방 전 작업공간 상태): F63 closed negative memory(F63 부정 기억 마감)
- F63 stage(단계): `stage_frontier_63__new_pf_source_after_event_compression_memory`
- F63 runtime candidate(런타임 후보): `f63b_inv_evt_t20_m0_h2_cd0_cof1`
- F63 proxy(프록시): validation/OOS PF(검증/표본외 수익 팩터) `0.8140 / 0.8527`, DD(손실폭) `12.33% / 6.68%`, density(거래 빈도) `4.14 / 4.76`
- F63 MT5 runtime probe(MT5 런타임 탐침): validation/OOS PF(검증/표본외 수익 팩터) `0.35 / 0.44`, DD(손실폭) `22.56% / 15.61%`, density(거래 빈도) `4.90 / 5.67`

## Negative Memory(부정 기억)

- F53 short path-quality label(숏 경로 품질 라벨) failed MT5 PF(MT5 수익 팩터 실패).
- F54 runtime-shaped payoff label(런타임형 손익 라벨) failed MT5 PF(MT5 수익 팩터 실패).
- F55 sparse admission/runtime veto(희소 진입 허용/런타임 차단)는 transfer(전이)되지 않았다.
- F56/F57/F58 path and execution labels(경로 및 실행 라벨)는 transfer(전이)되지 않았다.
- F61/F62/F63 side allocation family(방향 배분 계열)는 runtime PF(런타임 수익 팩터)를 만들지 못했다.

## Grok Packet(그록 묶음)

- prompt(프롬프트): `docs/agent_control/grok_reviews/2026-06-16_frontier64_stage_open/small_review/prompt.md`
- clean_output(정제 출력): `docs/agent_control/grok_reviews/2026-06-16_frontier64_stage_open/small_review/clean_output.md`
- metadata(메타데이터): `docs/agent_control/grok_reviews/2026-06-16_frontier64_stage_open/small_review/metadata.json`
- raw_diagnostics(원시 진단): `docs/agent_control/grok_reviews/2026-06-16_frontier64_stage_open/small_review/raw_diagnostics.json`
- caveat(주의): prompt_length_exceeds_small_limit(소규모 검토 길이 권장 초과) warning(경고)이 있었으나 wrapper success(래퍼 성공)는 `true`다.
