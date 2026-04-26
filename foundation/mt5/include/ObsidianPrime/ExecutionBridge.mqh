#ifndef OBSIDIAN_PRIME_EXECUTION_BRIDGE_MQH
#define OBSIDIAN_PRIME_EXECUTION_BRIDGE_MQH

#ifndef OP_DECISION_SHORT
#define OP_DECISION_SHORT -1
#define OP_DECISION_FLAT 0
#define OP_DECISION_LONG 1
#endif

struct SOpPositionState
  {
   bool   has_position;
   ulong  ticket;
   long   type;
   double volume;
   string label;
  };

struct SOpExecutionResult
  {
   bool   attempted;
   bool   sent;
   bool   filled;
   string action;
   uint   retcode;
   int    last_error;
   ulong  order;
   ulong  deal;
   string comment;
   string position_before;
   string position_after;
  };

class COpExecutionBridge
  {
private:
   string m_symbol;
   long   m_magic;
   bool   m_allow_trading;
   double m_fixed_lot;
   int    m_deviation_points;
   bool   m_close_on_flat;
   bool   m_reverse_on_opposite;
   int    m_max_hold_bars;
   int    m_max_concurrent_positions;
   int    m_bars_in_position;

   bool IsRetcodeFilled(const uint retcode)
     {
      return (retcode == TRADE_RETCODE_DONE || retcode == TRADE_RETCODE_DONE_PARTIAL);
     }

   ENUM_ORDER_TYPE_FILLING ResolveFillingType()
     {
      const long filling_flags = SymbolInfoInteger(m_symbol, SYMBOL_FILLING_MODE);
      if((filling_flags & SYMBOL_FILLING_IOC) == SYMBOL_FILLING_IOC)
         return ORDER_FILLING_IOC;
      if((filling_flags & SYMBOL_FILLING_FOK) == SYMBOL_FILLING_FOK)
         return ORDER_FILLING_FOK;
#ifdef SYMBOL_FILLING_RETURN
      if((filling_flags & SYMBOL_FILLING_RETURN) == SYMBOL_FILLING_RETURN)
         return ORDER_FILLING_RETURN;
#endif
      return ORDER_FILLING_FOK;
     }

   double NormalizeVolume(const double requested)
     {
      const double min_volume = SymbolInfoDouble(m_symbol, SYMBOL_VOLUME_MIN);
      const double max_volume = SymbolInfoDouble(m_symbol, SYMBOL_VOLUME_MAX);
      const double step = SymbolInfoDouble(m_symbol, SYMBOL_VOLUME_STEP);

      double volume = requested;
      if(volume < min_volume)
         volume = min_volume;
      if(max_volume > 0.0 && volume > max_volume)
         volume = max_volume;

      if(step > 0.0)
         volume = MathFloor((volume / step) + 0.0000001) * step;

      return NormalizeDouble(volume, 8);
     }

   string PositionLabel(const SOpPositionState &state)
     {
      if(!state.has_position)
         return "none";

      string side = "unknown";
      if(state.type == POSITION_TYPE_BUY)
         side = "long";
      else if(state.type == POSITION_TYPE_SELL)
         side = "short";

      return StringFormat("%s:ticket=%I64u:volume=%.8f", side, state.ticket, state.volume);
     }

   bool SendMarketOrder(const int signal,
                        const double volume,
                        const ulong close_ticket,
                        SOpExecutionResult &result)
     {
      MqlTick tick;
      if(!SymbolInfoTick(m_symbol, tick))
        {
         result.last_error = GetLastError();
         result.comment = "symbol_tick_unavailable";
         return false;
        }

      MqlTradeRequest request;
      MqlTradeResult trade_result;
      ZeroMemory(request);
      ZeroMemory(trade_result);

      request.action = TRADE_ACTION_DEAL;
      request.symbol = m_symbol;
      request.magic = (ulong)m_magic;
      request.volume = NormalizeVolume(volume);
      request.deviation = m_deviation_points;
      request.type_time = ORDER_TIME_GTC;
      request.type_filling = ResolveFillingType();
      request.comment = "ObsidianPrimeV2 AlphaScout";

      if(signal == OP_DECISION_LONG)
        {
         request.type = ORDER_TYPE_BUY;
         request.price = tick.ask;
        }
      else if(signal == OP_DECISION_SHORT)
        {
         request.type = ORDER_TYPE_SELL;
         request.price = tick.bid;
        }
      else
        {
         result.comment = "invalid_order_signal";
         return false;
        }

      if(close_ticket > 0)
         request.position = close_ticket;

      ResetLastError();
      result.attempted = true;
      result.sent = OrderSend(request, trade_result);
      result.last_error = GetLastError();
      result.retcode = trade_result.retcode;
      result.order = trade_result.order;
      result.deal = trade_result.deal;
      result.comment = trade_result.comment;
      result.filled = (result.sent && IsRetcodeFilled(trade_result.retcode));
      return result.filled;
     }

   int OppositeSignalForPosition(const SOpPositionState &state)
     {
      if(!state.has_position)
         return OP_DECISION_FLAT;
      if(state.type == POSITION_TYPE_BUY)
         return OP_DECISION_SHORT;
      if(state.type == POSITION_TYPE_SELL)
         return OP_DECISION_LONG;
      return OP_DECISION_FLAT;
     }

   bool SignalMatchesPosition(const int signal, const SOpPositionState &state)
     {
      if(!state.has_position)
         return false;
      if(signal == OP_DECISION_LONG && state.type == POSITION_TYPE_BUY)
         return true;
      if(signal == OP_DECISION_SHORT && state.type == POSITION_TYPE_SELL)
         return true;
      return false;
     }

   int ManagedPositionCount()
     {
      int count = 0;
      const int total = PositionsTotal();
      for(int i = 0; i < total; i++)
        {
         const string symbol = PositionGetSymbol(i);
         if(symbol != m_symbol)
            continue;
         if((long)PositionGetInteger(POSITION_MAGIC) != m_magic)
            continue;
         count++;
        }
      return count;
     }

public:
   COpExecutionBridge()
     {
      m_symbol = "";
      m_magic = 0;
      m_allow_trading = false;
      m_fixed_lot = 0.10;
      m_deviation_points = 20;
      m_close_on_flat = false;
      m_reverse_on_opposite = true;
      m_max_hold_bars = 12;
      m_max_concurrent_positions = 1;
      m_bars_in_position = 0;
     }

   void Configure(const string symbol,
                  const long magic,
                  const bool allow_trading,
                  const double fixed_lot,
                  const int deviation_points,
                  const bool close_on_flat,
                  const bool reverse_on_opposite,
                  const int max_hold_bars,
                  const int max_concurrent_positions)
     {
      m_symbol = symbol;
      m_magic = magic;
      m_allow_trading = allow_trading;
      m_fixed_lot = fixed_lot;
      m_deviation_points = deviation_points;
      m_close_on_flat = close_on_flat;
      m_reverse_on_opposite = reverse_on_opposite;
      m_max_hold_bars = max_hold_bars;
      m_max_concurrent_positions = max_concurrent_positions > 0 ? max_concurrent_positions : 1;
      m_bars_in_position = 0;
     }

   bool Init(string &reason)
     {
      reason = "";
      if(m_symbol == "")
        {
         reason = "execution_symbol_empty";
         return false;
        }

      if(!SymbolSelect(m_symbol, true))
        {
         reason = "execution_symbol_select_failed";
         return false;
        }

      if(m_allow_trading && NormalizeVolume(m_fixed_lot) <= 0.0)
        {
         reason = "execution_volume_invalid";
         return false;
        }

      return true;
     }

   SOpPositionState GetPositionState()
     {
      SOpPositionState state;
      state.has_position = false;
      state.ticket = 0;
      state.type = -1;
      state.volume = 0.0;
      state.label = "none";

      const int total = PositionsTotal();
      for(int i = 0; i < total; i++)
        {
         const string symbol = PositionGetSymbol(i);
         if(symbol != m_symbol)
            continue;
         if((long)PositionGetInteger(POSITION_MAGIC) != m_magic)
            continue;

         state.has_position = true;
         state.ticket = (ulong)PositionGetInteger(POSITION_TICKET);
         state.type = (long)PositionGetInteger(POSITION_TYPE);
         state.volume = PositionGetDouble(POSITION_VOLUME);
         state.label = PositionLabel(state);
         return state;
        }

      return state;
     }

   string PositionStateText()
     {
      const SOpPositionState state = GetPositionState();
      return state.label;
     }

   bool Execute(const int signal, SOpExecutionResult &result)
     {
      result.attempted = false;
      result.sent = false;
      result.filled = false;
      result.action = "none";
      result.retcode = 0;
      result.last_error = 0;
      result.order = 0;
      result.deal = 0;
      result.comment = "";
      result.position_before = PositionStateText();
      result.position_after = result.position_before;

      SOpPositionState state = GetPositionState();
      if(state.has_position)
         m_bars_in_position++;
      else
         m_bars_in_position = 0;

      if(!m_allow_trading)
        {
         result.action = "trading_disabled";
         result.comment = "trading_disabled";
         return true;
        }

      if(state.has_position && m_max_hold_bars > 0 && m_bars_in_position >= m_max_hold_bars)
        {
         result.action = "close_max_hold";
         const int close_signal = OppositeSignalForPosition(state);
         const bool closed = SendMarketOrder(close_signal, state.volume, state.ticket, result);
         result.position_after = PositionStateText();
         if(closed)
            m_bars_in_position = 0;
         return closed;
        }

      if(signal == OP_DECISION_FLAT)
        {
         if(state.has_position && m_close_on_flat)
           {
            result.action = "close_on_flat";
            const int close_signal = OppositeSignalForPosition(state);
            const bool closed = SendMarketOrder(close_signal, state.volume, state.ticket, result);
            result.position_after = PositionStateText();
            if(closed)
               m_bars_in_position = 0;
            return closed;
           }

         result.action = state.has_position ? "hold_existing" : "flat_no_position";
         result.position_after = PositionStateText();
         return true;
        }

      if(!state.has_position)
        {
         if(ManagedPositionCount() >= m_max_concurrent_positions)
           {
            result.action = "max_concurrent_position_skip";
            result.comment = "max_concurrent_positions_reached";
            result.position_after = PositionStateText();
            return true;
           }

         result.action = (signal == OP_DECISION_LONG) ? "open_long" : "open_short";
         const bool opened = SendMarketOrder(signal, m_fixed_lot, 0, result);
         result.position_after = PositionStateText();
         if(opened)
            m_bars_in_position = 0;
         return opened;
        }

      if(SignalMatchesPosition(signal, state))
        {
         result.action = "hold_same_direction";
         result.position_after = PositionStateText();
         return true;
        }

      if(!m_reverse_on_opposite)
        {
         result.action = "opposite_signal_held";
         result.comment = "reverse_disabled";
         result.position_after = PositionStateText();
         return true;
        }

      result.action = "reverse_close";
      const int close_signal = OppositeSignalForPosition(state);
      const bool closed = SendMarketOrder(close_signal, state.volume, state.ticket, result);
      if(!closed)
        {
         result.position_after = PositionStateText();
         return false;
        }

      state = GetPositionState();
      if(state.has_position)
        {
         result.position_after = PositionStateText();
         result.comment = "position_still_open_after_close";
         return false;
        }

      SOpExecutionResult open_result;
      const bool opened = SendMarketOrder(signal, m_fixed_lot, 0, open_result);
      result.action = (signal == OP_DECISION_LONG) ? "reverse_open_long" : "reverse_open_short";
      result.attempted = (result.attempted || open_result.attempted);
      result.sent = open_result.sent;
      result.filled = open_result.filled;
      result.retcode = open_result.retcode;
      result.last_error = open_result.last_error;
      result.order = open_result.order;
      result.deal = open_result.deal;
      result.comment = open_result.comment;
      result.position_after = PositionStateText();
      if(opened)
         m_bars_in_position = 0;
      return opened;
     }
  };

#endif
