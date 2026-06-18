# KPI Interpretation Governance Audit(KPI 해석 관리 감사)

Updated(갱신): 2026-06-19

## Scope(범위)

Objective(목표): KPI/PnL/trade interpretation(핵심 성과 지표/손익/거래 해석)이 multi-dimensional(다차원)으로 관리되는지, PF/PnL-only(수익 팩터/손익 단독) 해석이나 repeated hypothesis drift(반복 가설 표류)가 있는지 관련 agent(요원)와 함께 점검한다.

Current truth(현재 진실): F86 is pending open(F86 개방 대기), F85C closed negative/no authority(F85C 부정/권위 없음 마감), runtime authority/operating promotion/live readiness/Goal Achieve(런타임 권위/운영 승격/실거래 준비/목표 달성)는 not claimed(주장 없음)이다.

## Evidence Used(사용 근거)

- `docs/policies/kpi_measurement_standard.md`
- `docs/policies/run_result_management.md`
- `docs/policies/result_judgment_policy.md`
- `docs/registers/alpha_run_ledger.csv`
- `docs/registers/run_registry.csv`
- `stages/stage_frontier_83__realized_pnl_teacher_distillation_exportable_runtime_rotation/03_reviews/stage_run_ledger.csv`
- `stages/stage_frontier_84__runtime_realized_winrate_rebuild_after_signal_parity_gap/03_reviews/stage_run_ledger.csv`
- `stages/stage_frontier_85__runtime_path_contradiction_firewall_label_rebuild/03_reviews/stage_run_ledger.csv`
- `stages/stage_frontier_86__runtime_native_intrabar_path_label_source/03_reviews/stage_run_ledger.csv`
- `docs/agent_control/packets/kpi_interpretation_governance_audit_v1/kpi_interpretation_audit.json`
- `docs/agent_control/packets/kpi_interpretation_governance_audit_v1/kpi_interpretation_cleanup_manifest.json`

## Local Audit Result(로컬 감사 결과)

`foundation.control_plane.kpi_interpretation_audit(KPI 해석 감사)` scanned(점검) 6 ledger files(장부 파일), 16,623 rows(행), and 952 economic rows(경제 행) after cleanup(정리 후).

Result(결과): `pass_with_warnings(경고 포함 통과)`.

Blocking(차단):

- Direct missing/out-of-scope economic rows(직접 누락/범위 밖 경제 행): 64 -> 0.
- Cleanup manifest(정리 목록 기록): 64 rows(행), 478 values(값)을 비웠고 original values(원값)는 manifest(목록 기록)에 보존했다.
- Affected files(영향 파일): `docs/registers/alpha_run_ledger.csv` 60 rows(행), `docs/registers/run_registry.csv` 2 rows(행), F84 stage ledger(F84 단계 장부) 2 rows(행).

Warnings(경고):

- 245 mixed-scope rows(혼합 범위 행)는 economic KPI(경제 핵심 성과 지표)와 missing/out-of-scope language(누락/범위 밖 문구)를 함께 담아 attribution boundary(귀속 경계)가 필요하다.
- 368 economic rows(경제 행)는 kpi_scope/scoreboard_lane/judgment/external_verification_status(KPI 범위/점수판 선로/판정/외부 검증 상태) 중 하나 이상이 비어 있다.
- These warnings(이 경고들)는 goal closeout(목표 마감)을 막지는 않지만, future ledger enrichment(향후 장부 문맥 보강) 대상이다.

## Interpretation(해석)

Accepted(수용): 정책 체계는 multi-dimensional(다차원)이다. KPI standard(KPI 기준)는 signal/trading/risk/execution(신호/거래/위험/실행)을 분리하고, run management(실행 관리)는 run/subrun/view(실행/하위 실행/보기) 장부를 요구하며, result judgment(결과 판정)는 positive/negative/inconclusive/invalid(긍정/부정/불충분/무효)를 분리한다.

Accepted with boundary(경계 있는 수용): 최근 F83-F85 해석은 PF/PnL-only(수익 팩터/손익 단독)로만 흐르지는 않았다. F83은 runtime win-rate erosion(런타임 승률 침식), F84는 proxy-win -> runtime-loss(프록시 승리 -> 런타임 손실), F85는 leakage-safe firewall failure(누수 안전 방화벽 실패)로 회전했다.

Repaired(수리됨): historical ledger blocker(역사 장부 차단 요인)는 직접 차단 행 기준으로 정리됐다. Missing/out-of-scope rows(누락/범위 밖 행)는 더 이상 net profit/profit factor/drawdown/trade count(순이익/수익 팩터/손실폭/거래 수)를 직접 보유하지 않는다.

Residual risk(잔여 위험): warning rows(경고 행)는 장부 문맥 품질 문제다. 이것은 runtime authority(런타임 권위)나 selected baseline(선택 기준선)을 만들지 않으며, warning-free historical ledger(경고 없는 역사 장부) 주장도 아직 금지한다.

## Claim Boundary(주장 경계)

Allowed(허용):

- KPI interpretation governance audit passed with warnings(KPI 해석 관리 감사가 경고 포함 통과)
- direct missing/out-of-scope economic blocker removed(직접 누락/범위 밖 경제 차단 요인 제거)
- future guard exists for missing/out-of-scope economic rows(누락/범위 밖 경제 행에 대한 미래 보호 존재)
- recent interpretation is not PF/PnL-only(최근 해석은 수익 팩터/손익 단독이 아님)

Forbidden(금지):

- selected baseline/operating promotion/runtime authority/live readiness/Goal Achieve(선택 기준선/운영 승격/런타임 권위/실거래 준비/목표 달성)
- warning-free historical ledger(경고 없는 역사 장부)
- MT5/runtime verification complete(MT5/런타임 검증 완료)
- model superiority(모델 우위) or live trading readiness(실거래 준비)

## Operating Lessons(운영 교훈)

1. Missing_required/out_of_scope_by_claim(필수 누락/주장 범위 밖) rows(행)는 economic KPI columns(경제 KPI 열)를 비워야 한다.
2. Actual routed total/runtime evidence(실제 라우팅 전체/런타임 근거) rows(행)만 economic values(경제 값)를 보유할 수 있다.
3. KPI(핵심 성과 지표)는 profit factor/net profit(수익 팩터/순이익)만 보지 않고 density/drawdown/trade shape/runtime/proxy boundary(밀도/손실폭/거래 형태/런타임/프록시 경계)와 함께 읽어야 한다.
4. F86 onward(F86 이후)는 source/schema/hash/split/external verification status(원천/스키마/해시/분할/외부 검증 상태)를 먼저 적어, 같은 유형의 context warning(문맥 경고)을 새로 늘리지 않는다.

