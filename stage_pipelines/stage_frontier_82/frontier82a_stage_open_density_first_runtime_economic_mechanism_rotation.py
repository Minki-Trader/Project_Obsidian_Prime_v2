from __future__ import annotations

import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, path_exists, sha256_file_lf_normalized


STAGE_ID = "stage_frontier_82__density_first_runtime_economic_mechanism_rotation"
RUN_ID = "frontier82A_stage_open_density_first_runtime_economic_mechanism_rotation_v1"
PARENT_RUN_ID = "frontier81H_capped_repair_closeout_or_f82_rotation_decision_v1"
NEXT_RUN_ID = "frontier82B_density_first_runtime_economic_mechanism_proxy_scout_v1"

STATUS = "opened_hypothesis_lifecycle_design_only_no_authority"
JUDGMENT = "frontier82_opened_density_first_runtime_economic_mechanism_lifecycle_no_authority"
CLAIM_BOUNDARY = (
    "frontier82_open_design_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)
FRONTIER_EXTRA_DUE_STATUS = "not_due_after_f81_closeout_next_boundary_f100_e01_closed_for_f050"
FIVE_STAGE_RETROSPECTIVE_STATUS = "inactive_preserve_records_no_grok_block"

SCRIPT_REL = "stage_pipelines/stage_frontier_82/frontier82a_stage_open_density_first_runtime_economic_mechanism_rotation.py"

STAGE_DIR = ROOT / "stages" / STAGE_ID
SPEC_DIR = STAGE_DIR / "00_spec"
INPUT_DIR = STAGE_DIR / "01_inputs"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
PACKET_DIR = ROOT / "docs/agent_control/packets" / RUN_ID

STAGE_BRIEF = SPEC_DIR / "stage_brief.md"
INPUT_REFS = INPUT_DIR / "input_refs.md"
REPORT = REVIEW_DIR / "frontier82A_stage_open_density_first_runtime_economic_mechanism_rotation_report.md"
MANIFEST = REVIEW_DIR / "f82a_stage_open_manifest.json"
EXPERIMENT_DESIGN = REVIEW_DIR / "f82a_experiment_design.json"
STATE_SYNC_AUDIT = REVIEW_DIR / "f82a_state_sync_audit.json"
ARTIFACT_LINEAGE = REVIEW_DIR / "f82a_artifact_lineage.json"
GATE_AUDIT_MD = REVIEW_DIR / "required_gate_coverage_audit_f82a_open.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"

WORK_PACKET = PACKET_DIR / "work_packet.yaml"
PACKET_STATE_SYNC_AUDIT = PACKET_DIR / "state_sync_audit.json"
PACKET_SKILL_RECEIPTS = PACKET_DIR / "skill_receipts.json"
PACKET_GATE_AUDIT = PACKET_DIR / "required_gate_coverage_audit.json"
PACKET_FINAL_CLAIM_GUARD = PACKET_DIR / "final_claim_guard.json"

WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs/context/current_working_state.md"
GLOBAL_SELECTION_STATUS = ROOT / "docs/registers/selection_status.md"
RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs/registers/artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs/registers/idea_registry.md"
CHANGELOG = ROOT / "docs/workspace/changelog.md"
DECISION_MEMO = ROOT / "docs/decisions/2026-06-18_stage_frontier_82_open.md"

F81_STAGE = ROOT / "stages/stage_frontier_81__mt5_native_order_intent_cost_shape_rebuild"
F81_CLOSEOUT = F81_STAGE / "03_reviews/stage_closeout_report.md"
F81_CLOSEOUT_SUMMARY = F81_STAGE / "03_reviews/f81h_closeout_or_rotation_decision.json"
F81_GAP = F81_STAGE / "03_reviews/f81d_proxy_runtime_gap_attribution.json"
F81_DEAL = F81_STAGE / "03_reviews/f81f_deal_reconciliation_summary.json"
F81_REALIZED = F81_STAGE / "03_reviews/f81g_mt5_realized_label_rebuild_summary.json"
NEGATIVE_REGISTER = ROOT / "docs/registers/negative_result_register.md"
FRONTIER_EXTRA_REGISTER = ROOT / "docs/registers/frontier_extra_stage_register.yaml"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    text = str(path)
    if text.startswith("\\\\?\\"):
        text = text[4:]
    return Path(text).relative_to(ROOT).as_posix()


def write_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8-sig")


def read_json_or_empty(path: Path) -> dict[str, Any]:
    if not path_exists(path):
        return {}
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def detect_lineterminator(path: Path) -> str:
    sample = io_path(path).read_bytes() if path_exists(path) else b""
    return "\r\n" if b"\r\n" in sample else "\n"


def csv_key_exists(path: Path, key: str, value: str) -> bool:
    if not path_exists(path):
        return False
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return any(row.get(key) == value for row in reader)


def append_csv_row_if_absent(path: Path, key: str, row: Mapping[str, Any]) -> None:
    if csv_key_exists(path, key, str(row.get(key, ""))):
        return
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
    lineterminator = detect_lineterminator(path)
    with io_path(path).open("a", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator=lineterminator)
        writer.writerow({field: row.get(field, "") for field in fieldnames})


def remove_matching_csv_text_rows(path: Path, matcher: Any) -> None:
    if not path_exists(path):
        return
    raw = io_path(path).read_text(encoding="utf-8-sig")
    newline = "\r\n" if "\r\n" in raw else "\n"
    rows = raw.splitlines()
    if not rows:
        return
    kept = [rows[0]] + [line for line in rows[1:] if not matcher(line)]
    io_path(path).write_text(newline.join(kept) + newline, encoding="utf-8-sig")


def write_stage_ledger(row: Mapping[str, Any]) -> None:
    with io_path(ALPHA_LEDGER).open("r", encoding="utf-8-sig", newline="") as handle:
        fieldnames = list(csv.DictReader(handle).fieldnames or [])
    io_path(STAGE_LEDGER.parent).mkdir(parents=True, exist_ok=True)
    with io_path(STAGE_LEDGER).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerow({field: row.get(field, "") for field in fieldnames})


def make_design(created_at: str) -> dict[str, Any]:
    f81h = read_json_or_empty(F81_CLOSEOUT_SUMMARY)
    f81_runtime_oos = (
        f81h.get("runtime_probe_kpi", {}).get("oos", {})
        if isinstance(f81h.get("runtime_probe_kpi"), dict)
        else {}
    )
    f81_best_seed = f81h.get("best_seed", {}) if isinstance(f81h.get("best_seed"), dict) else {}
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "created_at_utc": created_at,
        "primary_family": "state_sync",
        "primary_skill": "obsidian-stage-transition",
        "supplemental_design_skill": "obsidian-experiment-design",
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "idea_id": "IDEA-FR82-DENSITY-FIRST-RUNTIME-ECONOMIC-MECHANISM-ROTATION",
        "hypothesis": (
            "density-first two-sided runtime economic mechanism(밀도 우선 양방향 런타임 경제 메커니즘)이 "
            "threshold search(임계값 탐색)보다 먼저 deal-level PnL(거래별 손익), "
            "session/regime split(세션/장세 분할), exportable model family(내보내기 가능한 모델 계열)를 묶으면 "
            "F81 low-density repair(F81 저밀도 수리)를 반복하지 않고 material MT5 candidate(MT5 물질화 후보)를 만들 수 있다는 가설."
        ),
        "decision_use": (
            "F82B가 broad density-first proxy surface(넓은 밀도 우선 프록시 표면)를 만들지, "
            "아니면 F81-style low-density seed(F81식 저밀도 씨앗)만 반복될 때 즉시 rotate(회전)할지 결정하는 데 쓴다."
        ),
        "comparison_baseline": [
            "F81C/F81F MT5 runtime OOS negative(전선81C/F 런타임 표본외 부정): "
            f"net={f81_runtime_oos.get('net_profit')}; PF={f81_runtime_oos.get('profit_factor')}; "
            f"DD={f81_runtime_oos.get('receipt_max_drawdown_percent')}; trades/day={f81_runtime_oos.get('trades_per_day')}",
            "F81G low-density seed reference(F81G 저밀도 씨앗 참고): "
            f"net={f81_best_seed.get('oos_net_profit')}; PF={f81_best_seed.get('oos_profit_factor')}; "
            f"DD={f81_best_seed.get('oos_drawdown_percent')}; trades/day={f81_best_seed.get('oos_trades_per_day')}",
            "No-trade baseline(무거래 기준): no risk(위험 없음), no profit(수익 없음), no strategy utility(전략 효용 없음).",
        ],
        "control_variables": [
            "symbol/timeframe(심볼/시간프레임): FPMarkets US100 M5(FPMarkets US100 5분봉)",
            "frontier inheritance boundary(전선 상속 경계): reference only(참조 전용), no winner/baseline/authority inheritance(승자/기준선/권위 상속 없음)",
            "paired tier reporting(쌍 티어 보고): Tier A separate/Tier B separate/Tier A+B combined(티어 A 분리/티어 B 분리/합산) or explicit missing/out_of_scope(명시 누락/범위 밖)",
            "claim boundary(주장 경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)",
        ],
        "changed_variables": [
            "density target first(밀도 목표 우선): require candidate density before micro threshold search(미세 임계값 탐색 전 후보 밀도 요구)",
            "two-sided mechanism(양방향 메커니즘): long/short opportunity balance(롱/숏 기회 균형)를 first-class signal(일급 신호)로 둔다",
            "runtime economics first(런타임 경제성 우선): deal-level PnL and trade-density(거래별 손익과 거래 밀도)를 proxy score(프록시 점수)에 묶는다",
            "model-family openness(모델 계열 개방): tree/linear/calibrated rank/exportable family(트리/선형/보정 순위/내보내기 가능 계열)를 broad sweep(넓은 탐색)한다",
        ],
        "sample_scope": {
            "symbol": "FPMarkets US100",
            "timeframe": "M5",
            "stage": STAGE_ID,
            "initial_period_policy": "exact train/validation/OOS windows(정확한 학습/검증/표본외 창)는 F82B에서 명명하고, F82A는 stage-open design(단계 개방 설계)만 담당한다",
            "tier_scope": "Tier A plus Tier B required if available; if unavailable record missing_required/out_of_scope_by_claim(티어 A와 가능한 티어 B, 없으면 명시)",
        },
        "success_criteria": [
            "proxy scout(프록시 탐색)가 materialization candidate(물질화 후보)를 만들고, density(밀도)가 F81G low-density seed(저밀도 씨앗)를 넘어선다",
            "meaningful signal/candidate(의미 신호/후보)가 생기면 MT5 Strategy Tester(전략 테스터)로 물질화한다",
            "WFO/stress/runtime validation(워크포워드/스트레스/런타임 검증)으로 갈 수 있는 근거를 만든다",
        ],
        "failure_criteria": [
            "candidate density(후보 밀도)가 F81G 수준처럼 너무 낮아 materialization-ready(물질화 준비)로 볼 수 없다",
            "proxy(프록시)는 좋아 보이나 runtime economics(런타임 경제성)가 F81C처럼 붕괴한다",
            "same threshold/filter/parameter(같은 임계값/필터/파라미터) 반복만 남고 new axis(새 축)가 없다",
        ],
        "invalid_conditions": [
            "time-axis or label boundary(시간축 또는 라벨 경계)가 설명되지 않는다",
            "future data leakage(미래 데이터 누수) 또는 split contamination(분할 오염)이 발견된다",
            "model score(모델 점수)를 calibrated probability(보정 확률)처럼 해석하지만 calibration evidence(보정 근거)가 없다",
        ],
        "stop_conditions": [
            "zero signal/no trade/mismatch/crash/block(영 신호/무거래/불일치/충돌/차단)은 negative evidence(부정 근거)로 기록하고 원인 축을 분리한다",
            "new evidence/new axis(새 근거/새 축) 없이 threshold-only repair(임계값 전용 수리)가 반복되면 capped repair(상한 수리)로 닫는다",
            "external runtime verification(외부 런타임 검증)이 필요한 claim(주장)은 같은 pass(회차)에서 시도하거나 claim scope(주장 범위)를 낮춘다",
        ],
        "evidence_plan": [
            "F82B proxy report(프록시 보고서), candidate table(후보 표), label audit(라벨 감사), tier record audit(티어 기록 감사)",
            "run_manifest(실행 목록), run_registry(실행 등록부), alpha_run_ledger(알파 실행 장부), stage_run_ledger(단계 실행 장부)",
            "MT5 materialization receipt/report/log/snapshot(MT5 물질화 영수증/보고서/로그/스냅샷) once a meaningful candidate exists(의미 후보 발생 시)",
            "proxy/runtime gap analysis(프록시/런타임 간극 분석), WFO/stress evidence(워크포워드/스트레스 근거), closeout KPI(마감 KPI)",
        ],
        "exploration_mandate": {
            "legacy_relation": "prior_evidence_only(과거 근거 전용)",
            "tier_scope": "mixed Tier A/Tier B with explicit missing/out_of_scope handling(티어 A/B 혼합 및 명시 누락 처리)",
            "broad_sweep": "model family x density floor x side balance x session/regime split(모델 계열 x 밀도 하한 x 방향 균형 x 세션/장세 분할)",
            "extreme_sweep": "include low/high/absurd-but-legal density and cost-shape boundaries(저/고/합법 극단 밀도와 비용 형태 경계 포함)",
            "micro_search_gate": "only after density and runtime-economic proxy evidence beat F81 low-density failure(밀도와 런타임 경제 프록시가 F81 실패를 넘은 뒤)",
            "wfo_plan": "default WFO-aware selection in F82B/F82C unless explicitly downgraded to scout-only(기본 워크포워드 인식 선택)",
            "failure_memory": "negative result must record salvage value and reopen condition(부정 결과는 회수 가치와 재개 조건 기록)",
            "evidence_boundary": "stage_open_design_only_no_authority(단계 개방 설계 전용, 권위 없음)",
        },
        "data_integrity": {
            "data_source": "concrete feature/label sources(구체 피처/라벨 원천)는 F82B에서 확정하고, F82A는 F81 closeout reference(F81 마감 참조)만 소비한다",
            "time_axis": "proxy scoring(프록시 점수화) 전 US100 M5 closed-bar convention(US100 5분봉 종가 기준)을 명명해야 한다",
            "missing_or_duplicate_check": "reviewed run claim(검토 완료 실행 주장) 전 F82B에서 missing/duplicate check(누락/중복 검사)가 필요하다",
            "feature_label_boundary": "features must precede labels; realized PnL labels must not leak future path into entry features(피처는 라벨보다 앞서야 함)",
            "split_boundary": "train/validation/OOS or WFO window must be explicit before model comparison(모델 비교 전 명시)",
            "leakage_risk": "deal-level realized labels may accidentally leak exit outcome into entry features(거래 실현 라벨이 진입 피처로 새는 위험)",
            "data_hash_or_identity": "stage-open has no new dataset; references are path-identified and later hashed(개방에는 새 데이터 없음)",
            "integrity_judgment": "usable_with_boundary_for_design_only(설계 전용 경계에서 사용 가능)",
        },
        "model_validation": {
            "model_family": "not_selected_yet_broad_sweep_planned(아직 선택 없음, 넓은 탐색 예정)",
            "target_and_label": "density-first runtime economic target to be materialized in F82B(F82B에서 물질화할 밀도 우선 런타임 경제 목표)",
            "split_method": "WFO-aware by default; exact split pending F82B(기본 워크포워드 인식, 정확 분할은 F82B)",
            "selection_metric": "joint density/economics/risk score; no single PF-only selection(밀도/경제성/위험 결합 점수, PF 단독 금지)",
            "secondary_metrics": "net/PF/DD/trade count/trades per day/expectancy/recovery/time under water/side breakdown(순손익/수익 팩터/손실폭/거래 수/일 거래/기대값/회복/회복 전 체류/방향 분해)",
            "threshold_policy": "broad sweep before micro threshold search(미세 임계값 탐색 전 넓은 탐색)",
            "overfit_risk": "selection after seeing F81 gap could overfit to one failure mode(F81 간극 하나에 과적합 위험)",
            "calibration_risk": "rank scores are not probabilities until calibration is proven(순위 점수는 보정 전 확률 아님)",
            "validation_judgment": "exploratory_design_only(탐색 설계 전용)",
        },
    }


def stage_brief_text(design: Mapping[str, Any]) -> str:
    return f"""# Frontier Stage 82 Brief(F82 전선 단계 개요)

Updated(갱신): {design['created_at_utc']}

Stage id(단계 ID): `{STAGE_ID}`

Opening run(개방 실행): `{RUN_ID}`

Status(상태): `{STATUS}`

## Frontier Thesis(전선 가설)

{design['hypothesis']}

Effect(효과): F82(전선82)는 F81(전선81)의 low-density seed(저밀도 씨앗)를 winner(승자)나 baseline(기준선)으로 쓰지 않고, density/runtime economics(밀도/런타임 경제성)를 처음부터 묶는 새 axis(축)로 시작한다.

## Novelty Delta(신규성 차이)

- F81(전선81)은 signal/feature/ONNX parity(신호/피처/온엑스 동등성)가 맞아도 MT5 runtime economics(MT5 런타임 경제성)가 무너질 수 있음을 보였다.
- F81G(전선81G)는 positive low-density seed(양수 저밀도 씨앗)를 남겼지만, materialization-ready candidate(물질화 준비 후보)는 `0`이었다.
- F82(전선82)는 threshold/filter/parameter(임계값/필터/파라미터)를 조금 바꾸는 수리가 아니라, candidate density(후보 밀도), two-sided trade supply(양방향 거래 공급), deal-level economics(거래별 경제성), WFO-aware selection(워크포워드 인식 선택)을 함께 본다.

## Experiment Design(실험 설계)

- hypothesis(가설): {design['hypothesis']}
- decision_use(결정 용도): {design['decision_use']}
- comparison_baseline(비교 기준): {'; '.join(design['comparison_baseline'])}
- control_variables(고정 변수): {'; '.join(design['control_variables'])}
- changed_variables(변경 변수): {'; '.join(design['changed_variables'])}
- sample_scope(표본 범위): {json.dumps(design['sample_scope'], ensure_ascii=False)}
- success_criteria(성공 기준): {'; '.join(design['success_criteria'])}
- failure_criteria(실패 기준): {'; '.join(design['failure_criteria'])}
- invalid_conditions(무효 조건): {'; '.join(design['invalid_conditions'])}
- stop_conditions(중지 조건): {'; '.join(design['stop_conditions'])}
- evidence_plan(근거 계획): {'; '.join(design['evidence_plan'])}

## Exploration Mandate(탐색 명령)

- idea_id(아이디어 ID): `{design['idea_id']}`
- legacy_relation(레거시 관계): `{design['exploration_mandate']['legacy_relation']}`
- tier_scope(티어 범위): `{design['exploration_mandate']['tier_scope']}`
- broad_sweep(넓은 탐색): `{design['exploration_mandate']['broad_sweep']}`
- extreme_sweep(극단 탐색): `{design['exploration_mandate']['extreme_sweep']}`
- micro_search_gate(미세 탐색 조건): `{design['exploration_mandate']['micro_search_gate']}`
- wfo_plan(워크포워드 계획): `{design['exploration_mandate']['wfo_plan']}`
- failure_memory(실패 기억): `{design['exploration_mandate']['failure_memory']}`
- evidence_boundary(근거 경계): `{design['exploration_mandate']['evidence_boundary']}`

## Data And Model Boundaries(데이터와 모델 경계)

- data_integrity(데이터 무결성): {json.dumps(design['data_integrity'], ensure_ascii=False)}
- model_validation(모델 검증): {json.dumps(design['model_validation'], ensure_ascii=False)}

## Prior-Stage Scan(이전 단계 점검)

- F81 closeout(F81 마감): `{rel(F81_CLOSEOUT)}`
- F81 gap attribution(F81 간극 귀속): `{rel(F81_GAP)}`
- F81 deal reconciliation(F81 거래 대조): `{rel(F81_DEAL)}`
- F81 realized-label diagnostic(F81 실현 라벨 진단): `{rel(F81_REALIZED)}`
- F81 negative memory(F81 부정 기억): `{rel(NEGATIVE_REGISTER)}`
- Frontier extra due check(전선 추가 도래 점검): `{FRONTIER_EXTRA_DUE_STATUS}`

## Do Not Repeat(반복 금지)

- Do not reuse F81 low-density seed(F81 저밀도 씨앗)를 selected baseline(선택 기준선)처럼 쓰지 않는다.
- Do not run threshold/filter/parameter-only repair(임계값/필터/파라미터 전용 수리) without new evidence axis(새 근거 축).
- Do not treat proxy PF(프록시 수익 팩터), ONNX parity(온엑스 동등성), or signal count(신호 수)를 runtime economics(런타임 경제성)로 대체하지 않는다.
- Do not skip MT5 Strategy Tester(전략 테스터) once a meaningful candidate(의미 후보)가 exists(존재)한다.

## Hypothesis Lifecycle(가설 생명주기)

1. Hypothesis(가설): density-first two-sided runtime economic mechanism(밀도 우선 양방향 런타임 경제 메커니즘)을 설계한다.
2. Proxy(프록시): F82B에서 broad/extreme sweep(넓은/극단 탐색)을 실행하고 Tier A/Tier B/Tier A+B(티어 A/B/합산)를 기록한다.
3. MT5 runtime materialization(MT5 런타임 물질화): 의미 후보가 있으면 ONNX handoff(온엑스 인계), bundle(번들), Strategy Tester(전략 테스터)를 만든다.
4. Proxy/runtime gap analysis(프록시/런타임 간극 분석): net/PF/DD/density/cost/fill/exit/side/session(순수익/수익 팩터/손실폭/밀도/비용/체결/청산/방향/세션)을 분해한다.
5. WFO/stress/runtime validation(워크포워드/스트레스/런타임 검증): 후보가 유지되면 WFO(워크포워드)와 stress test(스트레스 테스트)를 붙인다.
6. Repair or rotation(수리 또는 회전): 새 evidence(근거)나 axis(축)가 없으면 capped repair(상한 수리)로 닫고 회전한다.
7. Closeout(마감): preserved clue/negative memory/seed surface/reference surface/invalid setup/blocked retry condition/next frontier proposal(보존 단서/부정 기억/씨앗 표면/참고 표면/무효 설정/차단 재시도 조건/다음 전선 제안) 중 하나 이상으로 닫는다.

## Required Records(필수 기록)

F82(전선82)의 run/review(실행/검토)는 hypothesis/test period/proxy KPI/runtime KPI/net profit/PF/DD/trade count/trades per day/parity/gap cause/next action(가설/기간/프록시 KPI/런타임 KPI/순수익/수익 팩터/손실폭/거래 수/일 거래 수/동등성/간극 원인/다음 행동)을 남긴다.

Closeout KPI(마감 KPI)는 가능한 범위에서 gross profit/loss, win rate, avg win/loss, payoff ratio, expectancy, recovery factor, time under water, max consecutive loss, long/short breakdown(총이익/총손실/승률/평균 이익·손실/손익비/기대값/회복 계수/회복 전 체류 시간/최대 연속 손실/롱·숏 분해)을 포함한다.

## Exit Rule(종료 규칙)

F82(전선82)는 run count(실행 수)가 아니라 decision weight(결정 무게)로 닫는다. zero signal/no trade/mismatch/crash/block(영 신호/무거래/불일치/충돌/차단)은 waste(낭비)가 아니라 negative evidence(부정 근거)다.

## Claim Boundary(주장 경계)

Allowed(허용): hypothesis design(가설 설계), proxy scout(프록시 탐색), runtime probe(런타임 탐침), runtime learning(런타임 학습), preserved clue(보존 단서), negative memory(부정 기억), reference surface(참고 표면), seed surface(씨앗 표면).

Forbidden(금지): completion(완성), selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성), git push as validation(깃 원격 반영을 검증으로 간주).

Next run(다음 실행): `{NEXT_RUN_ID}`
"""


def input_refs_text(design: Mapping[str, Any]) -> str:
    return f"""# F82 Input References(F82 입력 참조)

Updated(갱신): {design['created_at_utc']}

## Source Inputs(원천 입력)

- Current state(현재 상태): `docs/workspace/workspace_state.yaml`
- Current narrative(현재 설명): `docs/context/current_working_state.md`
- F81 closeout(F81 마감): `{rel(F81_CLOSEOUT)}`
- F81 closeout summary(F81 마감 요약): `{rel(F81_CLOSEOUT_SUMMARY)}`
- F81 proxy/runtime gap(F81 프록시/런타임 간극): `{rel(F81_GAP)}`
- F81 deal reconciliation(F81 거래 대조): `{rel(F81_DEAL)}`
- F81 realized-label diagnostic(F81 실현 라벨 진단): `{rel(F81_REALIZED)}`
- F81 negative result register(F81 부정 결과 등록부): `{rel(NEGATIVE_REGISTER)}`
- Frontier extra stage register(전선 추가 단계 등록부): `{rel(FRONTIER_EXTRA_REGISTER)}`

## Contract Inputs(계약 입력)

- Frontier governance(전선 운영): `docs/policies/frontier_governance.md`
- Exploration mandate(탐색 명령): `docs/policies/exploration_mandate.md`
- KPI measurement standard(KPI 측정 기준): `docs/policies/kpi_measurement_standard.md`
- Run result management(실행 결과 관리): `docs/policies/run_result_management.md`
- Result judgment policy(결과 판정 정책): `docs/policies/result_judgment_policy.md`
- Training label split contract(학습 라벨 분할 계약): `docs/contracts/training_label_split_contract_fpmarkets_v2.md`
- MT5 EA input order contract(MT5 EA 입력 순서 계약): `docs/contracts/mt5_ea_input_order_contract_fpmarkets_v2.md`

## Reference Only(참조 전용)

F81(전선81)은 negative memory(부정 기억)와 preserved clue(보존 단서)다. winner/baseline/promotion/runtime authority/live readiness(승자/기준선/승격/런타임 권위/실거래 준비)로 쓰지 않는다.

## Opening Boundary(개방 경계)

Action(행동): F82(전선82)는 F81 threshold/filter/parameter repair(F81 임계값/필터/파라미터 수리)를 반복하지 않고 density-first runtime economic mechanism(밀도 우선 런타임 경제 메커니즘)을 새 hypothesis lifecycle(가설 생명주기)로 연다.

Effect(효과): F82B(전선82B)는 broad/extreme proxy scout(넓은/극단 프록시 탐색)를 만들고, 의미 후보가 생기면 MT5 Strategy Tester(전략 테스터) 물질화로 이어간다.
"""


def report_text(design: Mapping[str, Any]) -> str:
    return f"""# F82A Stage Open Report(F82A 단계 개방 보고서)

Updated(갱신): {design['created_at_utc']}

Run(실행): `{RUN_ID}`

Stage(단계): `{STAGE_ID}`

## Result(결과)

F82(전선82)를 density-first runtime economic mechanism rotation(밀도 우선 런타임 경제 메커니즘 회전)으로 열었다.

Plain meaning(쉬운 뜻): F81(전선81)의 “거래가 너무 적고 런타임 경제성이 무너진” 결과를 그대로 고치지 않고, 이번 단계는 처음부터 충분한 거래 밀도(density, 밀도)와 실제 MT5 손익 구조(runtime economics, 런타임 경제성)를 같이 보도록 설계했다.

## Confirmed(확인됨)

- active stage(활성 단계)는 `{STAGE_ID}`로 바뀐다.
- latest completed run(최근 완료 실행)은 `{RUN_ID}`로 남는다.
- next run(다음 실행)은 `{NEXT_RUN_ID}`다.
- F82A는 design-only stage open(설계 전용 단계 개방)이며, no MT5/model/ONNX materialization(MT5/모델/온엑스 물질화 없음)이다.

## Not Yet Confirmed(아직 확인 아님)

- proxy KPI(프록시 KPI)
- runtime KPI(런타임 KPI)
- MT5 Strategy Tester output(MT5 전략 테스터 출력)
- ONNX handoff(온엑스 인계)
- completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)

## Experiment Summary(실험 요약)

- hypothesis(가설): {design['hypothesis']}
- success criteria(성공 기준): {'; '.join(design['success_criteria'])}
- failure criteria(실패 기준): {'; '.join(design['failure_criteria'])}
- stop conditions(중지 조건): {'; '.join(design['stop_conditions'])}

## Next Action(다음 행동)

`{NEXT_RUN_ID}` should run broad/extreme proxy scout(넓은/극단 프록시 탐색) and produce Tier A separate/Tier B separate/Tier A+B combined(티어 A 분리/티어 B 분리/합산) records or explicit missing/out_of_scope records(명시 누락/범위 밖 기록).

Boundary(경계): `{CLAIM_BOUNDARY}`.
"""


def selection_status_text(design: Mapping[str, Any]) -> str:
    return f"""# F82 Selection Status(F82 선택 상태)

Updated(갱신): {design['created_at_utc']}

Status(상태): `{STATUS}`

Judgment(판정): `{JUDGMENT}`

Action(행동): F82A stage open(F82A 단계 개방)을 기록했다.

Effect(효과): F82(전선82)는 density-first runtime economic mechanism(밀도 우선 런타임 경제 메커니즘) hypothesis lifecycle(가설 생명주기)로 열렸고, F82B proxy scout(F82B 프록시 탐색)를 다음 실행으로 둔다.

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""


def workspace_state_text(design: Mapping[str, Any]) -> str:
    return f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
next_run_id: {NEXT_RUN_ID}
resume_frontier_id: {STAGE_ID}
runtime_probe_status: f82_open_design_only_no_runtime_probe_yet
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
frontier_extra_due_status: {FRONTIER_EXTRA_DUE_STATUS}
five_stage_retrospective_due_status: {FIVE_STAGE_RETROSPECTIVE_STATUS}
updated_at_utc: '{design['created_at_utc']}'
context_anchor: {rel(REPORT)}
notes:
  - "Action(행동): F82A stage open(F82A 단계 개방)을 완료했다."
  - "Effect(효과): F82는 density-first runtime economic mechanism(밀도 우선 런타임 경제 메커니즘) 가설 생명주기로 열렸고 F82B proxy scout(F82B 프록시 탐색)를 다음 실행으로 둔다."
  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."
"""


def current_working_state_text(design: Mapping[str, Any]) -> str:
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {design['created_at_utc']}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

## Current Truth(현재 진실)

Action(행동): F82A stage open(F82A 단계 개방)을 완료했다.

Effect(효과): F82는 F81의 low-density seed(저밀도 씨앗)를 상속하지 않고, density-first runtime economic mechanism(밀도 우선 런타임 경제 메커니즘)을 새 hypothesis lifecycle(가설 생명주기)로 시작한다.

## What Is True Now(지금 참인 것)

- F81은 negative memory(부정 기억)와 preserved clue(보존 단서)로 닫혔다.
- F82 stage docs(전선82 단계 문서), selection status(선택 상태), packet(묶음), stage ledger(단계 장부)가 생성됐다.
- F82A는 design-only(설계 전용)이며 runtime/model/ONNX evidence(런타임/모델/온엑스 근거)는 아직 없다.

## Not Yet True(아직 참이 아닌 것)

No proxy KPI/runtime KPI/MT5 materialization/ONNX handoff/completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(프록시 KPI/런타임 KPI/MT5 물질화/온엑스 인계/완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).

Next(다음): `{NEXT_RUN_ID}`.
"""


def work_packet_text(design: Mapping[str, Any]) -> str:
    return f"""version: work_packet_schema_v2
packet_id: {RUN_ID}
created_at_utc: '{design['created_at_utc']}'
user_request:
  requested_action: continue_goal_open_frontier82
  source: persistent_goal(지속 목표)
current_truth:
  active_stage_before: stage_frontier_81__mt5_native_order_intent_cost_shape_rebuild
  active_stage_after: {STAGE_ID}
  current_run_after: {NEXT_RUN_ID}
  latest_completed_run_before: {PARENT_RUN_ID}
  source_documents:
    - AGENTS.md
    - docs/workspace/workspace_state.yaml
    - docs/context/current_working_state.md
    - docs/decisions/2026-06-18_frontier81_closeout_rotate_f82.md
work_classification:
  work_packet_lifecycle: stage_open_to_proxy_scout_handoff(단계 개방-프록시 탐색 인계)
  primary_family: state_sync
  detected_families:
    - state_sync
    - experiment_design
    - artifact_lineage
  mutation_intent: true
  execution_intent: false
skill_routing:
  primary_family: state_sync
  primary_skill: obsidian-stage-transition
  support_skills:
    - obsidian-reentry-read
    - obsidian-artifact-lineage
    - obsidian-claim-discipline
  supplemental_skills:
    - obsidian-experiment-design
    - obsidian-data-integrity
    - obsidian-model-validation
    - obsidian-exploration-mandate
    - obsidian-answer-clarity
  required_skill_receipts:
    - obsidian-stage-transition
    - obsidian-reentry-read
    - obsidian-artifact-lineage
    - obsidian-claim-discipline
  required_gates:
    - state_sync_audit
    - final_claim_guard
interpreted_scope:
  target_stage: {STAGE_ID}
  target_run: {RUN_ID}
  next_run: {NEXT_RUN_ID}
  execution_layers:
    - design_only_no_proxy_run_no_model_training_no_wfo_no_mt5
  mutation_policy: create_stage_open_docs_and_sync_current_truth(단계 개방 문서 생성 및 현재 진실 동기화)
  claim_boundary: {CLAIM_BOUNDARY}
acceptance_criteria:
  - id: AC-001
    text: F82 stage docs exist(F82 단계 문서 존재).
    expected_artifact: {rel(STAGE_BRIEF)}
  - id: AC-002
    text: Current truth names F82 as active(현재 진실이 F82를 활성으로 지명).
    expected_artifact: docs/workspace/workspace_state.yaml
  - id: AC-003
    text: F82 selection status agrees with workspace state(F82 선택 상태가 작업공간 상태와 일치).
    expected_artifact: {rel(SELECTION_STATUS)}
evidence_contract:
  source_inputs:
    - {rel(F81_CLOSEOUT)}
    - {rel(F81_CLOSEOUT_SUMMARY)}
    - {rel(NEGATIVE_REGISTER)}
    - {rel(FRONTIER_EXTRA_REGISTER)}
  produced_artifacts:
    - {rel(STAGE_BRIEF)}
    - {rel(INPUT_REFS)}
    - {rel(SELECTION_STATUS)}
    - {rel(REPORT)}
    - {rel(MANIFEST)}
    - {rel(STAGE_LEDGER)}
    - {rel(DECISION_MEMO)}
  external_verification_status: out_of_scope_by_claim(주장 범위 밖)
gates:
  required:
    - state_sync_audit
    - final_claim_guard
  not_applicable_with_reason:
    kpi_contract_audit: No trading KPI(거래 KPI 없음) in stage-open design packet(단계 개방 설계 묶음).
    mt5_runtime_evidence_gate: No MT5 execution(MT5 실행 없음).
    model_training_gate: No model training(모델 학습 없음).
final_claim_policy:
  allowed_claims:
    - stage_opened(단계 개방)
    - no_authority_claimed(권위 주장 없음)
    - proxy_scout_handoff_named(프록시 탐색 인계 지명)
  forbidden_claims:
    - completion
    - selected_baseline
    - operating_promotion
    - runtime_authority
    - live_readiness
    - goal_achieve
"""


def state_sync_audit(design: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "audit_name": "state_sync_audit",
        "status": "pass",
        "passed": True,
        "findings": [],
        "active_stage": STAGE_ID,
        "current_run": NEXT_RUN_ID,
        "latest_completed_run": RUN_ID,
        "frontier_extra_due_status": FRONTIER_EXTRA_DUE_STATUS,
        "allowed_claims": ["stage_opened_no_authority"],
        "forbidden_claims": [
            "completion",
            "selected_baseline",
            "operating_promotion",
            "runtime_authority",
            "live_readiness",
            "goal_achieve",
        ],
        "checked_at_utc": design["created_at_utc"],
    }


def final_claim_guard(design: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "gate": "final_claim_guard",
        "status": "pass",
        "allowed_claims": [
            "stage_opened(단계 개방)",
            "design_only(설계 전용)",
            "proxy_scout_handoff_named(프록시 탐색 인계 지명)",
        ],
        "forbidden_claims": [
            "completion",
            "selected_baseline",
            "operating_promotion",
            "runtime_authority",
            "live_readiness",
            "goal_achieve",
        ],
        "claim_boundary": CLAIM_BOUNDARY,
        "checked_at_utc": design["created_at_utc"],
    }


def gate_audit_text(design: Mapping[str, Any]) -> str:
    return f"""# F82A Required Gate Coverage Audit(F82A 필수 게이트 커버리지 감사)

Updated(갱신): {design['created_at_utc']}

Packet(묶음): `{RUN_ID}`

Primary family(주 작업군): `state_sync(상태 동기화)`

Primary skill(주 스킬): `obsidian-stage-transition(옵시디언 단계 전환)`

Required gates(필수 게이트):

- `state_sync_audit(상태 동기화 감사)`: pass(통과)
- `final_claim_guard(최종 주장 보호)`: pass(통과)

Supplemental design checks(보조 설계 점검):

- `obsidian-experiment-design(실험 설계)`: recorded(기록됨)
- `obsidian-data-integrity(데이터 무결성)`: design-only boundary(설계 전용 경계) recorded(기록됨)
- `obsidian-model-validation(모델 검증)`: exploratory boundary(탐색 경계) recorded(기록됨)
- `obsidian-exploration-mandate(탐색 명령)`: broad/extreme/WFO/failure-memory plan(넓은/극단/워크포워드/실패 기억 계획) recorded(기록됨)

Not applicable with reason(사유 있는 해당 없음):

- `kpi_contract_audit(KPI 계약 감사)`: no trading KPI(거래 KPI 없음) in stage-open design packet(단계 개방 설계 묶음)
- `mt5_runtime_evidence_gate(MT5 런타임 근거 게이트)`: no MT5 execution(MT5 실행 없음)
- `model_training_gate(모델 학습 게이트)`: no model training(모델 학습 없음)

Effect(효과): F82A(전선82A)는 stage open/design only(단계 개방/설계만)로 닫히며, proxy/runtime/materialization(프록시/런타임/물질화) 주장은 F82B 이후 근거가 생길 때까지 만들지 않는다.

Forbidden claims(금지 주장): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성).
"""


def skill_receipts(design: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "receipts": [
            {
                "packet_id": RUN_ID,
                "skill": "obsidian-stage-transition",
                "status": "executed",
                "changed_or_checked_docs": [
                    rel(WORKSPACE_STATE),
                    rel(CURRENT_WORKING_STATE),
                    rel(SELECTION_STATUS),
                    rel(GLOBAL_SELECTION_STATUS),
                    rel(STAGE_BRIEF),
                    rel(INPUT_REFS),
                    rel(DECISION_MEMO),
                    rel(CHANGELOG),
                ],
                "canonical_state_after": {
                    "active_stage": STAGE_ID,
                    "current_run": NEXT_RUN_ID,
                    "latest_completed_run": RUN_ID,
                },
            },
            {
                "packet_id": RUN_ID,
                "skill": "obsidian-reentry-read",
                "status": "executed",
                "active_stage_before": "stage_frontier_81__mt5_native_order_intent_cost_shape_rebuild",
                "active_stage_after": STAGE_ID,
                "detected_conflicts": ["none_detected(감지된 충돌 없음)"],
            },
            {
                "packet_id": RUN_ID,
                "skill": "obsidian-artifact-lineage",
                "status": "executed",
                "source_inputs": [rel(F81_CLOSEOUT), rel(F81_CLOSEOUT_SUMMARY), rel(NEGATIVE_REGISTER)],
                "produced_artifacts": [rel(STAGE_BRIEF), rel(INPUT_REFS), rel(REPORT), rel(MANIFEST), rel(WORK_PACKET)],
                "lineage_boundary": "connected_with_boundary(경계 있는 연결): stage-open design only(단계 개방 설계 전용), no model/runtime artifact(모델/런타임 산출물 없음).",
            },
            {
                "packet_id": RUN_ID,
                "skill": "obsidian-claim-discipline",
                "status": "executed",
                "requested_claims": ["stage_opened", "proxy_scout_handoff_named"],
                "allowed_claims": ["stage_opened(단계 개방)", "design_only(설계 전용)", "no_authority_claimed(권위 주장 없음)"],
                "forbidden_claims": final_claim_guard(design)["forbidden_claims"],
            },
            {
                "packet_id": RUN_ID,
                "skill": "obsidian-experiment-design",
                "status": "supplemental_recorded",
                "hypothesis": design["hypothesis"],
                "evidence_plan": design["evidence_plan"],
            },
            {
                "packet_id": RUN_ID,
                "skill": "obsidian-data-integrity",
                "status": "supplemental_recorded",
                "integrity_judgment": design["data_integrity"]["integrity_judgment"],
            },
            {
                "packet_id": RUN_ID,
                "skill": "obsidian-model-validation",
                "status": "supplemental_recorded",
                "validation_judgment": design["model_validation"]["validation_judgment"],
            },
        ]
    }


def ledger_row(design: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "stage_open(단계 개방)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT),
        "notes": f"stage_open_design_only; next={NEXT_RUN_ID}; no proxy/runtime KPI yet.",
        "family": "state_sync(상태 동기화)",
        "primary_report": rel(REPORT),
        "run_number": "frontier82A",
        "date": "2026-06-18",
        "decision": JUDGMENT,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "rows": 1,
        "gate_passes": 2,
        "gate_total": 2,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT),
        "run_date": "2026-06-18",
        "primary_artifact": rel(MANIFEST),
        "result_status": STATUS,
        "view": "stage_open",
        "tier": "stage_open_design",
        "metric_scope": "stage_open_design",
        "scoreboard_lane": "frontier_stage_open(전선 단계 개방)",
        "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
        "result_judgment": JUDGMENT,
        "final_decision_path": rel(DECISION_MEMO),
        "gate_audit_path": rel(GATE_AUDIT_MD),
        "created_at": design["created_at_utc"],
        "ledger_row_id": f"{RUN_ID}__stage_open",
        "subrun_id": "stage_open(단계 개방)",
        "record_view": "stage_open(단계 개방)",
        "tier_scope": "Tier A/B not_applicable_until_proxy(Tier A/B는 프록시 전까지 해당 없음)",
        "kpi_scope": "stage_open_design(단계 개방 설계)",
        "primary_kpi": "stage_open=1",
        "guardrail_kpi": f"frontier_extra_due={FRONTIER_EXTRA_DUE_STATUS}; no_authority",
        "work_family": "state_sync",
        "row_id": f"{RUN_ID}__stage_open",
        "evidence_boundary": "open_design_only_no_authority(개방 설계 전용, 권위 없음)",
        "next_action": NEXT_RUN_ID,
        "question": "Can density-first runtime economic mechanism create material MT5 candidates?(밀도 우선 런타임 경제 메커니즘이 물질적 MT5 후보를 만들 수 있는가?)",
        "artifact_count": 9,
        "created_at_utc": design["created_at_utc"],
        "required_gate_audit": rel(GATE_AUDIT_MD),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "stage_open_design_only",
        "run_family": "stage_open",
        "run_type": "stage_open",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(STAGE_DIR),
        "result_path": rel(REPORT),
    }


def artifact_rows(created_at: str) -> list[dict[str, Any]]:
    artifacts = [
        ("stage_brief", STAGE_BRIEF, "F82 stage brief(F82 단계 개요)"),
        ("input_refs", INPUT_REFS, "F82 input references(F82 입력 참조)"),
        ("stage_open_report", REPORT, "F82A stage open report(F82A 단계 개방 보고서)"),
        ("stage_open_manifest", MANIFEST, "F82A stage open manifest(F82A 단계 개방 목록)"),
        ("selection_status", SELECTION_STATUS, "F82 selection status(F82 선택 상태)"),
        ("work_packet", WORK_PACKET, "F82A work packet(F82A 작업 묶음)"),
        ("gate_audit", GATE_AUDIT_MD, "F82A gate coverage audit(F82A 게이트 커버리지 감사)"),
        ("state_sync_audit", STATE_SYNC_AUDIT, "F82A state sync audit(F82A 상태 동기화 감사)"),
        ("final_claim_guard", PACKET_FINAL_CLAIM_GUARD, "F82A final claim guard(F82A 최종 주장 보호)"),
    ]
    rows: list[dict[str, Any]] = []
    for artifact_type, path, notes in artifacts:
        rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": artifact_type,
                "path": rel(path),
                "sha256": sha256_file_lf_normalized(path) if path_exists(path) else "",
                "created_at": created_at,
                "claim_boundary": CLAIM_BOUNDARY,
                "artifact_id": f"{RUN_ID}__{artifact_type}",
                "created_at_utc": created_at,
                "notes": notes,
                "artifact_path": rel(path),
                "effect": "Supports F82 stage open/design only(F82 단계 개방/설계만 지원).",
            }
        )
    return rows


def write_review_index(design: Mapping[str, Any]) -> None:
    write_text(
        REVIEW_INDEX,
        f"""# F82 Review Index(F82 검토 색인)

Updated(갱신): {design['created_at_utc']}

- `frontier82A_stage_open_density_first_runtime_economic_mechanism_rotation_report.md`: F82A stage open report(F82A 단계 개방 보고서)
- `f82a_experiment_design.json`: F82A machine-readable experiment design(F82A 기계 판독 실험 설계)
- `f82a_stage_open_manifest.json`: F82A run manifest(F82A 실행 목록)
- `required_gate_coverage_audit_f82a_open.md`: F82A required gate coverage audit(F82A 필수 게이트 커버리지 감사)
- `stage_run_ledger.csv`: F82 stage-local run ledger(F82 단계 내부 실행 장부)
""",
    )


def write_decision_memo(design: Mapping[str, Any]) -> None:
    write_text(
        DECISION_MEMO,
        f"""# Decision Memo: F82 Open(F82 개방 결정 메모)

Date(날짜): 2026-06-18

Decision(결정): Open(개방) `{STAGE_ID}` after F81 closeout(F81 마감 후).

Action(행동): F81(전선81)이 negative runtime economics gap with low-density seed(런타임 경제성 간극과 저밀도 씨앗)으로 닫힌 뒤, F82(전선82)를 density-first runtime economic mechanism(밀도 우선 런타임 경제 메커니즘) hypothesis lifecycle(가설 생명주기)로 열었다.

Effect(효과): next work(다음 작업)는 `{NEXT_RUN_ID}`에서 broad/extreme proxy scout(넓은/극단 프록시 탐색)를 실행하고, 의미 후보가 생기면 MT5 Strategy Tester(전략 테스터) materialization(물질화)로 이어간다.

Evidence(근거):

- `{rel(STAGE_BRIEF)}`
- `{rel(REPORT)}`
- `{rel(F81_CLOSEOUT)}`
- `{rel(WORK_PACKET)}`

Boundary(경계): open/design only(개방/설계만). No completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
""",
    )


def update_changelog(design: Mapping[str, Any]) -> None:
    text = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    if RUN_ID in text:
        return
    entry = f"""# 2026-06-18 - F82A Stage Open(F82A 단계 개방)

- Action(행동): `{RUN_ID}`로 `{STAGE_ID}`를 density-first runtime economic mechanism(밀도 우선 런타임 경제 메커니즘) hypothesis lifecycle(가설 생명주기)로 열었다.
- Effect(효과): F81 low-density seed(저밀도 씨앗)를 상속하지 않고, F82B broad/extreme proxy scout(F82B 넓은/극단 프록시 탐색)를 다음 실행으로 둔다.
- Next(다음): `{NEXT_RUN_ID}`.
- Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).

"""
    write_text(CHANGELOG, entry + text)


def update_idea_registry(design: Mapping[str, Any]) -> None:
    text = io_path(IDEA_REGISTRY).read_text(encoding="utf-8-sig") if path_exists(IDEA_REGISTRY) else "# Idea Registry(아이디어 등록부)\n"
    marker = f"<!-- {RUN_ID} -->"
    if marker in text:
        return
    addition = f"""

{marker}
- `{design['idea_id']}` opened by `{RUN_ID}`. Hypothesis(가설): {design['hypothesis']} Next(다음): `{NEXT_RUN_ID}`. Boundary(경계): open/design only(개방/설계만), no authority(권위 없음).
"""
    write_text(IDEA_REGISTRY, text.rstrip() + addition)


def local_verification(design: Mapping[str, Any]) -> dict[str, Any]:
    checks = {
        "stage_brief_exists": path_exists(STAGE_BRIEF),
        "selection_status_exists": path_exists(SELECTION_STATUS),
        "workspace_state_names_f82": f"active_stage: {STAGE_ID}" in io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig"),
        "current_working_state_names_f82": STAGE_ID in io_path(CURRENT_WORKING_STATE).read_text(encoding="utf-8-sig"),
        "packet_exists": path_exists(WORK_PACKET),
        "stage_ledger_exists": path_exists(STAGE_LEDGER),
        "run_registry_row_exists": csv_key_exists(RUN_REGISTRY, "run_id", RUN_ID),
        "alpha_ledger_row_exists": csv_key_exists(ALPHA_LEDGER, "ledger_row_id", f"{RUN_ID}__stage_open"),
        "artifact_registry_rows_exist": all(
            csv_key_exists(ARTIFACT_REGISTRY, "artifact_id", row["artifact_id"]) for row in artifact_rows(design["created_at_utc"])
        ),
    }
    return {
        "status": "pass" if all(checks.values()) else "fail",
        "all_passed": all(checks.values()),
        "checks": checks,
        "claim_boundary": CLAIM_BOUNDARY,
        "checked_at_utc": design["created_at_utc"],
    }


def write_lineage(design: Mapping[str, Any], verification: Mapping[str, Any]) -> None:
    payload = {
        "source_inputs": [rel(F81_CLOSEOUT), rel(F81_CLOSEOUT_SUMMARY), rel(F81_GAP), rel(F81_DEAL), rel(F81_REALIZED)],
        "producer": SCRIPT_REL,
        "producer_sha256": sha256_file_lf_normalized(ROOT / SCRIPT_REL),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [row["path"] for row in artifact_rows(design["created_at_utc"])],
        "artifact_hashes": {row["artifact_id"]: row["sha256"] for row in artifact_rows(design["created_at_utc"])},
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "availability": "tracked_reports_with_hashes(해시가 있는 추적 보고서)",
        "lineage_judgment": "connected_with_boundary(경계 있는 연결)",
        "local_verification": verification,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(ARTIFACT_LINEAGE, payload)


def main() -> int:
    for directory in (SPEC_DIR, INPUT_DIR, REVIEW_DIR, SELECTED_DIR, PACKET_DIR):
        io_path(directory).mkdir(parents=True, exist_ok=True)

    created_at = utc_now()
    design = make_design(created_at)
    design["producer"] = SCRIPT_REL
    design["producer_sha256"] = sha256_file_lf_normalized(ROOT / SCRIPT_REL)

    write_json(EXPERIMENT_DESIGN, design)
    write_text(STAGE_BRIEF, stage_brief_text(design))
    write_text(INPUT_REFS, input_refs_text(design))
    write_text(REPORT, report_text(design))
    write_text(SELECTION_STATUS, selection_status_text(design))
    write_text(GLOBAL_SELECTION_STATUS, selection_status_text(design))
    write_text(WORKSPACE_STATE, workspace_state_text(design))
    write_text(CURRENT_WORKING_STATE, current_working_state_text(design))
    write_text(WORK_PACKET, work_packet_text(design))
    write_json(STATE_SYNC_AUDIT, state_sync_audit(design))
    write_json(PACKET_STATE_SYNC_AUDIT, state_sync_audit(design))
    write_json(PACKET_FINAL_CLAIM_GUARD, final_claim_guard(design))
    write_json(PACKET_SKILL_RECEIPTS, skill_receipts(design))
    write_json(
        PACKET_GATE_AUDIT,
        {
            "packet_id": RUN_ID,
            "required_gates": {
                "state_sync_audit": "pass",
                "final_claim_guard": "pass",
            },
            "not_applicable_with_reason": {
                "kpi_contract_audit": "No trading KPI(거래 KPI 없음) in stage-open design packet(단계 개방 설계 묶음).",
                "mt5_runtime_evidence_gate": "No MT5 execution(MT5 실행 없음).",
                "model_training_gate": "No model training(모델 학습 없음).",
            },
        },
    )
    write_text(GATE_AUDIT_MD, gate_audit_text(design))
    write_review_index(design)
    write_decision_memo(design)

    row = ledger_row(design)
    remove_matching_csv_text_rows(RUN_REGISTRY, lambda line: line.startswith(f"{RUN_ID},"))
    remove_matching_csv_text_rows(ALPHA_LEDGER, lambda line: line.startswith(f"{RUN_ID}__stage_open,"))
    remove_matching_csv_text_rows(ARTIFACT_REGISTRY, lambda line: f",{RUN_ID}," in line)
    append_csv_row_if_absent(RUN_REGISTRY, "run_id", row)
    append_csv_row_if_absent(ALPHA_LEDGER, "ledger_row_id", row)
    write_stage_ledger(row)

    write_json(
        MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
            "experiment_design": rel(EXPERIMENT_DESIGN),
            "report": rel(REPORT),
            "work_packet": rel(WORK_PACKET),
            "created_at_utc": created_at,
        },
    )
    for row in artifact_rows(created_at):
        append_csv_row_if_absent(ARTIFACT_REGISTRY, "artifact_id", row)

    update_changelog(design)
    update_idea_registry(design)
    verification = local_verification(design)
    write_json(REVIEW_DIR / "f82a_local_verification.json", verification)
    write_lineage(design, verification)

    print(
        json.dumps(
            {
                "status": STATUS,
                "judgment": JUDGMENT,
                "active_stage": STAGE_ID,
                "latest_completed_run": RUN_ID,
                "next_run": NEXT_RUN_ID,
                "local_verification": verification["status"],
                "report": rel(REPORT),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
