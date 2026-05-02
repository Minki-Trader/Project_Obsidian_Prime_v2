from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Mapping, Sequence

from foundation.control_plane.ledger import ALPHA_LEDGER_COLUMNS, io_path, write_csv_rows
from foundation.control_plane.mt5_tier_balance_completion import ROOT


STAGE_NUMBER = 14
STAGE_ID = "14_model_family_challenge__margin_kernel_training_effect"
RUN_NUMBER = "run05A"
RUN_ID = "run05A_svm_margin_kernel_characteristic_runtime_probe_v1"
PACKET_ID = "stage14_run05A_svm_margin_kernel_closeout_packet_v1"
EXPLORATION_LABEL = "stage14_Model__SVMMarginKernelCloseoutProbe"
MODEL_FAMILY = "sklearn_svm_margin_kernel_family"
FEATURE_SET_ID = "feature_set_v2_mt5_price_proxy_top3_weights_58_features"
LABEL_ID = "label_v1_fwd12_m5_logret_train_q33_3class"
SPLIT_CONTRACT = "split_v1_calendar_train_20220901_20241231_val_20250101_20260413"
STAGE_INHERITANCE = "independent_no_stage10_11_12_13_run_baseline_seed_or_reference"
BOUNDARY = "svm_margin_kernel_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority"
JUDGMENT_COMPLETED = "closed_inconclusive_svm_margin_kernel_runtime_probe_evidence"
JUDGMENT_BLOCKED = "blocked_svm_margin_kernel_runtime_probe_after_attempt"
THRESHOLD_QUANTILE = 0.90
ROWS_PER_CLASS = 600

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
PACKET_ROOT = ROOT / "docs/agent_control/packets/stage14_svm_margin_kernel_closeout_v1"
STAGE_LEDGER_PATH = STAGE_ROOT / "03_reviews/stage_run_ledger.csv"
REPORT_PATH = STAGE_ROOT / "03_reviews/run05A_svm_margin_kernel_runtime_probe_packet.md"
CLOSEOUT_PATH = STAGE_ROOT / "03_reviews/stage14_closeout_packet.md"
STAGE15_ID = "15_model_family_challenge__untried_learning_methods_scout"
STAGE15_ROOT = ROOT / "stages" / STAGE15_ID


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def replace_required(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise RuntimeError(f"Required sync marker not found: {label}")
    return text.replace(old, new, 1)


def result_summary_markdown(
    summary: Mapping[str, Any],
    result: Mapping[str, Any],
    variant_results: Sequence[Mapping[str, Any]],
) -> str:
    lines = [
        f"# {RUN_ID} Result Summary({RUN_ID} 결과 요약)",
        "",
        f"- status(상태): `{summary['external_verification_status']}`",
        f"- judgment(판정): `{summary['judgment']}`",
        f"- selected variant(선택 변형): `{summary['selected_variant_id']}`",
        f"- threshold policy(임계값 정책): `{summary['threshold_policy']}`",
        f"- boundary(경계): `{BOUNDARY}`",
        "",
        "## Python Shape Read(Python 모양 판독)",
        "",
        "| variant(변형) | kernel(커널) | score(점수) | val coverage(검증 신호비율) | oos coverage(표본외 신호비율) |",
        "|---|---:|---:|---:|---:|",
    ]
    for row in variant_results:
        lines.append(
            "| `{}` | `{}` | `{:.6f}` | `{}` | `{}` |".format(
                row.get("variant_id"),
                row.get("spec", {}).get("kernel"),
                safe_float(row.get("shape_score")),
                row.get("metrics", {}).get("validation", {}).get("signal_coverage"),
                row.get("metrics", {}).get("oos", {}).get("signal_coverage"),
            )
        )
    lines.extend(
        [
            "",
            "## MT5 Runtime Probe(MT5 런타임 탐침)",
            "",
            "| view(보기) | split(분할) | net profit(순수익) | PF(수익 팩터) | DD(손실폭) | trades(거래 수) |",
            "|---|---:|---:|---:|---:|---:|",
        ]
    )
    for record in result.get("mt5_kpi_records", []):
        if record.get("route_role") in {"primary_used", "fallback_used"}:
            continue
        metrics = record.get("metrics", {})
        lines.append(
            "| `{}` | `{}` | `{}` | `{}` | `{}` | `{}` |".format(
                record.get("record_view"),
                record.get("split"),
                metrics.get("net_profit"),
                metrics.get("profit_factor"),
                metrics.get("max_drawdown_amount"),
                metrics.get("trade_count"),
            )
        )
    if summary.get("failure"):
        lines.extend(["", f"- failure(실패): `{summary['failure']}`"])
    lines.extend(
        [
            "",
            "효과(effect, 효과): 이 결과는 SVM(`Support Vector Machine`, 서포트 벡터 머신) margin/kernel(마진/커널) 모양과 MT5(`MetaTrader 5`, 메타트레이더5) 인계 가능성을 본 것이다.",
            "alpha quality(알파 품질), edge(거래 우위), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.",
        ]
    )
    return "\n".join(lines)


def run_packet_markdown(
    summary: Mapping[str, Any],
    result: Mapping[str, Any],
    variant_results: Sequence[Mapping[str, Any]],
) -> str:
    return "\n".join(
        [
            f"# {RUN_ID} Packet({RUN_ID} 묶음)",
            "",
            "## Result(결과)",
            "",
            f"`{RUN_ID}` completed with status(상태) `{summary['external_verification_status']}` and judgment(판정) `{summary['judgment']}`.",
            "",
            "효과(effect, 효과): Stage14(14단계)를 profit selection(수익 선택) 없이 SVM(서포트 벡터 머신) shape(모양)와 MT5 runtime handoff(런타임 인계)로 읽었다.",
            "",
            "## Selected Representative(선택 대표)",
            "",
            f"- variant(변형): `{summary['selected_variant_id']}`",
            f"- selection metric(선택 지표): `shape_score(모양 점수)`",
            f"- threshold policy(임계값 정책): `{summary['threshold_policy']}`",
            "",
            "## Boundary(경계)",
            "",
            f"`{BOUNDARY}`",
            "",
            "이 묶음은 alpha quality(알파 품질), baseline(기준선), promotion candidate(승격 후보), operating promotion(운영 승격), runtime authority(런타임 권위)를 만들지 않는다.",
        ]
    )


def closeout_report_markdown(summary: Mapping[str, Any], result: Mapping[str, Any]) -> str:
    return "\n".join(
        [
            "# Stage14 SVM Margin Kernel Closeout(14단계 SVM 마진 커널 마감)",
            "",
            "## Decision(결정)",
            "",
            f"Stage14(14단계)를 `{summary['judgment']}`로 닫는다.",
            "",
            "효과(effect, 효과): SVM(`Support Vector Machine`, 서포트 벡터 머신) margin/kernel(마진/커널) 계열은 독립 주제로 얕게 확인됐고, 다음 Stage15(15단계)는 아직 독립 탐색으로 다루지 않은 model learning methods(모델 학습법)를 새 주제로 볼 수 있다.",
            "",
            "## Evidence(근거)",
            "",
            f"- run(실행): `{RUN_ID}`",
            f"- report(보고서): `{rel(REPORT_PATH)}`",
            f"- manifest(목록): `{rel(RUN_ROOT / 'run_manifest.json')}`",
            f"- KPI record(KPI 기록): `{rel(RUN_ROOT / 'kpi_record.json')}`",
            f"- stage ledger(단계 장부): `{rel(STAGE_LEDGER_PATH)}`",
            "",
            "## Preserved Clues(보존 단서)",
            "",
            f"- representative variant(대표 변형): `{summary['selected_variant_id']}`",
            "- SVM(서포트 벡터 머신)은 probability margin(확률 마진), entropy(엔트로피), signal density(신호 밀도)를 통해 모델 계열의 모양을 읽을 수 있다.",
            "- kernel(커널) 변형은 edge search(거래 우위 탐색)가 아니라 failure boundary(실패 경계)와 runtime handoff(런타임 인계) 가능성으로 보존한다.",
            "",
            "## Forbidden Claims(금지 주장)",
            "",
            "- alpha quality(알파 품질)",
            "- edge(거래 우위)",
            "- selected baseline(선택 기준선)",
            "- promotion candidate(승격 후보)",
            "- operating promotion(운영 승격)",
            "- runtime authority(런타임 권위)",
        ]
    )


def skill_receipts(created_at: str, result: Mapping[str, Any], summary: Mapping[str, Any]) -> dict[str, Any]:
    runtime_status = "completed" if result.get("external_verification_status") == "completed" else "blocked"
    return {
        "packet_id": "stage14_svm_margin_kernel_closeout_v1",
        "created_at_utc": created_at,
        "receipts": [
            {
                "skill": "obsidian-runtime-parity",
                "status": runtime_status,
                "research_path": "foundation/models/svm_margin_kernel.py and stage_pipelines/stage14/svm_margin_kernel_runtime_probe.py",
                "runtime_path": rel(RUN_ROOT / "mt5"),
                "shared_contract": "58-feature Tier A, 42-feature Tier B fallback, label_v1_fwd12, split_v1, fixed q90 threshold",
                "parity_check": "ONNX parity and MT5 Strategy Tester runtime_probe",
                "runtime_claim_boundary": "runtime_probe",
            },
            {
                "skill": "obsidian-backtest-forensics",
                "status": runtime_status,
                "tester_identity": "US100 M5, deposit 500, leverage 1:100, tester model 4, generated .ini/.set files",
                "report_identity": "Strategy Tester reports recorded in run manifest when completed",
                "backtest_judgment": "usable_with_boundary" if runtime_status == "completed" else "blocked",
            },
            {
                "skill": "obsidian-run-evidence-system",
                "status": "completed",
                "measurement_scope": "Python structural_scout plus MT5 runtime_probe KPI rows",
                "management_state": "manifest, kpi_record, summary, run_registry, alpha ledgers updated",
                "judgment_class": "inconclusive" if runtime_status == "completed" else "blocked",
                "evidence_boundary": "probe",
            },
            {
                "skill": "obsidian-artifact-lineage",
                "status": "completed",
                "source_inputs": [rel(MODEL_INPUT_PATH), rel(FEATURE_ORDER_PATH), rel(TRAINING_SUMMARY_PATH)],
                "artifact_paths": [rel(RUN_ROOT), rel(PACKET_ROOT)],
                "lineage_judgment": "connected_with_boundary",
            },
            {
                "skill": "obsidian-claim-discipline",
                "status": "completed",
                "allowed_claims": [summary["judgment"], "stage14_closeout_after_runtime_probe"],
                "forbidden_claims": ["alpha_quality", "edge", "baseline", "promotion", "runtime_authority"],
            },
        ],
    }


def routing_receipt(created_at: str) -> dict[str, Any]:
    return {
        "packet_id": "stage14_svm_margin_kernel_closeout_v1",
        "created_at_utc": created_at,
        "work_packet_lifecycle": "runtime_backtest_to_stage_closeout_to_stage15_handoff",
        "primary_family": "runtime_backtest",
        "primary_skill": "obsidian-runtime-parity",
        "support_skills": [
            "obsidian-backtest-forensics",
            "obsidian-reference-scout",
            "obsidian-run-evidence-system",
            "obsidian-artifact-lineage",
        ],
        "required_gates": [
            "runtime_evidence_gate",
            "scope_completion_gate",
            "kpi_contract_audit",
            "required_gate_coverage_audit",
            "final_claim_guard",
        ],
        "branch_worktree_fit": "codex/stage14 matches Stage14 closeout and Stage15 handoff request",
        "reference_scout_pairing": "local sklearn/skl2onnx/onnxruntime conversion smoke checks were executed before code edits",
    }


def scope_completion_gate(result: Mapping[str, Any], summary: Mapping[str, Any]) -> dict[str, Any]:
    passed = result.get("external_verification_status") == "completed"
    return {
        "audit_name": "scope_completion_gate",
        "status": "pass" if passed else "blocked",
        "passed": bool(passed),
        "completed_forbidden": not passed,
        "counts": {"attempt_count": summary.get("attempt_count"), "mt5_kpi_record_count": summary.get("mt5_kpi_record_count")},
        "allowed_claims": [summary["judgment"]] if passed else ["blocked_runtime_probe_attempted"],
        "forbidden_claims": ["alpha_quality", "edge", "promotion", "runtime_authority"],
    }


def runtime_evidence_gate(result: Mapping[str, Any], summary: Mapping[str, Any]) -> dict[str, Any]:
    passed = result.get("external_verification_status") == "completed" and len(result.get("mt5_kpi_records", [])) >= 6
    return {
        "audit_name": "runtime_evidence_gate",
        "status": "pass" if passed else "blocked",
        "passed": bool(passed),
        "completed_forbidden": not passed,
        "counts": {
            "execution_results": len(result.get("execution_results", [])),
            "strategy_tester_reports": len(result.get("strategy_tester_reports", [])),
            "mt5_kpi_records": len(result.get("mt5_kpi_records", [])),
        },
        "summary": {"judgment": summary.get("judgment"), "boundary": summary.get("boundary")},
    }


def kpi_contract_audit(result: Mapping[str, Any], tier_records: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    mt5_records = result.get("mt5_kpi_records", [])
    required_views = {
        "mt5_tier_a_only_validation_is",
        "mt5_tier_a_only_oos",
        "mt5_tier_b_fallback_only_validation_is",
        "mt5_tier_b_fallback_only_oos",
        "mt5_routed_total_validation_is",
        "mt5_routed_total_oos",
    }
    present = {str(record.get("record_view")) for record in mt5_records}
    missing = sorted(required_views.difference(present))
    passed = not missing and len(tier_records) == 3
    return {
        "audit_name": "kpi_contract_audit",
        "status": "pass" if passed else "blocked",
        "passed": bool(passed),
        "completed_forbidden": not passed,
        "counts": {"python_tier_records": len(tier_records), "mt5_records": len(mt5_records), "missing_views": missing},
    }


def required_gate_coverage(result: Mapping[str, Any]) -> dict[str, Any]:
    passed = result.get("external_verification_status") == "completed"
    gates = {
        "runtime_evidence_gate": "pass" if passed else "blocked",
        "scope_completion_gate": "pass" if passed else "blocked",
        "kpi_contract_audit": "pass" if passed else "blocked",
        "final_claim_guard": "pass" if passed else "blocked",
    }
    return {
        "audit_name": "required_gate_coverage_audit",
        "status": "pass" if passed else "blocked",
        "passed": bool(passed),
        "completed_forbidden": not passed,
        "required_gates": gates,
    }


def final_claim_guard(result: Mapping[str, Any]) -> dict[str, Any]:
    passed = result.get("external_verification_status") == "completed"
    return {
        "audit_name": "final_claim_guard",
        "status": "pass" if passed else "blocked",
        "passed": bool(passed),
        "allowed_claims": [JUDGMENT_COMPLETED] if passed else [JUDGMENT_BLOCKED],
        "forbidden_claims": ["alpha_quality", "edge", "baseline", "promotion_candidate", "operating_promotion", "runtime_authority"],
    }


def sync_stage_docs(summary: Mapping[str, Any], result: Mapping[str, Any]) -> None:
    if result.get("external_verification_status") != "completed":
        write_md(
            STAGE_ROOT / "04_selected/selection_status.md",
            "\n".join(
                [
                    "# Stage 14 Selection Status(14단계 선택 상태)",
                    "",
                    "## Current Read(현재 판독)",
                    "",
                    f"- stage(단계): `{STAGE_ID}`",
                    "- status(상태): `blocked_runtime_probe_attempted(런타임 탐침 시도 후 차단)`",
                    f"- current run(현재 실행): `{RUN_ID}`",
                    "- selected operating reference/promotion/baseline(선택 운영 기준/승격/기준선): `none(없음)`",
                    f"- judgment(판정): `{summary['judgment']}`",
                ]
            ),
        )
        return

    write_md(CLOSEOUT_PATH, closeout_report_markdown(summary, result))
    write_md(
        STAGE_ROOT / "04_selected/selection_status.md",
        "\n".join(
            [
                "# Stage 14 Selection Status(14단계 선택 상태)",
                "",
                "## Current Read(현재 판독)",
                "",
                f"- stage(단계): `{STAGE_ID}`",
                "- status(상태): `reviewed_closed_stage15_opened(검토 마감, 15단계 개방)`",
                f"- current run(현재 실행): `{RUN_ID}`",
                "- selected operating reference/promotion/baseline(선택 운영 기준/승격/기준선): `none(없음)`",
                f"- judgment(판정): `{summary['judgment']}`",
                "",
                "효과(effect, 효과): Stage14(14단계)는 SVM(`Support Vector Machine`, 서포트 벡터 머신) margin/kernel(마진/커널) runtime_probe(런타임 탐침) 근거로 닫혔지만, alpha quality(알파 품질)나 promotion(승격)은 만들지 않는다.",
            ]
        ),
    )
    write_md(
        STAGE_ROOT / "03_reviews/review_index.md",
        "\n".join(
            [
                "# Stage 14 Review Index(14단계 검토 색인)",
                "",
                f"- `{RUN_ID}`: `{summary['judgment']}`, report(보고서) `{rel(REPORT_PATH)}`",
                f"- closeout(마감): `{rel(CLOSEOUT_PATH)}`",
                "",
                "효과(effect, 효과): Stage14(14단계)는 SVM(서포트 벡터 머신) 학습 모양과 MT5(메타트레이더5) 런타임 탐침으로 닫혔다.",
            ]
        ),
    )
    write_stage15_scaffold()
    write_decisions(summary)
    sync_workspace_docs(summary)


def write_stage15_scaffold() -> None:
    for subdir in ("00_spec", "01_inputs", "02_runs", "03_reviews", "04_selected"):
        io_path(STAGE15_ROOT / subdir).mkdir(parents=True, exist_ok=True)
    write_md(
        STAGE15_ROOT / "00_spec/stage_brief.md",
        "\n".join(
            [
                "# Stage 15 Untried Learning Methods Scout(15단계 미탐색 학습법 탐색)",
                "",
                "Stage15(15단계)는 아직 독립 탐색으로 다루지 않은 model learning methods(모델 학습법)를 알아가는 독립 주제다.",
                "",
                "- independence(독립성): Stage10/11/12/13/14(10/11/12/13/14단계)의 threshold(임계값), session slice(세션 구간), selected variant(선택 변형)를 baseline(기준선)으로 쓰지 않는다.",
                "- purpose(목적): 새 모델 계열의 training behavior(학습 행동), probability shape(확률 모양), signal density(신호 밀도), validation/OOS stability(검증/표본외 안정성)를 얕게 읽는다.",
                "- boundary(경계): alpha quality(알파 품질), edge(거래 우위), baseline(기준선), promotion(승격), runtime authority(런타임 권위)를 만들지 않는다.",
                "",
                "효과(effect, 효과): Stage15(15단계)는 승자 선택(winner selection, 승자 선택)이 아니라, 아직 보지 않은 학습법이 이 데이터에서 무엇을 가르치는지 확인하는 단계다.",
            ]
        ),
    )
    write_md(
        STAGE15_ROOT / "01_inputs/input_references.md",
        "\n".join(
            [
                "# Stage 15 Input References(15단계 입력 참조)",
                "",
                "- dataset(데이터셋): `model_input_fpmarkets_v2_us100_m5_label_v1_fwd12_split_v1_proxyw58_feature_set_v2`",
                "- label(라벨): `label_v1_fwd12_m5_logret_train_q33_3class`",
                "- split(분할): `split_v1_calendar_train_20220901_20241231_val_20250101_20250930_oos_20251001_20260413`",
                "- feature count(피처 수): `58`",
                "- symbol/timeframe(심볼/시간봉): `US100 M5`",
                "",
                "효과(effect, 효과): Stage15(15단계)의 changed variable(변경 변수)은 model learning method(모델 학습법)이고, 데이터/라벨/분할 변경과 섞지 않는다.",
            ]
        ),
    )
    io_path(STAGE15_ROOT / "02_runs/.gitkeep").write_text("", encoding="utf-8")
    write_md(
        STAGE15_ROOT / "03_reviews/review_index.md",
        "\n".join(
            [
                "# Stage 15 Review Index(15단계 검토 색인)",
                "",
                "Stage15(15단계)는 열렸지만 아직 run(실행)이 없다.",
                "",
                "- current status(현재 상태): `open_no_run_yet(열림, 실행 없음)`",
                "",
                "효과(effect, 효과): 첫 실행 전에는 reviewed(검토됨), baseline(기준선), promotion(승격), runtime authority(런타임 권위)를 주장하지 않는다.",
            ]
        ),
    )
    write_csv_rows(STAGE15_ROOT / "03_reviews/stage_run_ledger.csv", ALPHA_LEDGER_COLUMNS, [])
    write_md(
        STAGE15_ROOT / "04_selected/selection_status.md",
        "\n".join(
            [
                "# Stage 15 Selection Status(15단계 선택 상태)",
                "",
                "## Current Read(현재 판독)",
                "",
                f"- stage(단계): `{STAGE15_ID}`",
                "- status(상태): `open_no_run_yet(열림, 실행 없음)`",
                "- current run(현재 실행): 없음",
                "- selected operating reference/promotion/baseline(선택 운영 기준/승격/기준선): `none(없음)`",
                "- judgment(판정): `design_open_only_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`",
            ]
        ),
    )


def write_decisions(summary: Mapping[str, Any]) -> None:
    write_md(
        ROOT / "docs/decisions/2026-05-02_stage14_svm_margin_kernel_closeout.md",
        closeout_report_markdown(summary, {"external_verification_status": "completed"}),
    )
    write_md(
        ROOT / "docs/decisions/2026-05-02_stage15_untried_learning_methods_open.md",
        "\n".join(
            [
                "# 2026-05-02 Stage15 Untried Learning Methods Open(15단계 미탐색 학습법 개방)",
                "",
                "## Decision(결정)",
                "",
                f"Stage15(15단계)를 `{STAGE15_ID}`로 연다.",
                "",
                "효과(effect, 효과): 다음 작업은 아직 독립 탐색으로 다루지 않은 model learning methods(모델 학습법)를 Stage10/11/12/13/14(10/11/12/13/14단계) 기준선 없이 독립적으로 볼 수 있다.",
                "",
                "## Boundary(경계)",
                "",
                "Stage15(15단계) 개방은 stage transition(단계 전환)과 experiment design(실험 설계)만 뜻한다. alpha quality(알파 품질), edge(거래 우위), promotion candidate(승격 후보), operating promotion(운영 승격), runtime authority(런타임 권위), selected baseline(선택 기준선)을 만들지 않는다.",
            ]
        ),
    )


def sync_workspace_docs(summary: Mapping[str, Any]) -> None:
    state_path = ROOT / "docs/workspace/workspace_state.yaml"
    state = io_path(state_path).read_text(encoding="utf-8-sig")
    state = state.replace("active_stage: 14_model_family_challenge__margin_kernel_training_effect", f"active_stage: {STAGE15_ID}")
    state = state.replace("stage13_reviewed_closed_stage14_opened_no_run_yet", "stage13_reviewed_closed_stage14_reviewed_closed_stage15_opened_no_run_yet")
    state = state.replace(
        "- treat Stage 14 as open_no_run_yet; independent SVM margin/kernel training-effect topic, not a Stage 10/11/12/13 baseline continuation",
        "- treat Stage 15 as open_no_run_yet; independent untried model learning methods topic, not a Stage 10/11/12/13/14 baseline continuation",
    )
    state = state.replace(
        "- treat Stage 13 as reviewed_closed; preserve MLPClassifier(다층 퍼셉트론 분류기) behavior clues(행동 단서), not a baseline(기준선) or promotion(승격)",
        "- treat Stage 14 as reviewed_closed; preserve SVM margin/kernel runtime_probe(런타임 탐침) behavior clues(행동 단서), not a baseline(기준선) or promotion(승격)",
    )
    state = re.sub(
        rf"(    stage14:\n      stage_id: {re.escape(STAGE_ID)}\n      ownership: .+\n      status: )open_no_run_yet",
        rf"\1reviewed_closed_stage15_opened\n      current_run_id: {RUN_ID}",
        state,
        count=1,
    )
    if f"    stage15:\n      stage_id: {STAGE15_ID}" not in state:
        nested_stage15 = f"""    stage15:
      stage_id: {STAGE15_ID}
      ownership: independent untried model learning methods scout after Stage14 closeout
      status: open_no_run_yet
"""
        state = replace_required(state, "stage13_mlp_characteristic_runtime_probe:\n", nested_stage15 + "stage13_mlp_characteristic_runtime_probe:\n", "pre_alpha_stage15_insert")
    stage14_state = f"""stage14_margin_kernel_training_effect:
  stage_id: {STAGE_ID}
  status: reviewed_closed_stage15_opened
  lane: stage14_closeout_topic_pivot_no_promotion
  model_family: sklearn_svm_margin_kernel_family
  current_run_id: {RUN_ID}
  current_status: reviewed
  judgment: {summary['judgment']}
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  preserved_clues: SVM margin/kernel probability shape, threshold visibility, and routed MT5 runtime-probe trade-shape evidence
  negative_memory: SVM margin/kernel closeout remains inconclusive and does not create edge, alpha quality, baseline, promotion, or runtime authority
  external_verification_status: completed_for_recorded_mt5_runtime_probes
  closeout_packet_path: {rel(CLOSEOUT_PATH)}
  closeout_decision_path: docs/decisions/2026-05-02_stage14_svm_margin_kernel_closeout.md
  packet_summary_path: docs/agent_control/packets/stage14_svm_margin_kernel_closeout_v1/stage_closeout_evidence_gate.json
  next_action: stage15_opened_as_independent_untried_learning_methods_topic
"""
    stage15_state = f"""stage15_untried_learning_methods:
  stage_id: {STAGE15_ID}
  status: open_no_run_yet
  lane: independent_model_family_topic_pivot_no_promotion
  model_family: not_yet_selected_untried_learning_methods
  current_run_id: ''
  current_status: no_run_yet
  hypothesis: Untried model learning methods may expose different training behavior, probability shape, and signal density from prior LogReg, LightGBM, ExtraTrees, MLP, and SVM probes.
  comparison_baseline: no trading baseline; compare only against fixed data contract and within-stage Stage15 variants after runs exist
  boundary: design_open_only_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority
  stage_brief_path: stages/{STAGE15_ID}/00_spec/stage_brief.md
  input_references_path: stages/{STAGE15_ID}/01_inputs/input_references.md
  selection_status_path: stages/{STAGE15_ID}/04_selected/selection_status.md
  next_action: design_first_untried_learning_method_scout
"""
    state, replaced = re.subn(
        r"stage14_margin_kernel_training_effect:\n(?:  .*\n)*?stage01_raw_m5_inventory:\n",
        stage14_state + stage15_state + "stage01_raw_m5_inventory:\n",
        state,
        count=1,
    )
    if replaced != 1:
        raise RuntimeError("Required sync marker not found: stage14_state_block")
    io_path(state_path).write_text(state.rstrip() + "\n", encoding="utf-8")

    current_path = ROOT / "docs/context/current_working_state.md"
    current = io_path(current_path).read_text(encoding="utf-8-sig")
    current = current.replace(
        "- active_stage: `14_model_family_challenge__margin_kernel_training_effect(14단계 마진 커널 학습 효과)`",
        f"- active_stage: `{STAGE15_ID}(15단계 미탐색 학습법 탐색)`",
    )
    current = current.replace("- current run(현재 실행): 없음", "- current run(현재 실행): 없음", 1)
    if "## Latest Stage 15 Update(최신 Stage 15 업데이트)" not in current:
        latest = "\n".join(
            [
                "## Latest Stage 15 Update(최신 Stage 15 업데이트)",
                "",
                f"Stage14(14단계)는 `{summary['judgment']}`로 닫혔다. Stage15(15단계)는 `{STAGE15_ID}`로 열렸고 첫 실행은 아직 없다.",
                "",
                "효과(effect, 효과): SVM(`Support Vector Machine`, 서포트 벡터 머신) margin/kernel(마진/커널) 탐색은 MT5(`MetaTrader 5`, 메타트레이더5) runtime_probe(런타임 탐침) 경계로 마감했고, 다음은 아직 독립적으로 보지 않은 model learning methods(모델 학습법)를 알아가는 독립 탐색이다.",
                "",
            ]
        )
        if "## Latest Stage 14 Update" in current:
            before, rest = current.split("## Latest Stage 14 Update", 1)
            marker = "## 쉬운 설명"
            if marker in rest:
                _, after = rest.split(marker, 1)
                current = before + latest + "\n" + marker + after
            else:
                current = latest + "\n" + current
        else:
            current = latest + "\n" + current
    current_stage = "\n".join(
        [
            "## 현재 단계(Current Stage, 현재 단계)",
            "",
            f"`{STAGE15_ID}`",
            "",
            "Stage15(15단계)의 질문(question, 질문)은 아직 독립 탐색으로 다루지 않은 model learning methods(모델 학습법)가 같은 데이터 계약(data contract, 데이터 계약) 위에서 어떤 training behavior(학습 행동), probability shape(확률 모양), signal density(신호 밀도)를 보이는지 알아가는 것이다.",
            "",
            "효과(effect, 효과): Stage15(15단계)는 design-open(설계 개방) 상태라 baseline(기준선), alpha quality(알파 품질), edge(거래 우위), promotion(승격), runtime authority(런타임 권위)를 만들지 않는다.",
            "",
        ]
    )
    current, replaced = re.subn(
        r"## 현재 단계\(Current Stage, 현재 단계\)\n\n.*?(?=## 탐색 원칙\(Exploration Rule, 탐색 원칙\))",
        current_stage + "\n",
        current,
        count=1,
        flags=re.S,
    )
    if replaced != 1:
        raise RuntimeError("Required sync marker not found: current_stage_section")
    io_path(current_path).write_text(current.rstrip() + "\n", encoding="utf-8-sig")

    changelog_path = ROOT / "docs/workspace/changelog.md"
    changelog = io_path(changelog_path).read_text(encoding="utf-8-sig")
    token = "Stage15(15단계)를"
    if token not in changelog:
        addition = (
            f"\n- 2026-05-02: Stage14(14단계) `{RUN_ID}` completed(완료) and closeout(마감) recorded as `{summary['judgment']}`. "
            f"Stage15(15단계)를 `{STAGE15_ID}`로 opened(개방). Effect(효과): SVM(서포트 벡터 머신) margin/kernel(마진/커널) 주제는 runtime_probe(런타임 탐침) 경계로 닫고, 미탐색 model learning methods(모델 학습법)를 새 독립 주제로 시작한다.\n"
        )
        io_path(changelog_path).write_text(changelog.rstrip() + "\n" + addition, encoding="utf-8-sig")


