#property strict
#property script_show_inputs

input string InpRunId = "run337AB_custom_symbol_intraday_tester_visibility_probe_v1";
input string InpOriginSymbol = "US100";
input string InpCustomSymbol = "US100.OPV337AB";
input string InpCustomPath = "ObsidianPrime";
input string InpFromUtc = "2026.04.14 00:00:00";
input string InpToUtc = "2026.05.28 00:00:00";
input string InpOutputPath = "Project_Obsidian_Prime_v2/stage337/run337AB_custom_symbol_intraday_tester_visibility_probe/custom_symbol_seed_status.json";
input bool   InpOutputUseCommonFiles = true;
input int    InpShiftMinutes = 0;

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

string FormatIso(const datetime value)
  {
   if(value <= 0)
      return "";
   MqlDateTime dt;
   TimeToStruct(value, dt);
   return StringFormat("%04d-%02d-%02dT%02d:%02d:%02dZ", dt.year, dt.mon, dt.day, dt.hour, dt.min, dt.sec);
  }

void RateRange(const MqlRates &rates[], const int count, datetime &first_time, datetime &last_time)
  {
   first_time = 0;
   last_time = 0;
   for(int i = 0; i < count; i++)
     {
      datetime t = rates[i].time;
      if(t <= 0)
         continue;
      if(first_time == 0 || t < first_time)
         first_time = t;
      if(last_time == 0 || t > last_time)
         last_time = t;
     }
  }

bool WriteStatus(const string status,
                 const string detail,
                 const datetime from_time,
                 const datetime to_time,
                 const bool origin_selected,
                 const bool custom_selected,
                 const bool create_ok,
                 const int create_error,
                 const int copied_m1,
                 const int updated_m1,
                 const int copied_custom_m1,
                 const int copied_custom_m5,
                 const datetime origin_first_m1,
                 const datetime origin_last_m1,
                 const datetime target_first_m1,
                 const datetime target_last_m1,
                 const datetime custom_first_m1,
                 const datetime custom_last_m1,
                 const datetime custom_first_m5,
                 const datetime custom_last_m5,
                 const int last_error)
  {
   int flags = FILE_WRITE | FILE_TXT | FILE_ANSI;
   if(InpOutputUseCommonFiles)
      flags |= FILE_COMMON;
   int handle = FileOpen(InpOutputPath, flags);
   if(handle == INVALID_HANDLE)
     {
      PrintFormat("[ObsidianPrimeV2][CustomSymbolSeed] output_open_failed path=%s error=%d", InpOutputPath, GetLastError());
      return false;
     }

   string text = "{\n";
   text += "  \"run_id\": " + JsonQuoted(InpRunId) + ",\n";
   text += "  \"status\": " + JsonQuoted(status) + ",\n";
   text += "  \"detail\": " + JsonQuoted(detail) + ",\n";
   text += "  \"origin_symbol\": " + JsonQuoted(InpOriginSymbol) + ",\n";
   text += "  \"custom_symbol\": " + JsonQuoted(InpCustomSymbol) + ",\n";
   text += "  \"custom_path\": " + JsonQuoted(InpCustomPath) + ",\n";
   text += "  \"from_utc\": " + JsonQuoted(FormatIso(from_time)) + ",\n";
   text += "  \"to_utc\": " + JsonQuoted(FormatIso(to_time)) + ",\n";
   text += "  \"shift_minutes\": " + IntegerToString(InpShiftMinutes) + ",\n";
   text += "  \"origin_selected\": " + JsonBool(origin_selected) + ",\n";
   text += "  \"custom_selected\": " + JsonBool(custom_selected) + ",\n";
   text += "  \"custom_symbol_create_ok\": " + JsonBool(create_ok) + ",\n";
   text += "  \"custom_symbol_create_error\": " + IntegerToString(create_error) + ",\n";
   text += "  \"origin_m1_copied\": " + IntegerToString(copied_m1) + ",\n";
   text += "  \"custom_m1_updated\": " + IntegerToString(updated_m1) + ",\n";
   text += "  \"custom_m1_copied\": " + IntegerToString(copied_custom_m1) + ",\n";
   text += "  \"custom_m5_copied\": " + IntegerToString(copied_custom_m5) + ",\n";
   text += "  \"origin_first_m1_utc\": " + JsonQuoted(FormatIso(origin_first_m1)) + ",\n";
   text += "  \"origin_last_m1_utc\": " + JsonQuoted(FormatIso(origin_last_m1)) + ",\n";
   text += "  \"target_first_m1_utc\": " + JsonQuoted(FormatIso(target_first_m1)) + ",\n";
   text += "  \"target_last_m1_utc\": " + JsonQuoted(FormatIso(target_last_m1)) + ",\n";
   text += "  \"custom_first_m1_utc\": " + JsonQuoted(FormatIso(custom_first_m1)) + ",\n";
   text += "  \"custom_last_m1_utc\": " + JsonQuoted(FormatIso(custom_last_m1)) + ",\n";
   text += "  \"custom_first_m5_utc\": " + JsonQuoted(FormatIso(custom_first_m5)) + ",\n";
   text += "  \"custom_last_m5_utc\": " + JsonQuoted(FormatIso(custom_last_m5)) + ",\n";
   text += "  \"last_error\": " + IntegerToString(last_error) + ",\n";
   text += "  \"terminal_data_path\": " + JsonQuoted(TerminalInfoString(TERMINAL_DATA_PATH)) + "\n";
   text += "}\n";
   FileWriteString(handle, text);
   FileClose(handle);
   return true;
  }

void OnStart()
  {
   datetime from_time = StringToTime(InpFromUtc);
   datetime to_time = StringToTime(InpToUtc);
   if(from_time <= 0 || to_time <= 0 || to_time <= from_time)
     {
      WriteStatus("blocked_invalid_time_range", "InpFromUtc/InpToUtc parse failed", from_time, to_time, false, false, false, GetLastError(), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, GetLastError());
      return;
     }

   long shift_seconds = (long)InpShiftMinutes * 60;
   datetime target_from_time = (datetime)((long)from_time + shift_seconds);
   datetime target_to_time = (datetime)((long)to_time + shift_seconds);

   ResetLastError();
   bool origin_selected = SymbolSelect(InpOriginSymbol, true);
   int origin_select_error = GetLastError();
   if(!origin_selected)
     {
      WriteStatus("blocked_origin_symbol_select_failed", "SymbolSelect(origin) failed", from_time, to_time, false, false, false, origin_select_error, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, origin_select_error);
      return;
     }

   ResetLastError();
   bool create_ok = CustomSymbolCreate(InpCustomSymbol, InpCustomPath, InpOriginSymbol);
   int create_error = GetLastError();
   if(!create_ok && create_error != 5304)
     {
      WriteStatus("blocked_custom_symbol_create_failed", "CustomSymbolCreate failed", from_time, to_time, origin_selected, false, false, create_error, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, create_error);
      return;
     }

   ResetLastError();
   bool custom_selected = SymbolSelect(InpCustomSymbol, true);
   int custom_select_error = GetLastError();
   if(!custom_selected)
     {
      WriteStatus("blocked_custom_symbol_select_failed", "SymbolSelect(custom) failed", from_time, to_time, origin_selected, false, create_ok, create_error, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, custom_select_error);
      return;
     }

   MqlRates origin_m1[];
   ResetLastError();
   int copied_m1 = CopyRates(InpOriginSymbol, PERIOD_M1, from_time, to_time, origin_m1);
   int copy_error = GetLastError();
   datetime origin_first_m1 = 0;
   datetime origin_last_m1 = 0;
   RateRange(origin_m1, copied_m1, origin_first_m1, origin_last_m1);
   if(copied_m1 <= 0)
     {
      WriteStatus("blocked_origin_m1_copy_failed", "CopyRates(origin, PERIOD_M1) returned no rows", from_time, to_time, origin_selected, custom_selected, create_ok, create_error, copied_m1, 0, 0, 0, origin_first_m1, origin_last_m1, 0, 0, 0, 0, 0, 0, copy_error);
      return;
     }

   if(InpShiftMinutes != 0)
     {
      for(int i = 0; i < copied_m1; i++)
         origin_m1[i].time = (datetime)((long)origin_m1[i].time + shift_seconds);
     }
   datetime target_first_m1 = 0;
   datetime target_last_m1 = 0;
   RateRange(origin_m1, copied_m1, target_first_m1, target_last_m1);

   ResetLastError();
   int updated_m1 = CustomRatesUpdate(InpCustomSymbol, origin_m1);
   int update_error = GetLastError();
   if(updated_m1 <= 0)
     {
      WriteStatus("blocked_custom_rates_update_failed", "CustomRatesUpdate returned no updated rows", from_time, to_time, origin_selected, custom_selected, create_ok, create_error, copied_m1, updated_m1, 0, 0, origin_first_m1, origin_last_m1, target_first_m1, target_last_m1, 0, 0, 0, 0, update_error);
      return;
     }

   Sleep(1000);
   MqlRates custom_m1[];
   MqlRates custom_m5[];
   ResetLastError();
   int copied_custom_m1 = CopyRates(InpCustomSymbol, PERIOD_M1, target_from_time, target_to_time, custom_m1);
   int custom_m1_error = GetLastError();
   ResetLastError();
   int copied_custom_m5 = CopyRates(InpCustomSymbol, PERIOD_M5, target_from_time, target_to_time, custom_m5);
   int custom_m5_error = GetLastError();

   datetime custom_first_m1 = 0;
   datetime custom_last_m1 = 0;
   datetime custom_first_m5 = 0;
   datetime custom_last_m5 = 0;
   RateRange(custom_m1, copied_custom_m1, custom_first_m1, custom_last_m1);
   RateRange(custom_m5, copied_custom_m5, custom_first_m5, custom_last_m5);

   string status = "completed";
   string detail = "custom symbol M1 history copied from origin and M5 visibility verified";
   int last_error = custom_m5_error;
   if(copied_custom_m1 <= 0)
     {
      status = "blocked_custom_m1_visibility_failed";
      detail = "CopyRates(custom, PERIOD_M1) returned no rows after update";
      last_error = custom_m1_error;
     }
   else if(copied_custom_m5 <= 0)
     {
      status = "blocked_custom_m5_visibility_failed";
      detail = "CopyRates(custom, PERIOD_M5) returned no rows after update";
      last_error = custom_m5_error;
     }

   WriteStatus(status, detail, from_time, to_time, origin_selected, custom_selected, create_ok, create_error, copied_m1, updated_m1, copied_custom_m1, copied_custom_m5, origin_first_m1, origin_last_m1, target_first_m1, target_last_m1, custom_first_m1, custom_last_m1, custom_first_m5, custom_last_m5, last_error);
   PrintFormat("[ObsidianPrimeV2][CustomSymbolSeed] status=%s origin=%s custom=%s shift_minutes=%d copied_m1=%d updated_m1=%d custom_m5=%d",
               status, InpOriginSymbol, InpCustomSymbol, InpShiftMinutes, copied_m1, updated_m1, copied_custom_m5);
  }
