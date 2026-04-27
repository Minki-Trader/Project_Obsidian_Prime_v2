#property strict
#property version   "1.00"

#include "include/ObsidianPrime/FeatureInputs.mqh"
#include "include/ObsidianPrime/ModelRuntime.mqh"
#include "include/ObsidianPrime/DecisionSurface.mqh"
#include "include/ObsidianPrime/ExecutionBridge.mqh"
#include "include/ObsidianPrime/RuntimeTelemetry.mqh"

input string          InpRunId = "runtime_probe_default";
input string          InpExplorationLabel = "foundation_RuntimeProbeEA";
input string          InpTierLabel = "Tier A";
input string          InpPrimaryActiveTier = "tier_a";
input string          InpSplitLabel = "validation_is";
input string          InpMainSymbol = "US100";
input ENUM_TIMEFRAMES InpTimeframe = PERIOD_M5;
input bool            InpEnforceM5 = true;

input string          InpFeatureCsvPath = "Project_Obsidian_Prime_v2/runtime_probe/default/features.csv";
input int             InpFeatureCount = 58;
input bool            InpFeatureCsvUseCommonFiles = true;
input bool            InpFeatureRequireTimestampMatch = true;
input bool            InpFeatureAllowLatestFallback = false;
input bool            InpFeatureStrictHeader = true;
input string          InpFeatureCsvDelimiter = ",";
input bool            InpCsvTimestampIsBarClose = true;

input string          InpModelPath = "Project_Obsidian_Prime_v2/runtime_probe/default/model.onnx";
input string          InpModelId = "runtime_probe_default_model";
input bool            InpModelUseCommonFiles = true;
input bool            InpModelUseCpuOnly = true;
input bool            InpModelNoConversion = false;
input bool            InpSetOutputShape = true;
input string          InpFeatureOrderHash = "fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2";

input bool            InpFallbackEnabled = false;
input string          InpFallbackTierLabel = "Tier B fallback";
input string          InpFallbackFeatureCsvPath = "Project_Obsidian_Prime_v2/runtime_probe/default/fallback_features.csv";
input int             InpFallbackFeatureCount = 56;
input string          InpFallbackModelPath = "Project_Obsidian_Prime_v2/runtime_probe/default/fallback_model.onnx";
input string          InpFallbackModelId = "runtime_probe_default_tier_b_fallback_model";
input string          InpFallbackFeatureOrderHash = "";

input double          InpShortThreshold = 0.55;
input double          InpLongThreshold = 0.55;
input double          InpMinMargin = 0.05;
input double          InpFallbackShortThreshold = 0.55;
input double          InpFallbackLongThreshold = 0.55;
input double          InpFallbackMinMargin = 0.05;

input bool            InpAllowTrading = true;
input double          InpFixedLot = 0.10;
input long            InpMagic = 26041001;
input int             InpDeviationPoints = 20;
input bool            InpCloseOnFlatSignal = false;
input bool            InpReverseOnOppositeSignal = true;
input int             InpMaxHoldBars = 12;
input int             InpMaxConcurrentPositions = 1;

input bool            InpTelemetryEnabled = true;
input bool            InpTelemetryUseCommonFiles = true;
input string          InpTelemetryCsvPath = "Project_Obsidian_Prime_v2/runtime_probe/default/runtime_telemetry.csv";
input string          InpSummaryCsvPath = "Project_Obsidian_Prime_v2/runtime_probe/default/runtime_summary.csv";

COpFeatureCsvInput   g_feature_input;
COpFeatureCsvInput   g_fallback_feature_input;
COpModelRuntime      g_model_runtime;
COpModelRuntime      g_fallback_model_runtime;
COpDecisionSurface   g_decision_surface;
COpDecisionSurface   g_fallback_decision_surface;
COpExecutionBridge   g_execution_bridge;
COpRuntimeTelemetry  g_telemetry;

bool     g_runtime_ready = false;
datetime g_last_bar_open = 0;

string DeinitReasonText(const int reason)
  {
   switch(reason)
     {
      case REASON_PROGRAM:     return "program";
      case REASON_REMOVE:      return "remove";
      case REASON_RECOMPILE:   return "recompile";
      case REASON_CHARTCHANGE: return "chart_change";
      case REASON_CHARTCLOSE:  return "chart_close";
      case REASON_PARAMETERS:  return "parameters";
      case REASON_ACCOUNT:     return "account";
      case REASON_TEMPLATE:    return "template";
      case REASON_INITFAILED:  return "init_failed";
      case REASON_CLOSE:       return "terminal_close";
     }
   return "unknown:" + (string)reason;
  }

void PrintTelemetryFailure(const string where, const string reason)
  {
   if(reason != "")
      PrintFormat("[ObsidianPrimeV2][RuntimeProbe][telemetry][%s] %s", where, reason);
  }

int FailInit(const string detail)
  {
   string telemetry_reason = "";
   g_telemetry.RecordLifecycle("init_failed", detail, telemetry_reason);
   PrintTelemetryFailure("init_failed", telemetry_reason);
   PrintFormat("[ObsidianPrimeV2][RuntimeProbe][init_failed] %s", detail);
   g_model_runtime.Deinit();
   g_fallback_model_runtime.Deinit();
   g_runtime_ready = false;
   return INIT_FAILED;
  }

datetime CurrentClosedBarTimestamp()
  {
   const datetime closed_open = iTime(InpMainSymbol, InpTimeframe, 1);
   if(closed_open <= 0)
      return 0;

   if(InpCsvTimestampIsBarClose)
      return closed_open + PeriodSeconds(InpTimeframe);
   return closed_open;
  }

void RecordSkippedBar(const datetime bar_time,
                      const string active_tier,
                      const string model_id,
                      const string feature_order_hash,
                      const string source_time,
                      const string input_hash,
                      const string skip_reason,
                      const string position_before)
  {
   string telemetry_reason = "";
   g_telemetry.RecordCycle(bar_time,
                           active_tier,
                           model_id,
                           feature_order_hash,
                           source_time,
                           InpMainSymbol,
                           EnumToString(InpTimeframe),
                           false,
                           false,
                           skip_reason,
                           input_hash,
                           0.0,
                           0.0,
                           0.0,
                           "flat",
                           skip_reason,
                           position_before,
                           position_before,
                           "none",
                           false,
                           false,
                           0,
                           "",
                           telemetry_reason);
   PrintTelemetryFailure("cycle_skip", telemetry_reason);
  }

bool ResolveRoutedFeatures(const datetime target_time,
                           double &features[],
                           string &source_time,
                           string &input_hash,
                           string &skip_reason,
                           string &active_tier,
                           string &active_model_id,
                           string &active_feature_order_hash,
                           bool &use_fallback_model)
  {
   use_fallback_model = false;
   string primary_reason = "";
   if(g_feature_input.ReadForTime(target_time, features, source_time, input_hash, primary_reason))
     {
      active_tier = InpPrimaryActiveTier;
      active_model_id = InpModelId;
      active_feature_order_hash = InpFeatureOrderHash;
      skip_reason = "";
      return true;
     }

   if(!InpFallbackEnabled)
     {
      active_tier = "none";
      active_model_id = "";
      active_feature_order_hash = "";
      skip_reason = primary_reason;
      return false;
     }

   string fallback_source_time = "";
   string fallback_input_hash = "";
   string fallback_reason = "";
   double fallback_features[];
   if(g_fallback_feature_input.ReadForTime(target_time,
                                           fallback_features,
                                           fallback_source_time,
                                           fallback_input_hash,
                                           fallback_reason))
     {
      const int fallback_count = ArraySize(fallback_features);
      ArrayResize(features, fallback_count);
      for(int i = 0; i < fallback_count; i++)
         features[i] = fallback_features[i];
      source_time = fallback_source_time;
      input_hash = fallback_input_hash;
      active_tier = "tier_b_fallback";
      active_model_id = InpFallbackModelId;
      active_feature_order_hash = InpFallbackFeatureOrderHash;
      use_fallback_model = true;
      skip_reason = "";
      return true;
     }

   active_tier = "none";
   active_model_id = "";
   active_feature_order_hash = "";
   skip_reason = "tier_a_missing:" + primary_reason + "|tier_b_missing:" + fallback_reason;
   return false;
  }

void ProcessClosedBar()
  {
   const datetime target_time = CurrentClosedBarTimestamp();
   const string position_before = g_execution_bridge.PositionStateText();
   if(target_time <= 0)
     {
      RecordSkippedBar(0, "none", "", "", "", "", "closed_bar_unavailable", position_before);
      return;
     }

   double features[];
   string source_time = "";
   string input_hash = "";
   string reason = "";
   string active_tier = "none";
   string active_model_id = "";
   string active_feature_order_hash = "";
   bool use_fallback_model = false;
   const bool feature_ready = ResolveRoutedFeatures(target_time,
                                                    features,
                                                    source_time,
                                                    input_hash,
                                                    reason,
                                                    active_tier,
                                                    active_model_id,
                                                    active_feature_order_hash,
                                                    use_fallback_model);
   if(!feature_ready)
     {
      RecordSkippedBar(target_time,
                       active_tier,
                       active_model_id,
                       active_feature_order_hash,
                       source_time,
                       input_hash,
                       reason,
                       position_before);
      return;
     }

   double p_short = 0.0;
   double p_flat = 0.0;
   double p_long = 0.0;
   string model_reason = "";
   const bool model_ok = use_fallback_model
                         ? g_fallback_model_runtime.Run(features, p_short, p_flat, p_long, model_reason)
                         : g_model_runtime.Run(features, p_short, p_flat, p_long, model_reason);
   if(!model_ok)
     {
      string telemetry_reason = "";
      g_telemetry.RecordCycle(target_time,
                              active_tier,
                              active_model_id,
                              active_feature_order_hash,
                              source_time,
                              InpMainSymbol,
                              EnumToString(InpTimeframe),
                              true,
                              false,
                              model_reason,
                              input_hash,
                              p_short,
                              p_flat,
                              p_long,
                              "flat",
                              model_reason,
                              position_before,
                              position_before,
                              "none",
                              false,
                              false,
                              0,
                              "",
                              telemetry_reason);
      PrintTelemetryFailure("model_skip", telemetry_reason);
      return;
     }

   SOpDecisionResult decision;
   if(active_tier == "tier_b_fallback")
      g_fallback_decision_surface.Evaluate(p_short, p_flat, p_long, decision);
   else
      g_decision_surface.Evaluate(p_short, p_flat, p_long, decision);

   SOpExecutionResult execution;
   const bool execution_ok = g_execution_bridge.Execute(decision.signal, execution);
   string skip_reason = "";
   if(!execution_ok)
      skip_reason = "execution_failed:" + execution.comment;

   string telemetry_reason = "";
   g_telemetry.RecordCycle(target_time,
                           active_tier,
                           active_model_id,
                           active_feature_order_hash,
                           source_time,
                           InpMainSymbol,
                           EnumToString(InpTimeframe),
                           true,
                           true,
                           skip_reason,
                           input_hash,
                           p_short,
                           p_flat,
                           p_long,
                           decision.label,
                           decision.reason,
                           execution.position_before,
                           execution.position_after,
                           execution.action,
                           execution.attempted,
                           execution.filled,
                           execution.retcode,
                           execution.comment,
                           telemetry_reason);
   PrintTelemetryFailure("cycle", telemetry_reason);
  }

int OnInit()
  {
   g_runtime_ready = false;
   g_last_bar_open = 0;

   g_telemetry.Configure(InpTelemetryEnabled,
                         InpTelemetryUseCommonFiles,
                         InpRunId,
                         InpModelId,
                         InpFeatureOrderHash,
                         InpTelemetryCsvPath,
                         InpSummaryCsvPath);

   string telemetry_reason = "";
   if(!g_telemetry.RecordLifecycle("init_start", InpExplorationLabel, telemetry_reason))
      return FailInit(telemetry_reason);

   if(InpEnforceM5 && InpTimeframe != PERIOD_M5)
      return FailInit("timeframe_must_be_period_m5");

   if(!SymbolSelect(InpMainSymbol, true))
      return FailInit("main_symbol_select_failed:" + InpMainSymbol);

   g_feature_input.Configure(InpFeatureCsvPath,
                             InpFeatureCsvUseCommonFiles,
                             InpFeatureRequireTimestampMatch,
                             InpFeatureAllowLatestFallback,
                             InpFeatureStrictHeader,
                             InpFeatureCsvDelimiter,
                             InpFeatureCount);

   g_model_runtime.Configure(InpModelPath,
                             InpModelId,
                             InpModelUseCommonFiles,
                             InpModelUseCpuOnly,
                             InpModelNoConversion,
                             InpSetOutputShape,
                             InpFeatureCount);

   if(InpFallbackEnabled)
     {
      g_fallback_feature_input.Configure(InpFallbackFeatureCsvPath,
                                         InpFeatureCsvUseCommonFiles,
                                         InpFeatureRequireTimestampMatch,
                                         InpFeatureAllowLatestFallback,
                                         InpFeatureStrictHeader,
                                         InpFeatureCsvDelimiter,
                                         InpFallbackFeatureCount);

      g_fallback_model_runtime.Configure(InpFallbackModelPath,
                                         InpFallbackModelId,
                                         InpModelUseCommonFiles,
                                         InpModelUseCpuOnly,
                                         InpModelNoConversion,
                                         InpSetOutputShape,
                                         InpFallbackFeatureCount);
     }

   string reason = "";
   if(!g_model_runtime.Init(reason))
      return FailInit(reason);
   if(InpFallbackEnabled && !g_fallback_model_runtime.Init(reason))
      return FailInit("fallback_" + reason);

   g_decision_surface.Configure(InpShortThreshold,
                                InpLongThreshold,
                                InpMinMargin);
   g_fallback_decision_surface.Configure(InpFallbackShortThreshold,
                                         InpFallbackLongThreshold,
                                         InpFallbackMinMargin);

   g_execution_bridge.Configure(InpMainSymbol,
                                InpMagic,
                                InpAllowTrading,
                                InpFixedLot,
                                InpDeviationPoints,
                                InpCloseOnFlatSignal,
                                InpReverseOnOppositeSignal,
                                InpMaxHoldBars,
                                InpMaxConcurrentPositions);

   if(!g_execution_bridge.Init(reason))
      return FailInit(reason);

   if(!g_telemetry.RecordLifecycle("init_ok", "runtime_ready", telemetry_reason))
      return FailInit(telemetry_reason);

   g_runtime_ready = true;
   Print("[ObsidianPrimeV2][RuntimeProbe] init_ok");
   return INIT_SUCCEEDED;
  }

void OnTick()
  {
   g_telemetry.CountTick();
   if(!g_runtime_ready)
      return;

   const datetime current_bar_open = iTime(InpMainSymbol, InpTimeframe, 0);
   if(current_bar_open <= 0)
      return;

   if(current_bar_open == g_last_bar_open)
      return;

   g_last_bar_open = current_bar_open;
   ProcessClosedBar();
  }

void OnDeinit(const int reason)
  {
   g_runtime_ready = false;
   g_model_runtime.Deinit();
   g_fallback_model_runtime.Deinit();

   string telemetry_reason = "";
   const string reason_text = DeinitReasonText(reason);
   g_telemetry.RecordLifecycle("deinit", reason_text, telemetry_reason);
   PrintTelemetryFailure("deinit", telemetry_reason);

   telemetry_reason = "";
   g_telemetry.WriteSummary(reason_text, telemetry_reason);
   PrintTelemetryFailure("summary", telemetry_reason);
  }
