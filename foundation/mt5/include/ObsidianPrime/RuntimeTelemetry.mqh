#ifndef OBSIDIAN_PRIME_RUNTIME_TELEMETRY_MQH
#define OBSIDIAN_PRIME_RUNTIME_TELEMETRY_MQH

class COpRuntimeTelemetry
  {
private:
   bool   m_enabled;
   bool   m_common_files;
   string m_run_id;
   string m_model_id;
   string m_feature_order_hash;
   string m_telemetry_path;
   string m_summary_path;
   long   m_ticks_seen;
   long   m_bars_seen;
   long   m_feature_ready_count;
   long   m_feature_skip_count;
   long   m_model_ok_count;
   long   m_model_fail_count;
   long   m_tier_a_used_count;
   long   m_tier_b_fallback_used_count;
   long   m_no_tier_count;
   long   m_tier_a_long_count;
   long   m_tier_a_short_count;
   long   m_tier_a_flat_count;
   long   m_tier_a_order_attempt_count;
   long   m_tier_a_order_fill_count;
   long   m_tier_b_fallback_long_count;
   long   m_tier_b_fallback_short_count;
   long   m_tier_b_fallback_flat_count;
   long   m_tier_b_fallback_order_attempt_count;
   long   m_tier_b_fallback_order_fill_count;
   long   m_long_count;
   long   m_short_count;
   long   m_flat_count;
   long   m_order_attempt_count;
   long   m_order_fill_count;
   string m_last_skip_reason;

   string CleanPath(const string path)
     {
      string clean = path;
      StringReplace(clean, "/", "\\");
      return clean;
     }

   string Csv(const string value)
     {
      string text = value;
      bool needs_quote = (StringFind(text, ",") >= 0 ||
                          StringFind(text, "\"") >= 0 ||
                          StringFind(text, "\r") >= 0 ||
                          StringFind(text, "\n") >= 0);
      StringReplace(text, "\"", "\"\"");
      if(needs_quote)
         return "\"" + text + "\"";
      return text;
     }

   string Dbl(const double value)
     {
      if(!MathIsValidNumber(value) || MathAbs(value) >= (EMPTY_VALUE / 2.0))
         return "";
      return DoubleToString(value, 10);
     }

   string BoolText(const bool value)
     {
      return value ? "true" : "false";
     }

   void EnsureParentFolders(const string path)
     {
      string clean = CleanPath(path);
      int last_slash = -1;
      const int n = StringLen(clean);
      for(int i = 0; i < n; i++)
        {
         if(StringGetCharacter(clean, i) == '\\')
            last_slash = i;
        }

      if(last_slash <= 0)
         return;

      const string folder = StringSubstr(clean, 0, last_slash);
      string parts[];
      const int count = StringSplit(folder, '\\', parts);
      string current = "";
      const int common_flag = m_common_files ? FILE_COMMON : 0;
      for(int p = 0; p < count; p++)
        {
         const string part = parts[p];
         if(part == "")
            continue;

         if(current == "")
            current = part;
         else
            current = current + "\\" + part;

         ResetLastError();
         FolderCreate(current, common_flag);
        }
     }

   bool AppendLine(const string path,
                   const string header,
                   const string line,
                   string &reason)
     {
      reason = "";
      if(!m_enabled || path == "")
         return true;

      const string clean = CleanPath(path);
      EnsureParentFolders(clean);

      int flags = FILE_READ | FILE_WRITE | FILE_TXT | FILE_ANSI;
      if(m_common_files)
         flags |= FILE_COMMON;

      ResetLastError();
      int handle = FileOpen(clean, flags);
      if(handle == INVALID_HANDLE)
        {
         flags = FILE_WRITE | FILE_TXT | FILE_ANSI;
         if(m_common_files)
            flags |= FILE_COMMON;
         ResetLastError();
         handle = FileOpen(clean, flags);
        }

      if(handle == INVALID_HANDLE)
        {
         reason = StringFormat("telemetry_open_failed:%d", GetLastError());
         return false;
        }

      const bool write_header = (FileSize(handle) == 0);
      FileSeek(handle, 0, SEEK_END);
      if(write_header && header != "")
         FileWriteString(handle, header + "\r\n");
      FileWriteString(handle, line + "\r\n");
      FileClose(handle);
      return true;
     }

public:
   COpRuntimeTelemetry()
     {
      m_enabled = true;
      m_common_files = true;
      m_run_id = "";
      m_model_id = "";
      m_feature_order_hash = "";
      m_telemetry_path = "";
      m_summary_path = "";
      ResetCounters();
     }

   void ResetCounters()
     {
      m_ticks_seen = 0;
      m_bars_seen = 0;
      m_feature_ready_count = 0;
      m_feature_skip_count = 0;
      m_model_ok_count = 0;
      m_model_fail_count = 0;
      m_tier_a_used_count = 0;
      m_tier_b_fallback_used_count = 0;
      m_no_tier_count = 0;
      m_tier_a_long_count = 0;
      m_tier_a_short_count = 0;
      m_tier_a_flat_count = 0;
      m_tier_a_order_attempt_count = 0;
      m_tier_a_order_fill_count = 0;
      m_tier_b_fallback_long_count = 0;
      m_tier_b_fallback_short_count = 0;
      m_tier_b_fallback_flat_count = 0;
      m_tier_b_fallback_order_attempt_count = 0;
      m_tier_b_fallback_order_fill_count = 0;
      m_long_count = 0;
      m_short_count = 0;
      m_flat_count = 0;
      m_order_attempt_count = 0;
      m_order_fill_count = 0;
      m_last_skip_reason = "";
     }

   void Configure(const bool enabled,
                  const bool common_files,
                  const string run_id,
                  const string model_id,
                  const string feature_order_hash,
                  const string telemetry_path,
                  const string summary_path)
     {
      m_enabled = enabled;
      m_common_files = common_files;
      m_run_id = run_id;
      m_model_id = model_id;
      m_feature_order_hash = feature_order_hash;
      m_telemetry_path = telemetry_path;
      m_summary_path = summary_path;
      ResetCounters();
     }

   void CountTick()
     {
      m_ticks_seen++;
     }

   bool RecordLifecycle(const string event_name,
                        const string detail,
                        string &reason)
     {
      const string header = "record_type,written_at,run_id,active_tier,model_id,feature_order_hash,bar_time,source_time,symbol,timeframe,feature_ready,model_ok,skip_reason,input_hash,p_short,p_flat,p_long,decision,decision_reason,position_before,position_after,exec_action,order_attempted,order_filled,trade_retcode,trade_comment,event,detail";
      const string line = Csv("lifecycle") + "," +
                          Csv(TimeToString(TimeCurrent(), TIME_DATE | TIME_SECONDS)) + "," +
                          Csv(m_run_id) + "," +
                          "," +
                          Csv(m_model_id) + "," +
                          Csv(m_feature_order_hash) + "," +
                          ",,,,,,,,,,,,,,,,,,,,," +
                          Csv(event_name) + "," +
                          Csv(detail);
      return AppendLine(m_telemetry_path, header, line, reason);
     }

   bool RecordCycle(const datetime bar_time,
                    const string active_tier,
                    const string cycle_model_id,
                    const string cycle_feature_order_hash,
                    const string source_time,
                    const string symbol,
                    const string timeframe,
                    const bool feature_ready,
                    const bool model_ok,
                    const string skip_reason,
                    const string input_hash,
                    const double p_short,
                    const double p_flat,
                    const double p_long,
                    const string decision,
                    const string decision_reason,
                    const string position_before,
                    const string position_after,
                    const string exec_action,
                    const bool order_attempted,
                    const bool order_filled,
                    const uint trade_retcode,
                    const string trade_comment,
                    string &reason)
     {
      m_bars_seen++;
      if(feature_ready)
         m_feature_ready_count++;
      else
         m_feature_skip_count++;

      if(model_ok)
         m_model_ok_count++;
      else
         m_model_fail_count++;

      if(active_tier == "tier_a")
         m_tier_a_used_count++;
      else if(active_tier == "tier_b_fallback")
         m_tier_b_fallback_used_count++;
      else
         m_no_tier_count++;

      if(decision == "long")
         m_long_count++;
      else if(decision == "short")
         m_short_count++;
      else
         m_flat_count++;

      if(active_tier == "tier_a")
        {
         if(decision == "long")
            m_tier_a_long_count++;
         else if(decision == "short")
            m_tier_a_short_count++;
         else
            m_tier_a_flat_count++;
         if(order_attempted)
            m_tier_a_order_attempt_count++;
         if(order_filled)
            m_tier_a_order_fill_count++;
        }
      else if(active_tier == "tier_b_fallback")
        {
         if(decision == "long")
            m_tier_b_fallback_long_count++;
         else if(decision == "short")
            m_tier_b_fallback_short_count++;
         else
            m_tier_b_fallback_flat_count++;
         if(order_attempted)
            m_tier_b_fallback_order_attempt_count++;
         if(order_filled)
            m_tier_b_fallback_order_fill_count++;
        }

      if(order_attempted)
         m_order_attempt_count++;
      if(order_filled)
         m_order_fill_count++;
      if(skip_reason != "")
         m_last_skip_reason = skip_reason;

      if(!feature_ready && StringFind(skip_reason, "feature_csv_timestamp_not_found") == 0)
         return true;

      const string header = "record_type,written_at,run_id,active_tier,model_id,feature_order_hash,bar_time,source_time,symbol,timeframe,feature_ready,model_ok,skip_reason,input_hash,p_short,p_flat,p_long,decision,decision_reason,position_before,position_after,exec_action,order_attempted,order_filled,trade_retcode,trade_comment,event,detail";
      const string line = Csv("cycle") + "," +
                          Csv(TimeToString(TimeCurrent(), TIME_DATE | TIME_SECONDS)) + "," +
                          Csv(m_run_id) + "," +
                          Csv(active_tier) + "," +
                          Csv(cycle_model_id == "" ? m_model_id : cycle_model_id) + "," +
                          Csv(cycle_feature_order_hash == "" ? m_feature_order_hash : cycle_feature_order_hash) + "," +
                          Csv(TimeToString(bar_time, TIME_DATE | TIME_SECONDS)) + "," +
                          Csv(source_time) + "," +
                          Csv(symbol) + "," +
                          Csv(timeframe) + "," +
                          Csv(BoolText(feature_ready)) + "," +
                          Csv(BoolText(model_ok)) + "," +
                          Csv(skip_reason) + "," +
                          Csv(input_hash) + "," +
                          Csv(Dbl(p_short)) + "," +
                          Csv(Dbl(p_flat)) + "," +
                          Csv(Dbl(p_long)) + "," +
                          Csv(decision) + "," +
                          Csv(decision_reason) + "," +
                          Csv(position_before) + "," +
                          Csv(position_after) + "," +
                          Csv(exec_action) + "," +
                          Csv(BoolText(order_attempted)) + "," +
                          Csv(BoolText(order_filled)) + "," +
                          Csv((string)trade_retcode) + "," +
                          Csv(trade_comment) + ",,";

      return AppendLine(m_telemetry_path, header, line, reason);
     }

   bool WriteSummary(const string deinit_reason, string &reason)
     {
      const string header = "written_at,run_id,model_id,feature_order_hash,ticks_seen,bars_seen,feature_ready_count,feature_skip_count,model_ok_count,model_fail_count,tier_a_used_count,tier_b_fallback_used_count,no_tier_count,tier_a_long_count,tier_a_short_count,tier_a_flat_count,tier_a_order_attempt_count,tier_a_order_fill_count,tier_b_fallback_long_count,tier_b_fallback_short_count,tier_b_fallback_flat_count,tier_b_fallback_order_attempt_count,tier_b_fallback_order_fill_count,long_count,short_count,flat_count,order_attempt_count,order_fill_count,last_skip_reason,deinit_reason";
      const string line = Csv(TimeToString(TimeCurrent(), TIME_DATE | TIME_SECONDS)) + "," +
                          Csv(m_run_id) + "," +
                          Csv(m_model_id) + "," +
                          Csv(m_feature_order_hash) + "," +
                          Csv((string)m_ticks_seen) + "," +
                          Csv((string)m_bars_seen) + "," +
                          Csv((string)m_feature_ready_count) + "," +
                          Csv((string)m_feature_skip_count) + "," +
                          Csv((string)m_model_ok_count) + "," +
                          Csv((string)m_model_fail_count) + "," +
                          Csv((string)m_tier_a_used_count) + "," +
                          Csv((string)m_tier_b_fallback_used_count) + "," +
                          Csv((string)m_no_tier_count) + "," +
                          Csv((string)m_tier_a_long_count) + "," +
                          Csv((string)m_tier_a_short_count) + "," +
                          Csv((string)m_tier_a_flat_count) + "," +
                          Csv((string)m_tier_a_order_attempt_count) + "," +
                          Csv((string)m_tier_a_order_fill_count) + "," +
                          Csv((string)m_tier_b_fallback_long_count) + "," +
                          Csv((string)m_tier_b_fallback_short_count) + "," +
                          Csv((string)m_tier_b_fallback_flat_count) + "," +
                          Csv((string)m_tier_b_fallback_order_attempt_count) + "," +
                          Csv((string)m_tier_b_fallback_order_fill_count) + "," +
                          Csv((string)m_long_count) + "," +
                          Csv((string)m_short_count) + "," +
                          Csv((string)m_flat_count) + "," +
                          Csv((string)m_order_attempt_count) + "," +
                          Csv((string)m_order_fill_count) + "," +
                          Csv(m_last_skip_reason) + "," +
                          Csv(deinit_reason);
      return AppendLine(m_summary_path, header, line, reason);
     }
  };

#endif
