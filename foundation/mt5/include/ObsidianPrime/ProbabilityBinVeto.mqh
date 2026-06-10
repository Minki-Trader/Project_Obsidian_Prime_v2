#ifndef OBSIDIAN_PRIME_PROBABILITY_BIN_VETO_MQH
#define OBSIDIAN_PRIME_PROBABILITY_BIN_VETO_MQH

#define OP_PROBABILITY_BIN_VETO_VERSION "1.0.0"

class COpProbabilityBinVeto
  {
private:
   bool   m_enabled;
   double m_pflat_edges[];
   double m_short_long_gap_edges[];
   int    m_rule_hours[];
   int    m_rule_pflat_bins[];
   int    m_rule_short_long_gap_bins[];

   string CleanListText(const string raw_text)
     {
      string text = raw_text;
      StringReplace(text, "\r", "|");
      StringReplace(text, "\n", "|");
      StringReplace(text, ";", "|");
      StringReplace(text, ",", "|");
      return text;
     }

   int ParseEdgeList(const string raw_edges, double &edges[], string &reason)
     {
      reason = "";
      ArrayResize(edges, 0);
      string text = CleanListText(raw_edges);
      StringTrimLeft(text);
      StringTrimRight(text);
      if(text == "")
        {
         reason = "probability_bin_veto_edges_empty";
         return 0;
        }

      string parts[];
      const int part_count = StringSplit(text, '|', parts);
      for(int i = 0; i < part_count; i++)
        {
         string part = parts[i];
         StringTrimLeft(part);
         StringTrimRight(part);
         if(part == "")
            continue;

         const double value = StringToDouble(part);
         if(!MathIsValidNumber(value))
           {
            reason = "probability_bin_veto_edge_invalid:" + part;
            return 0;
           }

         const int index = ArraySize(edges);
         ArrayResize(edges, index + 1);
         edges[index] = value;
        }

      const int edge_count = ArraySize(edges);
      if(edge_count < 2)
        {
         reason = "probability_bin_veto_edges_too_short";
         return 0;
        }

      for(int i = 1; i < edge_count; i++)
        {
         if(edges[i] <= edges[i - 1])
           {
            reason = "probability_bin_veto_edges_not_increasing";
            return 0;
           }
        }
      return edge_count;
     }

   bool ParseRuleRecord(const string raw_record, int &hour, int &pflat_bin, int &short_long_gap_bin, string &reason)
     {
      reason = "";
      string record = raw_record;
      StringTrimLeft(record);
      StringTrimRight(record);
      if(record == "")
         return false;

      StringReplace(record, ",", "|");
      string fields[];
      const int field_count = StringSplit(record, '|', fields);
      if(field_count < 3)
        {
         reason = "probability_bin_veto_rule_field_count:" + record;
         return false;
        }

      for(int i = 0; i < field_count; i++)
        {
         StringTrimLeft(fields[i]);
         StringTrimRight(fields[i]);
        }

      hour = (int)StringToInteger(fields[0]);
      pflat_bin = (int)StringToInteger(fields[1]);
      short_long_gap_bin = (int)StringToInteger(fields[2]);
      if(hour < 0 || hour > 23 || pflat_bin < 0 || short_long_gap_bin < 0)
        {
         reason = "probability_bin_veto_rule_value_out_of_range:" + record;
         return false;
        }
      return true;
     }

   int ParseRules(const string raw_rules, string &reason)
     {
      reason = "";
      ArrayResize(m_rule_hours, 0);
      ArrayResize(m_rule_pflat_bins, 0);
      ArrayResize(m_rule_short_long_gap_bins, 0);

      string text = raw_rules;
      StringReplace(text, "\r", ";");
      StringReplace(text, "\n", ";");
      StringTrimLeft(text);
      StringTrimRight(text);
      if(text == "")
        {
         reason = "probability_bin_veto_rules_empty";
         return 0;
        }

      string records[];
      const int record_count = StringSplit(text, ';', records);
      int rule_count = 0;
      for(int i = 0; i < record_count; i++)
        {
         int hour = 0;
         int pflat_bin = 0;
         int short_long_gap_bin = 0;
         string rule_reason = "";
         if(!ParseRuleRecord(records[i], hour, pflat_bin, short_long_gap_bin, rule_reason))
           {
            string trimmed = records[i];
            StringTrimLeft(trimmed);
            StringTrimRight(trimmed);
            if(trimmed == "")
               continue;
            reason = rule_reason;
            return 0;
           }

         ArrayResize(m_rule_hours, rule_count + 1);
         ArrayResize(m_rule_pflat_bins, rule_count + 1);
         ArrayResize(m_rule_short_long_gap_bins, rule_count + 1);
         m_rule_hours[rule_count] = hour;
         m_rule_pflat_bins[rule_count] = pflat_bin;
         m_rule_short_long_gap_bins[rule_count] = short_long_gap_bin;
         rule_count++;
        }

      if(rule_count <= 0)
         reason = "probability_bin_veto_no_rules";
      return rule_count;
     }

   int BinForValue(const double value, const double &edges[])
     {
      if(!MathIsValidNumber(value))
         return -1;

      const int edge_count = ArraySize(edges);
      if(edge_count < 2)
         return -1;

      for(int i = 0; i < edge_count - 1; i++)
        {
         const double lower = edges[i];
         const double upper = edges[i + 1];
         if(i == 0)
           {
            if(value >= lower && value <= upper)
               return i;
           }
         else if(value > lower && value <= upper)
            return i;
        }
      return -1;
     }

public:
   COpProbabilityBinVeto()
     {
      m_enabled = false;
     }

   bool Configure(const bool enabled,
                  const string pflat_edges,
                  const string short_long_gap_edges,
                  const string rules,
                  string &reason)
     {
      reason = "";
      m_enabled = enabled;
      ArrayResize(m_pflat_edges, 0);
      ArrayResize(m_short_long_gap_edges, 0);
      ArrayResize(m_rule_hours, 0);
      ArrayResize(m_rule_pflat_bins, 0);
      ArrayResize(m_rule_short_long_gap_bins, 0);

      if(!m_enabled)
         return true;

      if(ParseEdgeList(pflat_edges, m_pflat_edges, reason) <= 0)
         return false;
      if(ParseEdgeList(short_long_gap_edges, m_short_long_gap_edges, reason) <= 0)
         return false;
      if(ParseRules(rules, reason) <= 0)
         return false;

      return true;
     }

   bool Enabled() const
     {
      return m_enabled;
     }

   int RuleCount() const
     {
      return ArraySize(m_rule_hours);
     }

   string Version() const
     {
      return OP_PROBABILITY_BIN_VETO_VERSION;
     }

   bool Apply(const datetime target_time,
              const double p_short,
              const double p_flat,
              const double p_long,
              SOpDecisionResult &decision)
     {
      if(!m_enabled || decision.signal == OP_DECISION_FLAT)
         return false;

      MqlDateTime parts;
      TimeToStruct(target_time, parts);

      const int pflat_bin = BinForValue(p_flat, m_pflat_edges);
      const double short_long_gap = p_short - p_long;
      const int short_long_gap_bin = BinForValue(short_long_gap, m_short_long_gap_edges);
      if(pflat_bin < 0 || short_long_gap_bin < 0)
         return false;

      const int rule_count = RuleCount();
      for(int i = 0; i < rule_count; i++)
        {
         if(parts.hour != m_rule_hours[i])
            continue;
         if(pflat_bin != m_rule_pflat_bins[i])
            continue;
         if(short_long_gap_bin != m_rule_short_long_gap_bins[i])
            continue;

         decision.signal = OP_DECISION_FLAT;
         decision.label = "flat";
         decision.confidence = 0.0;
         decision.margin = 0.0;
         decision.reason = "probability_bin_veto:hour="
                           + (string)parts.hour
                           + ",pflat_bin="
                           + (string)pflat_bin
                           + ",sl_gap_bin="
                           + (string)short_long_gap_bin
                           + ",p_flat="
                           + DoubleToString(p_flat, 10)
                           + ",sl_gap="
                           + DoubleToString(short_long_gap, 10)
                           + "|"
                           + decision.reason;
         return true;
        }
      return false;
     }
  };

#endif
