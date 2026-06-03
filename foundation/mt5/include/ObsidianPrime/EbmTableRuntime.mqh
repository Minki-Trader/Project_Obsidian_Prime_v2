#ifndef OBSIDIAN_PRIME_EBM_TABLE_RUNTIME_MQH
#define OBSIDIAN_PRIME_EBM_TABLE_RUNTIME_MQH

class COpEbmTableRuntime
  {
private:
   bool   m_ready;
   string m_table_path;
   string m_model_id;
   bool   m_common_files;
   int    m_feature_count;
   double m_intercept[3];
   int    m_cut_offsets[];
   int    m_cut_counts[];
   int    m_score_offsets[];
   int    m_score_counts[];
   double m_cuts[];
   double m_scores[];

   int EffectiveFeatureCount() const
     {
      if(m_feature_count > 0)
         return m_feature_count;
      return OP_DEFAULT_FEATURE_COUNT;
     }

   void ResetTable()
     {
      m_ready = false;
      m_intercept[0] = 0.0;
      m_intercept[1] = 0.0;
      m_intercept[2] = 0.0;
      const int feature_count = EffectiveFeatureCount();
      ArrayResize(m_cut_offsets, feature_count);
      ArrayResize(m_cut_counts, feature_count);
      ArrayResize(m_score_offsets, feature_count);
      ArrayResize(m_score_counts, feature_count);
      ArrayInitialize(m_cut_offsets, -1);
      ArrayInitialize(m_cut_counts, 0);
      ArrayInitialize(m_score_offsets, -1);
      ArrayInitialize(m_score_counts, 0);
      ArrayResize(m_cuts, 0);
      ArrayResize(m_scores, 0);
     }

   bool ValidFeatureIndex(const int feature_index)
     {
      return (feature_index >= 0 && feature_index < EffectiveFeatureCount());
     }

   bool ParseDoubleField(const string token, double &value, string &reason)
     {
      const string text = OP_Unquote(token);
      if(text == "" || OP_TokenLooksInvalidNumber(text))
        {
         reason = "ebm_table_invalid_number";
         return false;
        }
      value = StringToDouble(text);
      if(!OP_IsFiniteDouble(value))
        {
         reason = "ebm_table_nonfinite_number";
         return false;
        }
      return true;
     }

   bool AppendCut(const int feature_index,
                  const int item_index,
                  const double value,
                  string &reason)
     {
      if(!ValidFeatureIndex(feature_index))
        {
         reason = StringFormat("ebm_cut_feature_index_outside_width:%d", feature_index);
         return false;
        }
      if(item_index != m_cut_counts[feature_index])
        {
         reason = StringFormat("ebm_cut_index_order_mismatch:feature=%d:expected=%d:actual=%d",
                               feature_index,
                               m_cut_counts[feature_index],
                               item_index);
         return false;
        }
      if(item_index == 0)
         m_cut_offsets[feature_index] = ArraySize(m_cuts);
      const int position = ArraySize(m_cuts);
      ArrayResize(m_cuts, position + 1);
      m_cuts[position] = value;
      m_cut_counts[feature_index]++;
      return true;
     }

   bool AppendScore(const int feature_index,
                    const int item_index,
                    const double score_short,
                    const double score_flat,
                    const double score_long,
                    string &reason)
     {
      if(!ValidFeatureIndex(feature_index))
        {
         reason = StringFormat("ebm_score_feature_index_outside_width:%d", feature_index);
         return false;
        }
      if(item_index != m_score_counts[feature_index])
        {
         reason = StringFormat("ebm_score_index_order_mismatch:feature=%d:expected=%d:actual=%d",
                               feature_index,
                               m_score_counts[feature_index],
                               item_index);
         return false;
        }
      if(item_index == 0)
         m_score_offsets[feature_index] = ArraySize(m_scores) / 3;
      const int position = ArraySize(m_scores);
      ArrayResize(m_scores, position + 3);
      m_scores[position] = score_short;
      m_scores[position + 1] = score_flat;
      m_scores[position + 2] = score_long;
      m_score_counts[feature_index]++;
      return true;
     }

   bool LoadTable(string &reason)
     {
      reason = "";
      if(m_table_path == "")
        {
         reason = "ebm_table_path_empty";
         return false;
        }

      int flags = FILE_READ | FILE_TXT | FILE_ANSI;
      if(m_common_files)
         flags |= FILE_COMMON;

      ResetLastError();
      const int handle = FileOpen(m_table_path, flags, 0, CP_UTF8);
      if(handle == INVALID_HANDLE)
        {
         reason = StringFormat("ebm_table_open_failed:%d", GetLastError());
         return false;
        }

      int rows = 0;
      while(!FileIsEnding(handle))
        {
         string line = FileReadString(handle);
         line = OP_Trim(line);
         if(line == "")
            continue;

         string cols[];
         const int col_count = StringSplit(line, ',', cols);
         if(col_count < 7)
            continue;

         const string record_type = OP_Lower(OP_Unquote(cols[0]));
         if(record_type == "record_type")
            continue;

         rows++;
         if(record_type == "intercept")
           {
            if(!ParseDoubleField(cols[4], m_intercept[0], reason) ||
               !ParseDoubleField(cols[5], m_intercept[1], reason) ||
               !ParseDoubleField(cols[6], m_intercept[2], reason))
              {
               FileClose(handle);
               return false;
              }
            continue;
           }

         const int feature_index = (int)StringToInteger(OP_Unquote(cols[1]));
         const int item_index = (int)StringToInteger(OP_Unquote(cols[2]));
         if(record_type == "cut")
           {
            double cut_value = 0.0;
            if(!ParseDoubleField(cols[3], cut_value, reason) ||
               !AppendCut(feature_index, item_index, cut_value, reason))
              {
               FileClose(handle);
               return false;
              }
            continue;
           }

         if(record_type == "score")
           {
            double score_short = 0.0;
            double score_flat = 0.0;
            double score_long = 0.0;
            if(!ParseDoubleField(cols[4], score_short, reason) ||
               !ParseDoubleField(cols[5], score_flat, reason) ||
               !ParseDoubleField(cols[6], score_long, reason) ||
               !AppendScore(feature_index, item_index, score_short, score_flat, score_long, reason))
              {
               FileClose(handle);
               return false;
              }
            continue;
           }

         reason = "ebm_table_unknown_record_type:" + record_type;
         FileClose(handle);
         return false;
        }

      FileClose(handle);
      if(rows <= 0)
        {
         reason = "ebm_table_empty";
         return false;
        }

      const int feature_count = EffectiveFeatureCount();
      for(int i = 0; i < feature_count; i++)
        {
         if(m_score_counts[i] <= 0)
           {
            reason = StringFormat("ebm_table_missing_scores_for_feature:%d", i);
            return false;
           }
        }
      return true;
     }

   bool IsFiniteOutputValue(const double value)
     {
      return (MathIsValidNumber(value) && MathAbs(value) < (EMPTY_VALUE / 2.0));
     }

   int BinIndex(const int feature_index, const double value)
     {
      int bin_index = 1;
      const int offset = m_cut_offsets[feature_index];
      const int count = m_cut_counts[feature_index];
      for(int i = 0; i < count; i++)
        {
         if(value > m_cuts[offset + i])
            bin_index++;
        }
      return bin_index;
     }

public:
   COpEbmTableRuntime()
     {
      m_table_path = "";
      m_model_id = "";
      m_common_files = true;
      m_feature_count = OP_DEFAULT_FEATURE_COUNT;
      ResetTable();
     }

   void Configure(const string table_path,
                  const string model_id,
                  const bool common_files,
                  const int feature_count)
     {
      m_table_path = table_path;
      m_model_id = model_id;
      m_common_files = common_files;
      m_feature_count = feature_count > 0 ? feature_count : OP_DEFAULT_FEATURE_COUNT;
      ResetTable();
     }

   bool IsReady() const
     {
      return m_ready;
     }

   bool Init(string &reason)
     {
      ResetTable();
      if(!LoadTable(reason))
        {
         m_ready = false;
         return false;
        }
      m_ready = true;
      return true;
     }

   void Deinit()
     {
      ResetTable();
     }

   bool Run(const double &features[],
            double &p_short,
            double &p_flat,
            double &p_long,
            string &reason)
     {
      p_short = 0.0;
      p_flat = 0.0;
      p_long = 0.0;
      reason = "";

      if(!m_ready)
        {
         reason = "ebm_table_not_ready";
         return false;
        }

      const int feature_count = EffectiveFeatureCount();
      if(ArraySize(features) != feature_count)
        {
         reason = StringFormat("feature_count_mismatch:expected=%d:actual=%d", feature_count, ArraySize(features));
         return false;
        }

      double score_short = m_intercept[0];
      double score_flat = m_intercept[1];
      double score_long = m_intercept[2];
      for(int i = 0; i < feature_count; i++)
        {
         const double value = features[i];
         if(!OP_IsFiniteDouble(value))
           {
            reason = StringFormat("feature_nonfinite_at:%d", i);
            return false;
           }
         const int bin_index = BinIndex(i, value);
         if(bin_index < 0 || bin_index >= m_score_counts[i])
           {
            reason = StringFormat("ebm_bin_index_outside_score_table:feature=%d:bin=%d:scores=%d",
                                  i,
                                  bin_index,
                                  m_score_counts[i]);
            return false;
           }
         const int score_position = (m_score_offsets[i] + bin_index) * 3;
         score_short += m_scores[score_position];
         score_flat += m_scores[score_position + 1];
         score_long += m_scores[score_position + 2];
        }

      const double max_score = MathMax(score_short, MathMax(score_flat, score_long));
      const double exp_short = MathExp(score_short - max_score);
      const double exp_flat = MathExp(score_flat - max_score);
      const double exp_long = MathExp(score_long - max_score);
      const double denom = exp_short + exp_flat + exp_long;
      if(!OP_IsFiniteDouble(denom) || denom <= 0.0)
        {
         reason = "ebm_softmax_denominator_invalid";
         return false;
        }

      p_short = exp_short / denom;
      p_flat = exp_flat / denom;
      p_long = exp_long / denom;
      if(!IsFiniteOutputValue(p_short) || !IsFiniteOutputValue(p_flat) || !IsFiniteOutputValue(p_long))
        {
         reason = "ebm_output_nonfinite";
         return false;
        }
      return true;
     }
  };

#endif
