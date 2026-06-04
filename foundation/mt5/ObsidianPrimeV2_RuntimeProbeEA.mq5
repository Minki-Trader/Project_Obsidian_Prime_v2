#property strict
#property version   "1.00"

#include "include/ObsidianPrime/FeatureInputs.mqh"
#include "include/ObsidianPrime/ModelRuntime.mqh"
#include "include/ObsidianPrime/EbmTableRuntime.mqh"
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
input string          InpModelBackend = "onnx";
input bool            InpModelUseCommonFiles = true;
input bool            InpModelUseCpuOnly = true;
input bool            InpModelNoConversion = false;
input bool            InpSetOutputShape = true;
input bool            InpModelUseMatrixTensor = false;
input string          InpFeatureOrderHash = "fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2";

input bool            InpFallbackEnabled = false;
input string          InpFallbackTierLabel = "Tier B fallback";
input string          InpFallbackFeatureCsvPath = "Project_Obsidian_Prime_v2/runtime_probe/default/fallback_features.csv";
input int             InpFallbackFeatureCount = 56;
input string          InpFallbackModelPath = "Project_Obsidian_Prime_v2/runtime_probe/default/fallback_model.onnx";
input string          InpFallbackModelId = "runtime_probe_default_tier_b_fallback_model";
input string          InpFallbackModelBackend = "onnx";
input string          InpFallbackFeatureOrderHash = "";
input bool            InpFallbackUseOnPrimaryFlat = false;
input bool            InpFallbackPrimaryFlatRequiresNoPosition = true;
input bool            InpFallbackUseOnPrimaryLowConfidence = false;
input double          InpFallbackPrimaryMaxConfidence = 0.0;
input bool            InpFallbackLowConfidenceRequiresNoPosition = true;

input double          InpShortThreshold = 0.55;
input double          InpLongThreshold = 0.55;
input double          InpMinMargin = 0.05;
input string          InpDecisionMode = "threshold_margin";
input bool            InpInvertSignal = false;
input double          InpFallbackShortThreshold = 0.55;
input double          InpFallbackLongThreshold = 0.55;
input double          InpFallbackMinMargin = 0.05;
input string          InpFallbackDecisionMode = "threshold_margin";
input bool            InpFallbackInvertSignal = false;
input bool            InpSideFilterEnabled = false;
input int             InpSideFilterFeatureIndex = -1;
input int             InpFallbackSideFilterFeatureIndex = -1;
input bool            InpBlockShortFeatureRange = false;
input double          InpBlockShortFeatureMin = 0.0;
input double          InpBlockShortFeatureMax = 0.0;
input bool            InpBlockLongFeatureRange = false;
input double          InpBlockLongFeatureMin = 0.0;
input double          InpBlockLongFeatureMax = 0.0;
input bool            InpBlockPremarketShort = false;
input int             InpPremarketStartHour = 12;
input int             InpPremarketEndHour = 17;
input bool            InpMarchNonHour16MarginFilter = false;
input int             InpMarchFilterMonth = 3;
input int             InpMarchFilterBlockedHour = 16;
input double          InpMarchFilterAbsMarginMin = 0.10;
input double          InpEntryMarginFloor = 0.0;
input bool            InpTimeMarginGuardEnabled = false;
input string          InpTimeMarginGuardSide = "long";
input int             InpTimeMarginGuardStartHour = 0;
input int             InpTimeMarginGuardEndHour = 24;
input string          InpTimeMarginGuardBasis = "opposite";
input double          InpTimeMarginGuardMinMargin = 0.0;

input bool            InpAllowTrading = true;
input double          InpFixedLot = 0.10;
input long            InpMagic = 26041001;
input int             InpDeviationPoints = 20;
input bool            InpCloseOnFlatSignal = false;
input bool            InpReverseOnOppositeSignal = true;
input bool            InpCloseOnlyOnOppositeSignal = false;
input int             InpMaxHoldBars = 12;
input int             InpMaxConcurrentPositions = 1;
input int             InpReentryCooldownBars = 0;
input int             InpSameDirectionReentryCooldownBars = 0;
input bool            InpEntryTransitionOnly = false;
input double          InpEntryTransitionRearmMinConfidenceDelta = 0.0;
input bool            InpExitRiskOverlayEnabled = false;
input int             InpExitRiskCloseLongFeatureIndex = -1;
input int             InpExitRiskCloseShortFeatureIndex = -1;
input double          InpExitRiskCloseThreshold = 0.5;
input int             InpExitRiskMinHoldBars = 0;
input int             InpExitRiskMaxHoldFeatureIndex = -1;
input bool            InpAtrSltpEnabled = false;
input int             InpAtrPeriod = 14;
input double          InpAtrStopMultiplier = 0.0;
input double          InpAtrTakeProfitMultiplier = 0.0;
input double          InpAtrMinStopPoints = 0.0;
input double          InpAtrMaxStopPoints = 0.0;
input double          InpAtrMinTakeProfitPoints = 0.0;
input double          InpAtrMaxTakeProfitPoints = 0.0;
input bool            InpModelRiskSizingEnabled = false;
input double          InpModelRiskMinPct = 0.005;
input double          InpModelRiskMaxPct = 0.05;
input double          InpModelRiskConfidenceFloor = 0.55;
input double          InpModelRiskConfidenceCeiling = 0.85;
input double          InpModelRiskFallbackLot = 0.10;

input bool            InpTelemetryEnabled = true;
input bool            InpTelemetryUseCommonFiles = true;
input string          InpTelemetryCsvPath = "Project_Obsidian_Prime_v2/runtime_probe/default/runtime_telemetry.csv";
input string          InpSummaryCsvPath = "Project_Obsidian_Prime_v2/runtime_probe/default/runtime_summary.csv";

COpFeatureCsvInput   g_feature_input;
COpFeatureCsvInput   g_fallback_feature_input;
COpModelRuntime      g_model_runtime;
COpModelRuntime      g_fallback_model_runtime;
COpEbmTableRuntime   g_ebm_table_runtime;
COpEbmTableRuntime   g_fallback_ebm_table_runtime;
COpDecisionSurface   g_decision_surface;
COpDecisionSurface   g_fallback_decision_surface;
COpExecutionBridge   g_execution_bridge;
COpRuntimeTelemetry  g_telemetry;

bool     g_runtime_ready = false;
datetime g_last_bar_open = 0;
int      g_atr_handle = INVALID_HANDLE;
bool     g_last_routed_signal_seen = false;
int      g_last_routed_signal = OP_DECISION_FLAT;
double   g_last_routed_confidence = 0.0;

double FeatureValueOrDefault(const double &features[], const int feature_index, const double fallback)
  {
   if(feature_index < 0 || feature_index >= ArraySize(features))
      return fallback;
   const double value = features[feature_index];
   if(!MathIsValidNumber(value) || MathAbs(value) >= (EMPTY_VALUE / 2.0))
      return fallback;
   return value;
  }

bool FeatureFlagAtOrAbove(const double &features[], const int feature_index, const double threshold)
  {
   return FeatureValueOrDefault(features, feature_index, 0.0) >= threshold;
  }

int FeatureIntOrDefault(const double &features[], const int feature_index, const int fallback)
  {
   const double value = FeatureValueOrDefault(features, feature_index, (double)fallback);
   return (int)MathRound(value);
  }

bool FeatureInInclusiveRange(const double &features[],
                             const int feature_index,
                             const double range_min,
                             const double range_max,
                             double &value)
  {
   if(feature_index < 0 || range_min > range_max)
      return false;
   value = FeatureValueOrDefault(features, feature_index, EMPTY_VALUE);
   if(!MathIsValidNumber(value) || MathAbs(value) >= (EMPTY_VALUE / 2.0))
      return false;
   return value >= range_min && value <= range_max;
  }

void ApplySideFeatureFilter(const double &features[],
                            const string active_tier,
                            SOpDecisionResult &decision)
  {
   if(!InpSideFilterEnabled || decision.signal == OP_DECISION_FLAT)
      return;

   const int feature_index = (active_tier == "tier_b_fallback")
                             ? InpFallbackSideFilterFeatureIndex
                             : InpSideFilterFeatureIndex;
   double feature_value = 0.0;
   if(decision.signal == OP_DECISION_SHORT
      && InpBlockShortFeatureRange
      && FeatureInInclusiveRange(features,
                                 feature_index,
                                 InpBlockShortFeatureMin,
                                 InpBlockShortFeatureMax,
                                 feature_value))
     {
      decision.signal = OP_DECISION_FLAT;
      decision.label = "flat";
      decision.confidence = 0.0;
      decision.margin = 0.0;
      decision.reason = "side_filter_block_short_feature_range:index="
                        + (string)feature_index
                        + ",value="
                        + DoubleToString(feature_value, 6)
                        + "|"
                        + decision.reason;
      return;
     }

   if(decision.signal == OP_DECISION_LONG
      && InpBlockLongFeatureRange
      && FeatureInInclusiveRange(features,
                                 feature_index,
                                 InpBlockLongFeatureMin,
                                 InpBlockLongFeatureMax,
                                 feature_value))
     {
      decision.signal = OP_DECISION_FLAT;
      decision.label = "flat";
      decision.confidence = 0.0;
      decision.margin = 0.0;
      decision.reason = "side_filter_block_long_feature_range:index="
                        + (string)feature_index
                        + ",value="
                        + DoubleToString(feature_value, 6)
                        + "|"
                        + decision.reason;
     }
  }

double SignalSideMargin(const int signal,
                        const double p_short,
                        const double p_flat,
                        const double p_long)
  {
   if(signal == OP_DECISION_SHORT)
      return p_short - MathMax(p_flat, p_long);
   if(signal == OP_DECISION_LONG)
      return p_long - MathMax(p_flat, p_short);
   return 0.0;
  }

double DirectionalAbsMargin(const double p_short,
                            const double p_flat,
                            const double p_long)
  {
   const double short_margin = p_short - MathMax(p_flat, p_long);
   const double long_margin = p_long - MathMax(p_flat, p_short);
   return MathMax(MathAbs(short_margin), MathAbs(long_margin));
  }

bool HourInRange(const int hour, const int start_hour, const int end_hour)
  {
   const int normalized_hour = (hour % 24 + 24) % 24;
   const int normalized_start = (start_hour % 24 + 24) % 24;
   int normalized_end = end_hour;
   if(normalized_end == 24)
      normalized_end = 24;
   else
      normalized_end = (normalized_end % 24 + 24) % 24;

   if(normalized_end == 24)
      return normalized_hour >= normalized_start && normalized_hour < 24;
   if(normalized_start == normalized_end)
      return true;
   if(normalized_start < normalized_end)
      return normalized_hour >= normalized_start && normalized_hour < normalized_end;
   return normalized_hour >= normalized_start || normalized_hour < normalized_end;
  }

bool TimeMarginGuardSideMatches(const int signal)
  {
   string side = InpTimeMarginGuardSide;
   StringToLower(side);
   if(side == "long")
      return signal == OP_DECISION_LONG;
   if(side == "short")
      return signal == OP_DECISION_SHORT;
   if(side == "both" || side == "signal")
      return signal == OP_DECISION_LONG || signal == OP_DECISION_SHORT;
   return false;
  }

double TimeMarginGuardValue(const int signal,
                            const double p_short,
                            const double p_flat,
                            const double p_long)
  {
   string basis = InpTimeMarginGuardBasis;
   StringToLower(basis);

   if(basis == "opposite")
     {
      if(signal == OP_DECISION_SHORT)
         return p_short - p_long;
      if(signal == OP_DECISION_LONG)
         return p_long - p_short;
      return 0.0;
     }
   if(basis == "flat")
     {
      if(signal == OP_DECISION_SHORT)
         return p_short - p_flat;
      if(signal == OP_DECISION_LONG)
         return p_long - p_flat;
      return 0.0;
     }
   if(basis == "abs_directional")
      return DirectionalAbsMargin(p_short, p_flat, p_long);
   return SignalSideMargin(signal, p_short, p_flat, p_long);
  }

void ApplyRuntimeTimeFilters(const datetime target_time,
                             const double p_short,
                             const double p_flat,
                             const double p_long,
                             SOpDecisionResult &decision)
  {
   if(decision.signal == OP_DECISION_FLAT)
      return;

   MqlDateTime parts;
   TimeToStruct(target_time, parts);

   if(InpMarchNonHour16MarginFilter && parts.mon == InpMarchFilterMonth)
     {
      const double abs_margin = DirectionalAbsMargin(p_short, p_flat, p_long);
      if(parts.hour == InpMarchFilterBlockedHour || abs_margin < InpMarchFilterAbsMarginMin)
        {
         decision.signal = OP_DECISION_FLAT;
         decision.label = "flat";
         decision.confidence = 0.0;
         decision.margin = 0.0;
         decision.reason = "march_non_hour16_margin_filter:hour="
                           + (string)parts.hour
                           + ",abs_margin="
                           + DoubleToString(abs_margin, 6)
                           + "|"
                           + decision.reason;
         return;
        }
     }

   if(InpTimeMarginGuardEnabled && TimeMarginGuardSideMatches(decision.signal))
     {
      if(HourInRange(parts.hour, InpTimeMarginGuardStartHour, InpTimeMarginGuardEndHour))
        {
         const double guard_margin = TimeMarginGuardValue(decision.signal, p_short, p_flat, p_long);
         if(guard_margin < InpTimeMarginGuardMinMargin)
           {
            string guard_basis = InpTimeMarginGuardBasis;
            StringToLower(guard_basis);
            decision.signal = OP_DECISION_FLAT;
            decision.label = "flat";
            decision.confidence = 0.0;
            decision.margin = 0.0;
            decision.reason = "time_margin_guard:hour="
                              + (string)parts.hour
                              + ",side="
                              + InpTimeMarginGuardSide
                              + ",basis="
                              + guard_basis
                              + ",margin="
                              + DoubleToString(guard_margin, 6)
                              + "<"
                              + DoubleToString(InpTimeMarginGuardMinMargin, 6)
                              + "|"
                              + decision.reason;
            return;
           }
        }
     }

   if(InpEntryMarginFloor > 0.0)
     {
      const double side_margin = SignalSideMargin(decision.signal, p_short, p_flat, p_long);
      if(side_margin < InpEntryMarginFloor)
        {
         decision.signal = OP_DECISION_FLAT;
         decision.label = "flat";
         decision.confidence = 0.0;
         decision.margin = 0.0;
         decision.reason = "entry_margin_floor:"
                           + DoubleToString(side_margin, 6)
                           + "<"
                           + DoubleToString(InpEntryMarginFloor, 6)
                           + "|"
                           + decision.reason;
         return;
        }
     }

   if(InpBlockPremarketShort && decision.signal == OP_DECISION_SHORT)
     {
      if(parts.hour >= InpPremarketStartHour && parts.hour < InpPremarketEndHour)
        {
         decision.signal = OP_DECISION_FLAT;
         decision.label = "flat";
         decision.confidence = 0.0;
         decision.margin = 0.0;
         decision.reason = "premarket_short_block:hour="
                           + (string)parts.hour
                           + "|"
                           + decision.reason;
        }
     }
  }

double ClampAdapterPoints(const double value, const double min_points, const double max_points)
  {
   if(value <= 0.0 || !MathIsValidNumber(value))
      return 0.0;
   double output = value;
   if(min_points > 0.0 && output < min_points)
      output = min_points;
   if(max_points > 0.0 && output > max_points)
      output = max_points;
   return output;
  }

double CurrentAtrPoints()
  {
   if(!InpAtrSltpEnabled || g_atr_handle == INVALID_HANDLE)
      return 0.0;

   double values[];
   ArraySetAsSeries(values, true);
   ResetLastError();
   if(CopyBuffer(g_atr_handle, 0, 1, 1, values) != 1)
      return 0.0;

   const double point = SymbolInfoDouble(InpMainSymbol, SYMBOL_POINT);
   if(point <= 0.0 || !MathIsValidNumber(values[0]) || values[0] <= 0.0)
      return 0.0;

   return values[0] / point;
  }

struct SOpRiskSizingDecision
  {
   double model_risk_pct;
   double clipped_risk_pct;
   double computed_lot;
   double executed_lot;
   bool   min_lot_floor_applied;
   double actual_risk_pct_after_floor;
  };

double NormalizeAdapterLot(const double requested)
  {
   const double min_volume = SymbolInfoDouble(InpMainSymbol, SYMBOL_VOLUME_MIN);
   const double max_volume = SymbolInfoDouble(InpMainSymbol, SYMBOL_VOLUME_MAX);
   const double step = SymbolInfoDouble(InpMainSymbol, SYMBOL_VOLUME_STEP);
   const double floor_lot = MathMax(0.01, min_volume);

   double volume = requested;
   if(volume < floor_lot)
      volume = floor_lot;
   if(max_volume > 0.0 && volume > max_volume)
      volume = max_volume;
   if(step > 0.0)
      volume = MathFloor((volume / step) + 0.0000001) * step;
   if(volume < floor_lot)
      volume = floor_lot;
   return NormalizeDouble(volume, 8);
  }

double RiskMoneyPerLot(const double stop_points)
  {
   if(stop_points <= 0.0 || !MathIsValidNumber(stop_points))
      return 0.0;

   const double point = SymbolInfoDouble(InpMainSymbol, SYMBOL_POINT);
   const double tick_size = SymbolInfoDouble(InpMainSymbol, SYMBOL_TRADE_TICK_SIZE);
   const double tick_value = SymbolInfoDouble(InpMainSymbol, SYMBOL_TRADE_TICK_VALUE);
   if(point <= 0.0 || tick_size <= 0.0 || tick_value <= 0.0)
      return 0.0;

   const double ticks = (stop_points * point) / tick_size;
   if(ticks <= 0.0 || !MathIsValidNumber(ticks))
      return 0.0;
   return ticks * tick_value;
  }

double ModelRiskPctFromDecision(const SOpDecisionResult &decision)
  {
   if(!InpModelRiskSizingEnabled || decision.signal == OP_DECISION_FLAT)
      return 0.0;

   const double max_pct = MathMin(MathMax(InpModelRiskMaxPct, 0.0), 0.05);
   const double min_pct = MathMin(MathMax(InpModelRiskMinPct, 0.0), max_pct);
   if(max_pct <= 0.0)
      return 0.0;

   const double floor_conf = InpModelRiskConfidenceFloor;
   const double ceiling_conf = InpModelRiskConfidenceCeiling;
   if(ceiling_conf <= floor_conf)
      return max_pct;

   double weight = (decision.confidence - floor_conf) / (ceiling_conf - floor_conf);
   if(weight < 0.0)
      weight = 0.0;
   if(weight > 1.0)
      weight = 1.0;
   return min_pct + (max_pct - min_pct) * weight;
  }

SOpRiskSizingDecision BuildRiskSizingDecision(const SOpDecisionResult &decision,
                                              const double open_sl_points)
  {
   SOpRiskSizingDecision sizing;
   sizing.model_risk_pct = ModelRiskPctFromDecision(decision);
   sizing.clipped_risk_pct = MathMin(MathMax(sizing.model_risk_pct, 0.0), 0.05);
   sizing.computed_lot = 0.0;
   sizing.executed_lot = 0.0;
   sizing.min_lot_floor_applied = false;
   sizing.actual_risk_pct_after_floor = 0.0;

   if(decision.signal == OP_DECISION_FLAT)
      return sizing;

   const double risk_money_per_lot = RiskMoneyPerLot(open_sl_points);
   const double balance = AccountInfoDouble(ACCOUNT_BALANCE);
   if(!InpModelRiskSizingEnabled || risk_money_per_lot <= 0.0 || balance <= 0.0)
     {
      sizing.model_risk_pct = 0.0;
      sizing.clipped_risk_pct = 0.0;
      sizing.computed_lot = InpModelRiskFallbackLot > 0.0 ? InpModelRiskFallbackLot : InpFixedLot;
      sizing.executed_lot = NormalizeAdapterLot(sizing.computed_lot);
      sizing.min_lot_floor_applied = sizing.computed_lot < 0.01;
      return sizing;
     }

   const double risk_money = balance * sizing.clipped_risk_pct;
   sizing.computed_lot = risk_money / risk_money_per_lot;
   sizing.min_lot_floor_applied = sizing.computed_lot < 0.01;
   sizing.executed_lot = NormalizeAdapterLot(sizing.computed_lot);
   sizing.actual_risk_pct_after_floor = (sizing.executed_lot * risk_money_per_lot) / balance;
   return sizing;
  }

string DecisionSignalText(const int signal)
  {
   if(signal == OP_DECISION_LONG)
      return "long";
   if(signal == OP_DECISION_SHORT)
      return "short";
   return "flat";
  }

bool ShouldBlockEntryTransition(const int routed_signal,
                                const double routed_confidence,
                                const string position_before,
                                string &reason)
  {
   reason = "";
   if(!InpEntryTransitionOnly)
      return false;
   if(routed_signal == OP_DECISION_FLAT)
      return false;
   if(position_before != "none")
      return false;
   if(!g_last_routed_signal_seen)
      return false;
   if(g_last_routed_signal != routed_signal)
      return false;

   const double confidence_delta = routed_confidence - g_last_routed_confidence;
   if(InpEntryTransitionRearmMinConfidenceDelta > 0.0
      && MathIsValidNumber(confidence_delta)
      && confidence_delta >= InpEntryTransitionRearmMinConfidenceDelta)
      return false;

   reason = "entry_transition_same_signal_block:previous_signal="
            + DecisionSignalText(g_last_routed_signal)
            + ",current_signal="
            + DecisionSignalText(routed_signal)
            + ",confidence_delta="
            + DoubleToString(confidence_delta, 6);
   return true;
  }

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
   g_ebm_table_runtime.Deinit();
   g_fallback_ebm_table_runtime.Deinit();
   g_runtime_ready = false;
   return INIT_FAILED;
  }

bool IsEbmTableBackend(const string backend)
  {
   const string normalized = OP_Lower(OP_Trim(backend));
   return (normalized == "ebm_table" || normalized == "ebm_score_table" || normalized == "table");
  }

bool InitPrimaryModel(string &reason)
  {
   if(IsEbmTableBackend(InpModelBackend))
     {
      g_ebm_table_runtime.Configure(InpModelPath,
                                    InpModelId,
                                    InpModelUseCommonFiles,
                                    InpFeatureCount);
      return g_ebm_table_runtime.Init(reason);
     }
   g_model_runtime.Configure(InpModelPath,
                             InpModelId,
                             InpModelUseCommonFiles,
                              InpModelUseCpuOnly,
                              InpModelNoConversion,
                              InpSetOutputShape,
                              InpModelUseMatrixTensor,
                              InpFeatureCount);
   return g_model_runtime.Init(reason);
  }

bool InitFallbackModel(string &reason)
  {
   if(IsEbmTableBackend(InpFallbackModelBackend))
     {
      g_fallback_ebm_table_runtime.Configure(InpFallbackModelPath,
                                             InpFallbackModelId,
                                             InpModelUseCommonFiles,
                                             InpFallbackFeatureCount);
      return g_fallback_ebm_table_runtime.Init(reason);
     }
   g_fallback_model_runtime.Configure(InpFallbackModelPath,
                                      InpFallbackModelId,
                                      InpModelUseCommonFiles,
                                       InpModelUseCpuOnly,
                                       InpModelNoConversion,
                                       InpSetOutputShape,
                                       InpModelUseMatrixTensor,
                                       InpFallbackFeatureCount);
   return g_fallback_model_runtime.Init(reason);
  }

bool RunPrimaryModel(const double &features[],
                     double &p_short,
                     double &p_flat,
                     double &p_long,
                     string &reason)
  {
   if(IsEbmTableBackend(InpModelBackend))
      return g_ebm_table_runtime.Run(features, p_short, p_flat, p_long, reason);
   return g_model_runtime.Run(features, p_short, p_flat, p_long, reason);
  }

bool RunFallbackModel(const double &features[],
                      double &p_short,
                      double &p_flat,
                      double &p_long,
                      string &reason)
  {
   if(IsEbmTableBackend(InpFallbackModelBackend))
      return g_fallback_ebm_table_runtime.Run(features, p_short, p_flat, p_long, reason);
   return g_fallback_model_runtime.Run(features, p_short, p_flat, p_long, reason);
  }

bool ReadFallbackFeatures(const datetime target_time,
                          double &features[],
                          string &source_time,
                          string &input_hash,
                          string &reason)
  {
   string fallback_reason = "";
   double fallback_features[];
   if(!g_fallback_feature_input.ReadForTime(target_time,
                                            fallback_features,
                                            source_time,
                                            input_hash,
                                            fallback_reason))
     {
      reason = fallback_reason;
      return false;
     }

   const int fallback_count = ArraySize(fallback_features);
   ArrayResize(features, fallback_count);
   for(int i = 0; i < fallback_count; i++)
      features[i] = fallback_features[i];

   reason = "";
   return true;
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
                           0.0,
                           0.0,
                           0.0,
                           0.0,
                           false,
                           0.0,
                           0.0,
                           0.0,
                           0.0,
                           "skip",
                           InpFallbackEnabled,
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

   string fallback_reason = "";
   if(ReadFallbackFeatures(target_time,
                           features,
                           source_time,
                           input_hash,
                           fallback_reason))
     {
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

bool ShouldTryFallbackAfterPrimaryDecision(const SOpDecisionResult &decision,
                                           const string position_before,
                                           string &trigger_reason)
  {
   trigger_reason = "";
   if(!InpFallbackEnabled)
      return false;

   const bool no_position = (position_before == "none");
   if(InpFallbackUseOnPrimaryFlat
      && decision.signal == OP_DECISION_FLAT
      && (!InpFallbackPrimaryFlatRequiresNoPosition || no_position))
     {
      trigger_reason = "primary_flat_secondary_coverage";
      return true;
     }

   if(InpFallbackUseOnPrimaryLowConfidence
      && decision.signal != OP_DECISION_FLAT
      && decision.confidence <= InpFallbackPrimaryMaxConfidence
      && (!InpFallbackLowConfidenceRequiresNoPosition || no_position))
     {
      trigger_reason = "primary_low_confidence_secondary_coverage";
      return true;
     }

   return false;
  }

bool PromoteFallbackDecision(const datetime target_time,
                             double &features[],
                             string &source_time,
                             string &input_hash,
                             string &active_tier,
                             string &active_model_id,
                             string &active_feature_order_hash,
                             double &p_short,
                             double &p_flat,
                             double &p_long,
                             SOpDecisionResult &decision,
                             const string trigger_reason)
  {
   double fallback_features[];
   string fallback_source_time = "";
   string fallback_input_hash = "";
   string fallback_feature_reason = "";
   if(!ReadFallbackFeatures(target_time,
                            fallback_features,
                            fallback_source_time,
                            fallback_input_hash,
                            fallback_feature_reason))
     {
      decision.reason = "secondary_coverage_features_missing:" + fallback_feature_reason + "|" + decision.reason;
      return false;
     }

   double fallback_p_short = 0.0;
   double fallback_p_flat = 0.0;
   double fallback_p_long = 0.0;
   string fallback_model_reason = "";
   if(!RunFallbackModel(fallback_features,
                        fallback_p_short,
                        fallback_p_flat,
                        fallback_p_long,
                        fallback_model_reason))
     {
      decision.reason = "secondary_coverage_model_failed:" + fallback_model_reason + "|" + decision.reason;
      return false;
     }

   SOpDecisionResult fallback_decision;
   g_fallback_decision_surface.Evaluate(fallback_p_short,
                                        fallback_p_flat,
                                        fallback_p_long,
                                        fallback_decision);
   ApplySideFeatureFilter(fallback_features, "tier_b_fallback", fallback_decision);

   const int fallback_count = ArraySize(fallback_features);
   ArrayResize(features, fallback_count);
   for(int i = 0; i < fallback_count; i++)
      features[i] = fallback_features[i];

   source_time = fallback_source_time;
   input_hash = fallback_input_hash;
   active_tier = "tier_b_fallback";
   active_model_id = InpFallbackModelId;
   active_feature_order_hash = InpFallbackFeatureOrderHash;
   p_short = fallback_p_short;
   p_flat = fallback_p_flat;
   p_long = fallback_p_long;
   decision = fallback_decision;
   decision.reason = trigger_reason + "|" + decision.reason;
   return true;
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
                         ? RunFallbackModel(features, p_short, p_flat, p_long, model_reason)
                         : RunPrimaryModel(features, p_short, p_flat, p_long, model_reason);
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
                              0.0,
                              0.0,
                              0.0,
                              0.0,
                              false,
                              0.0,
                              0.0,
                              0.0,
                              0.0,
                              "model_skip",
                              InpFallbackEnabled,
                              telemetry_reason);
      PrintTelemetryFailure("model_skip", telemetry_reason);
      return;
     }

   SOpDecisionResult decision;
   if(active_tier == "tier_b_fallback")
      g_fallback_decision_surface.Evaluate(p_short, p_flat, p_long, decision);
   else
      g_decision_surface.Evaluate(p_short, p_flat, p_long, decision);
   ApplySideFeatureFilter(features, active_tier, decision);

   if(active_tier != "tier_b_fallback")
     {
      string secondary_trigger = "";
      if(ShouldTryFallbackAfterPrimaryDecision(decision, position_before, secondary_trigger))
         PromoteFallbackDecision(target_time,
                                 features,
                                 source_time,
                                 input_hash,
                                 active_tier,
                                 active_model_id,
                                 active_feature_order_hash,
                                 p_short,
                                 p_flat,
                                 p_long,
                                 decision,
                                 secondary_trigger);
     }
   ApplyRuntimeTimeFilters(target_time, p_short, p_flat, p_long, decision);

   const int routed_signal_before_entry_gate = decision.signal;
   const double routed_confidence_before_entry_gate = decision.confidence;
   string entry_transition_reason = "";
   if(ShouldBlockEntryTransition(routed_signal_before_entry_gate,
                                 routed_confidence_before_entry_gate,
                                 position_before,
                                 entry_transition_reason))
     {
      decision.signal = OP_DECISION_FLAT;
      decision.label = "flat";
      decision.confidence = 0.0;
      decision.margin = 0.0;
      decision.reason = entry_transition_reason + "|" + decision.reason;
     }

   bool overlay_close_long = false;
   bool overlay_close_short = false;
   int overlay_max_hold_bars = 0;
   if(InpExitRiskOverlayEnabled)
     {
      overlay_close_long = FeatureFlagAtOrAbove(features, InpExitRiskCloseLongFeatureIndex, InpExitRiskCloseThreshold);
      overlay_close_short = FeatureFlagAtOrAbove(features, InpExitRiskCloseShortFeatureIndex, InpExitRiskCloseThreshold);
      overlay_max_hold_bars = FeatureIntOrDefault(features, InpExitRiskMaxHoldFeatureIndex, 0);
     }

   const double atr_points = CurrentAtrPoints();
   const double open_sl_points = ClampAdapterPoints(atr_points * InpAtrStopMultiplier,
                                                    InpAtrMinStopPoints,
                                                    InpAtrMaxStopPoints);
   const double open_tp_points = ClampAdapterPoints(atr_points * InpAtrTakeProfitMultiplier,
                                                    InpAtrMinTakeProfitPoints,
                                                    InpAtrMaxTakeProfitPoints);
   const SOpRiskSizingDecision risk_sizing = BuildRiskSizingDecision(decision, open_sl_points);

   SOpExecutionResult execution;
   const bool execution_ok = g_execution_bridge.Execute(decision.signal,
                                                        execution,
                                                        overlay_close_long,
                                                        overlay_close_short,
                                                        InpExitRiskMinHoldBars,
                                                        overlay_max_hold_bars,
                                                        open_sl_points,
                                                        open_tp_points,
                                                        risk_sizing.executed_lot);
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
                           risk_sizing.model_risk_pct,
                           risk_sizing.clipped_risk_pct,
                           risk_sizing.computed_lot,
                           risk_sizing.executed_lot,
                           risk_sizing.min_lot_floor_applied,
                           risk_sizing.actual_risk_pct_after_floor,
                           atr_points,
                           open_sl_points,
                           open_tp_points,
                           execution.action,
                           InpFallbackEnabled,
                           telemetry_reason);
   PrintTelemetryFailure("cycle", telemetry_reason);
   g_last_routed_signal = routed_signal_before_entry_gate;
   g_last_routed_confidence = routed_confidence_before_entry_gate;
   g_last_routed_signal_seen = true;
  }

int OnInit()
  {
   g_runtime_ready = false;
   g_last_bar_open = 0;
   g_last_routed_signal_seen = false;
   g_last_routed_signal = OP_DECISION_FLAT;
   g_last_routed_confidence = 0.0;

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

   if(InpAtrSltpEnabled)
     {
      if(InpAtrPeriod <= 0)
         return FailInit("atr_sltp_invalid_period");
      g_atr_handle = iATR(InpMainSymbol, InpTimeframe, InpAtrPeriod);
      if(g_atr_handle == INVALID_HANDLE)
         return FailInit("atr_sltp_handle_failed:" + (string)GetLastError());
     }

   g_feature_input.Configure(InpFeatureCsvPath,
                             InpFeatureCsvUseCommonFiles,
                             InpFeatureRequireTimestampMatch,
                             InpFeatureAllowLatestFallback,
                             InpFeatureStrictHeader,
                             InpFeatureCsvDelimiter,
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
     }

   string reason = "";
   if(!InitPrimaryModel(reason))
      return FailInit(reason);
   if(InpFallbackEnabled && !InitFallbackModel(reason))
      return FailInit("fallback_" + reason);

   g_decision_surface.Configure(InpShortThreshold,
                                InpLongThreshold,
                                InpMinMargin,
                                InpInvertSignal);
   g_decision_surface.ConfigureDecisionMode(InpDecisionMode);
   g_fallback_decision_surface.Configure(InpFallbackShortThreshold,
                                         InpFallbackLongThreshold,
                                         InpFallbackMinMargin,
                                         InpFallbackInvertSignal);
   g_fallback_decision_surface.ConfigureDecisionMode(InpFallbackDecisionMode);

   g_execution_bridge.Configure(InpMainSymbol,
                                InpMagic,
                                InpAllowTrading,
                                InpFixedLot,
                                InpDeviationPoints,
                                InpCloseOnFlatSignal,
                                InpReverseOnOppositeSignal,
                                InpCloseOnlyOnOppositeSignal,
                                InpMaxHoldBars,
                                InpMaxConcurrentPositions,
                                InpReentryCooldownBars,
                                InpSameDirectionReentryCooldownBars);

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
   g_ebm_table_runtime.Deinit();
   g_fallback_ebm_table_runtime.Deinit();
   if(g_atr_handle != INVALID_HANDLE)
     {
      IndicatorRelease(g_atr_handle);
      g_atr_handle = INVALID_HANDLE;
     }

   string telemetry_reason = "";
   const string reason_text = DeinitReasonText(reason);
   g_telemetry.RecordLifecycle("deinit", reason_text, telemetry_reason);
   PrintTelemetryFailure("deinit", telemetry_reason);

   telemetry_reason = "";
   g_telemetry.WriteSummary(reason_text, telemetry_reason);
   PrintTelemetryFailure("summary", telemetry_reason);
  }
