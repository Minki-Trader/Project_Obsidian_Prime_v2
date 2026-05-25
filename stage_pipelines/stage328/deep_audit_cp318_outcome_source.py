from __future__ import annotations

import ast
import csv
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


STAGE_ID = "328_onnx_candidate_campaign__cp322a_frozen_signal_contract_extraction"
RUN_ID = "run328B_deep_audit_cp318_outcome_source_and_live_feature_rebuild_options_v1"
RUN_NUMBER = "run328B"
STATUS = "completed_cp318_outcome_source_audit_rebuild_required"
JUDGMENT = "blocked_repair_required_no_goal_achieve"
DECISION = "cp318_outcome_source_not_forward_authority_live_feature_rebuild_required"
NEXT_ACTION = "run328C_design_live_feature_rebuild_control_or_stage329_standalone_onnx_packet"
CLAIM_BOUNDARY = (
    "research_development_only_no_new_data_tuning_no_live_readiness_no_deployment_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
SPEC_DIR = STAGE_DIR / "00_spec"
INPUTS_DIR = STAGE_DIR / "01_inputs"
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"

STAGE318_DIR = ROOT / "stages" / "318_onnx_candidate_campaign__post_non_time_curve_stability_rebuild"
STAGE318_PIPELINE = ROOT / "stage_pipelines" / "stage318" / "design_post_non_time_curve_stability_rebuild.py"
STAGE318_RUN_A = STAGE318_DIR / "02_runs" / "run318A"
STAGE318_RUN_B = STAGE318_DIR / "02_runs" / "run318B"
STAGE318_REVIEWS = STAGE318_DIR / "03_reviews"
CP318A_MODEL_JSON = (
    STAGE318_RUN_A
    / "models"
    / "run318A_cp318A_outcome_dense20_curve_stability_curve_stability_surface.json"
)
TRAINING_DIAGNOSTICS = STAGE318_RUN_A / "runtime_outcome_training_diagnostics.json"
TRAINING_SET = STAGE318_RUN_A / "runtime_outcome_training_set.csv"
SCOUT_SCOREBOARD = STAGE318_RUN_A / "model_scout_scoreboard.csv"
MT5_KPI = STAGE318_RUN_B / "mt5_kpi_summary.csv"
RUN318A_REVIEW = STAGE318_REVIEWS / "run318A_materialization.md"
RUN318C_REVIEW = STAGE318_REVIEWS / "run318C_review_stage319_open.md"
RUN328A_REPORT = REVIEWS_DIR / "run328A_frozen_signal_contract_report.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"


def os_path(path: Path) -> Path:
    resolved = path.resolve()
    if os.name == "nt":
        text = str(resolved)
        if not text.startswith("\\\\?\\"):
            return Path("\\\\?\\" + text)
    return resolved


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def path_exists(path: Path) -> bool:
    return os_path(path).exists()


def read_text(path: Path) -> str:
    return os_path(path).read_text(encoding="utf-8-sig")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(read_text(path))


def write_text(path: Path, text: str, encoding: str = "utf-8") -> Path:
    os_path(path.parent).mkdir(parents=True, exist_ok=True)
    os_path(path).write_text(text, encoding=encoding)
    return path


def write_md(path: Path, text: str) -> Path:
    return write_text(path, text.strip() + "\n", encoding="utf-8-sig")


def write_json(path: Path, data: Any) -> Path:
    return write_text(path, json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_csv(path: Path, fieldnames: list[str], rows: Iterable[dict[str, Any]]) -> Path:
    os_path(path.parent).mkdir(parents=True, exist_ok=True)
    with os_path(path).open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})
    return path


def read_csv(path: Path) -> list[dict[str, str]]:
    with os_path(path).open("r", newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def sha256_file(path: Path) -> str:
    if not path_exists(path):
        return "missing"
    h = hashlib.sha256()
    with os_path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def upsert_csv(path: Path, key: str, row: dict[str, Any]) -> None:
    rows: list[dict[str, str]] = []
    if path_exists(path):
        with os_path(path).open("r", newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            fieldnames = list(reader.fieldnames or row.keys())
            rows = list(reader)
    else:
        fieldnames = list(row.keys())
    for name in row:
        if name not in fieldnames:
            fieldnames.append(name)
    clean_row = {name: str(row.get(name, "")) for name in fieldnames}
    replaced = False
    for idx, existing in enumerate(rows):
        if existing.get(key) == clean_row.get(key):
            rows[idx] = clean_row
            replaced = True
            break
    if not replaced:
        rows.append(clean_row)
    write_csv(path, fieldnames, rows)


def read_text_lossless(path: Path) -> tuple[str, bool]:
    raw = os_path(path).read_bytes()
    has_bom = raw.startswith(b"\xef\xbb\xbf")
    return raw.decode("utf-8-sig" if has_bom else "utf-8"), has_bom


def write_text_preserving(path: Path, text: str, had_bom: bool) -> None:
    encoding = "utf-8-sig" if had_bom or path.suffix.lower() in {".md", ".txt"} else "utf-8"
    write_text(path, text, encoding=encoding)


def replace_prefix_line(text: str, prefix: str, new_line: str) -> str:
    lines = text.splitlines()
    for idx, line in enumerate(lines):
        if line.startswith(prefix):
            lines[idx] = new_line
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + new_line + "\n"


def source_line_hits(path: Path, patterns: list[str]) -> str:
    if not path_exists(path):
        return ""
    hits: list[str] = []
    for line_no, line in enumerate(read_text(path).splitlines(), start=1):
        if any(pattern in line for pattern in patterns):
            hits.append(str(line_no))
    return ",".join(hits)


def safe_float(value: Any) -> float | None:
    try:
        if value in (None, ""):
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def safe_int(value: Any) -> int | None:
    try:
        if value in (None, ""):
            return None
        return int(float(value))
    except (TypeError, ValueError):
        return None


def ratio(numerator: float | None, denominator: float | None) -> float | None:
    if numerator is None or denominator in (None, 0):
        return None
    return numerator / denominator


def fmt_num(value: float | int | None, digits: int = 2) -> str:
    if value is None:
        return "NA"
    return f"{value:.{digits}f}"


def load_cp318a_model() -> dict[str, Any]:
    return read_json(CP318A_MODEL_JSON)


def load_cp318a_scout() -> dict[str, str]:
    for row in read_csv(SCOUT_SCOREBOARD):
        if row.get("package_id") == "cp318A_outcome_dense20_curve_stability_surface":
            return row
    raise RuntimeError("cp318A scout row not found")


def load_cp318a_actuals() -> dict[str, dict[str, Any]]:
    actuals: dict[str, dict[str, Any]] = {}
    for row in read_csv(MT5_KPI):
        if "cp318A_outcome_dense20_curve_stabili_actual_routed" not in row.get("record_view", ""):
            continue
        if row.get("route_role") != "actual_routed_total":
            continue
        metrics = ast.literal_eval(row.get("metrics", "{}"))
        split = "validation" if row.get("split") == "validation_is" else row.get("split", "")
        actuals[split] = metrics
    return actuals


def inspect_training_set() -> dict[str, Any]:
    if not path_exists(TRAINING_SET):
        return {"exists": False, "row_count": "missing", "columns": [], "sha256": "missing"}
    with os_path(TRAINING_SET).open("r", newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        header = next(reader, [])
        count = sum(1 for _ in reader)
    return {
        "exists": True,
        "row_count": count,
        "columns": header,
        "sha256": sha256_file(TRAINING_SET),
    }


def feature_class(feature: str) -> tuple[str, str, str]:
    upstream_prefixes = ("stage316_", "stage317_")
    upstream_names = {
        "payoff_edge_score",
        "anti_meta_score",
        "profit_quality_score",
        "density_head_score",
        "runtime_calibration_score",
        "profit_scale_score",
        "smooth_curve_score",
        "anti_regime_flag",
        "smooth_regime_flag",
        "precondition_pass",
    }
    macro_markets = (
        "vix_",
        "us10yr_",
        "usdx_",
        "nvda_",
        "aapl_",
        "msft_",
        "amzn_",
        "mega8_",
        "top3_",
        "us100_minus_",
    )
    if feature in {"source_code", "hyp_signal"}:
        return (
            "surface_identity_signal_dependency",
            "not_live_computable_without_upstream_surface",
            "source surface(원천 표면)와 route signal(경로 신호)이 필요해 cp322A forward handoff(전진 인계)를 직접 만들 수 없다.",
        )
    if feature.startswith(upstream_prefixes) or feature in upstream_names:
        return (
            "upstream_research_score_dependency",
            "requires_full_upstream_rebuild",
            "Stage316/317 또는 점수 표면(score surface, 점수 표면) 산출물이 필요해 raw market(원천 시장) 피처만으로는 재현되지 않는다.",
        )
    if feature.startswith(macro_markets):
        return (
            "macro_or_cross_symbol_market_feature",
            "live_computable_with_data_contract",
            "브로커/외부 심볼 데이터, timestamp(시각) 정렬, 결측 처리가 맞으면 live-like(실거래 유사) 피처로 다시 만들 수 있다.",
        )
    return (
        "us100_technical_market_feature",
        "live_computable_with_feature_contract",
        "US100 M5 가격열과 feature contract(피처 계약)가 맞으면 live-like(실거래 유사) 피처로 다시 만들 수 있다.",
    )


def build_training_audit(
    diagnostics: dict[str, Any],
    model: dict[str, Any],
    training_identity: dict[str, Any],
) -> list[dict[str, Any]]:
    line_hits = source_line_hits(
        STAGE318_PIPELINE,
        [
            "def build_training_set",
            "target = pd.to_numeric(training[\"net_profit\"]",
            "ExtraTreesRegressor",
            "ExtraTreesClassifier",
            "threshold_for_target",
            "positive_probability",
            "selection_caution",
        ],
    )
    return [
        {
            "audit_axis": "training_scope(학습 범위)",
            "evidence_value": diagnostics.get("training_scope", ""),
            "risk_read": "Stage317 validation+OOS actual MT5 trades(검증+표본외 실제 MT5 거래)가 학습에 포함됐다.",
            "judgment": "not_forward_authority",
            "source_path": rel(TRAINING_DIAGNOSTICS),
            "source_line_hits": "",
        },
        {
            "audit_axis": "target_and_label(목표와 라벨)",
            "evidence_value": "target=net_profit, target_class=net_profit>0",
            "risk_read": "실제 손익을 예측/분류한 outcome distillation(결과 증류)이므로 미래 신호 생성 권한이 아니다.",
            "judgment": "high_overfit_risk",
            "source_path": rel(STAGE318_PIPELINE),
            "source_line_hits": line_hits,
        },
        {
            "audit_axis": "model_family(모델 계열)",
            "evidence_value": "ExtraTreesRegressor+ExtraTreesClassifier n_estimators=700 max_depth=9 min_samples_leaf=15",
            "risk_read": "강한 비선형 표면이 과거 실제 거래 조각을 잘 외울 수 있다.",
            "judgment": "exploratory_only",
            "source_path": rel(STAGE318_PIPELINE),
            "source_line_hits": line_hits,
        },
        {
            "audit_axis": "in_sample_auc(표본내 AUC)",
            "evidence_value": diagnostics.get("auc_in_sample", ""),
            "risk_read": "표본내 점수이며 forward(전진) 또는 WFO(워크포워드) 검증이 아니다.",
            "judgment": "cannot_promote",
            "source_path": rel(TRAINING_DIAGNOSTICS),
            "source_line_hits": "",
        },
        {
            "audit_axis": "training_payoff_total(학습 손익 총합)",
            "evidence_value": diagnostics.get("net_profit_total", ""),
            "risk_read": "학습 조각 전체 손익은 음수인데, 모델은 그 안에서 과거 승자 조각을 선별한다.",
            "judgment": "selection_bias_risk",
            "source_path": rel(TRAINING_DIAGNOSTICS),
            "source_line_hits": "",
        },
        {
            "audit_axis": "threshold_policy(임계값 정책)",
            "evidence_value": f"score_threshold={model.get('score_threshold')}; probability_floor={model.get('probability_floor')}; target_raw_signals_per_day={model.get('target_raw_signals_per_day')}",
            "risk_read": "validation subset(검증 부분집합)의 목표 신호 밀도로 threshold(임계값)를 정했다.",
            "judgment": "not_forward_universal",
            "source_path": rel(CP318A_MODEL_JSON),
            "source_line_hits": "",
        },
        {
            "audit_axis": "training_set_identity(학습 세트 정체성)",
            "evidence_value": f"rows={training_identity.get('row_count')}; sha256={training_identity.get('sha256')}",
            "risk_read": "row identity(행 정체성)는 남겼지만, 이것은 과거 학습 세트 정체성일 뿐 forward handoff(전진 인계)가 아니다.",
            "judgment": "connected_with_boundary",
            "source_path": rel(TRAINING_SET),
            "source_line_hits": "",
        },
    ]


def build_feature_matrix(model: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for order, feature in enumerate(model.get("model_feature_order", []), start=1):
        dependency, live_status, effect = feature_class(str(feature))
        rows.append(
            {
                "feature_order": order,
                "feature": feature,
                "dependency_class": dependency,
                "live_rebuild_status": live_status,
                "forward_risk": effect,
            }
        )
    return rows


def build_gap_rows(scout: dict[str, str], actuals: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    split_specs = [
        ("validation", "estimated_validation"),
        ("oos", "estimated_oos"),
    ]
    rows: list[dict[str, Any]] = []
    for split, est_prefix in split_specs:
        actual = actuals.get(split, {})
        est_net = safe_float(scout.get(f"{est_prefix}_net_profit"))
        actual_net = safe_float(actual.get("net_profit"))
        est_pf = safe_float(scout.get(f"{est_prefix}_pf"))
        actual_pf = safe_float(actual.get("profit_factor"))
        est_trades = safe_int(scout.get(f"{est_prefix}_trade_count"))
        actual_trades = safe_int(actual.get("trade_count"))
        est_tpd = safe_float(scout.get(f"{est_prefix}_trades_per_day"))
        actual_tpd = safe_float(actual.get("trades_per_day"))
        actual_dd = safe_float(actual.get("max_drawdown_percent"))
        rows.append(
            {
                "split": split,
                "estimated_net_profit": est_net,
                "actual_mt5_net_profit": actual_net,
                "net_scale_ratio_actual_to_estimated": ratio(actual_net, est_net),
                "estimated_pf": est_pf,
                "actual_mt5_pf": actual_pf,
                "pf_gap_actual_minus_estimated": None if actual_pf is None or est_pf is None else actual_pf - est_pf,
                "estimated_trade_count": est_trades,
                "actual_mt5_trade_count": actual_trades,
                "trade_count_ratio_actual_to_estimated": ratio(actual_trades, est_trades),
                "estimated_trades_per_day": est_tpd,
                "actual_mt5_trades_per_day": actual_tpd,
                "actual_max_drawdown_percent": actual_dd,
                "stage318C_failed_gates": "smooth_curve;stability_pressure",
                "judgment": "estimated_replay_not_reliable_as_forward_calibration",
            }
        )
    return rows


def build_overfit_rows(diagnostics: dict[str, Any], gap_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    val_ratio = gap_rows[0].get("net_scale_ratio_actual_to_estimated")
    oos_ratio = gap_rows[1].get("net_scale_ratio_actual_to_estimated")
    return [
        {
            "risk_id": "stage317_actual_outcome_distillation",
            "evidence": diagnostics.get("training_scope", ""),
            "why_it_matters": "과거 validation+OOS(검증+표본외) 실제 손익을 학습 target(목표)으로 쓴다.",
            "forward_consequence": "새 forward(전진) 구간에서는 같은 outcome label(결과 라벨)이 존재하지 않아 frozen generator(고정 생성기)가 없다.",
            "severity": "critical",
            "repair_direction": "train-only/WFO(학습 전용/워크포워드) source rebuild(원천 재구축)",
        },
        {
            "risk_id": "in_sample_auc_interpreted_too_strongly",
            "evidence": diagnostics.get("auc_in_sample", ""),
            "why_it_matters": "AUC가 표본내(in-sample, 표본내)라 모델 일반화가 아니라 과거 조각 분류력을 보여준다.",
            "forward_consequence": "ONNX(온엑스)로 고정해도 forward authority(전진 권한)가 생기지 않는다.",
            "severity": "high",
            "repair_direction": "chronological holdout(시간순 보류)와 WFO(워크포워드)로 분리",
        },
        {
            "risk_id": "estimated_to_actual_scale_break",
            "evidence": f"validation_ratio={fmt_num(val_ratio)}; oos_ratio={fmt_num(oos_ratio)}",
            "why_it_matters": "Stage318 추정 replay(재생) 순수익과 실제 MT5(메타트레이더5) 순수익 규모가 140배 이상 벌어진다.",
            "forward_consequence": "estimated scoreboard(추정 점수판)를 forward calibration(전진 보정)으로 쓸 수 없다.",
            "severity": "high",
            "repair_direction": "MT5 actual(실제 MT5) 기준 재검증과 비용/슬리피지 압박",
        },
        {
            "risk_id": "upstream_research_feature_dependency",
            "evidence": "stage316_*, stage317_*, payoff_edge_score, smooth_curve_score, source_code, hyp_signal",
            "why_it_matters": "시장 원천 피처가 아니라 이전 연구 표면과 신호를 다시 입력으로 먹는다.",
            "forward_consequence": "Stage322/323/325 cp322A identity ONNX(정체성 온엑스)는 새 구간 신호를 자체 생성하지 못한다.",
            "severity": "critical",
            "repair_direction": "raw market(원천 시장) 피처 기반 standalone packet(독립 패킷) 또는 upstream full rebuild(상류 전체 재구축)",
        },
    ]


def build_rebuild_options() -> list[dict[str, Any]]:
    return [
        {
            "option_id": "live_feature_standalone_onnx_packet",
            "allowed": "yes_new_stage_required",
            "description": "Raw market/live-computable feature(원천 시장/실시간 계산 가능 피처)만으로 새 ONNX(온엑스) 후보 패킷을 설계한다.",
            "anti_overfit_control": "train-only threshold(학습 전용 임계값), WFO(워크포워드), untouched forward holdout(미접촉 전진 보류)",
            "effect": "cp322A를 수정하지 않고, 쓸만한 ONNX를 새로 만들 수 있는지 검증한다.",
        },
        {
            "option_id": "cp318_source_replay_fixture_only",
            "allowed": "yes_research_fixture_only",
            "description": "Stage318/322 historical replay(과거 재생)를 fixture(고정 테스트 조각)로만 보존한다.",
            "anti_overfit_control": "forward claims(전진 주장) 금지",
            "effect": "과거 parity(동등성) 테스트에는 쓰되, forward 신호 생성기로 오해하지 않는다.",
        },
        {
            "option_id": "upstream_train_only_rebuild_control",
            "allowed": "yes_research_control_not_cp322a",
            "description": "Stage316/317/318 source surface(원천 표면)를 train-only/WFO(학습 전용/워크포워드) 규칙으로 다시 만든다.",
            "anti_overfit_control": "old cp322A threshold/rank(임계값/순위) 재사용 금지, forward holdout(전진 보류) untouched(미접촉)",
            "effect": "cp322A의 위험 원인이 source outcome distillation(원천 결과 증류)인지 분리한다.",
        },
        {
            "option_id": "split_rank_forward_generation",
            "allowed": "no_rejected",
            "description": "새 forward(전진) 구간 안에서 score_rank(점수 순위)를 다시 계산해 cp322A 신호를 만든다.",
            "anti_overfit_control": "rejected because split-local rank(분할 내부 순위) leaks future distribution(미래 분포)",
            "effect": "과적합을 고치기 위한 또 다른 과적합화를 막는다.",
        },
        {
            "option_id": "preserve_cp322a_artifact_no_operating_claim",
            "allowed": "yes_current_boundary",
            "description": "cp322A를 ONNX research artifact(연구 산출물)로 보존한다.",
            "anti_overfit_control": "live readiness(실거래 준비), deployment(배포), operating promotion(운영 승격) 금지",
            "effect": "기존 산출물을 폐기하지 않되 권한을 과장하지 않는다.",
        },
    ]


def write_reports(
    generated_at_utc: str,
    diagnostics: dict[str, Any],
    model: dict[str, Any],
    training_identity: dict[str, Any],
    training_rows: list[dict[str, Any]],
    feature_rows: list[dict[str, Any]],
    gap_rows: list[dict[str, Any]],
    overfit_rows: list[dict[str, Any]],
    rebuild_rows: list[dict[str, Any]],
) -> list[Path]:
    artifacts: list[Path] = []
    feature_counts: dict[str, int] = {}
    for row in feature_rows:
        feature_counts[row["dependency_class"]] = feature_counts.get(row["dependency_class"], 0) + 1
    val_gap = gap_rows[0]
    oos_gap = gap_rows[1]
    artifacts.append(
        write_md(
            SPEC_DIR / "stage_brief.md",
            f"""
# Stage328 cp322A Frozen Signal Contract Extraction(328단계 cp322A 고정 신호 계약 추출)

- active_question(활성 질문): cp322A(322A 후보)를 수정하지 않고, `run322b_route_signal`의 upstream source(상류 원천)가 forward-safe(전진 안전)인지 확인한다.
- run328A(328A 실행): frozen signal contract(고정 신호 계약)을 추출했고, exact replay(정확 재생)는 과거 창 전용임을 확인했다.
- run328B(328B 실행): Stage318 outcome source(318단계 결과 원천)와 live feature rebuild(실시간 피처 재구축) 가능성을 감사한다.
- fixed_rules(고정 규칙): selected candidate(선택 후보), ONNX model(온엑스 모델), Adapter package(어댑터 패키지), feature order(피처 순서), D/B decision surface(D/B 판단 표면), score threshold(점수 임계값), risk/lot/ATR/runtime logic(위험/랏/ATR/런타임 로직)을 수정하지 않는다.
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
        )
    )
    artifacts.append(
        write_md(
            INPUTS_DIR / "input_refs_run328B.md",
            f"""
# run328B Input References(328B 입력 참조)

- generated_at_utc(생성 시각): `{generated_at_utc}`
- primary_source(주 원천): `{rel(STAGE318_PIPELINE)}`
- model_spec(모델 규격): `{rel(CP318A_MODEL_JSON)}`
- training_diagnostics(학습 진단): `{rel(TRAINING_DIAGNOSTICS)}`
- training_set(학습 세트): `{rel(TRAINING_SET)}`
- estimated_scoreboard(추정 점수판): `{rel(SCOUT_SCOREBOARD)}`
- actual_mt5_kpi(실제 MT5 핵심 성과 지표): `{rel(MT5_KPI)}`
- run318A_review(318A 검토): `{rel(RUN318A_REVIEW)}`
- run318C_review(318C 검토): `{rel(RUN318C_REVIEW)}`
- run328A_boundary(328A 경계): `{rel(RUN328A_REPORT)}`

Effect(효과): run328B(328B 실행)는 새 데이터로 cp322A를 튜닝하지 않고, 이미 생성된 Stage318/MT5 evidence(근거)의 source authority(원천 권한)만 판정한다.
""",
        )
    )
    artifacts.append(
        write_csv(
            RUN_DIR / "outcome_source_training_audit.csv",
            ["audit_axis", "evidence_value", "risk_read", "judgment", "source_path", "source_line_hits"],
            training_rows,
        )
    )
    artifacts.append(
        write_csv(
            RUN_DIR / "feature_live_rebuild_matrix.csv",
            ["feature_order", "feature", "dependency_class", "live_rebuild_status", "forward_risk"],
            feature_rows,
        )
    )
    artifacts.append(
        write_csv(
            RUN_DIR / "mt5_actual_vs_estimated_gap.csv",
            [
                "split",
                "estimated_net_profit",
                "actual_mt5_net_profit",
                "net_scale_ratio_actual_to_estimated",
                "estimated_pf",
                "actual_mt5_pf",
                "pf_gap_actual_minus_estimated",
                "estimated_trade_count",
                "actual_mt5_trade_count",
                "trade_count_ratio_actual_to_estimated",
                "estimated_trades_per_day",
                "actual_mt5_trades_per_day",
                "actual_max_drawdown_percent",
                "stage318C_failed_gates",
                "judgment",
            ],
            gap_rows,
        )
    )
    artifacts.append(
        write_csv(
            RUN_DIR / "overfit_pathology_matrix.csv",
            ["risk_id", "evidence", "why_it_matters", "forward_consequence", "severity", "repair_direction"],
            overfit_rows,
        )
    )
    artifacts.append(
        write_csv(
            RUN_DIR / "rebuild_option_queue.csv",
            ["option_id", "allowed", "description", "anti_overfit_control", "effect"],
            rebuild_rows,
        )
    )
    artifacts.append(
        write_md(
            REVIEWS_DIR / "run328B_cp318_outcome_source_audit.md",
            f"""
# run328B cp318 Outcome Source Audit(328B cp318 결과 원천 감사)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- goal_achieve(목표 달성): `not_claimed`

## Core Finding(핵심 발견)

cp318A(318A 후보)는 Stage317 validation+OOS(검증+표본외) 실제 MT5 손익을 학습한 outcome distillation(결과 증류) 표면이다. 학습 행은 `{diagnostics.get("training_rows")}`개, positive_rate(양수 비율)는 `{fmt_num(safe_float(diagnostics.get("positive_rate")), 4)}`, in_sample_auc(표본내 AUC)는 `{fmt_num(safe_float(diagnostics.get("auc_in_sample")), 4)}`다.

Effect(효과): 이 수치는 과거 조각을 잘 분류했다는 근거이지, 새 forward(전진) 구간에서 신호를 만들 권한은 아니다.

## Feature Authority(피처 권한)

- model_feature_count(모델 피처 수): `{len(feature_rows)}`
- market_live_computable(시장 기반 재구축 가능): `{feature_counts.get("us100_technical_market_feature", 0) + feature_counts.get("macro_or_cross_symbol_market_feature", 0)}`
- upstream_research_dependency(상류 연구 의존): `{feature_counts.get("upstream_research_score_dependency", 0)}`
- surface_signal_dependency(표면/신호 의존): `{feature_counts.get("surface_identity_signal_dependency", 0)}`

Effect(효과): raw market(원천 시장) 피처만 다시 계산해서 cp318A/cp322A를 forward(전진)에 옮길 수 없다. `source_code`와 `hyp_signal`은 upstream source surface(상류 원천 표면)를 요구한다.

## Estimated vs Actual Gap(추정 대 실제 차이)

| split(구간) | estimated net(추정 순수익) | actual MT5 net(실제 MT5 순수익) | scale ratio(규모 비율) | estimated PF(추정 수익 팩터) | actual PF(실제 수익 팩터) | actual DD%(실제 손실폭) |
|---|---:|---:|---:|---:|---:|---:|
| validation(검증) | {fmt_num(safe_float(val_gap.get("estimated_net_profit")))} | {fmt_num(safe_float(val_gap.get("actual_mt5_net_profit")))} | {fmt_num(safe_float(val_gap.get("net_scale_ratio_actual_to_estimated")))} | {fmt_num(safe_float(val_gap.get("estimated_pf")))} | {fmt_num(safe_float(val_gap.get("actual_mt5_pf")))} | {fmt_num(safe_float(val_gap.get("actual_max_drawdown_percent")))} |
| OOS(표본외) | {fmt_num(safe_float(oos_gap.get("estimated_net_profit")))} | {fmt_num(safe_float(oos_gap.get("actual_mt5_net_profit")))} | {fmt_num(safe_float(oos_gap.get("net_scale_ratio_actual_to_estimated")))} | {fmt_num(safe_float(oos_gap.get("estimated_pf")))} | {fmt_num(safe_float(oos_gap.get("actual_mt5_pf")))} | {fmt_num(safe_float(oos_gap.get("actual_max_drawdown_percent")))} |

Effect(효과): estimated replay(추정 재생)와 actual MT5(실제 MT5) 사이의 규모가 140배 이상 벌어져, 이 점수판을 forward calibration(전진 보정)으로 쓸 수 없다.

## Decision(결정)

cp322A(322A 후보)는 계속 frozen research artifact(고정 연구 산출물)로 보존한다. 그러나 cp318A outcome source(결과 원천)는 forward authority(전진 권한)가 아니며, cp322A forward generator(전진 생성기)는 아직 없다.

Next action(다음 행동): `{NEXT_ACTION}`

`{CLAIM_BOUNDARY}`
""",
        )
    )
    artifacts.append(
        write_md(
            REVIEWS_DIR / "final_stage328B_decision_report.md",
            f"""
# Stage328B Final Decision(328B 최종 판정)

- decision(결정): `{DECISION}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- forward_signal_generator(전진 신호 생성기): `not_available`
- cp318_outcome_source_authority(cp318 결과 원천 권한): `not_forward_authority`
- goal_achieve(목표 달성): `not_claimed`
- effect(효과): cp322A(322A 후보)를 수정하지 않고 원천을 감사한 결과, Stage318 outcome source(결과 원천)는 과거 실제 MT5 손익을 증류한 표면이라 forward-safe generation(전진 안전 생성)을 제공하지 않는다.
- next_action(다음 행동): `{NEXT_ACTION}`

Allowed path(허용 경로)는 cp322A를 튜닝하는 것이 아니라, raw market/live-computable feature(원천 시장/실시간 계산 가능 피처) 기반의 새 rebuild control(재구축 대조)이나 standalone ONNX packet(독립 온엑스 패킷)을 별도 단계에서 설계하는 것이다.
""",
        )
    )
    artifacts.append(
        write_md(
            SELECTED_DIR / "selection_status.md",
            f"""
# Stage328 Selection Status(328단계 선택 상태)

- selected_candidate(선택 후보): `cp322A_cp321b_exact_replay_control_surface`
- package_status(패키지 상태): `research_artifact_preserved`
- forward_usability(전진 사용 가능성): `blocked_rebuild_required`
- frozen_signal_contract(고정 신호 계약): `historical_exact_only_forward_not_safe`
- cp318_outcome_source_authority(cp318 결과 원천 권한): `not_forward_authority`
- live_readiness(실거래 준비): `not_claimed`
- deployment(배포): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`
- effect(효과): cp322A는 그대로 보존하지만, forward(전진)에서 쓸 신호 생성 권한은 없다.
""",
        )
    )
    return artifacts


def write_receipts(
    generated_at_utc: str,
    diagnostics: dict[str, Any],
    model: dict[str, Any],
    training_identity: dict[str, Any],
    feature_rows: list[dict[str, Any]],
    gap_rows: list[dict[str, Any]],
) -> list[Path]:
    generated_report = REVIEWS_DIR / "run328B_cp318_outcome_source_audit.md"
    feature_counts: dict[str, int] = {}
    for row in feature_rows:
        feature_counts[row["dependency_class"]] = feature_counts.get(row["dependency_class"], 0) + 1
    artifacts: list[Path] = []
    artifacts.append(
        write_json(
            RUN_DIR / "experiment_design_receipt.json",
            {
                "hypothesis": "cp318A outcome source(결과 원천)가 cp322A forward signal generation(전진 신호 생성)에 충분한 권한을 제공하는지 감사한다.",
                "decision_use": "forward robustness goal(전진 견고성 목표)의 차단 원인과 다음 rebuild direction(재구축 방향)을 정한다.",
                "comparison_baseline": "run328A frozen signal contract extraction(고정 신호 계약 추출)",
                "control_variables": [
                    "cp322A selected candidate unchanged(선택 후보 불변)",
                    "ONNX model unchanged(온엑스 모델 불변)",
                    "score threshold unchanged(점수 임계값 불변)",
                    "risk/lot/runtime logic unchanged(위험/랏/런타임 로직 불변)",
                ],
                "changed_variables": ["none_on_candidate; audit_only(후보 변경 없음; 감사 전용)"],
                "sample_scope": "Stage318 existing training diagnostics, model spec, estimated replay scoreboard, run318B MT5 actual KPI",
                "success_criteria": "source authority(원천 권한), leakage risk(누수 위험), rebuild options(재구축 선택지)를 문서와 receipt(영수증)에 고정",
                "failure_criteria": "cp318A can be trusted as forward authority without rebuild",
                "invalid_conditions": ["missing Stage318 artifacts", "missing run318B actual MT5 evidence"],
                "stop_conditions": ["do not tune cp322A", "do not generate forward signal from split-local rank"],
                "evidence_plan": [
                    rel(RUN_DIR / "outcome_source_training_audit.csv"),
                    rel(RUN_DIR / "feature_live_rebuild_matrix.csv"),
                    rel(RUN_DIR / "mt5_actual_vs_estimated_gap.csv"),
                    rel(RUN_DIR / "overfit_pathology_matrix.csv"),
                    rel(generated_report),
                ],
            },
        )
    )
    artifacts.append(
        write_json(
            RUN_DIR / "data_integrity_receipt.json",
            {
                "data_source": [
                    rel(TRAINING_DIAGNOSTICS),
                    rel(TRAINING_SET),
                    rel(SCOUT_SCOREBOARD),
                    rel(MT5_KPI),
                ],
                "time_axis": "existing Stage318 artifacts; no new bars created; timestamp policy inherited from Stage318/Stage317 MT5 evidence",
                "sample_scope": diagnostics.get("training_scope", ""),
                "missing_or_duplicate_check": "not re-run; this is source authority audit using existing materialized evidence",
                "feature_label_boundary": "net_profit and positive_trade are labels from actual MT5 trades; not available for forward features",
                "split_boundary": "Stage317 validation+OOS used in training, therefore not a clean forward boundary",
                "leakage_risk": "actual outcome distillation plus split-local threshold/rank paths",
                "data_hash_or_identity": {
                    "training_set_rows": training_identity.get("row_count"),
                    "training_set_sha256": training_identity.get("sha256"),
                    "training_diagnostics_sha256": sha256_file(TRAINING_DIAGNOSTICS),
                    "mt5_kpi_sha256": sha256_file(MT5_KPI),
                },
                "integrity_judgment": "usable_with_boundary_not_forward_authority",
            },
        )
    )
    artifacts.append(
        write_json(
            RUN_DIR / "model_validation_receipt.json",
            {
                "model_family": "ExtraTrees outcome distillation(결과 증류) from Stage318",
                "target_and_label": "net_profit regression and net_profit>0 classification",
                "split_method": "not clean forward; validation+OOS actual trades included in training",
                "selection_metric": "estimated net/PF/trades/day/gates plus later actual MT5 review",
                "secondary_metrics": {
                    "in_sample_auc": diagnostics.get("auc_in_sample"),
                    "positive_rate": diagnostics.get("positive_rate"),
                    "training_net_profit_total": diagnostics.get("net_profit_total"),
                    "actual_vs_estimated_gap": gap_rows,
                },
                "threshold_policy": {
                    "score_threshold": model.get("score_threshold"),
                    "probability_floor": model.get("probability_floor"),
                    "target_raw_signals_per_day": model.get("target_raw_signals_per_day"),
                },
                "overfit_risk": "high; outcome labels from validation+OOS actual MT5 trades and upstream research features",
                "calibration_risk": "scores rank/select historical winners; not calibrated forward probabilities",
                "comparison_baseline": "run328A frozen contract and Stage318 run318C no-selection review",
                "validation_judgment": "blocked_repair_required_no_goal_achieve",
            },
        )
    )
    artifacts.append(
        write_json(
            RUN_DIR / "runtime_parity_receipt.json",
            {
                "research_path": rel(STAGE318_PIPELINE),
                "runtime_path": "cp322A ONNX package remains unchanged; no new MT5 run in run328B",
                "shared_contract": "cp322A ONNX consumes run322b_route_signal identity input; Stage318 produced historical route_signal_value",
                "known_differences": "no forward-safe generator for run322b_route_signal",
                "parity_check": "existing Stage318 MT5 evidence and Stage325 ONNX parity only; no new runtime claim",
                "parity_identity": {
                    "cp318a_model_spec_sha256": sha256_file(CP318A_MODEL_JSON),
                    "stage318_pipeline_sha256": sha256_file(STAGE318_PIPELINE),
                },
                "runtime_claim_boundary": "blocked_no_runtime_authority",
            },
        )
    )
    artifacts.append(
        write_json(
            RUN_DIR / "artifact_lineage_receipt.json",
            {
                "source_inputs": [
                    rel(CP318A_MODEL_JSON),
                    rel(TRAINING_DIAGNOSTICS),
                    rel(TRAINING_SET),
                    rel(SCOUT_SCOREBOARD),
                    rel(MT5_KPI),
                    rel(RUN318A_REVIEW),
                    rel(RUN318C_REVIEW),
                ],
                "producer": rel(Path(__file__)),
                "consumer": [
                    rel(generated_report),
                    rel(REVIEWS_DIR / "final_stage328B_decision_report.md"),
                    rel(SELECTED_DIR / "selection_status.md"),
                    "docs/registers/run_registry.csv",
                    "docs/registers/alpha_run_ledger.csv",
                    "docs/registers/artifact_registry.csv",
                ],
                "artifact_paths": [
                    rel(RUN_DIR / "outcome_source_training_audit.csv"),
                    rel(RUN_DIR / "feature_live_rebuild_matrix.csv"),
                    rel(RUN_DIR / "mt5_actual_vs_estimated_gap.csv"),
                    rel(RUN_DIR / "overfit_pathology_matrix.csv"),
                    rel(RUN_DIR / "rebuild_option_queue.csv"),
                    rel(generated_report),
                ],
                "artifact_hashes": {
                    "cp318a_model_spec_sha256": sha256_file(CP318A_MODEL_JSON),
                    "training_set_sha256": training_identity.get("sha256"),
                    "stage318_pipeline_sha256": sha256_file(STAGE318_PIPELINE),
                },
                "registry_links": [
                    rel(RUN_REGISTRY),
                    rel(ALPHA_LEDGER),
                    rel(ARTIFACT_REGISTRY),
                    rel(REVIEWS_DIR / "stage_run_ledger.csv"),
                ],
                "availability": "tracked_reports_and_generated_run_artifacts",
                "lineage_judgment": "connected_with_boundary",
            },
        )
    )
    artifacts.append(
        write_csv(
            RUN_DIR / "required_gate_coverage_audit.csv",
            ["gate_name", "status", "evidence_path", "effect"],
            [
                {
                    "gate_name": "experiment_design(실험 설계)",
                    "status": "passed",
                    "evidence_path": rel(RUN_DIR / "experiment_design_receipt.json"),
                    "effect": "candidate(후보)를 변경하지 않는 audit-only(감사 전용) 범위를 고정했다.",
                },
                {
                    "gate_name": "data_integrity(데이터 무결성)",
                    "status": "passed_with_boundary",
                    "evidence_path": rel(RUN_DIR / "data_integrity_receipt.json"),
                    "effect": "Stage318 training scope(학습 범위)가 forward authority(전진 권한)가 아님을 기록했다.",
                },
                {
                    "gate_name": "model_validation(모델 검증)",
                    "status": "passed_blocked_for_forward",
                    "evidence_path": rel(RUN_DIR / "model_validation_receipt.json"),
                    "effect": "in-sample AUC(표본내 AUC)와 outcome distillation(결과 증류)을 overfit risk(과적합 위험)로 판정했다.",
                },
                {
                    "gate_name": "runtime_parity(런타임 동등성)",
                    "status": "blocked_no_new_runtime_claim",
                    "evidence_path": rel(RUN_DIR / "runtime_parity_receipt.json"),
                    "effect": "forward route signal generator(전진 경로 신호 생성기)가 없어 새 MT5 forward result(전진 결과)를 주장하지 않는다.",
                },
                {
                    "gate_name": "artifact_lineage(산출물 계보)",
                    "status": "passed",
                    "evidence_path": rel(RUN_DIR / "artifact_lineage_receipt.json"),
                    "effect": "Stage318 입력과 Stage328B 보고서/장부 연결을 남겼다.",
                },
                {
                    "gate_name": "result_judgment(결과 판정)",
                    "status": "passed_no_goal_achieve",
                    "evidence_path": rel(RUN_DIR / "result_judgment.csv"),
                    "effect": "Goal Achieve(목표 달성), live readiness(실거래 준비), deployment(배포)를 주장하지 않는다.",
                },
            ],
        )
    )
    artifacts.append(
        write_csv(
            RUN_DIR / "result_judgment.csv",
            ["run_id", "status", "judgment", "decision", "goal_achieve", "next_action", "claim_boundary"],
            [
                {
                    "run_id": RUN_ID,
                    "status": STATUS,
                    "judgment": JUDGMENT,
                    "decision": DECISION,
                    "goal_achieve": "not_claimed",
                    "next_action": NEXT_ACTION,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            ],
        )
    )
    artifacts.append(
        write_json(
            RUN_DIR / "run_manifest.json",
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "generated_at_utc": generated_at_utc,
                "command": "python stage_pipelines/stage328/deep_audit_cp318_outcome_source.py",
                "candidate_mutation": "none",
                "next_action": NEXT_ACTION,
                "goal_achieve": "not_claimed",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        )
    )
    upsert_csv(
        REVIEWS_DIR / "stage_run_ledger.csv",
        "row_id",
        {
            "row_id": f"{RUN_ID}__cp318_outcome_source_audit",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "view": "cp318_outcome_source_audit(318 결과 원천 감사)",
            "tier_scope": "existing Stage318 validation/OOS evidence only(기존 318단계 검증/표본외 근거 전용)",
            "scoreboard": "source_authority_and_overfit_audit(원천 권한 및 과적합 감사)",
            "status": STATUS,
            "judgment": JUDGMENT,
            "evidence_boundary": CLAIM_BOUNDARY,
            "report_path": rel(generated_report),
            "notes": "cp318_outcome_source_not_forward_authority;goal_achieve_not_claimed.",
        },
    )
    return artifacts + [REVIEWS_DIR / "stage_run_ledger.csv"]


def update_registers(generated_at_utc: str, artifacts: list[Path]) -> None:
    upsert_csv(
        RUN_REGISTRY,
        "run_id",
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "model_validation",
            "status": STATUS,
            "judgment": JUDGMENT,
            "path": rel(REVIEWS_DIR / "run328B_cp318_outcome_source_audit.md"),
            "notes": "cp318_outcome_source_not_forward_authority;live_feature_rebuild_required;goal_achieve_not_claimed.",
        },
    )
    upsert_csv(
        ALPHA_LEDGER,
        "ledger_row_id",
        {
            "ledger_row_id": f"{RUN_ID}__cp318_outcome_source_audit",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": RUN_NUMBER,
            "parent_run_id": "run328A_extract_frozen_signal_contract_no_new_data_tuning_v1",
            "record_view": "cp318_outcome_source_audit",
            "tier_scope": "existing Stage318 validation/OOS evidence only",
            "kpi_scope": "source_authority_and_overfit_audit",
            "scoreboard_lane": "model_validation",
            "status": STATUS,
            "judgment": JUDGMENT,
            "path": rel(REVIEWS_DIR / "run328B_cp318_outcome_source_audit.md"),
            "primary_kpi": "cp318_outcome_source_not_forward_authority",
            "guardrail_kpi": "goal_achieve_not_claimed;no_new_data_tuning;candidate_unchanged",
            "external_verification_status": "out_of_scope_by_claim_existing_mt5_evidence_only",
            "notes": f"next_action={NEXT_ACTION}.",
        },
    )
    for artifact in artifacts:
        if not path_exists(artifact) or os_path(artifact).is_dir():
            continue
        upsert_csv(
            ARTIFACT_REGISTRY,
            "artifact_id",
            {
                "artifact_id": f"{RUN_ID}__{artifact.stem}".replace("-", "_"),
                "artifact_type": artifact.suffix.lstrip(".") or "file",
                "path": rel(artifact),
                "sha256": sha256_file(artifact),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": generated_at_utc,
                "notes": STATUS,
            },
        )


def update_current_truth() -> Path:
    workspace = ROOT / "docs" / "workspace" / "workspace_state.yaml"
    text, had_bom = read_text_lossless(workspace)
    text = replace_prefix_line(text, "current_run_id:", f"current_run_id: {RUN_ID}")
    text = replace_prefix_line(text, "updated_on:", "updated_on: '2026-05-26'")
    text = replace_prefix_line(text, "active_stage:", f"active_stage: {STAGE_ID}")
    focus = (
        "- >-\n"
        "  Stage328(328단계) run328B(328B 실행) cp318 outcome source audit(cp318 결과 원천 감사)를 닫았다. "
        "Effect(효과): Stage318 outcome distillation(결과 증류)은 forward authority(전진 권한)가 아니며, "
        "cp322A forward signal generator(전진 신호 생성기)는 여전히 없어 Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    if "Stage328(328단계) run328B(328B 실행)" not in text:
        text = text.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    write_text_preserving(workspace, text, had_bom)

    current = ROOT / "docs" / "context" / "current_working_state.md"
    text, had_bom = read_text_lossless(current)
    replacements = {
        "- current_packet(": f"- current_packet(현재 작업 묶음): `{STAGE_ID}_v1`",
        "- current_run(": f"- current_run(현재 실행): `{RUN_ID}`",
        "- active_stage(": f"- active_stage(활성 단계): `{STAGE_ID}`",
        "- source_stage(": "- source_stage(원천 단계): `318_onnx_candidate_campaign__post_non_time_curve_stability_rebuild`",
        "- target_surface(": "- target_surface(목표 표면): `cp322A_cp321b_exact_replay_control_surface`",
        "- status(": f"- status(상태): `{STATUS}`",
        "- decision(": f"- decision(판정): `{JUDGMENT}`",
        "- next_action(": f"- next_action(다음 행동): `{NEXT_ACTION}`",
        "- claim_boundary(": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    }
    for prefix, new_line in replacements.items():
        text = replace_prefix_line(text, prefix, new_line)
    summary = (
        f"- run328B_summary(328B 요약): cp318A(318A 후보) outcome source audit(결과 원천 감사)를 `{STATUS}`로 닫았다. "
        "Effect(효과): Stage317 validation+OOS(검증+표본외) 실제 MT5 손익을 학습한 outcome distillation(결과 증류)은 forward authority(전진 권한)가 아니며, live feature rebuild(실시간 피처 재구축) 또는 standalone ONNX packet(독립 온엑스 패킷)이 필요하다."
    )
    if "run328B_summary(328B 요약)" not in text:
        text = text.replace(f"- decision(판정): `{JUDGMENT}`\n", f"- decision(판정): `{JUDGMENT}`\n{summary}\n", 1)
    write_text_preserving(current, text, had_bom)

    changelog = ROOT / "docs" / "workspace" / "changelog.md"
    text, had_bom = read_text_lossless(changelog)
    entry = f"""

## 2026-05-26 - Stage328B cp318 Outcome Source Audit(328B cp318 결과 원천 감사)

- run328B(328B 실행): Stage318(318단계) cp318A outcome source(결과 원천), live feature rebuild matrix(실시간 피처 재구축 행렬), estimated-vs-actual MT5 gap(추정 대 실제 MT5 차이)을 감사했다.
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): cp318A outcome distillation(결과 증류)은 forward authority(전진 권한)가 아니므로 cp322A Goal Achieve(목표 달성), live readiness(실거래 준비), deployment(배포)를 주장하지 않는다.
"""
    if "## 2026-05-26 - Stage328B cp318 Outcome Source Audit" not in text:
        write_text_preserving(changelog, text.rstrip() + entry, had_bom)

    decision_doc = ROOT / "docs" / "decisions" / "2026-05-26_stage328B_cp318_outcome_source_audit.md"
    return write_md(
        decision_doc,
        f"""
# Stage328B cp318 Outcome Source Audit Decision(328B cp318 결과 원천 감사 결정)

- decision(결정): `{DECISION}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- goal_achieve(목표 달성): `not_claimed`
- effect(효과): cp318A(318A 후보)는 Stage317 validation+OOS(검증+표본외) 실제 MT5 손익을 학습한 outcome distillation(결과 증류)이어서 cp322A forward generator(전진 생성기) 권한을 주지 않는다.
- next_action(다음 행동): `{NEXT_ACTION}`
- boundary(경계): `{CLAIM_BOUNDARY}`
""",
    )


def main() -> None:
    generated_at_utc = utc_now()
    for directory in (SPEC_DIR, INPUTS_DIR, RUN_DIR, REVIEWS_DIR, SELECTED_DIR):
        os_path(directory).mkdir(parents=True, exist_ok=True)

    diagnostics = read_json(TRAINING_DIAGNOSTICS)
    model = load_cp318a_model()
    scout = load_cp318a_scout()
    actuals = load_cp318a_actuals()
    training_identity = inspect_training_set()

    training_rows = build_training_audit(diagnostics, model, training_identity)
    feature_rows = build_feature_matrix(model)
    gap_rows = build_gap_rows(scout, actuals)
    overfit_rows = build_overfit_rows(diagnostics, gap_rows)
    rebuild_rows = build_rebuild_options()

    artifacts: list[Path] = []
    artifacts.extend(
        write_reports(
            generated_at_utc,
            diagnostics,
            model,
            training_identity,
            training_rows,
            feature_rows,
            gap_rows,
            overfit_rows,
            rebuild_rows,
        )
    )
    artifacts.extend(write_receipts(generated_at_utc, diagnostics, model, training_identity, feature_rows, gap_rows))
    artifacts.append(update_current_truth())
    update_registers(generated_at_utc, artifacts)

    print(
        json.dumps(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "goal_achieve": "not_claimed",
                "next_action": NEXT_ACTION,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
