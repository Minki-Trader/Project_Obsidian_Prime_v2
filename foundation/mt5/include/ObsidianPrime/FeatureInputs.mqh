#ifndef OBSIDIAN_PRIME_FEATURE_INPUTS_MQH
#define OBSIDIAN_PRIME_FEATURE_INPUTS_MQH

#define OP_DEFAULT_FEATURE_COUNT 58

string OP_Trim(const string value)
  {
   string text = value;
   StringTrimLeft(text);
   StringTrimRight(text);
   return text;
  }

string OP_Unquote(const string value)
  {
   string text = OP_Trim(value);
   const int n = StringLen(text);
   if(n >= 2 && StringGetCharacter(text, 0) == '"' && StringGetCharacter(text, n - 1) == '"')
      text = StringSubstr(text, 1, n - 2);
   StringReplace(text, "\"\"", "\"");
   return OP_Trim(text);
  }

string OP_Lower(const string value)
  {
   string text = value;
   StringToLower(text);
   return text;
  }

bool OP_IsFiniteDouble(const double value)
  {
   return (MathIsValidNumber(value) && MathAbs(value) < (EMPTY_VALUE / 2.0));
  }

bool OP_IsTimestampColumn(const string raw_name)
  {
   const string name = OP_Lower(OP_Unquote(raw_name));
   return (name == "time" ||
           name == "datetime" ||
           name == "timestamp" ||
           name == "timestamp_utc" ||
           name == "bar_time" ||
           name == "bar_time_server" ||
           name == "time_close" ||
           name == "time_close_utc" ||
           name == "bar_close_time" ||
           name == "bar_close_utc");
  }

bool OP_IsMetadataColumn(const string raw_name)
  {
   const string name = OP_Lower(OP_Unquote(raw_name));
   return (OP_IsTimestampColumn(name) ||
           name == "split" ||
            name == "row_index" ||
            name == "tier" ||
            name == "tier_label" ||
            name == "route_role" ||
            name == "partial_context_subtype" ||
            name == "missing_feature_group_mask" ||
            name == "available_feature_group_mask" ||
            name == "dataset_id" ||
            name == "run_id");
  }

bool OP_TokenLooksInvalidNumber(const string token)
  {
   const string text = OP_Lower(OP_Unquote(token));
   return (text == "" ||
           text == "nan" ||
           text == "inf" ||
           text == "+inf" ||
           text == "-inf" ||
           text == "infinity" ||
           text == "null" ||
           text == "none");
  }

datetime OP_ParseTimestamp(const string raw_value)
  {
   string text = OP_Unquote(raw_value);
   if(text == "")
      return 0;

   const long maybe_unix = StringToInteger(text);
   if(maybe_unix > 1000000000)
      return (datetime)maybe_unix;

   StringReplace(text, "T", " ");
   if(StringLen(text) > 0 && StringGetCharacter(text, StringLen(text) - 1) == 'Z')
      text = StringSubstr(text, 0, StringLen(text) - 1);

   const int space_pos = StringFind(text, " ");
   if(space_pos > 0)
     {
      const int plus_pos = StringFind(text, "+", space_pos);
      if(plus_pos > 0)
         text = StringSubstr(text, 0, plus_pos);
      else
        {
         const int zone_minus_pos = StringFind(text, "-", space_pos);
         if(zone_minus_pos > 0)
            text = StringSubstr(text, 0, zone_minus_pos);
        }
     }

   StringReplace(text, "-", ".");
   text = OP_Trim(text);
   return StringToTime(text);
  }

string OP_TimestampText(const datetime value)
  {
   if(value <= 0)
      return "";
   return TimeToString(value, TIME_DATE | TIME_SECONDS);
  }

string OP_CsvInputHash(const string line)
  {
   ulong hash = 1469598103934665603;
   const int n = StringLen(line);
   for(int i = 0; i < n; i++)
      hash = (hash ^ (ulong)StringGetCharacter(line, i)) * 1099511628211;
   return StringFormat("%I64X", hash);
  }

class COpFeatureCsvInput
  {
private:
   string   m_path;
   bool     m_common_files;
   bool     m_require_timestamp_match;
   bool     m_allow_latest_fallback;
   bool     m_strict_header;
   ushort   m_delimiter;
   int      m_feature_count;
   bool     m_loaded;
   string   m_load_reason;
   int      m_last_index;
   datetime m_times[];
   string   m_hashes[];
   double   m_values[];

   int EffectiveFeatureCount()
     {
      if(m_feature_count > 0)
         return m_feature_count;
      return OP_DEFAULT_FEATURE_COUNT;
     }

   void ResetCache()
     {
      m_loaded = false;
      m_load_reason = "";
      m_last_index = 0;
      ArrayResize(m_times, 0);
      ArrayResize(m_hashes, 0);
      ArrayResize(m_values, 0);
     }

   void FillDefaultColumns(const int column_count, int &timestamp_col, int &feature_cols[])
     {
      const int feature_count = EffectiveFeatureCount();
      ArrayResize(feature_cols, feature_count);
      ArrayInitialize(feature_cols, -1);

      timestamp_col = -1;
      int offset = 0;
      if(column_count >= feature_count + 1)
        {
         timestamp_col = 0;
         offset = 1;
        }

      for(int i = 0; i < feature_count; i++)
         feature_cols[i] = i + offset;
     }

   bool LooksLikeHeader(const string &cols[])
     {
      const int column_count = ArraySize(cols);
      int non_numeric = 0;
      for(int c = 0; c < column_count; c++)
        {
         const string token = OP_Unquote(cols[c]);
         if(OP_IsMetadataColumn(token))
            return true;

         const double numeric_value = StringToDouble(token);
         const bool explicit_zero = (token == "0" || token == "0.0" || token == "0.00" || token == "0.0000000000");
         if(OP_TokenLooksInvalidNumber(token) || (numeric_value == 0.0 && !explicit_zero))
            non_numeric++;
        }
      return (non_numeric >= 2);
     }

   bool BuildColumnsFromHeader(const string &cols[], int &timestamp_col, int &feature_cols[], string &reason)
     {
      const int feature_count = EffectiveFeatureCount();
      ArrayResize(feature_cols, feature_count);
      ArrayInitialize(feature_cols, -1);
      timestamp_col = -1;

      int next_feature = 0;
      const int column_count = ArraySize(cols);
      for(int c = 0; c < column_count; c++)
        {
         const string name = OP_Lower(OP_Unquote(cols[c]));
         if(OP_IsTimestampColumn(name) && timestamp_col < 0)
           {
            timestamp_col = c;
            continue;
           }

         if(OP_IsMetadataColumn(name))
            continue;

         if(next_feature < feature_count)
           {
            feature_cols[next_feature] = c;
            next_feature++;
           }
        }

      if(m_require_timestamp_match && timestamp_col < 0)
        {
         reason = "timestamp_header_missing";
         return false;
        }

      if(next_feature < feature_count)
        {
         reason = StringFormat("feature_header_count_mismatch:expected=%d:found=%d", feature_count, next_feature);
         return false;
        }

      return true;
     }

   bool ParseFeaturesFromColumns(const string &cols[], const int &feature_cols[], double &features[], string &reason)
     {
      const int feature_count = EffectiveFeatureCount();
      ArrayResize(features, feature_count);
      const int column_count = ArraySize(cols);

      for(int i = 0; i < feature_count; i++)
        {
         const int col = feature_cols[i];
         if(col < 0 || col >= column_count)
           {
            reason = StringFormat("feature_column_out_of_range:index=%d", i);
            return false;
           }

         const string token = OP_Unquote(cols[col]);
         if(OP_TokenLooksInvalidNumber(token))
           {
            reason = StringFormat("feature_invalid_token:index=%d", i);
            return false;
           }

         const double value = StringToDouble(token);
         if(!OP_IsFiniteDouble(value))
           {
            reason = StringFormat("feature_nonfinite:index=%d", i);
            return false;
           }

         features[i] = value;
        }

      return true;
     }

   void AppendRow(const datetime row_time, const string input_hash, const double &row_features[])
     {
      const int feature_count = EffectiveFeatureCount();
      const int row = ArraySize(m_times);
      ArrayResize(m_times, row + 1);
      ArrayResize(m_hashes, row + 1);
      ArrayResize(m_values, (row + 1) * feature_count);
      m_times[row] = row_time;
      m_hashes[row] = input_hash;
      for(int i = 0; i < feature_count; i++)
         m_values[(row * feature_count) + i] = row_features[i];
     }

   void CopyRow(const int row, double &features[])
     {
      const int feature_count = EffectiveFeatureCount();
      ArrayResize(features, feature_count);
      for(int i = 0; i < feature_count; i++)
         features[i] = m_values[(row * feature_count) + i];
     }

   bool LoadAllRows(string &reason)
     {
      reason = "";
      if(m_loaded)
        {
         reason = m_load_reason;
         return (reason == "");
        }

      ResetCache();
      m_loaded = true;

      if(m_path == "")
        {
         m_load_reason = "feature_csv_path_empty";
         reason = m_load_reason;
         return false;
        }

      int flags = FILE_READ | FILE_TXT | FILE_ANSI;
      if(m_common_files)
         flags |= FILE_COMMON;

      ResetLastError();
      const int handle = FileOpen(m_path, flags);
      if(handle == INVALID_HANDLE)
        {
         m_load_reason = StringFormat("feature_csv_open_failed:%d", GetLastError());
         reason = m_load_reason;
         return false;
        }

      bool columns_ready = false;
      int timestamp_col = -1;
      int feature_cols[];
      int data_rows = 0;

      while(!FileIsEnding(handle))
        {
         string line = FileReadString(handle);
         if(line == "")
            continue;

         string cols[];
         const int col_count = StringSplit(line, m_delimiter, cols);
         if(col_count <= 0)
            continue;

         if(!columns_ready)
           {
            if(LooksLikeHeader(cols))
              {
               if(!BuildColumnsFromHeader(cols, timestamp_col, feature_cols, m_load_reason))
                 {
                  FileClose(handle);
                  reason = m_load_reason;
                  return false;
                 }
               columns_ready = true;
               continue;
              }

            if(m_strict_header)
              {
               m_load_reason = "feature_header_required";
               FileClose(handle);
               reason = m_load_reason;
               return false;
              }

            FillDefaultColumns(col_count, timestamp_col, feature_cols);
            columns_ready = true;
           }

         data_rows++;
         datetime row_time = 0;
         if(timestamp_col >= 0)
           {
            if(timestamp_col >= col_count)
               continue;
            row_time = OP_ParseTimestamp(cols[timestamp_col]);
            if(row_time <= 0)
               continue;
           }

         double row_features[];
         string parse_reason = "";
         if(!ParseFeaturesFromColumns(cols, feature_cols, row_features, parse_reason))
           {
            m_load_reason = parse_reason;
            FileClose(handle);
            reason = m_load_reason;
            return false;
           }

         AppendRow(row_time, OP_CsvInputHash(line), row_features);
        }

      FileClose(handle);
      if(ArraySize(m_times) <= 0)
        {
         m_load_reason = data_rows <= 0 ? "feature_csv_no_data_rows" : "feature_csv_no_valid_timestamp_rows";
         reason = m_load_reason;
         return false;
        }

      reason = "";
      return true;
     }

   int FindExactOrLatestIndex(const datetime target_time, bool &exact)
     {
      exact = false;
      const int row_count = ArraySize(m_times);
      if(row_count <= 0)
         return -1;
      if(target_time <= 0)
        {
         exact = true;
         return 0;
        }

      int start = m_last_index;
      if(start < 0 || start >= row_count || m_times[start] > target_time)
         start = 0;

      int latest = -1;
      for(int i = start; i < row_count; i++)
        {
         if(m_times[i] == target_time)
           {
            exact = true;
            m_last_index = i;
            return i;
           }
         if(m_times[i] < target_time)
            latest = i;
         if(m_times[i] > target_time)
            break;
        }

      if(latest >= 0)
         m_last_index = latest;
      return latest;
     }

public:
   COpFeatureCsvInput()
     {
      m_path = "";
      m_common_files = true;
      m_require_timestamp_match = true;
      m_allow_latest_fallback = false;
      m_strict_header = true;
      m_delimiter = ',';
      m_feature_count = OP_DEFAULT_FEATURE_COUNT;
      ResetCache();
     }

   void Configure(const string path,
                  const bool common_files,
                  const bool require_timestamp_match,
                  const bool allow_latest_fallback,
                  const bool strict_header,
                  const string delimiter,
                  const int feature_count)
     {
      m_path = path;
      m_common_files = common_files;
      m_require_timestamp_match = require_timestamp_match;
      m_allow_latest_fallback = allow_latest_fallback;
      m_strict_header = strict_header;
      m_delimiter = ',';
      if(StringLen(delimiter) > 0)
         m_delimiter = (ushort)StringGetCharacter(delimiter, 0);
      m_feature_count = feature_count > 0 ? feature_count : OP_DEFAULT_FEATURE_COUNT;
      ResetCache();
     }

   bool ReadForTime(const datetime target_time,
                    double &features[],
                    string &source_time,
                    string &input_hash,
                    string &reason)
     {
      source_time = "";
      input_hash = "";
      reason = "";
      ArrayResize(features, EffectiveFeatureCount());
      ArrayInitialize(features, 0.0);

      if(!LoadAllRows(reason))
         return false;

      bool exact = false;
      const int row = FindExactOrLatestIndex(target_time, exact);
      if(row >= 0 && (exact || (m_allow_latest_fallback && !m_require_timestamp_match)))
        {
         CopyRow(row, features);
         source_time = OP_TimestampText(m_times[row]);
         input_hash = m_hashes[row];
         return true;
        }

      if(target_time > 0)
         reason = "feature_csv_timestamp_not_found:" + OP_TimestampText(target_time);
      else
         reason = "feature_csv_no_matching_row";
      return false;
     }
  };

#endif
