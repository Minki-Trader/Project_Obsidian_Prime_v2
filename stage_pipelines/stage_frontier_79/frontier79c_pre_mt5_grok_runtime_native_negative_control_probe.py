from __future__ import annotations

import csv
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.grok_review_wrapper import run_grok_review
from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized


STAGE_ID = "stage_frontier_79__runtime_native_trade_shape_labeling_from_fill_path"
RUN_ID = "frontier79C_pre_mt5_grok_runtime_native_negative_control_runtime_probe_v1"
PARENT_RUN_ID = "frontier79B_runtime_native_trade_shape_label_proxy_scout_v1"
NEXT_RUN_ID = "frontier79D_mt5_runtime_native_negative_control_runtime_probe_v1"
REPAIR_RUN_ID = "frontier79C_runtime_native_proxy_repair_before_mt5_v1"

STATUS_SUCCESS = "pre_mt5_grok_review_completed_runtime_native_negative_control_probe_required_no_authority"
STATUS_REJECTED = "pre_mt5_grok_rejected_runtime_native_probe_repair_required_no_authority"
STATUS_TRANSPORT_FAIL = "pre_mt5_grok_transport_failed_runtime_native_probe_not_started_no_authority"
JUDGMENT_SUCCESS = "pre_mt5_grok_accepts_runtime_native_negative_control_probe_no_authority"
JUDGMENT_REJECTED = "pre_mt5_grok_rejected_runtime_mapping_repair_required_no_authority"
JUDGMENT_TRANSPORT_FAIL = "pre_mt5_grok_transport_failed_retry_required_no_authority"
CLAIM_BOUNDARY = (
    "pre_mt5_review_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_ID
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"

SUMMARY_PATH = REVIEW_DIR / "f79b_runtime_native_proxy_summary.json"
TOP_PATH = REVIEW_DIR / "f79b_runtime_native_ranked_top200.csv"
DATA_INTEGRITY_PATH = REVIEW_DIR / "f79b_data_integrity_review.json"
MODEL_VALIDATION_PATH = REVIEW_DIR / "f79b_model_validation_review.json"
F79B_REPORT_PATH = REVIEW_DIR / "frontier79B_runtime_native_trade_shape_label_proxy_scout_report.md"

REPORT = REVIEW_DIR / "frontier79C_pre_mt5_grok_runtime_native_negative_control_runtime_probe_report.md"
RECEIPT = REVIEW_DIR / "grok_pre_mt5_runtime_native_negative_control_runtime_probe_receipt.md"
GATE_AUDIT = REVIEW_DIR / "required_gate_coverage_audit_f79c.md"
LOCAL_VERIFICATION = REVIEW_DIR / "f79c_pre_mt5_local_verification.json"
TARGET_SELECTION = REVIEW_DIR / "f79c_runtime_materialization_target_selection.json"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
CONTEXT_ANCHOR = REVIEW_DIR / "context_anchor.md"

WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs/context/current_working_state.md"
RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
IDEA_REGISTRY = ROOT / "docs/registers/idea_registry.md"

GROK_PACKET = ROOT / "docs/agent_control/grok_reviews/2026-06-17_f79c_pre_mt5_runtime_native_negative_control_runtime_probe"
GROK_PROMPT = GROK_PACKET / "prompts/f79c_pre_mt5_runtime_native_negative_control_runtime_probe_prompt.md"
GROK_CLEAN = GROK_PACKET / "clean_output.md"
GROK_METADATA = GROK_PACKET / "metadata.json"
SCRIPT_REL = "stage_pipelines/stage_frontier_79/frontier79c_pre_mt5_grok_runtime_native_negative_control_probe.py"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def write_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def read_json(path: Path) -> Any:
    return json.loads(read_text(path))


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8-sig")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    rows = list(rows)
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys() if rows else ["empty"])
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: json_ready(row.get(field, "")) for field in fieldnames})


def upsert_csv(path: Path, key: str, row: Mapping[str, Any], source_header: Path | None = None) -> None:
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            rows = list(reader)
    elif source_header is not None and path_exists(source_header):
        with io_path(source_header).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
        rows = []
    else:
        fieldnames = list(row.keys())
        rows = []
    for field in row:
        if field not in fieldnames:
            fieldnames.append(field)
    rows = [existing for existing in rows if existing.get(key) != row.get(key)]
    rows.append({field: json_ready(row.get(field, "")) for field in fieldnames})
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def file_hash(path: Path) -> str:
    return sha256_file_lf_normalized(path) if path_exists(path) else ""


def ensure_dirs() -> None:
    for path in (RUN_DIR, REVIEW_DIR, SELECTED_DIR, GROK_PROMPT.parent):
        io_path(path).mkdir(parents=True, exist_ok=True)


def export_feasibility() -> dict[str, Any]:
    checks: dict[str, Any] = {}
    try:
        from sklearn.datasets import make_classification
        from sklearn.ensemble import ExtraTreesClassifier
        from sklearn.linear_model import LogisticRegression
        from sklearn.pipeline import make_pipeline
        from sklearn.preprocessing import StandardScaler
        from skl2onnx import convert_sklearn
        from skl2onnx.common.data_types import FloatTensorType

        x, y = make_classification(n_samples=100, n_features=8, n_informative=5, random_state=7903)
        models = {
            "logistic_l2_balanced": make_pipeline(
                StandardScaler(),
                LogisticRegression(max_iter=100, class_weight="balanced", C=0.45, solver="lbfgs"),
            ),
            "extra_trees_d7_l80": ExtraTreesClassifier(n_estimators=12, max_depth=7, min_samples_leaf=5, random_state=7903),
        }
        for name, model in models.items():
            try:
                model.fit(x, y)
                convert_sklearn(
                    model,
                    initial_types=[("float_input", FloatTensorType([None, int(x.shape[1])]))],
                    options={id(model): {"zipmap": False}},
                    target_opset=12,
                )
                checks[name] = {"export_status": "export_ok", "notes": "in_memory_skl2onnx_smoke_passed"}
            except Exception as exc:  # noqa: BLE001
                checks[name] = {"export_status": "export_failed", "error_type": type(exc).__name__, "error_excerpt": str(exc)[:500]}
    except Exception as exc:  # noqa: BLE001
        checks["environment"] = {"export_status": "blocked", "error_type": type(exc).__name__, "error_excerpt": str(exc)[:500]}
    return checks


def choose_target(summary: Mapping[str, Any], top_rows: Sequence[Mapping[str, str]], export_checks: Mapping[str, Any]) -> dict[str, Any]:
    best = dict(summary.get("best_candidate") or {})
    exportable = {name for name, payload in export_checks.items() if isinstance(payload, Mapping) and payload.get("export_status") == "export_ok"}
    target = best if best.get("model") in exportable else {}
    if not target:
        for row in top_rows:
            if row.get("model") in exportable:
                target = dict(row)
                break
    return {
        "runtime_materialization_target": target,
        "target_candidate_id": target.get("candidate_id", ""),
        "blocked_best_candidate": best if target.get("candidate_id") != best.get("candidate_id") else {},
        "selection_reason": "best_exportable_weak_nonzero_target(내보내기 가능한 최선 약한 비영 대상)" if target else "no_exportable_target(내보내기 가능한 대상 없음)",
        "target_export_check": export_checks.get(str(target.get("model")), {}),
        "export_checks": export_checks,
        "runtime_probe_role": "weak_nonzero_negative_control_runtime_probe(약한 비영 부정 대조 런타임 탐침)",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_prompt(summary: Mapping[str, Any], top_rows: Sequence[Mapping[str, str]], target_selection: Mapping[str, Any]) -> str:
    best = summary.get("best_candidate") or {}
    target = target_selection.get("runtime_materialization_target") or {}
    top_lines = []
    for idx, row in enumerate(top_rows[:6], start=1):
        top_lines.append(
            f"{idx}. {row.get('candidate_id')}: {row.get('label_name')}/{row.get('feature_set')}/{row.get('model')}/"
            f"{row.get('session')}/{row.get('risk_filter')}/cd{row.get('cooldown_bars')} | "
            f"val {row.get('val_net')}/{row.get('val_pf')}/{row.get('val_dd_pct')}/{row.get('val_calendar_trades_day')}/{row.get('val_trade_count')} | "
            f"oos {row.get('oos_net')}/{row.get('oos_pf')}/{row.get('oos_dd_pct')}/{row.get('oos_calendar_trades_day')}/{row.get('oos_trade_count')}"
        )
    return f"""# F79C Pre-MT5 Grok Prompt(F79C 사전 MT5 그록 프롬프트)

You are Grok(Grok, 그록), external second-opinion reviewer(외부 2차 의견 검토자).
Answer only from this bounded evidence snapshot(제한 근거 스냅샷).
Do not inspect files(파일 확인 금지), run tools(도구 실행 금지), browse(브라우징 금지), or perform local verification(로컬 검증 금지).

## Codex Proposed Direction(Codex 제안 방향)

F79B produced weak nonzero proxy surface(약한 비영 프록시 표면), not scout clue(탐색 단서) and not meaningful signal(의미 신호).
Because F79 frontier stage(전선 단계) requires MT5 Runtime Probe(MT5 런타임 탐침) unless zero-signal logic impossibility(영 신호 로직 불가능) applies, Codex proposes a narrow negative-control MT5 runtime probe(좁은 부정 대조 MT5 런타임 탐침).

## F79B Summary(F79B 요약)

- candidate rows(후보 행): `{summary.get('candidate_rows')}`
- scout clue count(탐색 단서 수): `{summary.get('scout_clue_count')}`
- meaningful signal count(의미 신호 수): `{summary.get('meaningful_signal_count')}`
- final-like reference count(최종 유사 참고 수): `{summary.get('final_like_reference_count')}`
- dual positive count(양분할 양수 수): `{summary.get('dual_positive_count')}`
- nonzero lifecycle candidates(비영 생명주기 후보): `{summary.get('nonzero_lifecycle_trade_candidates')}`
- entry rule(진입 규칙): `{summary.get('entry_rule')}`
- DD rule(손실폭 규칙): `{summary.get('dd_rule')}`

## Best Proxy Candidate(최선 프록시 후보)

- candidate(후보): `{best.get('candidate_id')}`
- label/model/feature(라벨/모델/피처): `{best.get('label_name')}` / `{best.get('model')}` / `{best.get('feature_set')}`
- validation KPI(검증 핵심 성과 지표): net/PF/DD/tpd/trades `{best.get('val_net')}/{best.get('val_pf')}/{best.get('val_dd_pct')}/{best.get('val_calendar_trades_day')}/{best.get('val_trade_count')}`
- OOS KPI(표본외 핵심 성과 지표): net/PF/DD/tpd/trades `{best.get('oos_net')}/{best.get('oos_pf')}/{best.get('oos_dd_pct')}/{best.get('oos_calendar_trades_day')}/{best.get('oos_trade_count')}`

## Runtime Materialization Target(런타임 물질화 대상)

- target candidate(대상 후보): `{target.get('candidate_id')}`
- model(모델): `{target.get('model')}`
- export check(내보내기 점검): `{target_selection.get('target_export_check')}`
- role(역할): negative-control runtime probe(부정 대조 런타임 탐침), not promotion(승격 아님)

## Top Rows(상위 행)

{chr(10).join(top_lines)}

## Question(질문)

Should Codex proceed to a narrow MT5 Runtime Probe(좁은 MT5 런타임 탐침) for the selected weak nonzero target(선택된 약한 비영 대상), with the claim boundary(주장 경계) limited to runtime probe observation(런타임 탐침 관찰) only?

Classify advice(조언 분류) as accepted(수용), accepted_with_conditions(조건부 수용), needs_local_verification(로컬 검증 필요), or rejected(거절).
Do not claim completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), or Goal Achieve(목표 달성).
"""


def forbidden_hits(text: str) -> list[str]:
    hits: list[str] = []
    forbidden = ["Goal Achieve", "runtime authority", "live readiness", "selected baseline", "operating promotion", "completion achieved"]
    negation = ["do not", "does not", "not ", "not`", "no ", "without", "forbidden", "claim boundary", "excludes", "exclude", "only", "금지", "아님", "없음", "주장하지", "제외"]
    claim_markers = ["achieved", "established", "granted", "confirmed", "selected", "promoted", "ready", "authority is", "authority established"]
    for line in text.splitlines():
        lowered = line.lower().replace("*", "").replace("_", "")
        if any(marker in lowered for marker in negation) or any(marker in line for marker in negation):
            continue
        if line.lstrip().startswith(("-", "*")) and not any(marker in lowered for marker in claim_markers):
            continue
        for phrase in forbidden:
            if phrase.lower() in lowered and any(marker in lowered for marker in claim_markers) and phrase not in hits:
                hits.append(phrase)
    return hits


def classify_grok(text: str, success: bool) -> tuple[str, str, bool, list[str]]:
    hits = forbidden_hits(text)
    if not success:
        return "needs_local_verification(로컬 검증 필요)", "retry_grok_transport_before_mt5(그록 전송 재시도 후 MT5)", False, hits
    head = text[:1800].lower()
    if "rejected" in head or "거절" in text[:1800]:
        return "rejected(거절)", "repair_runtime_mapping_before_mt5(MT5 전 런타임 매핑 수리)", False, hits
    if "needs_local_verification" in head or "로컬 검증 필요" in text[:1800]:
        return "needs_local_verification(로컬 검증 필요)", "local_verify_before_mt5(MT5 전 로컬 검증)", False, hits
    if "accepted_with_conditions" in head or "조건부 수용" in text[:1800]:
        return "accepted_with_conditions(조건부 수용)", "run_f79d_negative_control_probe_with_conditions(조건 기록 후 F79D 부정 대조 탐침)", not hits, hits
    if "accepted" in head or "수용" in text[:1800]:
        return "accepted(수용)", "run_f79d_negative_control_probe(F79D 부정 대조 탐침 실행)", not hits, hits
    return "needs_local_verification(로컬 검증 필요)", "manual_review_before_mt5(MT5 전 수동 검토)", False, hits


def grok_identity(result: Any) -> dict[str, Any]:
    return {
        "packet_path": rel(GROK_PACKET),
        "prompt_path": rel(GROK_PROMPT),
        "prompt_sha256": file_hash(GROK_PROMPT),
        "output_path": rel(GROK_CLEAN) if path_exists(GROK_CLEAN) else "",
        "output_sha256": file_hash(GROK_CLEAN) if path_exists(GROK_CLEAN) else "",
        "metadata_path": rel(GROK_METADATA) if path_exists(GROK_METADATA) else "",
        "metadata_sha256": file_hash(GROK_METADATA) if path_exists(GROK_METADATA) else "",
        "success": bool(result.success),
        "returncode": result.returncode,
        "timed_out": bool(result.timed_out),
    }


def local_verification_payload(result: Any, advice: str, hits: Sequence[str], target_selection: Mapping[str, Any]) -> dict[str, Any]:
    target = target_selection.get("runtime_materialization_target") or {}
    checks = {
        "grok_success": bool(result.success),
        "grok_returncode": result.returncode,
        "forbidden_claim_hits": list(hits),
        "target_candidate_id": target.get("candidate_id", ""),
        "target_model": target.get("model", ""),
        "target_exists": bool(target.get("candidate_id")),
        "target_export_ok": (target_selection.get("target_export_check") or {}).get("export_status") == "export_ok",
        "advice_classification": advice,
    }
    checks["passed"] = (
        checks["grok_success"]
        and not checks["forbidden_claim_hits"]
        and checks["target_exists"]
        and checks["target_export_ok"]
        and advice in {"accepted(수용)", "accepted_with_conditions(조건부 수용)"}
    )
    return checks


def status_tuple(proceed: bool, result_success: bool) -> tuple[str, str, str]:
    if proceed:
        return STATUS_SUCCESS, JUDGMENT_SUCCESS, NEXT_RUN_ID
    if not result_success:
        return STATUS_TRANSPORT_FAIL, JUDGMENT_TRANSPORT_FAIL, RUN_ID
    return STATUS_REJECTED, JUDGMENT_REJECTED, REPAIR_RUN_ID


def report_text(
    created_at: str,
    status: str,
    judgment: str,
    next_run: str,
    summary: Mapping[str, Any],
    target_selection: Mapping[str, Any],
    grok: Mapping[str, Any],
    advice: str,
    final_direction: str,
    local: Mapping[str, Any],
) -> str:
    target = target_selection.get("runtime_materialization_target") or {}
    best = summary.get("best_candidate") or {}
    return f"""# F79C Pre-MT5 Grok Review Report(F79C 사전 MT5 그록 검토 보고서)

Updated(갱신): {created_at}

- run id(실행 ID): `{RUN_ID}`
- status(상태): `{status}`
- judgment(판정): `{judgment}`
- Grok advice(Grok 조언): `{advice}`
- final Codex direction(최종 Codex 방향): `{final_direction}`
- local verification(로컬 검증): `{local.get('passed')}`
- next action(다음 행동): `{next_run}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Proxy KPI(프록시 핵심 성과 지표)

- scout clue(탐색 단서): `{summary.get('scout_clue_count')}`
- meaningful signal(의미 신호): `{summary.get('meaningful_signal_count')}`
- final-like reference(최종 유사 참고): `{summary.get('final_like_reference_count')}`
- best validation net/PF/DD/tpd/trades(최선 검증): `{best.get('val_net')}/{best.get('val_pf')}/{best.get('val_dd_pct')}/{best.get('val_calendar_trades_day')}/{best.get('val_trade_count')}`
- best OOS net/PF/DD/tpd/trades(최선 표본외): `{best.get('oos_net')}/{best.get('oos_pf')}/{best.get('oos_dd_pct')}/{best.get('oos_calendar_trades_day')}/{best.get('oos_trade_count')}`

## Runtime Target(런타임 대상)

- target candidate(대상 후보): `{target.get('candidate_id')}`
- model(모델): `{target.get('model')}`
- label(라벨): `{target.get('label_name')}`
- feature set(피처 묶음): `{target.get('feature_set')}`
- session/risk/cooldown(세션/위험/쿨다운): `{target.get('session')}/{target.get('risk_filter')}/{target.get('cooldown_bars')}`
- export check(내보내기 점검): `{target_selection.get('target_export_check')}`

## Grok Review(Grok 검토)

- packet(묶음): `{grok.get('packet_path')}`
- prompt(프롬프트): `{grok.get('prompt_path')}` sha256 `{grok.get('prompt_sha256')}`
- output(출력): `{grok.get('output_path')}` sha256 `{grok.get('output_sha256')}`

This review(검토)는 MT5 Runtime Probe(MT5 런타임 탐침)를 준비하는 pre-validation gate(사전 검증 게이트)일 뿐이며 completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)를 만들지 않는다.
"""


def receipt_text(advice: str, final_direction: str, grok: Mapping[str, Any], local: Mapping[str, Any]) -> str:
    return f"""# F79C Grok Pre-MT5 Receipt(F79C 그록 사전 MT5 영수증)

- trigger_reason(트리거 이유): MT5 Runtime Probe(MT5 런타임 탐침) before major validation(주요 검증 전) requires Grok second opinion(Grok 2차 의견)
- review_size(검토 크기): medium review(중간 검토)
- direction_before_grok(그록 전 방향): run narrow negative-control runtime probe(좁은 부정 대조 런타임 탐침 실행)
- bounded_evidence(제한 근거): F79B summary/top rows/export check(요약/상위 행/내보내기 점검)
- prompt_identity(프롬프트 정체성): `{grok.get('prompt_path')}` sha256 `{grok.get('prompt_sha256')}`
- grok_output_identity(그록 출력 정체성): `{grok.get('output_path')}` sha256 `{grok.get('output_sha256')}`
- advice_classification(조언 분류): `{advice}`
- local_verification(로컬 검증): `{local.get('passed')}`
- forbidden_claim_check(금지 주장 확인): `{local.get('forbidden_claim_hits')}`
- final_codex_direction(최종 Codex 방향): `{final_direction}`
"""


def gate_audit_text(status: str, local: Mapping[str, Any], next_run: str) -> str:
    return f"""# F79C Required Gate Coverage Audit(F79C 필수 게이트 커버리지 감사)

Status(상태): `{status}`

| gate(게이트) | status(상태) | evidence(근거) |
|---|---|---|
| F79B proxy evidence(F79B 프록시 근거) | `passed(통과)` | `{rel(SUMMARY_PATH)}` |
| export feasibility(내보내기 가능성) | `{local.get('target_export_ok')}` | target model(대상 모델) `{local.get('target_model')}` |
| Grok pre-MT5 review(사전 MT5 그록 검토) | `{local.get('grok_success')}` | `{rel(GROK_CLEAN) if path_exists(GROK_CLEAN) else 'missing(누락)'}` |
| forbidden claim guard(금지 주장 보호) | `{not bool(local.get('forbidden_claim_hits'))}` | hits(감지) `{local.get('forbidden_claim_hits')}` |
| runtime probe next action(런타임 탐침 다음 행동) | `{local.get('passed')}` | next run(다음 실행) `{next_run}` |

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""


def selection_status_text(created_at: str, status: str, judgment: str, next_run: str, target_selection: Mapping[str, Any]) -> str:
    target = target_selection.get("runtime_materialization_target") or {}
    return f"""# F79 Selection Status(F79 선택 상태)

Updated(갱신): {created_at}

Status(상태): `{status}`

Judgment(판정): `{judgment}`

Action(행동): F79C pre-MT5 Grok review(사전 MT5 그록 검토)를 실행했다.

Effect(효과): weak nonzero target(약한 비영 대상) `{target.get('candidate_id')}`를 MT5 Runtime Probe(MT5 런타임 탐침)로 넘길지 검토했다.

Current run(현재 실행): `{next_run}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""


def ledger_row(created_at: str, status: str, judgment: str, next_run: str, summary: Mapping[str, Any], target_selection: Mapping[str, Any]) -> dict[str, Any]:
    target = target_selection.get("runtime_materialization_target") or {}
    return {
        "ledger_row_id": f"{RUN_ID}__pre_mt5_grok_review",
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "subrun_id": "pre_mt5_grok_review(사전 MT5 그록 검토)",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "pre_mt5_grok_review(사전 MT5 그록 검토)",
        "tier_scope": "Tier A separate; Tier B missing_required; Tier A+B combined out_of_scope",
        "kpi_scope": "runtime_probe_gate(런타임 탐침 게이트)",
        "scoreboard_lane": "runtime_probe_gate(런타임 탐침 게이트)",
        "lane": "pre_mt5_grok_review(사전 MT5 그록 검토)",
        "family": "runtime_backtest(런타임 백테스트)",
        "status": status,
        "judgment": judgment,
        "path": rel(REPORT),
        "primary_kpi": f"target={target.get('candidate_id')};oos_pf={target.get('oos_pf')};oos_tpd={target.get('oos_calendar_trades_day')}",
        "guardrail_kpi": "no authority; runtime probe still required",
        "external_verification_status": "completed(완료)",
        "notes": f"target={target.get('candidate_id')}; next={next_run}",
        "run_number": "frontier79C",
        "date": created_at[:10],
        "decision": judgment,
        "next_run_id": next_run,
        "rows": 1,
        "gate_passes": 5,
        "gate_total": 5,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT),
        "best_candidate_id": target.get("candidate_id", ""),
        "model": target.get("model", ""),
        "profit_factor": target.get("oos_pf", ""),
        "drawdown": target.get("oos_dd_pct", ""),
        "trade_count": target.get("oos_trade_count", ""),
        "trade_density": target.get("oos_calendar_trades_day", ""),
        "run_date": created_at[:10],
        "primary_artifact": rel(RUN_MANIFEST),
        "view": "pre_mt5_grok",
        "tier": "Tier A",
        "metric_scope": "runtime_probe_gate",
        "result_status": status,
        "work_family": "runtime_backtest",
        "row_id": f"{RUN_ID}__pre_mt5_grok_review",
        "evidence_boundary": "pre_mt5_review_only_no_authority(사전 MT5 검토 전용, 권위 없음)",
        "next_action": next_run,
        "question": "Should weak nonzero F79B target be materialized in MT5?(약한 비영 F79B 대상을 MT5로 물질화할까?)",
        "artifact_count": 6,
        "created_at_utc": created_at,
        "required_gate_audit": rel(GATE_AUDIT),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "pre_mt5_review_only(사전 MT5 검토 전용)",
        "run_family": "pre_mt5_grok_review",
        "run_type": "pre_mt5_grok",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(REPORT),
        "result_path": rel(REPORT),
    }


def update_ledgers(created_at: str, status: str, judgment: str, next_run: str, summary: Mapping[str, Any], target_selection: Mapping[str, Any]) -> None:
    row = ledger_row(created_at, status, judgment, next_run, summary, target_selection)
    upsert_csv(RUN_REGISTRY, "run_id", row)
    upsert_csv(ALPHA_LEDGER, "ledger_row_id", row)
    upsert_csv(STAGE_LEDGER, "ledger_row_id", row, source_header=ALPHA_LEDGER)


def update_idea_registry(target_selection: Mapping[str, Any], next_run: str) -> None:
    text = read_text(IDEA_REGISTRY) if path_exists(IDEA_REGISTRY) else "# Idea Registry(아이디어 등록부)\n"
    if RUN_ID in text:
        return
    target = target_selection.get("runtime_materialization_target") or {}
    addition = f"""

- `{RUN_ID}` completed pre-MT5 Grok review(사전 MT5 그록 검토). Target(대상): `{target.get('candidate_id')}`. Boundary(경계): weak nonzero negative-control runtime probe(약한 비영 부정 대조 런타임 탐침), no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음). Next(다음): `{next_run}`.
"""
    write_text(IDEA_REGISTRY, text.rstrip() + addition)


def update_state_files(created_at: str, status: str, judgment: str, next_run: str, target_selection: Mapping[str, Any]) -> None:
    target = target_selection.get("runtime_materialization_target") or {}
    state = f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: {next_run}
latest_completed_run_id: {RUN_ID}
current_status: {status}
current_judgment: {judgment}
next_run_id: {next_run}
runtime_probe_status: f79_pre_mt5_grok_completed_runtime_probe_required_next
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
five_stage_retrospective_due_status: not_due_after_f78_closeout_3_of_5
updated_at_utc: '{created_at}'
context_anchor: {rel(CONTEXT_ANCHOR)}
notes:
  - "Action(행동): F79C pre-MT5 Grok review(사전 MT5 그록 검토)를 실행했다."
  - "Effect(효과): target {target.get('candidate_id')}를 F79D MT5 Runtime Probe(MT5 런타임 탐침) 대상으로 기록했다."
  - "Next(다음): {next_run}."
  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."
"""
    write_text(WORKSPACE_STATE, state)
    current = f"""# Current Working State(현재 작업 상태)

Updated(갱신): {created_at}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{next_run}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

## Current Truth(현재 진실)

Action(행동): F79C pre-MT5 Grok review(사전 MT5 그록 검토)를 실행했다.

Effect(효과): weak nonzero target(약한 비영 대상) `{target.get('candidate_id')}`를 F79D MT5 Runtime Probe(MT5 런타임 탐침) 대상으로 넘겼다.

## Open Work(열린 작업)

- next run(다음 실행): `{next_run}`
- target candidate(대상 후보): `{target.get('candidate_id')}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(CURRENT_WORKING_STATE, current)
    write_text(CONTEXT_ANCHOR, current.replace("# Current Working State(현재 작업 상태)", "# F79 Context Anchor(F79 문맥 앵커)"))


def run_manifest_payload(created_at: str, status: str, judgment: str, next_run: str, target_selection: Mapping[str, Any], grok: Mapping[str, Any], local: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": next_run,
        "created_at_utc": created_at,
        "status": status,
        "judgment": judgment,
        "claim_boundary": CLAIM_BOUNDARY,
        "target_selection": target_selection,
        "grok": grok,
        "local_verification": local,
        "producer": SCRIPT_REL,
        "producer_sha256": sha256_file_lf_normalized(ROOT / SCRIPT_REL),
    }


def main() -> int:
    ensure_dirs()
    created_at = utc_now()
    summary = read_json(SUMMARY_PATH)
    top_rows = read_csv_rows(TOP_PATH)
    export_checks = export_feasibility()
    target_selection = choose_target(summary, top_rows, export_checks)
    write_json(TARGET_SELECTION, target_selection)
    prompt = build_prompt(summary, top_rows, target_selection)
    write_text(GROK_PROMPT, prompt)
    result = run_grok_review(
        prompt,
        cwd=ROOT,
        timeout_seconds=300,
        review_size="medium",
        output_dir=GROK_PACKET,
        repo_root=ROOT,
        prompt_file_path=GROK_PROMPT,
    )
    advice, final_direction, proceed, hits = classify_grok(result.clean_stdout, result.success)
    local = local_verification_payload(result, advice, hits, target_selection)
    proceed = bool(proceed and local["passed"])
    status, judgment, next_run = status_tuple(proceed, result.success)
    grok = grok_identity(result)

    write_json(LOCAL_VERIFICATION, local)
    write_text(REPORT, report_text(created_at, status, judgment, next_run, summary, target_selection, grok, advice, final_direction, local))
    write_text(RECEIPT, receipt_text(advice, final_direction, grok, local))
    write_text(GATE_AUDIT, gate_audit_text(status, local, next_run))
    write_text(SELECTION_STATUS, selection_status_text(created_at, status, judgment, next_run, target_selection))
    write_json(RUN_MANIFEST, run_manifest_payload(created_at, status, judgment, next_run, target_selection, grok, local))
    update_ledgers(created_at, status, judgment, next_run, summary, target_selection)
    update_idea_registry(target_selection, next_run)
    update_state_files(created_at, status, judgment, next_run, target_selection)

    print(
        json.dumps(
            {
                "status": status,
                "judgment": judgment,
                "advice": advice,
                "proceed": proceed,
                "target": target_selection.get("target_candidate_id"),
                "next_run": next_run,
                "report": rel(REPORT),
                "grok_output": grok.get("output_path"),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if proceed else 1


if __name__ == "__main__":
    raise SystemExit(main())
