#property strict
#property script_show_inputs

input string InpOutputPath = "Project_Obsidian_Prime_v2/runtime_parity/runtime_parity_pack_0001/mt5_feature_snapshot_audit_fpmarkets_v2_runtime_minimum_0001.jsonl";
input bool   InpOutputUseCommonFiles = true;
input string InpTargetWindowsUtc = "2022.09.02 17:00:00;2022.09.01 20:00:00;2022.11.09 21:00:00;2022.09.01 19:55:00;2022.09.01 13:35:00";
input string InpMainSymbol = "US100";
input ENUM_TIMEFRAMES InpTimeframe = PERIOD_M5;
input int    InpMainWarmupBars = 300;
input int    InpExternalWarmupBars = 25;
input string InpWindowStartUtc = "2022.08.01 00:00:00";
input string InpDatasetId = "dataset_fpmarkets_v2_us100_m5_20220801_20260413_freeze01";
input string InpFixtureSetId = "fixture_fpmarkets_v2_runtime_minimum_0001";
input string InpBundleId = "bundle_fpmarkets_v2_runtime_minimum_0001";
input string InpRuntimeId = "runtime_fpmarkets_v2_mt5_snapshot_0001";
input string InpReportId = "report_fpmarkets_v2_runtime_parity_0001";
input string InpParserVersion = "fpmarkets_v2_stage01_materializer_v1";
input string InpParserContractVersion = "docs/contracts/python_feature_parser_spec_fpmarkets_v2.md@2026-04-16";
input string InpFeatureContractVersion = "docs/contracts/feature_calculation_spec_fpmarkets_v2.md@2026-04-16";
input string InpRuntimeContractVersion = "docs/contracts/mt5_ea_input_order_contract_fpmarkets_v2.md@2026-04-16";
input string InpFeatureOrderHash = "fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2";

string FEATURE_NAMES[58] =
  {
   "log_return_1",
   "log_return_3",
   "hl_range",
   "close_open_ratio",
   "gap_percent",
   "close_prev_close_ratio",
   "return_zscore_20",
   "hl_zscore_50",
   "overnight_return",
   "return_1_over_atr_14",
   "close_ema20_ratio",
   "close_ema50_ratio",
   "ema9_ema20_diff",
   "ema20_ema50_diff",
   "ema50_ema200_diff",
   "ema20_ema50_spread_zscore_50",
   "sma50_sma200_ratio",
   "rsi_14",
   "rsi_50",
   "rsi_14_slope_3",
   "rsi_14_minus_50",
   "stoch_kd_diff",
   "stochrsi_kd_diff",
   "ppo_hist_12_26_9",
   "roc_12",
   "trix_15",
   "atr_14",
   "atr_50",
   "atr_14_over_atr_50",
   "bollinger_width_20",
   "bb_position_20",
   "bb_squeeze",
   "historical_vol_20",
   "historical_vol_5_over_20",
   "adx_14",
   "di_spread_14",
   "supertrend_10_3",
   "vortex_indicator",
   "is_us_cash_open",
   "minutes_from_cash_open",
   "is_first_30m_after_open",
   "is_last_30m_before_cash_close",
   "vix_change_1",
   "vix_zscore_20",
   "us10yr_change_1",
   "us10yr_zscore_20",
   "usdx_change_1",
   "usdx_zscore_20",
   "nvda_xnas_log_return_1",
   "aapl_xnas_log_return_1",
   "msft_xnas_log_return_1",
   "amzn_xnas_log_return_1",
   "mega8_equal_return_1",
   "top3_weighted_return_1",
   "mega8_pos_breadth_1",
   "mega8_dispersion_5",
   "us100_minus_mega8_equal_return_1",
   "us100_minus_top3_weighted_return_1"
  };

string g_stock_symbols[8] =
  {
   "AAPL.xnas",
   "AMZN.xnas",
   "AMD.xnas",
   "GOOGL.xnas",
   "META.xnas",
   "MSFT.xnas",
   "NVDA.xnas",
   "TSLA.xnas"
  };

double g_top3_equal_weight = 0.333333333333;

struct ExternalAuditItem
  {
   string symbol;
   string requested_close_utc;
   string selected_close_utc;
   string status;
   bool   fallback_used;
   int    stale_bars;
   string detail;
  };

bool IsUsableValue(const double value)
  {
   return MathIsValidNumber(value) && MathAbs(value) < (EMPTY_VALUE / 2.0);
  }

string JsonEscape(string value)
  {
   StringReplace(value, "\\", "\\\\");
   StringReplace(value, "\"", "\\\"");
   StringReplace(value, "\r", "\\r");
   StringReplace(value, "\n", "\\n");
   return value;
  }

string JsonQuoted(const string value)
  {
   return "\"" + JsonEscape(value) + "\"";
  }

string JsonBool(const bool value)
  {
   return value ? "true" : "false";
  }

string JsonNumber(const double value)
  {
   if(!IsUsableValue(value))
      return "null";
   return DoubleToString(value, 10);
  }

string FormatUtc(const datetime value)
  {
   return TimeToString(value, TIME_DATE | TIME_SECONDS);
  }

string FormatUtcIso(const datetime value)
  {
   MqlDateTime dt;
   TimeToStruct(value, dt);
   return StringFormat("%04d-%02d-%02dT%02d:%02d:%02dZ", dt.year, dt.mon, dt.day, dt.hour, dt.min, dt.sec);
  }

bool ParseUtcText(const string raw_text, datetime &out_value)
  {
   string text = raw_text;
   StringTrimLeft(text);
   StringTrimRight(text);
   if(text == "")
      return false;
   out_value = StringToTime(text);
   return (out_value > 0);
  }

int SplitText(const string raw_text, const string delimiter, string &parts[])
  {
   return StringSplit(raw_text, StringGetCharacter(delimiter, 0), parts);
  }

bool BuildTargetWindows(datetime &windows[])
  {
   ArrayResize(windows, 0);
   string parts[];
   int part_count = SplitText(InpTargetWindowsUtc, ";", parts);
   if(part_count <= 0)
      return false;

   for(int i = 0; i < part_count; i++)
     {
      datetime value = 0;
      if(!ParseUtcText(parts[i], value))
         continue;
      int next_size = ArraySize(windows) + 1;
      ArrayResize(windows, next_size);
      windows[next_size - 1] = value;
     }
   return (ArraySize(windows) > 0);
  }

int DayOfWeekForDate(const int year, const int month, const int day)
  {
   MqlDateTime dt;
   dt.year = year;
   dt.mon = month;
   dt.day = day;
   dt.hour = 0;
   dt.min = 0;
   dt.sec = 0;
   datetime value = StructToTime(dt);
   MqlDateTime out_dt;
   TimeToStruct(value, out_dt);
   return out_dt.day_of_week;
  }

int FirstSunday(const int year, const int month)
  {
   int dow = DayOfWeekForDate(year, month, 1);
   return (dow == 0 ? 1 : 8 - dow);
  }

int SecondSunday(const int year, const int month)
  {
   return FirstSunday(year, month) + 7;
  }

bool IsNewYorkDstActive(const datetime utc_time)
  {
   MqlDateTime dt;
   TimeToStruct(utc_time, dt);
   int year = dt.year;

   MqlDateTime dst_start_local;
   dst_start_local.year = year;
   dst_start_local.mon = 3;
   dst_start_local.day = SecondSunday(year, 3);
   dst_start_local.hour = 7;
   dst_start_local.min = 0;
   dst_start_local.sec = 0;
   datetime dst_start_utc = StructToTime(dst_start_local);

   MqlDateTime dst_end_local;
   dst_end_local.year = year;
   dst_end_local.mon = 11;
   dst_end_local.day = FirstSunday(year, 11);
   dst_end_local.hour = 6;
   dst_end_local.min = 0;
   dst_end_local.sec = 0;
   datetime dst_end_utc = StructToTime(dst_end_local);

   return (utc_time >= dst_start_utc && utc_time < dst_end_utc);
  }

datetime ToNewYorkTime(const datetime utc_time)
  {
   int offset_hours = IsNewYorkDstActive(utc_time) ? -4 : -5;
   return utc_time + (offset_hours * 3600);
  }

string OffsetText(const int offset_hours)
  {
   string sign = (offset_hours >= 0 ? "+" : "-");
   return StringFormat("%s%02d:00", sign, MathAbs(offset_hours));
  }

string FormatNewYorkIso(const datetime utc_time)
  {
   int offset_hours = IsNewYorkDstActive(utc_time) ? -4 : -5;
   datetime ny_time = utc_time + (offset_hours * 3600);
   MqlDateTime dt;
   TimeToStruct(ny_time, dt);
   return StringFormat("%04d-%02d-%02dT%02d:%02d:%02d%s", dt.year, dt.mon, dt.day, dt.hour, dt.min, dt.sec, OffsetText(offset_hours));
  }

string CanonicalWindowStartUtc()
  {
   datetime parsed = 0;
   if(!ParseUtcText(InpWindowStartUtc, parsed))
      return "";
   return FormatUtcIso(parsed);
  }

double SafeDivide(const double numerator, const double denominator)
  {
   if(!IsUsableValue(numerator) || !IsUsableValue(denominator) || denominator == 0.0)
      return EMPTY_VALUE;
   return numerator / denominator;
  }

double PopulationStdSlice(const double &values[], const int start_index, const int count)
  {
   if(count <= 0 || start_index < 0 || (start_index + count) > ArraySize(values))
      return EMPTY_VALUE;

   double sum = 0.0;
   for(int i = start_index; i < start_index + count; i++)
     {
      if(!IsUsableValue(values[i]))
         return EMPTY_VALUE;
      sum += values[i];
     }

   double mean = sum / count;
   double variance = 0.0;
   for(int j = start_index; j < start_index + count; j++)
     {
      double diff = values[j] - mean;
      variance += diff * diff;
     }
   variance /= count;
   return MathSqrt(variance);
  }

double RollingMeanSlice(const double &values[], const int start_index, const int count)
  {
   if(count <= 0 || start_index < 0 || (start_index + count) > ArraySize(values))
      return EMPTY_VALUE;
   double sum = 0.0;
   for(int i = start_index; i < start_index + count; i++)
     {
      if(!IsUsableValue(values[i]))
         return EMPTY_VALUE;
      sum += values[i];
     }
   return sum / count;
  }

double RollingMinSlice(const double &values[], const int start_index, const int count)
  {
   if(count <= 0 || start_index < 0 || (start_index + count) > ArraySize(values))
      return EMPTY_VALUE;
   double current_min = DBL_MAX;
   for(int i = start_index; i < start_index + count; i++)
     {
      if(!IsUsableValue(values[i]))
         return EMPTY_VALUE;
      if(values[i] < current_min)
         current_min = values[i];
     }
   return current_min;
  }

double RollingMaxSlice(const double &values[], const int start_index, const int count)
  {
   if(count <= 0 || start_index < 0 || (start_index + count) > ArraySize(values))
      return EMPTY_VALUE;
   double current_max = -DBL_MAX;
   for(int i = start_index; i < start_index + count; i++)
     {
      if(!IsUsableValue(values[i]))
         return EMPTY_VALUE;
      if(values[i] > current_max)
         current_max = values[i];
     }
   return current_max;
  }

double RollingSumSlice(const double &values[], const int start_index, const int count)
  {
   if(count <= 0 || start_index < 0 || (start_index + count) > ArraySize(values))
      return EMPTY_VALUE;
   double sum = 0.0;
   for(int i = start_index; i < start_index + count; i++)
     {
      if(!IsUsableValue(values[i]))
         return EMPTY_VALUE;
      sum += values[i];
     }
   return sum;
  }

double RollingZscoreCurrent(const double &values[], const int total_count, const int window)
  {
   if(window <= 0 || total_count < window)
      return EMPTY_VALUE;
   int start_index = total_count - window;
   double mean = RollingMeanSlice(values, start_index, window);
   double std = PopulationStdSlice(values, start_index, window);
   if(!IsUsableValue(mean) || !IsUsableValue(std))
      return EMPTY_VALUE;
   if(std == 0.0)
      return 0.0;
   return (values[total_count - 1] - mean) / std;
  }

bool ComputeEmaSeries(const double &values[], const int count, const int period, double &out[])
  {
   ArrayResize(out, count);
   if(count <= 0 || period <= 0)
      return false;
   double alpha = 2.0 / (period + 1.0);
   double prev = EMPTY_VALUE;
   for(int i = 0; i < count; i++)
     {
      out[i] = EMPTY_VALUE;
      if(!IsUsableValue(values[i]))
         continue;
      if(!IsUsableValue(prev))
         prev = values[i];
      else
         prev = (alpha * values[i]) + ((1.0 - alpha) * prev);
      if(i >= period - 1)
         out[i] = prev;
     }
   return true;
  }

bool ComputeSmaSeries(const double &values[], const int count, const int period, double &out[])
  {
   ArrayResize(out, count);
   for(int i = 0; i < count; i++)
      out[i] = EMPTY_VALUE;
   if(count <= 0 || period <= 0)
      return false;
   for(int i = period - 1; i < count; i++)
      out[i] = RollingMeanSlice(values, i - period + 1, period);
   return true;
  }

bool ComputeWilderSmoothSeries(const double &values[], const int count, const int period, double &out[])
  {
   ArrayResize(out, count);
   if(count <= 0 || period <= 0)
      return false;
   double alpha = 1.0 / period;
   double prev = EMPTY_VALUE;
   for(int i = 0; i < count; i++)
     {
      out[i] = EMPTY_VALUE;
      if(!IsUsableValue(values[i]))
         continue;
      if(!IsUsableValue(prev))
         prev = values[i];
      else
         prev = (alpha * values[i]) + ((1.0 - alpha) * prev);
      if(i >= period - 1)
         out[i] = prev;
     }
   return true;
  }

bool ComputeTrueRangeSeries(const MqlRates &rates[], const int count, double &tr[])
  {
   ArrayResize(tr, count);
   for(int i = 0; i < count; i++)
      tr[i] = EMPTY_VALUE;
   if(count <= 0)
      return false;
   for(int i = 1; i < count; i++)
     {
      double a = rates[i].high - rates[i].low;
      double b = MathAbs(rates[i].high - rates[i - 1].close);
      double c = MathAbs(rates[i].low - rates[i - 1].close);
      tr[i] = MathMax(a, MathMax(b, c));
     }
   return true;
  }

bool ComputeRsiSeries(const double &close_values[], const int count, const int period, double &rsi[])
  {
   ArrayResize(rsi, count);
   double gains[];
   double losses[];
   ArrayResize(gains, count);
   ArrayResize(losses, count);
   for(int i = 0; i < count; i++)
     {
      rsi[i] = EMPTY_VALUE;
      gains[i] = EMPTY_VALUE;
      losses[i] = EMPTY_VALUE;
     }
   for(int i = 1; i < count; i++)
     {
      if(!IsUsableValue(close_values[i]) || !IsUsableValue(close_values[i - 1]))
         continue;
      double delta = close_values[i] - close_values[i - 1];
      gains[i] = (delta > 0.0 ? delta : 0.0);
      losses[i] = (delta < 0.0 ? -delta : 0.0);
     }

   double avg_gain[];
   double avg_loss[];
   if(!ComputeWilderSmoothSeries(gains, count, period, avg_gain))
      return false;
   if(!ComputeWilderSmoothSeries(losses, count, period, avg_loss))
      return false;

   for(int j = 0; j < count; j++)
     {
      if(!IsUsableValue(avg_gain[j]) || !IsUsableValue(avg_loss[j]))
         continue;
      if(avg_gain[j] == 0.0 && avg_loss[j] == 0.0)
        {
         rsi[j] = 50.0;
         continue;
        }
      double rs = SafeDivide(avg_gain[j], avg_loss[j]);
      if(!IsUsableValue(rs))
         continue;
      rsi[j] = 100.0 - (100.0 / (1.0 + rs));
     }
   return true;
  }

bool ComputeAtrSeries(const MqlRates &rates[], const int count, const int period, double &atr[])
  {
   double tr[];
   if(!ComputeTrueRangeSeries(rates, count, tr))
      return false;
   return ComputeWilderSmoothSeries(tr, count, period, atr);
  }

bool ComputeStochasticSeries(const double &high_values[], const double &low_values[], const double &close_values[], const int count, const int lookback, const int smooth_k, const int smooth_d, double &raw_k[], double &k[], double &d[])
  {
   ArrayResize(raw_k, count);
   ArrayResize(k, count);
   ArrayResize(d, count);
   for(int i = 0; i < count; i++)
     {
      raw_k[i] = EMPTY_VALUE;
      k[i] = EMPTY_VALUE;
      d[i] = EMPTY_VALUE;
     }

   for(int i = lookback - 1; i < count; i++)
     {
      double lowest_low = RollingMinSlice(low_values, i - lookback + 1, lookback);
      double highest_high = RollingMaxSlice(high_values, i - lookback + 1, lookback);
      if(!IsUsableValue(lowest_low) || !IsUsableValue(highest_high))
         continue;
      double denom = highest_high - lowest_low;
      if(denom == 0.0)
         continue;
      raw_k[i] = 100.0 * SafeDivide(close_values[i] - lowest_low, denom);
     }

   if(!ComputeSmaSeries(raw_k, count, smooth_k, k))
      return false;
   if(!ComputeSmaSeries(k, count, smooth_d, d))
      return false;
   return true;
  }

bool ComputeAdxSeries(const MqlRates &rates[], const int count, const int period, double &adx[], double &plus_di[], double &minus_di[])
  {
   ArrayResize(adx, count);
   ArrayResize(plus_di, count);
   ArrayResize(minus_di, count);
   double plus_dm[];
   double minus_dm[];
   ArrayResize(plus_dm, count);
   ArrayResize(minus_dm, count);
   for(int i = 0; i < count; i++)
     {
      adx[i] = EMPTY_VALUE;
      plus_di[i] = EMPTY_VALUE;
      minus_di[i] = EMPTY_VALUE;
      plus_dm[i] = EMPTY_VALUE;
      minus_dm[i] = EMPTY_VALUE;
     }

   for(int i = 1; i < count; i++)
     {
      double up_move = rates[i].high - rates[i - 1].high;
      double down_move = rates[i - 1].low - rates[i].low;
      plus_dm[i] = ((up_move > down_move) && (up_move > 0.0)) ? up_move : 0.0;
      minus_dm[i] = ((down_move > up_move) && (down_move > 0.0)) ? down_move : 0.0;
     }

   double atr[];
   double smooth_plus_dm[];
   double smooth_minus_dm[];
   if(!ComputeAtrSeries(rates, count, period, atr))
      return false;
   if(!ComputeWilderSmoothSeries(plus_dm, count, period, smooth_plus_dm))
      return false;
   if(!ComputeWilderSmoothSeries(minus_dm, count, period, smooth_minus_dm))
      return false;

   double dx[];
   ArrayResize(dx, count);
   for(int j = 0; j < count; j++)
     {
      dx[j] = EMPTY_VALUE;
      if(!IsUsableValue(atr[j]))
         continue;
      plus_di[j] = 100.0 * SafeDivide(smooth_plus_dm[j], atr[j]);
      minus_di[j] = 100.0 * SafeDivide(smooth_minus_dm[j], atr[j]);
      double denom = plus_di[j] + minus_di[j];
      if(!IsUsableValue(plus_di[j]) || !IsUsableValue(minus_di[j]) || denom == 0.0)
         continue;
      dx[j] = 100.0 * MathAbs(plus_di[j] - minus_di[j]) / denom;
     }
   return ComputeWilderSmoothSeries(dx, count, period, adx);
  }

int FindBarIndexByCloseTime(const MqlRates &rates[], const datetime target_close)
  {
   for(int i = 0; i < ArraySize(rates); i++)
     {
      datetime close_time = rates[i].time + PeriodSeconds(InpTimeframe);
      if(close_time == target_close)
         return i;
     }
   return -1;
  }

bool LoadAlignedClosedWindow(const string symbol, const datetime target_close, const int bars_needed, MqlRates &out_rates[], string &error)
  {
   ArrayResize(out_rates, 0);
   if(!SymbolSelect(symbol, true))
     {
      error = "SYMBOL_SELECT_FAIL_" + symbol;
      return false;
     }

   datetime start_open = 0;
   datetime parsed_window_start = 0;
   if(symbol == InpMainSymbol && ParseUtcText(InpWindowStartUtc, parsed_window_start))
      start_open = parsed_window_start - PeriodSeconds(InpTimeframe);
   else
     {
      // Use a wider time span because session gaps and weekends can leave a much
      // smaller bar count than a naive bars_needed * timeframe backstep would imply.
      start_open = target_close - (bars_needed * PeriodSeconds(InpTimeframe) * 12);
     }
   datetime end_open = target_close - PeriodSeconds(InpTimeframe);

   MqlRates loaded[];
   int copied = CopyRates(symbol, InpTimeframe, start_open, end_open, loaded);
   if(copied <= 0)
     {
      error = "RATES_NOT_READY_" + symbol;
      return false;
     }

   ArraySetAsSeries(loaded, false);
   int target_index = FindBarIndexByCloseTime(loaded, target_close);
   if(target_index < 0)
     {
      error = "EXTERNAL_TIMESTAMP_MISMATCH_" + symbol;
      return false;
     }

   if((target_index + 1) < bars_needed)
     {
      error = "WARMUP_INSUFFICIENT_" + symbol;
      return false;
     }

   int start_index = target_index - bars_needed + 1;
   if(symbol == InpMainSymbol && parsed_window_start > 0)
      start_index = 0;

   int out_count = target_index - start_index + 1;
   ArrayResize(out_rates, out_count);
   for(int i = 0; i < out_count; i++)
      out_rates[i] = loaded[start_index + i];

   return true;
  }

double ComputeOvernightReturn(const MqlRates &rates[], const int count, const int target_index, string &error)
  {
   datetime target_close = rates[target_index].time + PeriodSeconds(InpTimeframe);
   datetime target_ny = ToNewYorkTime(target_close);
   MqlDateTime ny_dt;
   TimeToStruct(target_ny, ny_dt);

   double cash_open_today = EMPTY_VALUE;
   int target_date_key = ny_dt.year * 10000 + ny_dt.mon * 100 + ny_dt.day;

   for(int i = 0; i < count; i++)
     {
      datetime close_time = rates[i].time + PeriodSeconds(InpTimeframe);
      datetime ny_time = ToNewYorkTime(close_time);
      MqlDateTime row_dt;
      TimeToStruct(ny_time, row_dt);
      int row_date_key = row_dt.year * 10000 + row_dt.mon * 100 + row_dt.day;
      if(row_date_key == target_date_key && row_dt.hour == 9 && row_dt.min == 35)
        {
         cash_open_today = rates[i].open;
         break;
        }
     }
   if(!IsUsableValue(cash_open_today))
     {
      error = "SESSION_CASH_OPEN_NOT_FOUND";
      return EMPTY_VALUE;
     }

   double prev_cash_close = EMPTY_VALUE;
   datetime best_prev = 0;
   for(int j = 0; j < count; j++)
     {
      datetime close_time = rates[j].time + PeriodSeconds(InpTimeframe);
      datetime ny_time = ToNewYorkTime(close_time);
      MqlDateTime row_dt2;
      TimeToStruct(ny_time, row_dt2);
      int row_date_key2 = row_dt2.year * 10000 + row_dt2.mon * 100 + row_dt2.day;
      if(row_date_key2 >= target_date_key)
         continue;
      if(row_dt2.hour == 16 && row_dt2.min == 0 && close_time > best_prev)
        {
         best_prev = close_time;
         prev_cash_close = rates[j].close;
        }
     }

   if(!IsUsableValue(prev_cash_close))
     {
      error = "SESSION_PREV_CLOSE_NOT_FOUND";
      return EMPTY_VALUE;
     }
   return SafeDivide(cash_open_today, prev_cash_close) - 1.0;
  }

void ComputeSessionValues(const datetime target_close, double &is_us_cash_open, double &minutes_from_cash_open, double &is_first_30m_after_open, double &is_last_30m_before_cash_close)
  {
   datetime ny_time = ToNewYorkTime(target_close);
   MqlDateTime dt;
   TimeToStruct(ny_time, dt);

   int close_minutes = (dt.hour * 60) + dt.min;
   int open_bar_minutes = (9 * 60) + 35;
   int cash_open_minutes = (9 * 60) + 30;
   int cash_close_minutes = (16 * 60);

   is_us_cash_open = (((close_minutes >= open_bar_minutes) && (close_minutes <= cash_close_minutes)) ? 1.0 : 0.0);
   minutes_from_cash_open = (double)(close_minutes - cash_open_minutes);
   is_first_30m_after_open = ((minutes_from_cash_open > 0.0 && minutes_from_cash_open <= 30.0) ? 1.0 : 0.0);
   double minutes_to_cash_close = (double)(cash_close_minutes - close_minutes);
   is_last_30m_before_cash_close = ((minutes_to_cash_close >= 0.0 && minutes_to_cash_close <= 25.0) ? 1.0 : 0.0);
  }

string BuildFeatureJson(const double &features[])
  {
   string out = "[";
   for(int i = 0; i < ArraySize(features); i++)
     {
      if(i > 0)
         out += ",";
      out +=
         "{"
         "\"index\":" + IntegerToString(i) + ","
         "\"name\":" + JsonQuoted(FEATURE_NAMES[i]) + ","
         "\"value\":" + JsonNumber(features[i]) +
         "}";
     }
   out += "]";
   return out;
  }

string BuildExternalAuditJson(const ExternalAuditItem &items[])
  {
   string out = "[";
   for(int i = 0; i < ArraySize(items); i++)
     {
      if(i > 0)
         out += ",";
      out +=
         "{"
         "\"symbol\":" + JsonQuoted(items[i].symbol) + ","
         "\"requested_close_utc\":" + JsonQuoted(items[i].requested_close_utc) + ","
         "\"selected_close_utc\":" + (items[i].selected_close_utc == "" ? "null" : JsonQuoted(items[i].selected_close_utc)) + ","
         "\"status\":" + JsonQuoted(items[i].status) + ","
         "\"fallback_used\":" + JsonBool(items[i].fallback_used) + ","
         "\"stale_bars\":" + IntegerToString(items[i].stale_bars) + ","
         "\"detail\":" + JsonQuoted(items[i].detail) +
         "}";
     }
   out += "]";
   return out;
  }

string BuildSnapshotIdentityJson(const datetime target_close)
  {
   return
      "\"dataset_id\":" + JsonQuoted(InpDatasetId) + ","
      "\"fixture_set_id\":" + JsonQuoted(InpFixtureSetId) + ","
      "\"bundle_id\":" + JsonQuoted(InpBundleId) + ","
      "\"report_id\":" + JsonQuoted(InpReportId) + ","
      "\"runtime_id\":" + JsonQuoted(InpRuntimeId) + ","
      "\"parser_version\":" + JsonQuoted(InpParserVersion) + ","
      "\"parser_contract_version\":" + JsonQuoted(InpParserContractVersion) + ","
      "\"feature_contract_version\":" + JsonQuoted(InpFeatureContractVersion) + ","
      "\"runtime_contract_version\":" + JsonQuoted(InpRuntimeContractVersion) + ","
      "\"feature_order_hash\":" + JsonQuoted(InpFeatureOrderHash) + ","
      "\"window_start_utc\":" + JsonQuoted(CanonicalWindowStartUtc()) + ","
      "\"timestamp_utc\":" + JsonQuoted(FormatUtcIso(target_close)) + ","
      "\"timestamp_america_new_york\":" + JsonQuoted(FormatNewYorkIso(target_close)) + ",";
  }

void FillZeroFeatures(double &features[])
  {
   ArrayResize(features, 58);
   for(int i = 0; i < 58; i++)
      features[i] = 0.0;
  }

bool BuildSnapshotForWindow(const datetime target_close, string &json_line)
  {
   string error = "";
   MqlRates main_rates[];
   if(!LoadAlignedClosedWindow(InpMainSymbol, target_close, InpMainWarmupBars, main_rates, error))
     {
      double zero_features[];
      FillZeroFeatures(zero_features);
      ExternalAuditItem empty_items[];
      ArrayResize(empty_items, 0);
      json_line =
         "{"
         "\"event_timestamp_utc\":" + JsonQuoted(FormatUtc(target_close)) + ","
         "\"bar_time_server\":" + JsonQuoted(FormatUtc(target_close)) + ","
         "\"symbol\":" + JsonQuoted(InpMainSymbol) + ","
         "\"timeframe\":" + JsonQuoted(EnumToString(InpTimeframe)) + ","
         "\"cycle_tag\":\"SNAPSHOT_AUDIT\","
         "\"feature_mode\":\"V2_NATIVE_AUDIT\","
         "\"feature_count\":58,"
         "\"feature_ready_count\":0,"
         "\"feature_vector_complete\":false,"
         "\"row_ready\":false,"
         "\"skip_reason\":" + JsonQuoted(error) + ","
         "\"feature_checksum\":0,"
         "\"feature_fingerprint\":\"fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2\","
         "\"external_inputs\":" + BuildExternalAuditJson(empty_items) + ","
         "\"features\":" + BuildFeatureJson(zero_features) +
         "}";
      return true;
     }

   int count = ArraySize(main_rates);
   int t = count - 1;

   double close_values[];
   double high_values[];
   double low_values[];
   double open_values[];
   double log_return_1_series[];
   double hl_range_series[];
   ArrayResize(close_values, count);
   ArrayResize(high_values, count);
   ArrayResize(low_values, count);
   ArrayResize(open_values, count);
   ArrayResize(log_return_1_series, count);
   ArrayResize(hl_range_series, count);

   for(int i = 0; i < count; i++)
     {
      close_values[i] = main_rates[i].close;
      high_values[i] = main_rates[i].high;
      low_values[i] = main_rates[i].low;
      open_values[i] = main_rates[i].open;
      log_return_1_series[i] = EMPTY_VALUE;
      hl_range_series[i] = EMPTY_VALUE;
      if(main_rates[i].close != 0.0)
         hl_range_series[i] = (main_rates[i].high - main_rates[i].low) / main_rates[i].close;
     }

   for(int j = 1; j < count; j++)
     {
      if(main_rates[j - 1].close > 0.0 && main_rates[j].close > 0.0)
         log_return_1_series[j] = MathLog(main_rates[j].close / main_rates[j - 1].close);
     }

   double atr14[];
   double atr20[];
   double atr50[];
   double ema9[];
   double ema20[];
   double ema50[];
   double ema200[];
   double sma50[];
   double sma200[];
   double rsi14[];
   double rsi50[];
   double raw_k[];
   double stoch_k[];
   double stoch_d[];
   double stochrsi_k[];
   double stochrsi_d[];
   double ppo_hist[];
   double trix15[];
   double adx14[];
   double plus_di14[];
   double minus_di14[];

   if(!ComputeAtrSeries(main_rates, count, 14, atr14) ||
      !ComputeAtrSeries(main_rates, count, 20, atr20) ||
      !ComputeAtrSeries(main_rates, count, 50, atr50) ||
      !ComputeEmaSeries(close_values, count, 9, ema9) ||
      !ComputeEmaSeries(close_values, count, 20, ema20) ||
      !ComputeEmaSeries(close_values, count, 50, ema50) ||
      !ComputeEmaSeries(close_values, count, 200, ema200) ||
      !ComputeSmaSeries(close_values, count, 50, sma50) ||
      !ComputeSmaSeries(close_values, count, 200, sma200) ||
      !ComputeRsiSeries(close_values, count, 14, rsi14) ||
      !ComputeRsiSeries(close_values, count, 50, rsi50) ||
      !ComputeStochasticSeries(high_values, low_values, close_values, count, 14, 3, 3, raw_k, stoch_k, stoch_d) ||
      !ComputeAdxSeries(main_rates, count, 14, adx14, plus_di14, minus_di14))
      return false;

   double stochrsi_raw[];
   ArrayResize(stochrsi_raw, count);
   for(int s = 0; s < count; s++)
      stochrsi_raw[s] = EMPTY_VALUE;
   for(int s2 = 13; s2 < count; s2++)
     {
      double low_rsi = RollingMinSlice(rsi14, s2 - 13, 14);
      double high_rsi = RollingMaxSlice(rsi14, s2 - 13, 14);
      double denom = high_rsi - low_rsi;
      if(!IsUsableValue(low_rsi) || !IsUsableValue(high_rsi) || denom == 0.0)
         continue;
      stochrsi_raw[s2] = 100.0 * SafeDivide(rsi14[s2] - low_rsi, denom);
     }
   if(!ComputeSmaSeries(stochrsi_raw, count, 3, stochrsi_k) || !ComputeSmaSeries(stochrsi_k, count, 3, stochrsi_d))
      return false;

   double ema12[];
   double ema26[];
   double ppo_series[];
   double ppo_signal[];
   if(!ComputeEmaSeries(close_values, count, 12, ema12) || !ComputeEmaSeries(close_values, count, 26, ema26))
      return false;
   ArrayResize(ppo_series, count);
   for(int p = 0; p < count; p++)
     {
      ppo_series[p] = EMPTY_VALUE;
      if(IsUsableValue(ema12[p]) && IsUsableValue(ema26[p]) && ema26[p] != 0.0)
         ppo_series[p] = 100.0 * (ema12[p] - ema26[p]) / ema26[p];
     }
   if(!ComputeEmaSeries(ppo_series, count, 9, ppo_signal))
      return false;
   ArrayResize(ppo_hist, count);
   for(int p2 = 0; p2 < count; p2++)
     {
      ppo_hist[p2] = EMPTY_VALUE;
      if(IsUsableValue(ppo_series[p2]) && IsUsableValue(ppo_signal[p2]))
         ppo_hist[p2] = ppo_series[p2] - ppo_signal[p2];
     }

   double trix_ema1[];
   double trix_ema2[];
   double trix_ema3[];
   if(!ComputeEmaSeries(close_values, count, 15, trix_ema1) ||
      !ComputeEmaSeries(trix_ema1, count, 15, trix_ema2) ||
      !ComputeEmaSeries(trix_ema2, count, 15, trix_ema3))
      return false;
   ArrayResize(trix15, count);
   for(int tr = 0; tr < count; tr++)
     {
      trix15[tr] = EMPTY_VALUE;
      if(tr > 0 && IsUsableValue(trix_ema3[tr]) && IsUsableValue(trix_ema3[tr - 1]) && trix_ema3[tr - 1] != 0.0)
         trix15[tr] = (trix_ema3[tr] / trix_ema3[tr - 1]) - 1.0;
     }

   double true_range[];
   if(!ComputeTrueRangeSeries(main_rates, count, true_range))
      return false;

   double atr10[];
   if(!ComputeAtrSeries(main_rates, count, 10, atr10))
      return false;

   double supertrend_state[];
   double final_upper[];
   double final_lower[];
   ArrayResize(supertrend_state, count);
   ArrayResize(final_upper, count);
   ArrayResize(final_lower, count);
   for(int st = 0; st < count; st++)
     {
      supertrend_state[st] = EMPTY_VALUE;
      final_upper[st] = EMPTY_VALUE;
      final_lower[st] = EMPTY_VALUE;
     }

   for(int st2 = 1; st2 < count; st2++)
     {
      if(!IsUsableValue(atr10[st2]))
         continue;
      double hl2 = (main_rates[st2].high + main_rates[st2].low) / 2.0;
      double basic_upper = hl2 + (3.0 * atr10[st2]);
      double basic_lower = hl2 - (3.0 * atr10[st2]);
      if(!IsUsableValue(supertrend_state[st2 - 1]))
        {
         final_upper[st2] = basic_upper;
         final_lower[st2] = basic_lower;
         supertrend_state[st2] = (main_rates[st2].close >= basic_lower ? 1.0 : -1.0);
        }
      else
        {
         final_upper[st2] = (basic_upper < final_upper[st2 - 1] || main_rates[st2 - 1].close > final_upper[st2 - 1]) ? basic_upper : final_upper[st2 - 1];
         final_lower[st2] = (basic_lower > final_lower[st2 - 1] || main_rates[st2 - 1].close < final_lower[st2 - 1]) ? basic_lower : final_lower[st2 - 1];
         if(supertrend_state[st2 - 1] == 1.0)
            supertrend_state[st2] = (main_rates[st2].close < final_lower[st2] ? -1.0 : 1.0);
         else
            supertrend_state[st2] = (main_rates[st2].close > final_upper[st2] ? 1.0 : -1.0);
        }
     }

   double vortex_indicator[];
   double vm_plus[];
   double vm_minus[];
   ArrayResize(vortex_indicator, count);
   ArrayResize(vm_plus, count);
   ArrayResize(vm_minus, count);
   for(int vm = 0; vm < count; vm++)
     {
      vortex_indicator[vm] = EMPTY_VALUE;
      vm_plus[vm] = EMPTY_VALUE;
      vm_minus[vm] = EMPTY_VALUE;
      if(vm == 0)
         continue;
      vm_plus[vm] = MathAbs(main_rates[vm].high - main_rates[vm - 1].low);
      vm_minus[vm] = MathAbs(main_rates[vm].low - main_rates[vm - 1].high);
      if(vm >= 13)
        {
         double tr_sum = RollingSumSlice(true_range, vm - 13, 14);
         double plus_sum = RollingSumSlice(vm_plus, vm - 13, 14);
         double minus_sum = RollingSumSlice(vm_minus, vm - 13, 14);
         if(IsUsableValue(tr_sum) && tr_sum != 0.0 && IsUsableValue(plus_sum) && IsUsableValue(minus_sum))
            vortex_indicator[vm] = (plus_sum / tr_sum) - (minus_sum / tr_sum);
        }
     }

   double is_us_cash_open = 0.0;
   double minutes_from_cash_open = 0.0;
   double is_first_30m_after_open = 0.0;
   double is_last_30m_before_cash_close = 0.0;
   ComputeSessionValues(target_close, is_us_cash_open, minutes_from_cash_open, is_first_30m_after_open, is_last_30m_before_cash_close);

   double overnight_return = ComputeOvernightReturn(main_rates, count, t, error);
   if(!IsUsableValue(overnight_return) && error == "")
      error = "SESSION_OVERNIGHT_NOT_READY";

   double external_values[16];
   for(int ev = 0; ev < 16; ev++)
      external_values[ev] = EMPTY_VALUE;

   ExternalAuditItem audit_items[];
   ArrayResize(audit_items, 0);

   string proxy_symbols[3] = {"VIX", "US10YR", "USDX"};
   for(int proxy = 0; proxy < 3; proxy++)
     {
      MqlRates proxy_rates[];
      string proxy_error = "";
      if(!LoadAlignedClosedWindow(proxy_symbols[proxy], target_close, InpExternalWarmupBars, proxy_rates, proxy_error))
        {
         int slot_fail = ArraySize(audit_items);
         ArrayResize(audit_items, slot_fail + 1);
         audit_items[slot_fail].symbol = proxy_symbols[proxy];
         audit_items[slot_fail].requested_close_utc = FormatUtc(target_close);
         audit_items[slot_fail].selected_close_utc = "";
         audit_items[slot_fail].status = "timestamp_mismatch";
         audit_items[slot_fail].fallback_used = false;
         audit_items[slot_fail].stale_bars = 0;
         audit_items[slot_fail].detail = proxy_error;
         if(error == "")
            error = proxy_error;
         continue;
        }

      int slot = ArraySize(audit_items);
      ArrayResize(audit_items, slot + 1);
      audit_items[slot].symbol = proxy_symbols[proxy];
      audit_items[slot].requested_close_utc = FormatUtc(target_close);
      audit_items[slot].selected_close_utc = FormatUtc(target_close);
      audit_items[slot].status = "exact_match";
      audit_items[slot].fallback_used = false;
      audit_items[slot].stale_bars = 0;
      audit_items[slot].detail = "";

      int pt = ArraySize(proxy_rates) - 1;
      double proxy_close_values[];
      ArrayResize(proxy_close_values, ArraySize(proxy_rates));
      for(int pidx = 0; pidx < ArraySize(proxy_rates); pidx++)
         proxy_close_values[pidx] = proxy_rates[pidx].close;

      double change_1 = SafeDivide(proxy_rates[pt].close, proxy_rates[pt - 1].close) - 1.0;
      double zscore_20 = RollingZscoreCurrent(proxy_close_values, ArraySize(proxy_rates), 20);
      if(proxy == 0)
        {
         external_values[0] = change_1;
         external_values[1] = zscore_20;
        }
      else if(proxy == 1)
        {
         external_values[2] = change_1;
         external_values[3] = zscore_20;
        }
      else
        {
         external_values[4] = change_1;
         external_values[5] = zscore_20;
        }
     }

   double mega8_return_1[8];
   double mega8_return_5[8];
   int positive_count = 0;
   for(int stock = 0; stock < 8; stock++)
     {
      mega8_return_1[stock] = EMPTY_VALUE;
      mega8_return_5[stock] = EMPTY_VALUE;

      MqlRates stock_rates[];
      string stock_error = "";
      if(!LoadAlignedClosedWindow(g_stock_symbols[stock], target_close, InpExternalWarmupBars, stock_rates, stock_error))
        {
         int slot_fail2 = ArraySize(audit_items);
         ArrayResize(audit_items, slot_fail2 + 1);
         audit_items[slot_fail2].symbol = g_stock_symbols[stock];
         audit_items[slot_fail2].requested_close_utc = FormatUtc(target_close);
         audit_items[slot_fail2].selected_close_utc = "";
         audit_items[slot_fail2].status = "timestamp_mismatch";
         audit_items[slot_fail2].fallback_used = false;
         audit_items[slot_fail2].stale_bars = 0;
         audit_items[slot_fail2].detail = stock_error;
         if(error == "")
            error = stock_error;
         continue;
        }

      int slot2 = ArraySize(audit_items);
      ArrayResize(audit_items, slot2 + 1);
      audit_items[slot2].symbol = g_stock_symbols[stock];
      audit_items[slot2].requested_close_utc = FormatUtc(target_close);
      audit_items[slot2].selected_close_utc = FormatUtc(target_close);
      audit_items[slot2].status = "exact_match";
      audit_items[slot2].fallback_used = false;
      audit_items[slot2].stale_bars = 0;
      audit_items[slot2].detail = "";

      int stt = ArraySize(stock_rates) - 1;
      mega8_return_1[stock] = SafeDivide(stock_rates[stt].close, stock_rates[stt - 1].close) - 1.0;
      mega8_return_5[stock] = SafeDivide(stock_rates[stt].close, stock_rates[stt - 5].close) - 1.0;
      if(mega8_return_1[stock] > 0.0)
         positive_count++;

      double log_return_1 = MathLog(stock_rates[stt].close / stock_rates[stt - 1].close);
      if(g_stock_symbols[stock] == "NVDA.xnas")
         external_values[6] = log_return_1;
      else if(g_stock_symbols[stock] == "AAPL.xnas")
         external_values[7] = log_return_1;
      else if(g_stock_symbols[stock] == "MSFT.xnas")
         external_values[8] = log_return_1;
      else if(g_stock_symbols[stock] == "AMZN.xnas")
         external_values[9] = log_return_1;
     }

   double mega8_equal = RollingMeanSlice(mega8_return_1, 0, 8);
   double top3_weighted = EMPTY_VALUE;
   if(IsUsableValue(mega8_return_1[5]) && IsUsableValue(mega8_return_1[6]) && IsUsableValue(mega8_return_1[0]))
      top3_weighted = (mega8_return_1[5] * g_top3_equal_weight) + (mega8_return_1[6] * g_top3_equal_weight) + (mega8_return_1[0] * g_top3_equal_weight);
   double mega8_breadth = (double)positive_count / 8.0;
   double mega8_dispersion = PopulationStdSlice(mega8_return_5, 0, 8);

   external_values[10] = mega8_equal;
   external_values[11] = top3_weighted;
   external_values[12] = mega8_breadth;
   external_values[13] = mega8_dispersion;

   double us100_simple_return_1 = SafeDivide(main_rates[t].close, main_rates[t - 1].close) - 1.0;
   external_values[14] = us100_simple_return_1 - mega8_equal;
   external_values[15] = us100_simple_return_1 - top3_weighted;

   double features[];
   FillZeroFeatures(features);
   features[0] = log_return_1_series[t];
   features[1] = MathLog(main_rates[t].close / main_rates[t - 3].close);
   features[2] = hl_range_series[t];
   features[3] = SafeDivide(main_rates[t].close, main_rates[t].open);
   features[4] = SafeDivide(main_rates[t].open, main_rates[t - 1].close) - 1.0;
   features[5] = SafeDivide(main_rates[t].close, main_rates[t - 1].close);
   features[6] = RollingZscoreCurrent(log_return_1_series, count, 20);
   features[7] = RollingZscoreCurrent(hl_range_series, count, 50);
   features[8] = overnight_return;
   features[9] = SafeDivide(us100_simple_return_1, SafeDivide(atr14[t], main_rates[t].close));
   features[10] = SafeDivide(main_rates[t].close, ema20[t]);
   features[11] = SafeDivide(main_rates[t].close, ema50[t]);
   features[12] = ema9[t] - ema20[t];
   features[13] = ema20[t] - ema50[t];
   features[14] = ema50[t] - ema200[t];

   double ema20_ema50_diff_values[];
   ArrayResize(ema20_ema50_diff_values, count);
   for(int zz = 0; zz < count; zz++)
      ema20_ema50_diff_values[zz] = (IsUsableValue(ema20[zz]) && IsUsableValue(ema50[zz])) ? (ema20[zz] - ema50[zz]) : EMPTY_VALUE;
   features[15] = RollingZscoreCurrent(ema20_ema50_diff_values, count, 50);
   features[16] = SafeDivide(sma50[t], sma200[t]);
   features[17] = rsi14[t];
   features[18] = rsi50[t];
   features[19] = (IsUsableValue(rsi14[t]) && IsUsableValue(rsi14[t - 3])) ? (rsi14[t] - rsi14[t - 3]) / 3.0 : EMPTY_VALUE;
   features[20] = IsUsableValue(rsi14[t]) ? (rsi14[t] - 50.0) : EMPTY_VALUE;
   features[21] = stoch_k[t] - stoch_d[t];
   features[22] = stochrsi_k[t] - stochrsi_d[t];
   features[23] = ppo_hist[t];
   features[24] = SafeDivide(main_rates[t].close, main_rates[t - 12].close) - 1.0;
   features[25] = trix15[t];
   features[26] = atr14[t];
   features[27] = atr50[t];
   features[28] = SafeDivide(atr14[t], atr50[t]);

   double bb_mid = RollingMeanSlice(close_values, count - 20, 20);
   double bb_std = PopulationStdSlice(close_values, count - 20, 20);
   double bb_upper = (IsUsableValue(bb_mid) && IsUsableValue(bb_std)) ? (bb_mid + 2.0 * bb_std) : EMPTY_VALUE;
   double bb_lower = (IsUsableValue(bb_mid) && IsUsableValue(bb_std)) ? (bb_mid - 2.0 * bb_std) : EMPTY_VALUE;
   double kc_upper = (IsUsableValue(ema20[t]) && IsUsableValue(atr20[t])) ? (ema20[t] + (1.5 * atr20[t])) : EMPTY_VALUE;
   double kc_lower = (IsUsableValue(ema20[t]) && IsUsableValue(atr20[t])) ? (ema20[t] - (1.5 * atr20[t])) : EMPTY_VALUE;
   features[29] = SafeDivide(bb_upper - bb_lower, bb_mid);
   features[30] = SafeDivide(main_rates[t].close - bb_lower, bb_upper - bb_lower);
   features[31] = ((IsUsableValue(bb_upper) && IsUsableValue(kc_upper) && IsUsableValue(bb_lower) && IsUsableValue(kc_lower) && bb_upper <= kc_upper && bb_lower >= kc_lower) ? 1.0 : 0.0);

   double hv20 = PopulationStdSlice(log_return_1_series, count - 20, 20);
   double hv5 = PopulationStdSlice(log_return_1_series, count - 5, 5);
   if(IsUsableValue(hv20))
      features[32] = hv20 * MathSqrt(252.0 * 288.0);
   if(IsUsableValue(hv5) && IsUsableValue(features[32]) && features[32] != 0.0)
      features[33] = (hv5 * MathSqrt(252.0 * 288.0)) / features[32];

   features[34] = adx14[t];
   features[35] = plus_di14[t] - minus_di14[t];
   features[36] = supertrend_state[t];
   features[37] = vortex_indicator[t];
   features[38] = is_us_cash_open;
   features[39] = minutes_from_cash_open;
   features[40] = is_first_30m_after_open;
   features[41] = is_last_30m_before_cash_close;
   features[42] = external_values[0];
   features[43] = external_values[1];
   features[44] = external_values[2];
   features[45] = external_values[3];
   features[46] = external_values[4];
   features[47] = external_values[5];
   features[48] = external_values[6];
   features[49] = external_values[7];
   features[50] = external_values[8];
   features[51] = external_values[9];
   features[52] = external_values[10];
   features[53] = external_values[11];
   features[54] = external_values[12];
   features[55] = external_values[13];
   features[56] = external_values[14];
   features[57] = external_values[15];

   bool row_ready = (error == "");
   if(row_ready)
     {
      for(int fv = 0; fv < 58; fv++)
        {
         if(!IsUsableValue(features[fv]))
           {
            row_ready = false;
            error = "NUMERIC_INVALID_" + FEATURE_NAMES[fv];
            break;
           }
        }
     }

   if(!row_ready)
      FillZeroFeatures(features);

   json_line =
      "{" +
      BuildSnapshotIdentityJson(target_close) +
      "\"event_timestamp_utc\":" + JsonQuoted(FormatUtc(target_close)) + ","
      "\"bar_time_server\":" + JsonQuoted(FormatUtc(target_close)) + ","
      "\"symbol\":" + JsonQuoted(InpMainSymbol) + ","
      "\"timeframe\":" + JsonQuoted(EnumToString(InpTimeframe)) + ","
      "\"cycle_tag\":\"SNAPSHOT_AUDIT\","
      "\"feature_mode\":\"V2_NATIVE_AUDIT\","
      "\"feature_count\":58,"
      "\"feature_ready_count\":" + IntegerToString(row_ready ? 58 : 0) + ","
      "\"feature_vector_complete\":" + JsonBool(row_ready) + ","
      "\"row_ready\":" + JsonBool(row_ready) + ","
      "\"skip_reason\":" + JsonQuoted(error) + ","
      "\"feature_checksum\":0,"
      "\"feature_fingerprint\":" + JsonQuoted(InpFeatureOrderHash) + ","
      "\"external_inputs\":" + BuildExternalAuditJson(audit_items) + ","
      "\"features\":" + BuildFeatureJson(features) +
      "}";

   return true;
  }

bool ResetOutputFile()
  {
   int flags = FILE_WRITE | FILE_TXT | FILE_ANSI;
   if(InpOutputUseCommonFiles)
      flags |= FILE_COMMON;
   int handle = FileOpen(InpOutputPath, flags);
   if(handle == INVALID_HANDLE)
      return false;
   FileClose(handle);
   return true;
  }

bool AppendLine(const string line)
  {
   int flags = FILE_READ | FILE_WRITE | FILE_TXT | FILE_ANSI;
   if(InpOutputUseCommonFiles)
      flags |= FILE_COMMON;
   int handle = FileOpen(InpOutputPath, flags);
   if(handle == INVALID_HANDLE)
      return false;
   FileSeek(handle, 0, SEEK_END);
   FileWriteString(handle, line + "\r\n");
   FileClose(handle);
   return true;
  }

void OnStart()
  {
   datetime windows[];
   if(!BuildTargetWindows(windows))
     {
      Print("No usable target windows were parsed.");
      return;
     }

   if(!ResetOutputFile())
     {
      Print("Failed to reset output file: ", InpOutputPath);
      return;
     }

   int written = 0;
   for(int i = 0; i < ArraySize(windows); i++)
     {
      string line = "";
      if(!BuildSnapshotForWindow(windows[i], line))
        {
         Print("Failed to build snapshot for ", FormatUtc(windows[i]));
         continue;
        }
      if(!AppendLine(line))
        {
         Print("Failed to append audit line for ", FormatUtc(windows[i]));
         continue;
        }
      written++;
     }

   Print("ObsidianPrimeV2_RuntimeParityAudit wrote ", written, " line(s) to ", InpOutputPath);
  }
