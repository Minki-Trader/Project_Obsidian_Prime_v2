#ifndef OBSIDIAN_PRIME_RUNTIME_VETO_TAPE_MQH
#define OBSIDIAN_PRIME_RUNTIME_VETO_TAPE_MQH

#define OP_RUNTIME_VETO_TAPE_VERSION "1.0.0"

class COpRuntimeVetoTape
  {
private:
   bool     m_enabled;
   bool     m_common_files;
   bool     m_loaded;
   string   m_path;
   ushort   m_delimiter;
   string   m_load_reason;
   int      m_last_index;
   datetime m_times[];
   bool     m_veto[];

   void ResetCache()
     {
      m_loaded = false;
      m_load_reason = "";
      m_last_index = 0;
      ArrayResize(m_times, 0);
      ArrayResize(m_veto, 0);
     }

   bool IsTimestampColumn(const string raw_name)
     {
      return OP_IsTimestampColumn(raw_name);
     }

   bool IsVetoColumn(const string raw_name)
     {
      const string name = OP_Lower(OP_Unquote(raw_name));
      return (name == "runtime_veto" ||
              name == "adverse_veto" ||
              name == "veto" ||
              name == "block_entry" ||
              name == "entry_veto");
     }

   bool ParseBoolToken(const string raw_value)
     {
      const string text = OP_Lower(OP_Unquote(raw_value));
      return (text == "1" ||
              text == "true" ||
              text == "yes" ||
              text == "y" ||
              text == "veto" ||
              text == "block" ||
              text == "blocked");
     }

   bool BuildColumnsFromHeader(const string &cols[], int &timestamp_col, int &veto_col, string &reason)
     {
      timestamp_col = -1;
      veto_col = -1;
      const int column_count = ArraySize(cols);
      for(int c = 0; c < column_count; c++)
        {
         if(timestamp_col < 0 && IsTimestampColumn(cols[c]))
           {
            timestamp_col = c;
            continue;
           }
         if(veto_col < 0 && IsVetoColumn(cols[c]))
            veto_col = c;
        }

      if(timestamp_col < 0)
        {
         reason = "runtime_veto_tape_timestamp_column_missing";
         return false;
        }
      if(veto_col < 0)
        {
         reason = "runtime_veto_tape_veto_column_missing";
         return false;
        }
      return true;
     }

   void AppendRow(const datetime row_time, const bool veto)
     {
      const int row = ArraySize(m_times);
      ArrayResize(m_times, row + 1);
      ArrayResize(m_veto, row + 1);
      m_times[row] = row_time;
      m_veto[row] = veto;
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

      if(!m_enabled)
         return true;
      if(m_path == "")
        {
         m_load_reason = "runtime_veto_tape_path_empty";
         reason = m_load_reason;
         return false;
        }

      int flags = FILE_READ | FILE_TXT | FILE_ANSI;
      if(m_common_files)
         flags |= FILE_COMMON;

      ResetLastError();
      const int handle = FileOpen(m_path, flags, 0, CP_UTF8);
      if(handle == INVALID_HANDLE)
        {
         m_load_reason = StringFormat("runtime_veto_tape_open_failed:%d", GetLastError());
         reason = m_load_reason;
         return false;
        }

      bool header_ready = false;
      int timestamp_col = -1;
      int veto_col = -1;
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

         if(!header_ready)
           {
            if(!BuildColumnsFromHeader(cols, timestamp_col, veto_col, m_load_reason))
              {
               FileClose(handle);
               reason = m_load_reason;
               return false;
              }
            header_ready = true;
            continue;
           }

         data_rows++;
         if(timestamp_col >= col_count || veto_col >= col_count)
            continue;
         const datetime row_time = OP_ParseTimestamp(cols[timestamp_col]);
         if(row_time <= 0)
            continue;
         AppendRow(row_time, ParseBoolToken(cols[veto_col]));
        }

      FileClose(handle);
      if(ArraySize(m_times) <= 0)
        {
         m_load_reason = data_rows <= 0 ? "runtime_veto_tape_no_data_rows" : "runtime_veto_tape_no_valid_timestamp_rows";
         reason = m_load_reason;
         return false;
        }

      reason = "";
      return true;
     }

   int FindExactIndex(const datetime target_time)
     {
      const int row_count = ArraySize(m_times);
      if(row_count <= 0 || target_time <= 0)
         return -1;

      int start = m_last_index;
      if(start < 0 || start >= row_count || m_times[start] > target_time)
         start = 0;

      for(int i = start; i < row_count; i++)
        {
         if(m_times[i] == target_time)
           {
            m_last_index = i;
            return i;
           }
         if(m_times[i] > target_time)
            break;
        }
      return -1;
     }

public:
   COpRuntimeVetoTape()
     {
      m_enabled = false;
      m_common_files = true;
      m_path = "";
      m_delimiter = ',';
      ResetCache();
     }

   bool Configure(const bool enabled,
                  const string path,
                  const bool common_files,
                  const string delimiter,
                  string &reason)
     {
      reason = "";
      m_enabled = enabled;
      m_path = path;
      m_common_files = common_files;
      m_delimiter = ',';
      if(StringLen(delimiter) > 0)
         m_delimiter = (ushort)StringGetCharacter(delimiter, 0);
      ResetCache();
      if(!m_enabled)
         return true;
      return LoadAllRows(reason);
     }

   bool Enabled() const
     {
      return m_enabled;
     }

   int RowCount() const
     {
      return ArraySize(m_times);
     }

   string Version() const
     {
      return OP_RUNTIME_VETO_TAPE_VERSION;
     }

   bool Apply(const datetime target_time, SOpDecisionResult &decision)
     {
      if(!m_enabled || decision.signal == OP_DECISION_FLAT)
         return false;

      string reason = "";
      if(!LoadAllRows(reason))
         return false;

      const int row = FindExactIndex(target_time);
      if(row < 0 || !m_veto[row])
         return false;

      decision.signal = OP_DECISION_FLAT;
      decision.label = "flat";
      decision.confidence = 0.0;
      decision.margin = 0.0;
      decision.reason = "runtime_veto_tape:time=" + OP_TimestampText(target_time) + "|" + decision.reason;
      return true;
     }
  };

#endif
