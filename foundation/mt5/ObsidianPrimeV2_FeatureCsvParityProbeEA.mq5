#property strict
#property version   "1.00"

#include "include/ObsidianPrime/FeatureInputs.mqh"

input string          InpRunId = "feature_csv_parity_probe_default";
input string          InpFeatureCsvPath = "Project_Obsidian_Prime_v2/feature_parity/default/features.csv";
input int             InpFeatureCount = 58;
input bool            InpFeatureCsvUseCommonFiles = true;
input bool            InpFeatureRequireTimestampMatch = true;
input bool            InpFeatureAllowLatestFallback = false;
input bool            InpFeatureStrictHeader = true;
input string          InpFeatureCsvDelimiter = ",";
input string          InpMainSymbol = "US100";
input ENUM_TIMEFRAMES InpTimeframe = PERIOD_M5;
input bool            InpCsvTimestampIsBarClose = true;
input string          InpFeatureOrderHash = "";
input string          InpOutputCsvPath = "Project_Obsidian_Prime_v2/feature_parity/default/feature_parity_probe.csv";
input string          InpSummaryCsvPath = "Project_Obsidian_Prime_v2/feature_parity/default/feature_parity_summary.csv";
input bool            InpOutputUseCommonFiles = true;
input int             InpMaxRows = 0;

COpFeatureCsvInput g_feature_input;
int      g_output_handle = INVALID_HANDLE;
datetime g_last_bar_open = 0;
int      g_row_count = 0;
int      g_ready_count = 0;
int      g_skip_count = 0;
datetime g_first_bar_time = 0;
datetime g_last_bar_time = 0;
string   g_last_reason = "";

datetime CurrentClosedBarTimestamp()
  {
   const datetime closed_open = iTime(InpMainSymbol, InpTimeframe, 1);
   if(closed_open <= 0)
      return 0;
   if(InpCsvTimestampIsBarClose)
      return closed_open + PeriodSeconds(InpTimeframe);
   return closed_open;
  }

bool OpenOutput()
  {
   int flags = FILE_WRITE | FILE_CSV | FILE_ANSI;
   if(InpOutputUseCommonFiles)
      flags |= FILE_COMMON;
   ResetLastError();
   g_output_handle = FileOpen(InpOutputCsvPath, flags, ',');
   if(g_output_handle == INVALID_HANDLE)
     {
      PrintFormat("[ObsidianPrimeV2][FeatureCsvParityProbe][output_open_failed] %d", GetLastError());
      return false;
     }
   FileWrite(g_output_handle,
             "record_type",
             "run_id",
             "bar_time",
             "feature_ready",
             "source_time",
             "input_hash",
             "skip_reason",
             "feature_count",
             "feature_order_hash",
             "first_feature",
             "last_feature",
             "feature_sum",
             "feature_abs_sum");
   return true;
  }

void WriteProbeRow(const datetime target_time,
                   const bool ready,
                   const string source_time,
                   const string input_hash,
                   const string reason,
                   const double &features[])
  {
   if(g_output_handle == INVALID_HANDLE)
      return;

   const int feature_count = ArraySize(features);
   double feature_sum = 0.0;
   double feature_abs_sum = 0.0;
   for(int i = 0; i < feature_count; i++)
     {
      feature_sum += features[i];
      feature_abs_sum += MathAbs(features[i]);
     }
   const double first_feature = feature_count > 0 ? features[0] : 0.0;
   const double last_feature = feature_count > 0 ? features[feature_count - 1] : 0.0;

   FileWrite(g_output_handle,
             "feature_probe",
             InpRunId,
             OP_TimestampText(target_time),
             ready ? "true" : "false",
             source_time,
             input_hash,
             reason,
             IntegerToString(feature_count),
             InpFeatureOrderHash,
             DoubleToString(first_feature, 10),
             DoubleToString(last_feature, 10),
             DoubleToString(feature_sum, 10),
             DoubleToString(feature_abs_sum, 10));
  }

void ProcessClosedBar()
  {
   if(InpMaxRows > 0 && g_row_count >= InpMaxRows)
      return;

   const datetime target_time = CurrentClosedBarTimestamp();
   double features[];
   string source_time = "";
   string input_hash = "";
   string reason = "";
   bool ready = false;
   if(target_time > 0)
      ready = g_feature_input.ReadForTime(target_time, features, source_time, input_hash, reason);
   else
      reason = "closed_bar_unavailable";

   g_row_count++;
   if(ready)
      g_ready_count++;
   else
      g_skip_count++;
   if(g_first_bar_time <= 0 && target_time > 0)
      g_first_bar_time = target_time;
   if(target_time > 0)
      g_last_bar_time = target_time;
   g_last_reason = reason;
   WriteProbeRow(target_time, ready, source_time, input_hash, reason, features);
  }

bool WriteSummary(const int reason)
  {
   int flags = FILE_WRITE | FILE_CSV | FILE_ANSI;
   if(InpOutputUseCommonFiles)
      flags |= FILE_COMMON;
   ResetLastError();
   const int handle = FileOpen(InpSummaryCsvPath, flags, ',');
   if(handle == INVALID_HANDLE)
     {
      PrintFormat("[ObsidianPrimeV2][FeatureCsvParityProbe][summary_open_failed] %d", GetLastError());
      return false;
     }
   FileWrite(handle,
             "record_type",
             "run_id",
             "deinit_reason",
             "feature_csv_path",
             "feature_count",
             "feature_order_hash",
             "row_count",
             "ready_count",
             "skip_count",
             "first_bar_time",
             "last_bar_time",
             "last_reason");
   FileWrite(handle,
             "summary",
             InpRunId,
             IntegerToString(reason),
             InpFeatureCsvPath,
             IntegerToString(InpFeatureCount),
             InpFeatureOrderHash,
             IntegerToString(g_row_count),
             IntegerToString(g_ready_count),
             IntegerToString(g_skip_count),
             OP_TimestampText(g_first_bar_time),
             OP_TimestampText(g_last_bar_time),
             g_last_reason);
   FileClose(handle);
   return true;
  }

int OnInit()
  {
   g_feature_input.Configure(InpFeatureCsvPath,
                             InpFeatureCsvUseCommonFiles,
                             InpFeatureRequireTimestampMatch,
                             InpFeatureAllowLatestFallback,
                             InpFeatureStrictHeader,
                             InpFeatureCsvDelimiter,
                             InpFeatureCount);
   if(!OpenOutput())
      return INIT_FAILED;
   Print("[ObsidianPrimeV2][FeatureCsvParityProbe] init_ok");
   return INIT_SUCCEEDED;
  }

void OnDeinit(const int reason)
  {
   if(g_output_handle != INVALID_HANDLE)
     {
      FileClose(g_output_handle);
      g_output_handle = INVALID_HANDLE;
     }
   WriteSummary(reason);
   PrintFormat("[ObsidianPrimeV2][FeatureCsvParityProbe] deinit rows=%d ready=%d skipped=%d",
               g_row_count,
               g_ready_count,
               g_skip_count);
  }

void OnTick()
  {
   const datetime bar_open = iTime(InpMainSymbol, InpTimeframe, 0);
   if(bar_open <= 0)
      return;
   if(bar_open == g_last_bar_open)
      return;
   g_last_bar_open = bar_open;
   ProcessClosedBar();
  }
