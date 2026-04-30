from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from stage_pipelines.stage11 import lgbm_training_support as _support

globals().update({name: getattr(_support, name) for name in dir(_support) if not name.startswith("__")})


def run_stage11_lgbm_training_method_scout(
    *,
    model_input_path: Path,
    feature_order_path: Path,
    tier_b_model_input_path: Path,
    tier_b_feature_order_path: Path,
    raw_root: Path,
    training_summary_path: Path,
    run_output_root: Path,
    common_files_root: Path,
    terminal_data_root: Path,
    tester_profile_root: Path,
    terminal_path: Path,
    metaeditor_path: Path,
    run_id: str,
    run_number: str,
    exploration_label: str,
    config: LgbmTrainingConfig,
    session_slice_id: str,
    max_hold_bars: int,
    tier_a_rule: scout.ThresholdRule,
    tier_b_rule: scout.ThresholdRule,
    attempt_mt5: bool = False,
    label_spec: Any | None = None,
    tier_a_model_input_dataset_id: str = MODEL_INPUT_DATASET_ID,
    tier_a_feature_set_id: str = FEATURE_SET_ID,
    decision_surface_id: str = DECISION_SURFACE_ID,
    selection_policy: str = "reuse_run01Y_threshold_surface_for_method_only_comparison",
    hypothesis: str | None = None,
    run_registry_lane: str = "alpha_training_method_scout",
    judgment_prefix: str = "training_method_scout",
) -> dict[str, Any]:
    if max_hold_bars != RUN01Y_REFERENCE["max_hold_bars"]:
        raise RuntimeError("RUN02A keeps run01Y max_hold_bars fixed for method-only comparison.")
    scout.configure_run_identity(
        run_number=run_number,
        run_id=run_id,
        exploration_label=exploration_label,
        common_run_root=f"Project_Obsidian_Prime_v2/stage11/{run_id}",
        stage_id=STAGE_ID,
    )

    tier_a_feature_order = scout.load_feature_order(feature_order_path)
    tier_a_feature_hash = scout.ordered_hash(tier_a_feature_order)
    if tier_a_feature_hash != scout.FEATURE_ORDER_HASH:
        raise RuntimeError(f"Feature order hash mismatch: {tier_a_feature_hash} != {scout.FEATURE_ORDER_HASH}")

    stage04_tier_b_feature_order = scout.load_feature_order(tier_b_feature_order_path)
    tier_b_feature_order = list(scout.TIER_B_CORE_FEATURE_ORDER)
    missing_core_features = sorted(set(tier_b_feature_order).difference(stage04_tier_b_feature_order))
    if missing_core_features:
        raise RuntimeError(f"Tier B core feature order is missing Stage04 reference features: {missing_core_features}")
    tier_b_feature_hash = scout.ordered_hash(tier_b_feature_order)
    label_threshold = scout.load_label_threshold(training_summary_path)
    active_label_spec = label_spec or scout.TrainingLabelSplitSpec()

    tier_a_frame = pd.read_parquet(_io_path(model_input_path))
    tier_a_frame["timestamp"] = pd.to_datetime(tier_a_frame["timestamp"], utc=True)
    tier_a_frame["route_role"] = scout.ROUTE_ROLE_A_PRIMARY
    tier_a_frame["partial_context_subtype"] = "Tier_A_full_context"
    tier_a_frame["missing_feature_group_mask"] = "none"
    tier_a_frame["available_feature_group_mask"] = "macro|constituent|basket"
    tier_a_frame["tier_a_primary_available"] = True
    tier_a_frame["tier_a_full_feature_ready"] = True
    tier_a_frame["tier_b_core_ready"] = True

    tier_b_context = scout.build_tier_b_partial_context_frames(
        raw_root=raw_root,
        tier_a_frame=tier_a_frame,
        tier_a_feature_order=tier_a_feature_order,
        tier_b_feature_order=tier_b_feature_order,
        label_threshold=label_threshold,
        label_spec=active_label_spec,
    )
    tier_b_training_frame = tier_b_context["tier_b_training_frame"]
    tier_b_frame = tier_b_context["tier_b_fallback_frame"]
    no_tier_frame = tier_b_context["no_tier_frame"]
    route_coverage_base = tier_b_context["summary"]

    _io_path(run_output_root).mkdir(parents=True, exist_ok=True)
    models_root = run_output_root / "models"
    predictions_root = run_output_root / "predictions"
    sweeps_root = run_output_root / "sweeps"
    reports_root = run_output_root / "reports"
    mt5_root = run_output_root / "mt5"

    tier_a_model = train_lgbm_model(tier_a_frame, tier_a_feature_order, config)
    tier_b_model = train_lgbm_model(tier_b_training_frame, tier_b_feature_order, config)
    model_metrics = {
        "tier_a": classification_metrics(tier_a_model, tier_a_frame, tier_a_feature_order),
        "tier_b": classification_metrics(tier_b_model, tier_b_training_frame, tier_b_feature_order),
    }

    session_slice = scout.session_slice_payload(session_slice_id)
    tier_a_eval_frame = scout.apply_session_slice(tier_a_frame, session_slice)
    tier_b_eval_frame = scout.apply_session_slice(tier_b_frame, session_slice)
    no_tier_eval_frame = scout.apply_session_slice(no_tier_frame, session_slice)
    route_coverage = scout.build_eval_route_coverage_summary(
        base_summary=route_coverage_base,
        tier_a_eval_frame=tier_a_eval_frame,
        tier_b_eval_frame=tier_b_eval_frame,
        no_tier_eval_frame=no_tier_eval_frame,
        session_slice=session_slice,
    )

    if tier_a_eval_frame.empty:
        raise RuntimeError(f"Tier A evaluation frame is empty for session slice: {session_slice_id}")
    if tier_b_eval_frame.empty:
        raise RuntimeError(f"Tier B evaluation frame is empty for session slice: {session_slice_id}")

    tier_a_predictions = build_lgbm_prediction_frame(tier_a_model, tier_a_eval_frame, tier_a_feature_order, tier_a_rule)
    tier_b_predictions = build_lgbm_prediction_frame(tier_b_model, tier_b_eval_frame, tier_b_feature_order, tier_b_rule)
    tier_a_predictions[scout.TIER_COLUMN] = scout.TIER_A
    tier_b_predictions[scout.TIER_COLUMN] = scout.TIER_B
    tier_a_predictions["feature_count"] = len(tier_a_feature_order)
    tier_b_predictions["feature_count"] = len(tier_b_feature_order)
    tier_a_predictions["feature_order_hash"] = tier_a_feature_hash
    tier_b_predictions["feature_order_hash"] = tier_b_feature_hash
    predictions = pd.concat([tier_a_predictions, tier_b_predictions], ignore_index=True)

    _io_path(predictions_root).mkdir(parents=True, exist_ok=True)
    tier_a_predictions_path = predictions_root / "tier_a_predictions.parquet"
    tier_b_predictions_path = predictions_root / "tier_b_predictions.parquet"
    combined_predictions_path = predictions_root / "tier_ab_combined_predictions.parquet"
    no_tier_route_path = predictions_root / "no_tier_route_rows.parquet"
    route_coverage_path = predictions_root / "route_coverage_summary.json"
    tier_a_predictions.to_parquet(_io_path(tier_a_predictions_path), index=False)
    tier_b_predictions.to_parquet(_io_path(tier_b_predictions_path), index=False)
    predictions.to_parquet(_io_path(combined_predictions_path), index=False)
    no_tier_eval_frame.to_parquet(_io_path(no_tier_route_path), index=False)
    write_json(route_coverage_path, route_coverage)

    _io_path(sweeps_root).mkdir(parents=True, exist_ok=True)
    validation_a = tier_a_eval_frame.loc[tier_a_eval_frame["split"].astype(str).eq("validation")]
    validation_b = tier_b_eval_frame.loc[tier_b_eval_frame["split"].astype(str).eq("validation")]
    threshold_sweeps = {
        "tier_a_separate": scout.sweep_threshold_rules(
            ordered_probabilities(tier_a_model, validation_a, tier_a_feature_order),
            validation_a["label_class"].astype("int64").to_numpy(),
        ),
        "tier_b_separate": scout.sweep_threshold_rules(
            ordered_probabilities(tier_b_model, validation_b, tier_b_feature_order),
            validation_b["label_class"].astype("int64").to_numpy(),
        ),
        "tier_ab_combined": scout.sweep_threshold_rules(
            np.vstack(
                [
                    ordered_probabilities(tier_a_model, validation_a, tier_a_feature_order),
                    ordered_probabilities(tier_b_model, validation_b, tier_b_feature_order),
                ]
            ),
            np.concatenate(
                [
                    validation_a["label_class"].astype("int64").to_numpy(),
                    validation_b["label_class"].astype("int64").to_numpy(),
                ]
            ),
        ),
    }
    threshold_sweep_paths = {
        "tier_a_separate": sweeps_root / "threshold_sweep_validation_tier_a.csv",
        "tier_b_separate": sweeps_root / "threshold_sweep_validation_tier_b.csv",
        "tier_ab_combined": sweeps_root / "threshold_sweep_validation_combined.csv",
    }
    for view_name, sweep in threshold_sweeps.items():
        sweep.to_csv(_io_path(threshold_sweep_paths[view_name]), index=False)
    diagnostic_threshold_selection = {
        view_name: scout.select_threshold_from_sweep(sweep)
        for view_name, sweep in threshold_sweeps.items()
    }

    tier_views = scout.build_tier_prediction_views(predictions)
    tier_outputs = scout.materialize_tier_prediction_views(tier_views, predictions_root)
    selected_threshold_id = (
        f"a_{tier_a_rule.threshold_id}__b_{tier_b_rule.threshold_id}"
        f"__hold{max_hold_bars}__slice_{session_slice_id}__model_lgbm"
    )
    tier_records = scout.build_paired_tier_records(
        tier_views,
        run_id=run_id,
        stage_id=STAGE_ID,
        base_path=predictions_root,
        kpi_scope="signal_probability_threshold",
        scoreboard_lane="structural_scout",
        external_verification_status="out_of_scope_by_claim",
    )
    ledger_rows = build_python_alpha_ledger_rows(
        run_id=run_id,
        tier_records=tier_records,
        selected_threshold_id=selected_threshold_id,
        model_family=config.model_family,
    )
    ledger_payload = materialize_ledgers(ledger_rows)
    run_registry_payload = materialize_run_registry_row(
        run_id=run_id,
        run_output_root=run_output_root,
        route_coverage=route_coverage,
        tier_records=tier_records,
        model_family=config.model_family,
        decision_surface_id=decision_surface_id,
        lane=run_registry_lane,
        judgment_prefix=judgment_prefix,
        session_slice_id=session_slice_id,
        max_hold_bars=max_hold_bars,
    )

    _io_path(models_root).mkdir(parents=True, exist_ok=True)
    tier_a_model_path = models_root / "tier_a_lgbm_58_model.joblib"
    tier_b_model_path = models_root / "tier_b_lgbm_core42_model.joblib"
    tier_a_feature_order_run_path = models_root / "tier_a_58_feature_order.txt"
    tier_b_feature_order_run_path = models_root / "tier_b_core42_feature_order.txt"
    joblib.dump(tier_a_model, _io_path(tier_a_model_path))
    joblib.dump(tier_b_model, _io_path(tier_b_model_path))
    _io_path(tier_a_feature_order_run_path).write_text("\n".join(tier_a_feature_order) + "\n", encoding="utf-8")
    _io_path(tier_b_feature_order_run_path).write_text("\n".join(tier_b_feature_order) + "\n", encoding="utf-8")

    tier_a_onnx_path = models_root / "tier_a_lgbm_58_model.onnx"
    tier_b_onnx_path = models_root / "tier_b_lgbm_core42_model.onnx"
    tier_a_onnx_export = export_lgbm_to_onnx_zipmap_disabled(
        tier_a_model,
        tier_a_onnx_path,
        feature_count=len(tier_a_feature_order),
    )
    tier_b_onnx_export = export_lgbm_to_onnx_zipmap_disabled(
        tier_b_model,
        tier_b_onnx_path,
        feature_count=len(tier_b_feature_order),
    )
    tier_a_parity_frame = tier_a_eval_frame.head(max(1, min(128, len(tier_a_eval_frame))))
    tier_b_parity_frame = tier_b_eval_frame.head(max(1, min(128, len(tier_b_eval_frame))))
    tier_a_onnx_parity = check_lgbm_onnxruntime_probability_parity(
        tier_a_model,
        tier_a_onnx_path,
        tier_a_parity_frame,
        tier_a_feature_order,
    )
    tier_b_onnx_parity = check_lgbm_onnxruntime_probability_parity(
        tier_b_model,
        tier_b_onnx_path,
        tier_b_parity_frame,
        tier_b_feature_order,
    )
    onnx_parity = {
        "passed": bool(tier_a_onnx_parity["passed"] and tier_b_onnx_parity["passed"]),
        "tier_a": tier_a_onnx_parity,
        "tier_b": tier_b_onnx_parity,
    }

    split_specs = {
        "validation_is": ("validation", "2025.01.01", "2025.10.01"),
        "oos": ("oos", "2025.10.01", "2026.04.14"),
    }
    mt5_attempts: list[dict[str, Any]] = []
    mt5_feature_matrices: list[dict[str, Any]] = []
    common_copies: list[dict[str, Any]] = []
    _io_path(mt5_root).mkdir(parents=True, exist_ok=True)
    common_copies.append(
        scout.copy_to_common_files(common_files_root, tier_a_onnx_path, scout.common_ref("models", tier_a_onnx_path.name))
    )
    common_copies.append(
        scout.copy_to_common_files(common_files_root, tier_b_onnx_path, scout.common_ref("models", tier_b_onnx_path.name))
    )
    metadata_columns = (
        "route_role",
        "partial_context_subtype",
        "missing_feature_group_mask",
        "available_feature_group_mask",
    )
    for split_label, (source_split, from_date, to_date) in split_specs.items():
        tier_a_split = tier_a_eval_frame.loc[tier_a_eval_frame["split"].astype(str).eq(source_split)].copy()
        tier_b_split = tier_b_eval_frame.loc[tier_b_eval_frame["split"].astype(str).eq(source_split)].copy()
        tier_a_feature_matrix_path = mt5_root / f"tier_a_{split_label}_feature_matrix.csv"
        tier_b_feature_matrix_path = mt5_root / f"tier_b_{split_label}_feature_matrix.csv"
        tier_a_matrix_payload = scout.export_mt5_feature_matrix_csv(
            tier_a_split,
            tier_a_feature_order,
            tier_a_feature_matrix_path,
            metadata_columns=metadata_columns,
        )
        tier_b_matrix_payload = scout.export_mt5_feature_matrix_csv(
            tier_b_split,
            tier_b_feature_order,
            tier_b_feature_matrix_path,
            metadata_columns=metadata_columns,
        )
        mt5_feature_matrices.extend(
            [
                {"tier": scout.TIER_A, "split": split_label, **tier_a_matrix_payload},
                {"tier": scout.TIER_B, "split": split_label, **tier_b_matrix_payload},
            ]
        )
        common_copies.append(
            scout.copy_to_common_files(
                common_files_root,
                tier_a_feature_matrix_path,
                scout.common_ref("features", tier_a_feature_matrix_path.name),
            )
        )
        common_copies.append(
            scout.copy_to_common_files(
                common_files_root,
                tier_b_feature_matrix_path,
                scout.common_ref("features", tier_b_feature_matrix_path.name),
            )
        )
        tier_a_attempt = scout.materialize_mt5_attempt_files(
            run_output_root=run_output_root,
            tier_name=scout.TIER_A,
            split_name=split_label,
            local_onnx_path=tier_a_onnx_path,
            local_feature_matrix_path=tier_a_feature_matrix_path,
            feature_count=len(tier_a_feature_order),
            feature_order_hash=tier_a_feature_hash,
            rule=tier_a_rule,
            from_date=from_date,
            to_date=to_date,
            stem_prefix="tier_a_only",
            record_view_prefix=scout.MT5_RECORD_TIER_A_ONLY_PREFIX,
            primary_active_tier="tier_a",
            attempt_role="tier_only_total",
            max_hold_bars=max_hold_bars,
        )
        tier_a_attempt["feature_matrix"] = tier_a_matrix_payload
        mt5_attempts.append(tier_a_attempt)

        tier_b_attempt = scout.materialize_mt5_attempt_files(
            run_output_root=run_output_root,
            tier_name=scout.TIER_B,
            split_name=split_label,
            local_onnx_path=tier_b_onnx_path,
            local_feature_matrix_path=tier_b_feature_matrix_path,
            feature_count=len(tier_b_feature_order),
            feature_order_hash=tier_b_feature_hash,
            rule=tier_b_rule,
            from_date=from_date,
            to_date=to_date,
            stem_prefix="tier_b_fallback_only",
            record_view_prefix=scout.MT5_RECORD_TIER_B_FALLBACK_ONLY_PREFIX,
            primary_active_tier="tier_b_fallback",
            attempt_role="tier_b_fallback_only_total",
            max_hold_bars=max_hold_bars,
        )
        tier_b_attempt["feature_matrix"] = tier_b_matrix_payload
        mt5_attempts.append(tier_b_attempt)

        routed_attempt = scout.materialize_mt5_routed_attempt_files(
            run_output_root=run_output_root,
            split_name=split_label,
            primary_onnx_path=tier_a_onnx_path,
            primary_feature_matrix_path=tier_a_feature_matrix_path,
            primary_feature_count=len(tier_a_feature_order),
            primary_feature_order_hash=tier_a_feature_hash,
            fallback_onnx_path=tier_b_onnx_path,
            fallback_feature_matrix_path=tier_b_feature_matrix_path,
            fallback_feature_count=len(tier_b_feature_order),
            fallback_feature_order_hash=tier_b_feature_hash,
            rule=tier_a_rule,
            fallback_rule=tier_b_rule,
            max_hold_bars=max_hold_bars,
            fallback_enabled=True,
            from_date=from_date,
            to_date=to_date,
        )
        routed_attempt["primary_feature_matrix"] = tier_a_matrix_payload
        routed_attempt["fallback_feature_matrix"] = tier_b_matrix_payload
        mt5_attempts.append(routed_attempt)

    compile_payload: dict[str, Any] | None = None
    mt5_execution_results: list[dict[str, Any]] = []
    if attempt_mt5:
        for attempt in mt5_attempts:
            for common_output_key in ("common_telemetry_path", "common_summary_path"):
                output_path = common_files_root / Path(str(attempt[common_output_key]))
                if scout._path_exists(output_path):
                    scout._io_path(output_path).unlink()
            scout.remove_existing_mt5_report_artifacts(terminal_data_root, attempt)
        if not onnx_parity["passed"]:
            compile_payload = {
                "status": "blocked",
                "blocker": "onnx_probability_parity_failed",
                "tier_a": tier_a_onnx_parity,
                "tier_b": tier_b_onnx_parity,
            }
        else:
            compile_payload = scout.compile_mql5_ea(
                metaeditor_path,
                scout.EA_SOURCE_PATH,
                mt5_root / "mt5_compile.log",
            )
        if compile_payload["status"] == "completed":
            for attempt in mt5_attempts:
                try:
                    result = scout.run_mt5_tester(
                        terminal_path,
                        Path(attempt["ini"]["path"]),
                        set_path=Path(attempt["set"]["path"]),
                        tester_profile_set_path=tester_profile_root / scout.EA_TESTER_SET_NAME,
                        tester_profile_ini_path=tester_profile_root
                        / scout.mt5_short_profile_ini_name(attempt["tier"], attempt["split"]),
                        timeout_seconds=300,
                    )
                except Exception as exc:  # pragma: no cover - defensive external tool boundary
                    result = {
                        "status": "blocked",
                        "blocker": "mt5_tester_exception",
                        "error": repr(exc),
                    }
                result["tier"] = attempt["tier"]
                result["split"] = attempt["split"]
                if "routing_mode" in attempt:
                    result["routing_mode"] = attempt["routing_mode"]
                if "attempt_role" in attempt:
                    result["attempt_role"] = attempt["attempt_role"]
                if "record_view_prefix" in attempt:
                    result["record_view_prefix"] = attempt["record_view_prefix"]
                result["ini_path"] = attempt["ini"]["path"]
                result["runtime_outputs"] = (
                    scout.wait_for_mt5_runtime_outputs(common_files_root, attempt, timeout_seconds=180)
                    if result.get("status") == "completed"
                    else scout.validate_mt5_runtime_outputs(common_files_root, attempt)
                )
                if result["runtime_outputs"]["status"] != "completed":
                    result["status"] = "blocked"
                mt5_execution_results.append(result)

    mt5_report_records = (
        scout.collect_mt5_strategy_report_artifacts(
            terminal_data_root=terminal_data_root,
            run_output_root=run_output_root,
            attempts=mt5_attempts,
        )
        if attempt_mt5
        else []
    )
    scout.attach_mt5_report_metrics(mt5_execution_results, mt5_report_records)
    mt5_kpi_records = scout.build_mt5_kpi_records(mt5_execution_results)
    mt5_kpi_records = scout.enrich_mt5_kpi_records_with_route_coverage(mt5_kpi_records, route_coverage)
    mt5_module_hashes = scout.mt5_runtime_module_hashes()
    expected_mt5_kpi_record_count = sum(
        3 if attempt.get("routing_mode") == scout.ROUTING_MODE_A_B_FALLBACK else 1 for attempt in mt5_attempts
    )
    mt5_runtime_completed = bool(mt5_execution_results) and all(
        item.get("status") == "completed" for item in mt5_execution_results
    )
    mt5_reports_completed = len(mt5_kpi_records) >= expected_mt5_kpi_record_count and all(
        item.get("status") == "completed" for item in mt5_kpi_records
    )
    external_status = (
        "completed"
        if mt5_runtime_completed and mt5_reports_completed
        else "blocked"
        if attempt_mt5
        else "out_of_scope_by_claim"
    )
    mt5_ledger_rows = build_mt5_alpha_ledger_rows(
        run_id=run_id,
        mt5_kpi_records=mt5_kpi_records,
        run_output_root=run_output_root,
        external_verification_status=external_status,
    )
    ledger_payload = materialize_ledgers([*ledger_rows, *mt5_ledger_rows])
    run_registry_payload = materialize_run_registry_row(
        run_id=run_id,
        run_output_root=run_output_root,
        route_coverage=route_coverage,
        tier_records=tier_records,
        model_family=config.model_family,
        decision_surface_id=decision_surface_id,
        lane=run_registry_lane,
        judgment_prefix=judgment_prefix,
        external_verification_status=external_status,
        mt5_kpi_records=mt5_kpi_records,
        session_slice_id=session_slice_id,
        max_hold_bars=max_hold_bars,
    )

    artifacts = [
        {"role": "tier_a_lgbm_model", "path": tier_a_model_path.as_posix(), "format": "joblib", "sha256": scout.sha256_file(tier_a_model_path)},
        {"role": "tier_b_lgbm_model", "path": tier_b_model_path.as_posix(), "format": "joblib", "sha256": scout.sha256_file(tier_b_model_path)},
        {"role": "tier_a_feature_order", "path": tier_a_feature_order_run_path.as_posix(), "format": "txt", "sha256": scout.sha256_file(tier_a_feature_order_run_path)},
        {"role": "tier_b_feature_order", "path": tier_b_feature_order_run_path.as_posix(), "format": "txt", "sha256": scout.sha256_file(tier_b_feature_order_run_path)},
        {"role": "tier_a_onnx_model", **tier_a_onnx_export, "format": "onnx"},
        {"role": "tier_b_onnx_model", **tier_b_onnx_export, "format": "onnx"},
        {"role": "onnx_probability_parity", "parity": onnx_parity},
        {"role": "tier_a_predictions", "path": tier_a_predictions_path.as_posix(), "format": "parquet", "sha256": scout.sha256_file(tier_a_predictions_path)},
        {"role": "tier_b_predictions", "path": tier_b_predictions_path.as_posix(), "format": "parquet", "sha256": scout.sha256_file(tier_b_predictions_path)},
        {"role": "tier_ab_combined_predictions", "path": combined_predictions_path.as_posix(), "format": "parquet", "sha256": scout.sha256_file(combined_predictions_path)},
        {"role": "no_tier_route_rows", "path": no_tier_route_path.as_posix(), "format": "parquet", "sha256": scout.sha256_file(no_tier_route_path)},
        {"role": "route_coverage_summary", "path": route_coverage_path.as_posix(), "format": "json", "sha256": scout.sha256_file(route_coverage_path)},
        *[
            {"role": f"threshold_sweep_{view_name}", "path": path.as_posix(), "format": "csv", "sha256": scout.sha256_file(path)}
            for view_name, path in threshold_sweep_paths.items()
        ],
        {"role": "tier_prediction_views", "views": tier_outputs},
        {"role": "mt5_feature_matrices", "matrices": mt5_feature_matrices},
        {"role": "mt5_attempts", "attempts": mt5_attempts},
        {"role": "mt5_common_file_copies", "copies": common_copies},
        {"role": "mt5_compile", "compile": compile_payload},
        {"role": "mt5_execution_results", "execution_results": mt5_execution_results},
        {"role": "mt5_strategy_tester_reports", "reports": mt5_report_records},
        {"role": "mt5_runtime_module_hashes", "modules": mt5_module_hashes},
        {"role": "stage_run_ledger", **ledger_payload["stage_run_ledger"]},
        {"role": "project_alpha_run_ledger", **ledger_payload["project_alpha_run_ledger"]},
        {"role": "project_run_registry", **run_registry_payload},
    ]

    input_refs = {
        "tier_a": {
            "model_input_dataset_id": tier_a_model_input_dataset_id,
            "feature_set_id": tier_a_feature_set_id,
            "model_input_path": model_input_path.as_posix(),
            "model_input_sha256": scout.sha256_file(model_input_path),
            "feature_order_path": feature_order_path.as_posix(),
            "feature_order_sha256": scout.sha256_file(feature_order_path),
            "feature_count": len(tier_a_feature_order),
            "feature_order_hash": tier_a_feature_hash,
        },
        "tier_b": {
            "model_input_dataset_id": scout.TIER_B_PARTIAL_CONTEXT_DATASET_ID,
            "feature_set_id": scout.TIER_B_PARTIAL_CONTEXT_FEATURE_SET_ID,
            "model_input_path": "materialized_in_run_from_raw_feature_frame_and_label_contract",
            "feature_order_path": tier_b_feature_order_run_path.as_posix(),
            "feature_order_sha256": scout.sha256_file(tier_b_feature_order_run_path),
            "feature_count": len(tier_b_feature_order),
            "feature_order_hash": tier_b_feature_hash,
            "policy_id": scout.TIER_B_PARTIAL_CONTEXT_POLICY_ID,
            "stage04_quarantine_reference": {
                "model_input_dataset_id": scout.TIER_B_MODEL_INPUT_DATASET_ID,
                "feature_set_id": scout.TIER_B_FEATURE_SET_ID,
                "model_input_path": tier_b_model_input_path.as_posix(),
                "model_input_sha256": scout.sha256_file(tier_b_model_input_path),
                "feature_order_path": tier_b_feature_order_path.as_posix(),
                "feature_order_sha256": scout.sha256_file(tier_b_feature_order_path),
            },
        },
    }

    kpi = {
        "run_id": run_id,
        "stage_id": STAGE_ID,
        "run_number": run_number,
        "exploration_label": exploration_label,
        "model_family": config.model_family,
        "comparison_reference": RUN01Y_REFERENCE,
        "decision_surface": {
            "decision_surface_id": decision_surface_id,
            "tier_a_rule": scout.threshold_rule_payload(tier_a_rule),
            "tier_b_rule": scout.threshold_rule_payload(tier_b_rule),
            "selected_threshold_id": selected_threshold_id,
            "selection_policy": selection_policy,
            "diagnostic_threshold_selection": diagnostic_threshold_selection,
        },
        "route_coverage": route_coverage,
        "model_metrics": model_metrics,
        "tier_records": tier_records,
        "onnx_parity": onnx_parity,
        "external_verification_status": external_status,
        "boundary": (
            "mt5_runtime_probe_only_not_alpha_quality_live_readiness_or_operating_promotion"
            if external_status == "completed"
            else "python_side_training_method_scout_with_blocked_mt5_probe_not_alpha_quality"
            if external_status == "blocked"
            else "python_side_training_method_scout_only_not_mt5_runtime_probe_or_alpha_quality"
        ),
        "mt5": {
            "attempted": bool(attempt_mt5),
            "compile": compile_payload,
            "execution_results": mt5_execution_results,
            "strategy_tester_reports": mt5_report_records,
            "kpi_records": mt5_kpi_records,
            "module_hashes": mt5_module_hashes,
            "attempt_count": len(mt5_attempts),
            "expected_kpi_record_count": expected_mt5_kpi_record_count,
            "runtime_completed": mt5_runtime_completed,
            "reports_completed": mt5_reports_completed,
            "tester_defaults": {
                "symbol": "US100",
                "period": "M5",
                "model": 4,
                "deposit": 500,
                "leverage": "1:100",
                "fixed_lot": 0.1,
                "max_hold_bars": int(max_hold_bars),
                "max_concurrent_positions": 1,
            },
        },
    }
    manifest = {
        "identity": {
            "run_id": run_id,
            "run_number": run_number,
            "stage_id": STAGE_ID,
            "exploration_label": exploration_label,
            "model_family": config.model_family,
            "status": "reviewed_payload",
            "judgment": (
                f"inconclusive_{judgment_prefix}_mt5_runtime_probe_completed"
                if external_status == "completed"
                else f"inconclusive_{judgment_prefix}_mt5_runtime_probe_blocked"
                if external_status == "blocked"
                else f"inconclusive_python_side_{judgment_prefix}"
            ),
        },
        "hypothesis": hypothesis or (
            "LightGBM training can improve the signal surface versus the run01Y logistic-regression comparison "
            "reference while keeping the same feature, label/split, session slice, hold, and threshold surface."
        ),
        "comparison_reference": RUN01Y_REFERENCE,
        "training_config": asdict(config),
        "input_refs": input_refs,
        "artifacts": artifacts,
        "decision_surface": kpi["decision_surface"],
        "route_coverage": route_coverage,
        "tier_records": tier_records,
        "onnx_probability_parity": onnx_parity,
        "external_verification_status": external_status,
        "boundary": kpi["boundary"],
        "mt5": kpi["mt5"],
    }
    manifest_path = run_output_root / "run_manifest.json"
    kpi_path = run_output_root / "kpi_record.json"
    summary_path = run_output_root / "summary.json"
    result_summary_path = reports_root / "result_summary.md"
    write_json(manifest_path, manifest)
    write_json(kpi_path, kpi)
    summary = {
        "run_id": run_id,
        "stage_id": STAGE_ID,
        "status": "reviewed_payload",
        "judgment": manifest["identity"]["judgment"],
        "model_family": config.model_family,
        "selected_threshold_id": selected_threshold_id,
        "route_coverage": route_coverage,
        "tier_records": tier_records,
        "model_metrics": model_metrics,
        "onnx_parity": onnx_parity,
        "external_verification_status": external_status,
        "mt5_attempted": bool(attempt_mt5),
        "mt5_execution_results": mt5_execution_results,
        "mt5_kpi_records": mt5_kpi_records,
        "mt5_ledger_rows": mt5_ledger_rows,
        "ledger_payload": ledger_payload,
        "run_registry_payload": run_registry_payload,
        "boundary": kpi["boundary"],
    }
    write_json(summary_path, summary)
    write_result_summary(
        path=result_summary_path,
        run_id=run_id,
        tier_records=tier_records,
        selected_threshold_id=selected_threshold_id,
        route_coverage=route_coverage,
        model_metrics=model_metrics,
        external_verification_status=external_status,
        mt5_kpi_records=mt5_kpi_records,
        session_slice_id=session_slice_id,
        max_hold_bars=max_hold_bars,
    )

    return {
        "status": "ok",
        "run_id": run_id,
        "run_output_root": run_output_root.as_posix(),
        "summary_path": summary_path.as_posix(),
        "result_summary_path": result_summary_path.as_posix(),
        "manifest_path": manifest_path.as_posix(),
        "kpi_path": kpi_path.as_posix(),
        "selected_threshold_id": selected_threshold_id,
        "onnx_parity": onnx_parity,
        "external_verification_status": external_status,
        "mt5_attempted": bool(attempt_mt5),
        "mt5_execution_results": mt5_execution_results,
        "mt5_kpi_records": mt5_kpi_records,
        "ledger_payload": ledger_payload,
        "run_registry_payload": run_registry_payload,
        "tier_records": tier_records,
        "model_metrics": model_metrics,
    }


def main() -> int:
    args = parse_args()
    config = LgbmTrainingConfig(
        random_seed=args.random_seed,
        n_estimators=args.n_estimators,
        learning_rate=args.learning_rate,
        num_leaves=args.num_leaves,
        max_depth=args.max_depth,
        min_child_samples=args.min_child_samples,
        subsample=args.subsample,
        colsample_bytree=args.colsample_bytree,
        reg_alpha=args.reg_alpha,
        reg_lambda=args.reg_lambda,
        class_weight=None if args.class_weight == "none" else args.class_weight,
    )
    tier_a_rule = scout.threshold_rule_from_values(
        threshold_id="short0.600_long0.450_margin0.000",
        short_threshold=args.tier_a_short_threshold,
        long_threshold=args.tier_a_long_threshold,
        min_margin=args.tier_a_min_margin,
    )
    tier_b_rule = scout.threshold_rule_from_values(
        threshold_id="short0.600_long0.450_margin0.000",
        short_threshold=args.tier_b_short_threshold,
        long_threshold=args.tier_b_long_threshold,
        min_margin=args.tier_b_min_margin,
    )
    payload = run_stage11_lgbm_training_method_scout(
        model_input_path=Path(args.model_input_path),
        feature_order_path=Path(args.feature_order_path),
        tier_b_model_input_path=Path(args.tier_b_model_input_path),
        tier_b_feature_order_path=Path(args.tier_b_feature_order_path),
        raw_root=Path(args.raw_root),
        training_summary_path=Path(args.training_summary_path),
        run_output_root=Path(args.run_output_root),
        common_files_root=Path(args.common_files_root),
        terminal_data_root=Path(args.terminal_data_root),
        tester_profile_root=Path(args.tester_profile_root),
        terminal_path=Path(args.terminal_path),
        metaeditor_path=Path(args.metaeditor_path),
        run_id=args.run_id,
        run_number=args.run_number,
        exploration_label=args.exploration_label,
        config=config,
        session_slice_id=args.session_slice_id,
        max_hold_bars=args.max_hold_bars,
        tier_a_rule=tier_a_rule,
        tier_b_rule=tier_b_rule,
        attempt_mt5=bool(args.attempt_mt5),
    )
    print(json.dumps(_json_ready(payload), indent=2))
    return 0 if payload["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
