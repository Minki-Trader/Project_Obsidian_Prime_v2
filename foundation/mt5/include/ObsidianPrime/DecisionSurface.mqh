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

   bool IsFiniteProbability(const double value)
     {
      return (MathIsValidNumber(value) && value >= -0.000001 && value <= 1.000001);
     }

public:
   COpDecisionSurface()
     {
      m_short_threshold = 0.55;
      m_long_threshold = 0.55;
      m_min_margin = 0.05;
     }

   void Configure(const double short_threshold,
                  const double long_threshold,
                  const double min_margin)
     {
      m_short_threshold = short_threshold;
      m_long_threshold = long_threshold;
      m_min_margin = min_margin;
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

      const double short_margin = p_short - MathMax(p_flat, p_long);
      const double long_margin = p_long - MathMax(p_flat, p_short);
      const bool short_ok = (p_short >= m_short_threshold && short_margin >= m_min_margin);
      const bool long_ok = (p_long >= m_long_threshold && long_margin >= m_min_margin);

      if(long_ok && (!short_ok || p_long >= p_short))
        {
         result.signal = OP_DECISION_LONG;
         result.label = "long";
         result.reason = "long_threshold_met";
         result.confidence = p_long;
         result.margin = long_margin;
         return;
        }

      if(short_ok)
        {
         result.signal = OP_DECISION_SHORT;
         result.label = "short";
         result.reason = "short_threshold_met";
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
