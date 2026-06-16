# F65 Stage Closeout(F65 단계 마감)

Updated(갱신): `2026-06-16T02:22:15Z`

- closeout_label(마감 라벨): `preserved_clue(보존 단서)`
- judgment(판정): `preserved_clue_sltp_unit_semantics_supported_but_economics_incomplete_no_authority(보존 단서, 손절/익절 단위 의미 지원, 그러나 경제성 불완전, 권위 없음)`
- next_stage(다음 단계): `stage_frontier_66__runtime_unit_aligned_exit_economics_pf_source_after_semantics_gap`
- next_run(다음 실행): `frontier66A_stage_open_runtime_unit_aligned_exit_economics_pf_source_v1`

## Action And Effect(행동과 효과)

Action(행동): F65B proxy-runtime attribution(프록시-런타임 귀속), F65C targeted MT5 runtime probe(표적 MT5 런타임 탐침), Grok closeout review(그록 마감 검토)를 묶어 stage(단계)를 닫았다.

Effect(효과): SL/TP unit semantics(손절/익절 단위 의미)는 reusable clue(재사용 단서)로 보존하고, economics gap(PF/DD 경제성 차이)은 미해결로 남겨 다음 stage(단계)가 새 가설로 시작하게 했다.

## What Caused The Proxy-Runtime Gap(프록시-런타임 차이 발생 지점)

- Signal count gap(신호 수 차이): raw adapter(원 어댑터)에서 runtime veto tape(런타임 차단 테이프)와 entry transition gate(진입 전환 게이트)를 지나며 압축됐다. validation/OOS는 raw `5269/4206`, veto `1196/881`, entry transition block `2973/2483`, actual non-flat `1100/842`로 맞물린다.
- Residual signal diff(잔여 신호 차이): F65C signal_count_diff(신호 수 차이) `-2199/-1892`는 F66에서 open attribution(열린 귀속)으로 남긴다. Effect(효과): F65 closeout(마감)이 exit semantics clue(청산 의미 단서)를 넘어 signal layer closure(신호 층 폐쇄)로 과장되지 않는다.
- Feature/data gap(피처/데이터 차이): feature_ready_diff(피처 준비 차이)가 validation/OOS `0/0`이라 1순위 원인이 아니다.
- Fill/reject gap(체결/거절 차이): F65B 기준 fills(체결) `1098/838`, invalid stops(무효 손절) `2/4`로 작다.
- Exit economics gap(청산 경제성 차이): proxy(프록시)는 price units(가격 단위)로 손절/익절을 계산했고, MT5는 points(포인트)로 해석했다. 이 단위 의미 차이가 exit shape(청산 형태)를 크게 바꿨다.

## Runtime Probe Observation(런타임 탐침 관찰)

| split(분할) | PF(수익 팩터) | DD%(손실폭) | trades/day(일 거래) | signal diff(신호 차이) | density gap(빈도 차이) |
|---|---:|---:|---:|---:|---:|
| validation_is | 0.97 | 21.83 | 5.442622950819672 | -2199 | 0.021857923497267784 |
| oos | 1.11 | 14.66 | 5.816793893129771 | -1892 | -0.022900763358778775 |

## Exit Shape Evidence(청산 형태 근거)

| split(분할) | F64E stop%(기존 손절률) | F65C stop%(보정 손절률) | F64E maxhold%(기존 최대보유률) | F65C close_max_hold%(보정 최대보유 청산률) |
|---|---:|---:|---:|---:|
| validation_is | 79.51% | 25.90% | 0.00% | 64.76% |
| oos | 67.54% | 26.38% | 0.00% | 62.47% |

## Closeout Judgment(마감 판정)

F65는 `preserved_clue(보존 단서)`로 마감한다.

unit-semantics clue(단위 의미 단서)는 supported(지원)된다. 이유는 unit-adjusted MT5 runtime probe(단위 보정 MT5 런타임 탐침)가 stop rate(손절률)를 낮추고 maxhold behavior(최대보유 행동)를 크게 늘렸기 때문이다. 하지만 completion candidate(완성 후보)는 아니다. validation PF(검증 수익 팩터)는 `0.97`, OOS PF(OOS 수익 팩터)는 `1.11`, DD(손실폭)는 `21.83/14.66`로 아직 높다.

## Do-Not-Repeat Note(반복 금지 메모)

explicit unit contract(명시 단위 계약) 없이 proxy price-unit exits(프록시 가격 단위 청산)와 MT5 point exits(MT5 포인트 청산)를 비교하지 않는다. Effect(효과): later frontier stages(다음 전선 단계들)가 fake PF gap(가짜 PF 차이)을 signal edge(신호 우위)처럼 읽지 않게 한다.

## Artifact Lineage(산출물 계보)

- source_inputs(원천 입력): F64D direction adapter ONNX(방향 어댑터 온엑스), F64D runtime veto tape(런타임 차단 테이프), F64E MT5 runtime probe(MT5 런타임 탐침), F65B attribution summary(귀속 요약), F65C final decision(최종 결정), Grok closeout review(그록 마감 검토).
- producer(생산자): `frontier65_gap_attribution.py`, `frontier65c_targeted_sltp_runtime_probe.py`, `frontier65d_stage_closeout.py`, MT5 Strategy Tester(MT5 전략 테스터).
- consumer(소비자): F65 closeout reports(마감 보고서), run registry(실행 등록부), alpha ledger(알파 장부), stage ledger(단계 장부), F66 stage-open(다음 단계 개방).
- artifact_paths(산출물 경로): `stages/stage_frontier_65__runtime_semantics_pf_source_after_hazard_gate_failure/02_runs/frontier65B_proxy_runtime_gap_attribution_scout_v1/gap_attribution_summary.json`, `stages/stage_frontier_65__runtime_semantics_pf_source_after_hazard_gate_failure/02_runs/frontier65C_targeted_sltp_unit_runtime_probe_v1/final_decision.json`, `stages/stage_frontier_65__runtime_semantics_pf_source_after_hazard_gate_failure/03_reviews/runtime_probe_unit_adjusted_report.md`, `stages/stage_frontier_65__runtime_semantics_pf_source_after_hazard_gate_failure/03_reviews/proxy_runtime_gap_after_unit_adjustment_report.md`, `stages/stage_frontier_65__runtime_semantics_pf_source_after_hazard_gate_failure/03_reviews/stage_closeout_report.md`.
- artifact_hashes(산출물 해시): F65B `362980ef81e3f3786b55c9c14f0aaf060594d79c92b8f93931cfa8639826f110`, F65C `bcffa8f230ce3795d3206e30427437eaad0598a5a8e30541fb10b812e8600e52`, Grok clean output(그록 정리 출력) `e85877f18dd8e5fc0c6222e1b55b833b2759b23903f6f1457b1722e6777939fe`, compile log(컴파일 로그) `e628738512448969092167f283c93b4508aed134ff89e857b6050e210e5998f8`.
- registry_links(장부 연결): `docs/registers/run_registry.csv`, `docs/registers/alpha_run_ledger.csv`, `stages/stage_frontier_65__runtime_semantics_pf_source_after_hazard_gate_failure/03_reviews/stage_run_ledger.csv`.
- availability(가용성): durable reports tracked(지속 보고서 추적됨); `02_runs` outputs(실행 산출물)는 ignored_with_manifest(목록 기반 추적 제외)이며 command reproduction(명령 재현)으로 연결된다.
- reproduction_commands(재현 명령): `python -m stage_pipelines.stage_frontier_65.frontier65_gap_attribution`, `python -m stage_pipelines.stage_frontier_65.frontier65c_targeted_sltp_runtime_probe --timeout-seconds 900 --wait-timeout-seconds 240`, `python -m stage_pipelines.stage_frontier_65.frontier65d_stage_closeout`.
- lineage_judgment(계보 판정): `connected_with_boundary(경계 있는 연결)`.

## Boundary(경계)

completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)이다.
