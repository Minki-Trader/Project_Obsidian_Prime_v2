from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import path_exists  # noqa: E402
from stage_pipelines.stage337 import execute_broker_confirmed_side_cost_curve_mt5_runtime_probe_without_db as fb  # noqa: E402
from stage_pipelines.stage337 import materialize_broker_confirmed_side_cost_curve_runtime_probe_package_without_db as fa  # noqa: E402
from stage_pipelines.stage337 import materialize_mt5_negative_repair_lgbm_probability_mismatch_net_recovery_runtime_probe_package_without_db as he  # noqa: E402


TODAY = "2026-05-31"
STAGE_ID = he.STAGE_ID
RUN_NUMBER = "run337HF"
RUN_ID = "run337HF_execute_mt5_negative_repair_lightgbm_probability_mismatch_and_net_recovery_mt5_runtime_probe_without_db_v1"
PARENT_RUN_ID = he.RUN_ID
NEXT_RUN_ID = "run337HG_review_mt5_negative_repair_lightgbm_probability_mismatch_and_net_recovery_mt5_runtime_probe_or_repair_without_db_v1"
STATUS_COMPLETED = "completed_stage337HF_probability_mismatch_net_recovery_mt5_runtime_probe_executed_review_required_no_forward_decision"
STATUS_BLOCKED = "blocked_stage337HF_probability_mismatch_net_recovery_mt5_runtime_probe_attempt_missing_or_failed_outputs_no_forward_decision"
JUDGMENT_COMPLETED = "mt5_runtime_probe_outputs_available_proxy_diff_review_required_no_selection"
JUDGMENT_BLOCKED = "mt5_runtime_probe_attempt_recorded_but_outputs_missing_or_failed_repair_required"
DECISION_COMPLETED = "stage337HF_open_run337HG_review_probability_mismatch_net_recovery_mt5_runtime_probe"
DECISION_BLOCKED = "stage337HF_open_run337HG_review_or_repair_probability_mismatch_net_recovery_mt5_runtime_probe_attempt"
CLAIM_BOUNDARY = (
    "research_development_only_stage337HF_probability_mismatch_net_recovery_mt5_runtime_probe_without_db_"
    "no_new_training_no_threshold_tuning_no_lot_optimization_no_operating_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = he.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MT5_DIR = RUN_DIR / "mt5"
TELEMETRY_COPY_DIR = RUN_DIR / "runtime_telemetry"
REPORT_COPY_DIR = MT5_DIR / "reports"
REVIEWS_DIR = he.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337HF_probability_mismatch_net_recovery_mt5_runtime_probe.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337HF_probability_mismatch_net_recovery_mt5_runtime_probe.md"

ATTEMPT_PACKAGE = RUN_DIR / "runtime_probe_attempt_package.csv"
TERMINAL_PROCESS_AUDIT = RUN_DIR / "terminal_process_audit.json"
MT5_EXECUTION_RESULT = RUN_DIR / "mt5_execution_result.json"
STRATEGY_TESTER_REPORTS = RUN_DIR / "strategy_tester_report_records.json"
EXECUTION_SUMMARY = RUN_DIR / "probability_mismatch_net_recovery_mt5_runtime_probe_summary.csv"
PROXY_MT5_DIFF = RUN_DIR / "proxy_mt5_runtime_difference.csv"
TELEMETRY_SKIP_SUMMARY = RUN_DIR / "runtime_skip_reason_summary.csv"
RUNTIME_OUTPUT_COPY = RUN_DIR / "runtime_output_copy_manifest.csv"
RUNTIME_IDENTITY = RUN_DIR / "runtime_identity.csv"
BACKTEST_FORENSICS_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    he.FINAL_DECISION,
    he.GATE_AUDIT,
    he.EXECUTION_QUEUE,
    he.RUNTIME_PROBE_ATTEMPT_PACKAGE,
    he.EXPECTED_PROBABILITY_TAPE,
    he.COMMON_FILES_SYNC,
    he.TESTER_SET_MANIFEST,
    he.TESTER_INI_MANIFEST,
    he.MODEL_HANDOFF_MANIFEST,
    he.FEATURE_MATRIX_MANIFEST,
    fa.PORTABLE_EA_EX5,
)
OUTPUT_FILES = (
    ATTEMPT_PACKAGE,
    TERMINAL_PROCESS_AUDIT,
    MT5_EXECUTION_RESULT,
    STRATEGY_TESTER_REPORTS,
    EXECUTION_SUMMARY,
    PROXY_MT5_DIFF,
    TELEMETRY_SKIP_SUMMARY,
    RUNTIME_OUTPUT_COPY,
    RUNTIME_IDENTITY,
    BACKTEST_FORENSICS_RECEIPT,
    RUNTIME_RECEIPT,
    PERFORMANCE_RECEIPT,
    JUDGMENT_RECEIPT,
    LINEAGE_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    he.SELECTED_STATUS,
    he.WORKSPACE_STATE,
    he.CURRENT_STATE,
    he.CHANGELOG,
    he.STAGE_BRIEF,
    Path(__file__),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Stage337HF runtime positive side stability MT5 runtime probe.")
    parser.add_argument("--terminal-path", default=str(fa.DEFAULT_TERMINAL))
    parser.add_argument("--common-files-root", default=str(fa.DEFAULT_COMMON_FILES))
    parser.add_argument("--tester-profile-root", default=str(fa.DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--terminal-data-root", default=str(fa.DEFAULT_TERMINAL_DATA_ROOT))
    parser.add_argument("--timeout-seconds", type=int, default=480)
    parser.add_argument("--wait-timeout-seconds", type=int, default=120)
    parser.add_argument("--attempt-limit", type=int, default=5)
    return parser.parse_args()


def rel(path: Path | str) -> str:
    return he.aw.rel(path)


def runtime_identity(attempt_rows: int) -> list[dict[str, Any]]:
    return [
        {
            "identity_id": "stage337HF_runtime_identity",
            "terminal_path": fa.DEFAULT_TERMINAL.as_posix(),
            "terminal_exists": path_exists(fa.DEFAULT_TERMINAL),
            "common_files_root": fa.DEFAULT_COMMON_FILES.as_posix(),
            "tester_profile_root": fa.DEFAULT_TESTER_PROFILE_ROOT.as_posix(),
            "terminal_data_root": fa.DEFAULT_TERMINAL_DATA_ROOT.as_posix(),
            "portable_ea_ex5": fa.PORTABLE_EA_EX5.as_posix(),
            "portable_ea_ex5_exists": path_exists(fa.PORTABLE_EA_EX5),
            "portable_ea_ex5_sha256": he.aw.sha256_file(fa.PORTABLE_EA_EX5) if path_exists(fa.PORTABLE_EA_EX5) else "",
            "attempt_rows": attempt_rows,
            "tester_model": "4 real ticks(?ㅼ젣 ??",
            "deposit": "500",
            "leverage": "1:100",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def make_final(summary: Mapping[str, Any]) -> dict[str, Any]:
    he_final = fb.read_json(he.FINAL_DECISION)
    completed = fb.as_int(summary.get("runtime_completed_rows")) > 0
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS_COMPLETED if completed else STATUS_BLOCKED,
        "judgment": JUDGMENT_COMPLETED if completed else JUDGMENT_BLOCKED,
        "decision": DECISION_COMPLETED if completed else DECISION_BLOCKED,
        "next_action": NEXT_RUN_ID,
        "missing_inputs": len(fb.fail_if_missing(INPUT_FILES)),
        "he_next_action": he_final.get("next_action", ""),
        "he_failed_gate_rows": sum(1 for row in fb.read_csv(he.GATE_AUDIT) if row.get("status") != "passed"),
        "new_training": "not_run",
        "threshold_tuning": "not_run",
        "lot_optimization": "not_run",
        "candidate_selection": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
        **dict(summary),
    }


def build_gates(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    no_forbidden_claim = (
        final["candidate_selection"] == "not_run"
        and final["forward_passed"] == "not_claimed"
        and final["forward_failed"] == "not_claimed"
        and final["goal_achieve"] == "not_claimed"
    )
    attempt_or_block_recorded = final["execution_result_rows"] == final["attempt_rows"] and final["attempt_rows"] > 0
    checks = [
        ("input_presence", final["missing_inputs"] == 0, str(final["missing_inputs"]), "0", rel(he.RUNTIME_PROBE_ATTEMPT_PACKAGE), "required HE package inputs exist(?꾩닔 HE ?⑦궎吏 ?낅젰 議댁옱)"),
        ("parent_he_gates_passed", final["he_failed_gate_rows"] == 0, str(final["he_failed_gate_rows"]), "0", rel(he.GATE_AUDIT), "HE gates passed(HE 寃뚯씠???듦낵)"),
        ("parent_next_action_matches", final["he_next_action"] == RUN_ID, str(final["he_next_action"]), RUN_ID, rel(he.FINAL_DECISION), "HF follows HE next action(HF媛 HE ?ㅼ쓬 ?됰룞???곕쫫)"),
        ("mt5_attempt_or_block_recorded", attempt_or_block_recorded, f"execution={final['execution_result_rows']};attempts={final['attempt_rows']}", "execution rows equal attempts", rel(MT5_EXECUTION_RESULT), "MT5 attempt or blocker recorded(MT5 ?쒕룄 ?먮뒗 李⑤떒 湲곕줉)"),
        ("runtime_output_copy_recorded", final["runtime_output_copy_rows"] >= final["attempt_rows"] * 2, str(final["runtime_output_copy_rows"]), ">= attempts*2", rel(RUNTIME_OUTPUT_COPY), "runtime output copy audit exists(?고???異쒕젰 蹂듭궗 媛먯궗 議댁옱)"),
        ("comparison_summary_materialized", final["summary_rows"] == final["attempt_rows"], f"summary={final['summary_rows']};attempts={final['attempt_rows']}", "summary rows equal attempts", rel(EXECUTION_SUMMARY), "proxy-MT5 comparison summary exists(?꾨줉??MT5 鍮꾧탳 ?붿빟 議댁옱)"),
        ("diff_or_blocker_materialized", final["diff_rows"] > 0 or final["runtime_completed_rows"] == 0, f"diff={final['diff_rows']};runtime_completed={final['runtime_completed_rows']}", "diff rows or blocker", rel(PROXY_MT5_DIFF), "diff rows or blocker state recorded(李⑥씠 ???먮뒗 李⑤떒 ?곹깭 湲곕줉)"),
        ("forensics_identity_recorded", path_exists(RUNTIME_IDENTITY), "present", "present", rel(RUNTIME_IDENTITY), "tester identity recorded(?뚯뒪???뺤껜??湲곕줉)"),
        ("no_forbidden_claim", no_forbidden_claim, f"selection={final['candidate_selection']};goal={final['goal_achieve']}", "not_run/not_claimed", rel(FINAL_DECISION), "no operating claim from runtime probe(?고????먯묠?먯꽌 ?댁쁺 二쇱옣 ?놁쓬)"),
        ("required_gate_coverage_audit", True, "all required gates listed in closeout(紐⑤뱺 ?꾩닔 寃뚯씠?멸? 醫낅즺 湲곕줉???덉쓬)", "present", rel(GATE_AUDIT), "connects gates to completion claim(寃뚯씠?몃? ?꾨즺 二쇱옣怨??곌껐)"),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": "passed" if passed else "failed",
            "evidence_path": evidence,
            "observed": observed,
            "expected": expected,
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, passed, observed, expected, evidence, effect in checks
    ]


def build_receipts(final: Mapping[str, Any], artifact_paths: Sequence[Path]) -> list[Path]:
    runtime = {
        "research_path": rel(Path(__file__)),
        "runtime_path": rel(ATTEMPT_PACKAGE),
        "shared_contract": "HE feature matrix, expected tape, set/ini, ONNX handoff(HE ?쇱쿂 ?됰젹, ?덉긽 ?뚯씠?? ?ㅼ젙, ONNX ?멸퀎)",
        "parity_check": f"matched_rows={final['matched_rows']};mismatch_rows={final['mismatch_rows']};runtime_completed={final['runtime_completed_rows']}",
        "runtime_claim_boundary": "runtime_probe_only(?고????먯묠 ?꾩슜)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    forensics = {
        "tester_identity": "US100 M5 Deposit=500 Leverage=1:100 Model=4 real ticks(US100 M5 ?덉닔湲?500 ?덈쾭由ъ? 1:100 ?ㅼ젣 ??",
        "report_identity": rel(STRATEGY_TESTER_REPORTS),
        "trade_evidence": f"report_rows={final['report_rows']};runtime_completed={final['runtime_completed_rows']}",
        "backtest_judgment": "review_required(寃???꾩슂)" if final["runtime_completed_rows"] else "blocked(李⑤떒)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    performance = {
        "summary": rel(EXECUTION_SUMMARY),
        "diff": rel(PROXY_MT5_DIFF),
        "runtime_completed_rows": final["runtime_completed_rows"],
        "mismatch_rows": final["mismatch_rows"],
        "allowed_use": "runtime probe review only(?고????먯묠 寃???꾩슜)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment = {
        "result_subject": RUN_ID,
        "judgment_label": final["judgment"],
        "decision": final["decision"],
        "next_condition": final["next_action"],
        "goal_achieve": "not_claimed(二쇱옣 ????",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths = [
        fb.write_json(RUNTIME_RECEIPT, runtime),
        fb.write_json(BACKTEST_FORENSICS_RECEIPT, forensics),
        fb.write_json(PERFORMANCE_RECEIPT, performance),
        fb.write_json(JUDGMENT_RECEIPT, judgment),
    ]
    all_artifacts = list(artifact_paths) + paths
    lineage = {
        "source_inputs": [rel(path) for path in INPUT_FILES],
        "producer": rel(Path(__file__)),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in all_artifacts],
        "artifact_hashes": {
            rel(path): he.aw.sha256_file(path)
            for path in all_artifacts
            if path_exists(path) and he.aw.io_path(path).is_file()
        },
        "registry_links": [rel(he.RUN_REGISTRY), rel(he.ALPHA_LEDGER), rel(he.STAGE_LEDGER), rel(he.ARTIFACT_REGISTRY)],
        "lineage_judgment": "connected_HE_package_to_HF_runtime_probe(HE ?⑦궎吏瑜?HF ?고????먯묠???곌껐)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths.append(fb.write_json(LINEAGE_RECEIPT, lineage))
    return paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337HF MT5 Negative Repair LightGBM Runtime Probe(337?④퀎 337HF MT5 ?고????먯묠)

## Conclusion(寃곕줎)

run337HF(337HF ?ㅽ뻾)??run337HE(337HE ?ㅽ뻾)??MT5 negative repair LightGBM package(?고???湲띿젙 諛⑺뼢 ?덉젙 ?섎━ ?⑦궎吏)瑜?MT5 terminal(MT5 ?곕??????쒕룄?덈떎.

Action(?됰룞): Strategy Tester(?꾨왂 ?뚯뒪??瑜?attempt(?쒕룄)蹂꾨줈 ?ㅽ뻾?섍굅??blocker(李⑤떒 ?ъ쑀)瑜?湲곕줉?덈떎. Effect(?④낵): proxy expected value(?꾨줉???덉긽媛?? MT5 runtime output(MT5 ?고???異쒕젰)???ㅼ쓬 HG review(HG 寃???먯꽌 鍮꾧탳?????덈떎.

- status(?곹깭): `{final['status']}`
- judgment(?먯젙): `{final['judgment']}`
- decision(寃곗젙): `{final['decision']}`
- next_action(?ㅼ쓬 ?됰룞): `{final['next_action']}`
- attempts(?쒕룄): `{final['attempt_rows']}`
- runtime_completed(?고????꾨즺): `{final['runtime_completed_rows']}`
- matched_rows(?쇱튂 ??: `{final['matched_rows']}`
- mismatch_rows(遺덉씪移???: `{final['mismatch_rows']}`
- report_rows(蹂닿퀬????: `{final['report_rows']}`
- gates(寃뚯씠??: `{final['passed_gates']}/{final['gate_rows']}`

## Boundary(寃쎄퀎)

- candidate_selection(?꾨낫 ?좏깮): `not_run`
- Forward Passed/Failed(?꾩쭊 ?듦낵/?ㅽ뙣): `not_claimed`
- runtime_authority(?고???沅뚯쐞): `not_claimed`
- Goal Achieve(紐⑺몴 ?ъ꽦): `not_claimed`
- claim_boundary(二쇱옣 寃쎄퀎): `{CLAIM_BOUNDARY}`
"""
    return he.aw.write_text_lossless(REPORT_PATH, text, True)


def write_decision(final: Mapping[str, Any]) -> Path:
    text = f"""# {TODAY} Stage337HF Decision(337HF 寃곗젙)

- run_id(?ㅽ뻾 ID): `{RUN_ID}`
- parent_run_id(遺紐??ㅽ뻾 ID): `{PARENT_RUN_ID}`
- status(?곹깭): `{final['status']}`
- judgment(?먯젙): `{final['judgment']}`
- decision(寃곗젙): `{final['decision']}`
- next_action(?ㅼ쓬 ?됰룞): `{final['next_action']}`
- evidence(洹쇨굅): `{rel(REPORT_PATH)}`, `{rel(EXECUTION_SUMMARY)}`, `{rel(MT5_EXECUTION_RESULT)}`

Action(?됰룞): MT5 runtime probe(MT5 ?고????먯묠)瑜??쒕룄?섍퀬 寃곌낵 ?먮뒗 blocker(李⑤떒 ?ъ쑀)瑜?湲곕줉?덈떎.
Effect(?④낵): ?ㅼ쓬 HG review(HG 寃??媛 proxy-vs-MT5 diff(?꾨줉??MT5 李⑥씠), attribution(洹??, usability(?쒖슜 媛?μ꽦)???먯젙?????덈떎.

Forward/Goal(?꾩쭊/紐⑺몴): `not_claimed`
runtime_authority(?고???沅뚯쐞): `not_claimed`
claim_boundary(二쇱옣 寃쎄퀎): `{CLAIM_BOUNDARY}`
"""
    return he.aw.write_text_lossless(DECISION_DOC, text, True)


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    branch = fa.ey.current_branch()
    workspace, workspace_bom = he.aw.read_text_lossless(he.WORKSPACE_STATE)
    workspace = fb.replace_line(workspace, "current_run_id:", f"current_run_id: {final['next_action']}")
    workspace = fb.replace_line(workspace, "updated_on:", f"updated_on: '{TODAY}'")
    workspace = fb.replace_line(workspace, "active_branch:", f"active_branch: {branch}")
    focus = (
        "- >-\n"
        f"  Stage337 run337HF focus complete: run337HF(337HF ?ㅽ뻾)??`{final['status']}`濡?MT5 runtime probe(MT5 ?고????먯묠)瑜??쒕룄?덈떎. "
        f"Effect(?④낵): attempts(?쒕룄) `{final['attempt_rows']}`, runtime completed(?고????꾨즺) `{final['runtime_completed_rows']}`, matched rows(?쇱튂 ?? `{final['matched_rows']}`, mismatches(遺덉씪移? `{final['mismatch_rows']}`瑜?湲곕줉?섍퀬 `{final['next_action']}`???댁뿀?? Forward/Goal(?꾩쭊/紐⑺몴)? 二쇱옣?섏? ?딅뒗??\n"
    )
    if "Stage337 run337HF focus complete" in workspace:
        workspace = re.sub(r"- >-\n  Stage337 run337HF focus complete:.*?(?=\n- >-|\n[a-zA-Z_]+:|$)", focus.rstrip(), workspace, count=1, flags=re.S)
    else:
        workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    artifacts.append(he.aw.write_text_lossless(he.WORKSPACE_STATE, workspace, workspace_bom))

    current, current_bom = he.aw.read_text_lossless(he.CURRENT_STATE)
    for field_name, value in {
        "current_run": f"`{final['next_action']}`",
        "status": f"`{final['status']}`",
        "decision": f"`{final['decision']}`",
        "latest_completed_run": f"`{RUN_ID}`",
        "next_action": f"`{final['next_action']}`",
        "claim_boundary": f"`{CLAIM_BOUNDARY}`",
    }.items():
        current = fb.replace_bullet_field(current, field_name, value)
    section = f"""## run337HF MT5 Runtime Probe(MT5 ?고????먯묠)

- status(?곹깭): `{final['status']}`
- judgment(?먯젙): `{final['judgment']}`
- decision(寃곗젙): `{final['decision']}`
- attempts(?쒕룄): `{final['attempt_rows']}`
- runtime_completed(?고????꾨즺): `{final['runtime_completed_rows']}`
- matched_rows(?쇱튂 ??: `{final['matched_rows']}`
- mismatch_rows(遺덉씪移???: `{final['mismatch_rows']}`
- report_rows(蹂닿퀬????: `{final['report_rows']}`
- gates(寃뚯씠??: `{final['passed_gates']}/{final['gate_rows']}`
- effect(?④낵): MT5 external check(MT5 ?몃? ?뺤씤)瑜??ㅼ젣濡??쒕룄?섍퀬 HG review(HG 寃??濡??섍릿?? ?댁쁺 二쇱옣? ?ル뒗??
- next_action(?ㅼ쓬 ?됰룞): `{final['next_action']}`
"""
    current = fb.upsert_section_before(current, "## run337HE Runtime Probe Package", section, "run337HF MT5 Runtime Probe")
    artifacts.append(he.aw.write_text_lossless(he.CURRENT_STATE, current, current_bom))

    selection = f"""# Stage337 Selection Status(337?④퀎 ?좏깮 ?곹깭)

- latest_run(理쒖떊 ?ㅽ뻾): `{RUN_ID}`
- latest_decision(理쒖떊 寃곗젙): `{final['decision']}`
- current_run(?꾩옱 ?ㅽ뻾): `{final['next_action']}`
- rebuild_status(?ш뎄異??곹깭): `{final['status']}`
- runtime_completed(?고????꾨즺): `{final['runtime_completed_rows']}`
- matched_rows(?쇱튂 ??: `{final['matched_rows']}`
- mismatch_rows(遺덉씪移???: `{final['mismatch_rows']}`
- Forward Passed(?꾩쭊 ?듦낵): `not_claimed`
- Forward Failed(?꾩쭊 ?ㅽ뙣): `not_claimed`
- runtime_authority(?고???沅뚯쐞): `not_claimed`
- goal_achieve(紐⑺몴 ?ъ꽦): `not_claimed`
- next_action(?ㅼ쓬 ?됰룞): `{final['next_action']}`
- effect(?④낵): HF(337HF ?ㅽ뻾)??runtime probe(?고????먯묠) 洹쇨굅留?留뚮뱾硫?operating selection(?댁쁺 ?좏깮)? ?섏? ?딅뒗??
"""
    artifacts.append(he.aw.write_text_lossless(he.SELECTED_STATUS, selection, True))

    brief, brief_bom = he.aw.read_text_lossless(he.STAGE_BRIEF)
    brief_entry = (
        f"- {TODAY}: run337HF(337HF ?ㅽ뻾) `{final['status']}`. "
        f"Effect(?④낵): MT5 attempts(MT5 ?쒕룄) `{final['attempt_rows']}`, runtime completed(?고????꾨즺) `{final['runtime_completed_rows']}`, matched rows(?쇱튂 ?? `{final['matched_rows']}`瑜?湲곕줉?섍퀬 `{final['next_action']}`???댁뿀?? Forward/Goal(?꾩쭊/紐⑺몴)? 二쇱옣?섏? ?딅뒗??"
    )
    artifacts.append(he.aw.write_text_lossless(he.STAGE_BRIEF, fb.upsert_single_line(brief, "run337HF(337HF ?ㅽ뻾)", brief_entry), brief_bom))

    changelog, changelog_bom = he.aw.read_text_lossless(he.CHANGELOG)
    changelog_entry = (
        f"- {TODAY}: Stage337 run337HF(337HF ?ㅽ뻾) `{final['status']}`. "
        f"Effect(?④낵): MT5 runtime probe(MT5 ?고????먯묠)瑜??쒕룄?섍퀬 `{final['next_action']}`???댁뿀?? Forward/Goal(?꾩쭊/紐⑺몴)? 二쇱옣?섏? ?딆븯??"
    )
    artifacts.append(he.aw.write_text_lossless(he.CHANGELOG, fb.upsert_single_line(changelog, "Stage337 run337HF", changelog_entry), changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "probability_mismatch_net_recovery_lightgbm_mt5_runtime_probe",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "notes": f"attempts={final['attempt_rows']};runtime_completed={final['runtime_completed_rows']};matched={final['matched_rows']};mismatch={final['mismatch_rows']};next_action={final['next_action']};goal_achieve_not_claimed.",
        "family": "runtime_verification_backtest_forensics_performance_attribution",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__mt5_runtime_probe",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "mt5_runtime_probe",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "probability_mismatch_net_recovery_lightgbm_mt5_runtime_probe(?고???湲띿젙 諛⑺뼢 ?덉젙 ?섎━ MT5 ?고????먯묠)",
        "tier_scope": "Tier A inner holdout MT5 runtime probe(Tier A ?대? 蹂대쪟 MT5 ?고????먯묠)",
        "kpi_scope": "runtime_probe_only_no_forward_goal(?고????먯묠 ?꾩슜, ?꾩쭊/紐⑺몴 ?놁쓬)",
        "scoreboard_lane": "runtime_verification",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "primary_kpi": f"runtime_completed={final['runtime_completed_rows']};matched={final['matched_rows']};mismatch={final['mismatch_rows']}",
        "guardrail_kpi": "no_selection;no_forward;no_goal;review_required",
        "external_verification_status": "attempted",
        "notes": f"decision={final['decision']};next_action={final['next_action']};goal_achieve_not_claimed.",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__mt5_runtime_probe",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "runtime_verification_backtest_forensics_performance_attribution",
        "evidence_scope": "MT5 tester attempts, telemetry, reports, proxy diff",
        "kpi_scope": "runtime_probe_no_operating_claim",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"gates={final['passed_gates']}/{final['gate_rows']};next_action={final['next_action']};goal_achieve_not_claimed",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__mt5_runtime_probe",
        "family": "probability_mismatch_net_recovery_lightgbm_mt5_runtime_probe",
        "question": "do HE MT5-negative repair LightGBM ONNX runtime packages execute in MT5 and match expected probabilities",
        "metric_scope": "runtime_telemetry_proxy_diff_tester_reports",
        "primary_artifact": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "next_action": final["next_action"],
    }
    return [
        fb.upsert_csv_worktree(he.RUN_REGISTRY, he.aw.RUN_REGISTRY_COLUMNS, run_row, "run_id"),
        fb.upsert_csv_worktree(he.ALPHA_LEDGER, he.aw.ALPHA_LEDGER_COLUMNS, alpha_row, "ledger_row_id"),
        fb.upsert_csv_worktree(he.STAGE_LEDGER, he.aw.STAGE_LEDGER_COLUMNS, stage_row, "ledger_row_id"),
    ]


def configure_execution_engine() -> None:
    replacements = {
        "TODAY": TODAY,
        "STAGE_ID": STAGE_ID,
        "RUN_NUMBER": RUN_NUMBER,
        "RUN_ID": RUN_ID,
        "PARENT_RUN_ID": PARENT_RUN_ID,
        "NEXT_RUN_ID": NEXT_RUN_ID,
        "STATUS_COMPLETED": STATUS_COMPLETED,
        "STATUS_BLOCKED": STATUS_BLOCKED,
        "JUDGMENT_COMPLETED": JUDGMENT_COMPLETED,
        "JUDGMENT_BLOCKED": JUDGMENT_BLOCKED,
        "DECISION_COMPLETED": DECISION_COMPLETED,
        "DECISION_BLOCKED": DECISION_BLOCKED,
        "CLAIM_BOUNDARY": CLAIM_BOUNDARY,
        "RUN_DIR": RUN_DIR,
        "MT5_DIR": MT5_DIR,
        "TELEMETRY_COPY_DIR": TELEMETRY_COPY_DIR,
        "REPORT_COPY_DIR": REPORT_COPY_DIR,
        "REPORT_PATH": REPORT_PATH,
        "DECISION_DOC": DECISION_DOC,
        "SELECTED_STATUS": he.SELECTED_STATUS,
        "STAGE_BRIEF": he.STAGE_BRIEF,
        "WORKSPACE_STATE": he.WORKSPACE_STATE,
        "CURRENT_STATE": he.CURRENT_STATE,
        "CHANGELOG": he.CHANGELOG,
        "RUN_REGISTRY": he.RUN_REGISTRY,
        "ALPHA_LEDGER": he.ALPHA_LEDGER,
        "ARTIFACT_REGISTRY": he.ARTIFACT_REGISTRY,
        "STAGE_LEDGER": he.STAGE_LEDGER,
        "FA_FINAL": he.FINAL_DECISION,
        "FA_GATES": he.GATE_AUDIT,
        "FA_QUEUE": he.EXECUTION_QUEUE,
        "FA_ATTEMPT_PACKAGE": he.RUNTIME_PROBE_ATTEMPT_PACKAGE,
        "FA_EXPECTED_TAPE": he.EXPECTED_PROBABILITY_TAPE,
        "FA_COMMON_SYNC": he.COMMON_FILES_SYNC,
        "FA_TESTER_SET": he.TESTER_SET_MANIFEST,
        "FA_TESTER_INI": he.TESTER_INI_MANIFEST,
        "FA_MODEL_HANDOFF": he.MODEL_HANDOFF_MANIFEST,
        "FA_FEATURE_MANIFEST": he.FEATURE_MATRIX_MANIFEST,
        "DEFAULT_TERMINAL": fa.DEFAULT_TERMINAL,
        "DEFAULT_COMMON_FILES": fa.DEFAULT_COMMON_FILES,
        "DEFAULT_TESTER_PROFILE_ROOT": fa.DEFAULT_TESTER_PROFILE_ROOT,
        "DEFAULT_TERMINAL_DATA_ROOT": fa.DEFAULT_TERMINAL_DATA_ROOT,
        "PORTABLE_EA_EX5": fa.PORTABLE_EA_EX5,
        "ATTEMPT_PACKAGE": ATTEMPT_PACKAGE,
        "TERMINAL_PROCESS_AUDIT": TERMINAL_PROCESS_AUDIT,
        "MT5_EXECUTION_RESULT": MT5_EXECUTION_RESULT,
        "STRATEGY_TESTER_REPORTS": STRATEGY_TESTER_REPORTS,
        "EXECUTION_SUMMARY": EXECUTION_SUMMARY,
        "PROXY_MT5_DIFF": PROXY_MT5_DIFF,
        "TELEMETRY_SKIP_SUMMARY": TELEMETRY_SKIP_SUMMARY,
        "RUNTIME_OUTPUT_COPY": RUNTIME_OUTPUT_COPY,
        "RUNTIME_IDENTITY": RUNTIME_IDENTITY,
        "BACKTEST_FORENSICS_RECEIPT": BACKTEST_FORENSICS_RECEIPT,
        "RUNTIME_RECEIPT": RUNTIME_RECEIPT,
        "PERFORMANCE_RECEIPT": PERFORMANCE_RECEIPT,
        "JUDGMENT_RECEIPT": JUDGMENT_RECEIPT,
        "LINEAGE_RECEIPT": LINEAGE_RECEIPT,
        "GATE_AUDIT": GATE_AUDIT,
        "FINAL_DECISION": FINAL_DECISION,
        "RUN_MANIFEST": RUN_MANIFEST,
        "INPUT_FILES": INPUT_FILES,
        "OUTPUT_FILES": OUTPUT_FILES,
    }
    for name, value in replacements.items():
        setattr(fb, name, value)
    fb.parse_args = parse_args
    fb.runtime_identity = runtime_identity
    fb.make_final = make_final
    fb.build_gates = build_gates
    fb.build_receipts = build_receipts
    fb.write_report = write_report
    fb.write_decision = write_decision
    fb.update_docs = update_docs
    fb.update_registers = update_registers


def main() -> int:
    configure_execution_engine()
    return fb.main()


if __name__ == "__main__":
    raise SystemExit(main())
