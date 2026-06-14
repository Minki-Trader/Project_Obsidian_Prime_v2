#ifndef OBSIDIAN_PRIME_DECISION_SURFACE_MQH
#define OBSIDIAN_PRIME_DECISION_SURFACE_MQH

#define OP_DECISION_SHORT -1
#define OP_DECISION_FLAT 0
#define OP_DECISION_LONG 1

struct SOpDecisionResult
  {
   int    signal;
   string label;
   string reason;
   double confidence;
   double margin;
  };

class COpDecisionSurface
  {
private:
   double m_short_threshold;
   double m_long_threshold;
   double m_min_margin;
   bool   m_invert_signal;
   string m_decision_mode;

   bool IsFiniteProbability(const double value)
     {
      return (MathIsValidNumber(value) && value >= -0.000001 && value <= 1.000001);
     }

   string NormalizeDecisionMode(const string value)
     {
      string text = value;
      StringTrimLeft(text);
      StringTrimRight(text);
      StringToLower(text);
      if(text == "" || text == "threshold" || text == "threshold_margin")
         return "threshold_margin";
      if(text == "argmax" || text == "argmax_probe" || text == "three_class_argmax")
         return "argmax_probe";
      if(text == "edge_margin" || text == "edge_margin_probe" || text == "max_direction_vs_flat")
         return "edge_margin";
      return "threshold_margin";
     }

   bool IsArgmaxProbeMode()
     {
      return (m_decision_mode == "argmax_probe");
     }

   bool IsEdgeMarginMode()
     {
      return (m_decision_mode == "edge_margin");
     }

   void EvaluateArgmax(const double p_short,
                       const double p_flat,
                       const double p_long,
                       SOpDecisionResult &result)
     {
      int signal = OP_DECISION_SHORT;
      string label = "short";
      string reason = "argmax_probe_short";
      double confidence = p_short;
      double margin = p_short - MathMax(p_flat, p_long);

      if(p_flat > confidence)
        {
         signal = OP_DECISION_FLAT;
         label = "flat";
         reason = "argmax_probe_flat";
         confidence = p_flat;
         margin = p_flat - MathMax(p_short, p_long);
        }

      if(p_long > confidence)
        {
         signal = OP_DECISION_LONG;
         label = "long";
         reason = "argmax_probe_long";
         confidence = p_long;
         margin = p_long - MathMax(p_short, p_flat);
        }

      if(m_invert_signal && signal == OP_DECISION_LONG)
        {
         signal = OP_DECISION_SHORT;
         label = "short";
         reason = "inverse_" + reason;
        }
      else if(m_invert_signal && signal == OP_DECISION_SHORT)
        {
         signal = OP_DECISION_LONG;
         label = "long";
         reason = "inverse_" + reason;
        }

      result.signal = signal;
      result.label = label;
      result.reason = reason;
      result.confidence = confidence;
      result.margin = margin;
     }

   void EvaluateEdgeMargin(const double p_short,
                           const double p_flat,
                           const double p_long,
                           SOpDecisionResult &result)
     {
      const bool short_side = (p_short >= p_long);
      const double direction_probability = short_side ? p_short : p_long;
      const double edge_margin = direction_probability - p_flat;
      const double threshold = short_side ? m_short_threshold : m_long_threshold;

      if(direction_probability < threshold || edge_margin < m_min_margin)
        {
         result.signal = OP_DECISION_FLAT;
         result.label = "flat";
         result.reason = "edge_margin_not_met";
         result.confidence = p_flat;
         result.margin = edge_margin;
         return;
        }

      if(short_side)
        {
         result.signal = m_invert_signal ? OP_DECISION_LONG : OP_DECISION_SHORT;
         result.label = m_invert_signal ? "long" : "short";
         result.reason = m_invert_signal ? "inverse_edge_margin_short" : "edge_margin_short";
         result.confidence = p_short;
         result.margin = edge_margin;
         return;
        }

      result.signal = m_invert_signal ? OP_DECISION_SHORT : OP_DECISION_LONG;
      result.label = m_invert_signal ? "short" : "long";
      result.reason = m_invert_signal ? "inverse_edge_margin_long" : "edge_margin_long";
      result.confidence = p_long;
      result.margin = edge_margin;
     }

public:
   COpDecisionSurface()
     {
      m_short_threshold = 0.55;
      m_long_threshold = 0.55;
      m_min_margin = 0.05;
      m_invert_signal = false;
      m_decision_mode = "threshold_margin";
     }

   void Configure(const double short_threshold,
                  const double long_threshold,
                  const double min_margin,
                  const bool invert_signal=false)
     {
      m_short_threshold = short_threshold;
      m_long_threshold = long_threshold;
      m_min_margin = min_margin;
      m_invert_signal = invert_signal;
     }

   void ConfigureDecisionMode(const string decision_mode)
     {
      m_decision_mode = NormalizeDecisionMode(decision_mode);
     }

   string DecisionMode() const
     {
      return m_decision_mode;
     }

   void Evaluate(const double p_short,
                 const double p_flat,
                 const double p_long,
                 SOpDecisionResult &result)
     {
      result.signal = OP_DECISION_FLAT;
      result.label = "flat";
      result.reason = "";
      result.confidence = 0.0;
      result.margin = 0.0;

      if(!IsFiniteProbability(p_short) || !IsFiniteProbability(p_flat) || !IsFiniteProbability(p_long))
        {
         result.reason = "probability_invalid";
         return;
        }

      if(IsArgmaxProbeMode())
        {
         EvaluateArgmax(p_short, p_flat, p_long, result);
         return;
        }

      if(IsEdgeMarginMode())
        {
         EvaluateEdgeMargin(p_short, p_flat, p_long, result);
         return;
        }

      const double short_margin = p_short - MathMax(p_flat, p_long);
      const double long_margin = p_long - MathMax(p_flat, p_short);
      const bool short_ok = (p_short >= m_short_threshold && short_margin >= m_min_margin);
      const bool long_ok = (p_long >= m_long_threshold && long_margin >= m_min_margin);

      if(long_ok && (!short_ok || p_long >= p_short))
        {
         result.signal = m_invert_signal ? OP_DECISION_SHORT : OP_DECISION_LONG;
         result.label = m_invert_signal ? "short" : "long";
         result.reason = m_invert_signal ? "inverse_long_threshold_met" : "long_threshold_met";
         result.confidence = p_long;
         result.margin = long_margin;
         return;
        }

      if(short_ok)
        {
         result.signal = m_invert_signal ? OP_DECISION_LONG : OP_DECISION_SHORT;
         result.label = m_invert_signal ? "long" : "short";
         result.reason = m_invert_signal ? "inverse_short_threshold_met" : "short_threshold_met";
         result.confidence = p_short;
         result.margin = short_margin;
         return;
        }

      result.signal = OP_DECISION_FLAT;
      result.label = "flat";
      result.reason = "threshold_or_margin_not_met";
      result.confidence = p_flat;
      result.margin = MathMax(short_margin, long_margin);
     }
  };

#endif
