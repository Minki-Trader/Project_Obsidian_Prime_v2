# Stage56 Account-Cost + Tier B Disabled Reevaluation(계좌 비용 + Tier B 비활성 재평가)

- created_at_utc(생성 시각): `2026-05-14T10:45:00Z`
- result_subject(판정 대상): Stage56(56단계) existing BaselineAdapter candidate evidence(기존 기준선 어댑터 후보 근거)
- new_facts(새 사실): current FPMarketsSC-Live US100 account history(현재 실계좌 US100 이력) and run50BH reports(보고서) show commission(거래수수료) `0.0`; swap(스왑)는 작지만 존재한다.
- design_decision(설계 결정): Tier B(티어 B)는 current BaselineAdapter anchor(현재 기준선 어댑터 기준점)에서 explicitly disabled(명시 비활성화)로 재판독한다.

## New Fact Read(새 사실 판독)

- commission(거래수수료): current account history(현재 계좌 이력) US100 185 deals(체결) commission sum(수수료 합계) `0.0`; run50BH(실행50BH) MT5 reports(보고서) 6개도 commission sum(수수료 합계) `0.0`.
- swap(스왑): current account history(현재 계좌 이력) US100 swap sum(스왑 합계) `-0.75`; run50BH routed validation/OOS(라우팅 검증/표본외) swap(스왑) `+3.08` / `+2.82`.
- spread(스프레드): current recent live M5(현재 최근 실계좌 5분봉) spread median/max(스프레드 중앙/최대) `60/60` points(포인트). run50BH raw validation/OOS(원천 검증/표본외) median/max(중앙/최대)는 `140/150` and `60/140` points(포인트).
- cost stress(비용 압박): prior `0.5 USD/trade` synthetic stress(거래당 합성 압박)는 0.1 lot 기준 약 `500` spread points(스프레드 포인트)에 해당한다. Effect(효과): account-specific cost(계좌별 비용)로 보면 run50BH cost failure(비용 실패)는 약해지지만, hidden slippage(숨은 미끄러짐)와 spread-regime drift(스프레드 환경 변화)는 계속 감시해야 한다.

## Reweighted Candidate Ranking(가중 재판독 후보 순위)

| rank(순위) | candidate(후보) | new read(새 판독) | still fails(아직 실패) |
|---:|---|---|---|
| 1 | `run50BH/et40h6_r001_a` | account-cost-adjusted development anchor(계좌 비용 반영 개발 기준점). validation/OOS(검증/표본외) trades/day(일 거래) `6.846995/5.102564`, PF(수익 팩터) `1.10/1.26`, net(순손익) `313.49/613.58`; Tier B disabled(티어 B 비활성) already true(이미 참). | same-move ratio(동일 이동 비율) `0.683958/0.718593`, cooldown12 trades/day(12봉 쿨다운 후 일 거래) `2.163934/1.435897`, validation drawdown(검증 손실) `286.67` high flag(높음 표시). |
| 2 | `run50BK/s43c02_h4c0_no_b` | Tier B disabled(티어 B 비활성) true and density(밀도) survives headline(겉보기 생존): trades/day(일 거래) `6.693989/5.082051`, PF(수익 팩터) `1.11/1.07`, net(순손익) `317.36/156.81`. | OOS PF(표본외 수익 팩터) `1.07` below 1.10, same-move ratio(동일 이동 비율) `0.734694/0.766902`, cooldown12 day(12봉 쿨다운 후 일 거래) `1.775956/1.184615`, drawdown high flag(손실 높음 표시). |
| 3 | `run50BK/s43c02_h4c0_with_b_blvl` | A+B actual routed(A+B 실제 라우팅) meets headline density/PF barely: trades/day(일 거래) `6.846995/5.066667`, PF(수익 팩터) `1.12/1.10`, net(순손익) `346.59/233.41`. | Tier B fallback-only OOS(Tier B 대체 전용 표본외) net/PF `-81.85/0.85`; if Tier B is discarded, its Tier A-only OOS density(표본외 밀도) is `4.687179`, below 5. |
| 4 | `run50BH/et40h6_r005_a` | OOS PF/net(표본외 수익 팩터/순손익) very strong `1.43/911.32`; Tier B disabled(티어 B 비활성). | OOS density(표본외 밀도) `4.902564` below 5 and same-move/cooldown survival(동일 이동/쿨다운 생존) still fails. |
| 5 | `run50BH/et40h6_r010_a` | PF/net(수익 팩터/순손익) stronger than r001 in validation/OOS(검증/표본외) `1.18/1.38`, `505.33/743.61`; Tier B disabled(티어 B 비활성). | OOS density(표본외 밀도) `4.620513` below 5 and same-move/cooldown survival(동일 이동/쿨다운 생존) still fails. |

## Updated Judgment(갱신 판정)

- selected_research_baseline(선택 연구 기준선): `none` remains(유지).
- current_frontier_candidate(현재 최전선 후보): `run50BH/et40h6_r001_a` remains(유지).
- revised_label(수정 라벨): `account_cost_adjusted_development_anchor` / `tier_b_disabled_reference` / `not_selected_baseline`.
- claim_boundary(주장 경계): this is not live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(운영 기준선), or reviewed_closed(검토 종료).

## What Changed(바뀐 점)

- previous cost_stressed_expectancy failure(이전 비용 압박 기대값 실패)는 no longer primary blocker(더 이상 1차 병목 아님) under this account-cost read(이 계좌 비용 판독 기준).
- previous Tier B rule failure(이전 Tier B 규칙 실패)는 resolved as an explicit disablement decision(명시 비활성화 결정으로 해소) for the current anchor(현재 기준점).
- the remaining primary blocker(남은 1차 병목)는 real density(실제 밀도): high same-move re-entry(높은 동일 이동 재진입), cooldown12 density collapse(12봉 쿨다운 밀도 붕괴), and validation drawdown(검증 손실).

## Next Hypothesis(다음 가설)

The next Stage56 branch should not immediately harden ONNX or polish Tier B(Tier B를 다듬기). It should test whether `run50BH/et40h6_r001_a` can preserve validation/OOS trades/day(검증/표본외 일 거래) above `5.0` while reducing same-move density(동일 이동 밀도) and drawdown(손실).

Proposed branch(제안 분기): `run50BL_run50BH_real_density_repair_anchor`.

Smallest useful probe(가장 작은 유용한 시험):
- keep Tier B disabled(티어 B 비활성 유지)
- keep account-cost read(계좌 비용 판독) separate from synthetic cost stress(합성 비용 압박) instead of deleting stress evidence(압박 근거 삭제)
- add real-density controls(실제 밀도 제어): same-direction re-entry guard(동일 방향 재진입 가드), new-move confirmation(새 움직임 확인), and drawdown-aware lifecycle(손실 인식 생명주기)
- require actual MT5 validation/OOS(실제 MT5 검증/표본외) with Tier A-only, Tier B disabled reason(비활성 사유), and actual routed total(실제 라우팅 전체) recorded

## Evidence Missing(아직 빠진 근거)

- live request-vs-fill slippage(실계좌 요청가 대비 체결가 미끄러짐): current MT5 order history(주문 이력) stores market-order request price(시장가 주문 요청가) as `0.0`, so this is inconclusive(불충분).
- risk_per_trade(거래당 위험), ATR SL/TP(ATR 손절/익절), and lot-floor telemetry(최소 랏 기록)는 BaselineAdapter hardening(기준선 어댑터 경화) 전에 still missing(아직 누락).
- same-move repair(동일 이동 수리) has not yet reproduced the run50BH headline density(겉보기 밀도) after cooldown-style controls(쿨다운식 제어).
