#ifndef OBSIDIAN_PRIME_MODEL_RUNTIME_MQH
#define OBSIDIAN_PRIME_MODEL_RUNTIME_MQH

#ifndef OP_DEFAULT_FEATURE_COUNT
#define OP_DEFAULT_FEATURE_COUNT 58
#endif

class COpModelRuntime
  {
private:
   long   m_handle;
   bool   m_ready;
   string m_model_path;
   string m_model_id;
   bool   m_common_files;
   bool   m_use_cpu_only;
   bool   m_no_conversion;
   bool   m_set_output_shape;
   int    m_feature_count;
   long   m_output_count;
   ulong  m_input_shape[];
   ulong  m_label_shape[];
   ulong  m_probability_shape[];
   float  m_input[];
   long   m_label[];
   float  m_probability[];
   uint   m_create_flags;
   uint   m_run_flags;

   int EffectiveFeatureCount()
     {
      if(m_feature_count > 0)
         return m_feature_count;
      return OP_DEFAULT_FEATURE_COUNT;
     }

   bool IsFiniteOutputValue(const double value)
     {
      return (MathIsValidNumber(value) && MathAbs(value) < (EMPTY_VALUE / 2.0));
     }

   void BuildShapes()
     {
      const int feature_count = EffectiveFeatureCount();

      ArrayResize(m_input_shape, 2);
      m_input_shape[0] = 1;
      m_input_shape[1] = (ulong)feature_count;

      ArrayResize(m_label_shape, 1);
      m_label_shape[0] = 1;

      ArrayResize(m_probability_shape, 2);
      m_probability_shape[0] = 1;
      m_probability_shape[1] = 3;

      ArrayResize(m_input, feature_count);
      ArrayResize(m_label, 1);
      ArrayResize(m_probability, 3);
      ArrayInitialize(m_input, 0.0f);
      ArrayInitialize(m_label, 0);
      ArrayInitialize(m_probability, 0.0f);
     }

   void BuildFlags()
     {
      m_create_flags = ONNX_LOGLEVEL_WARNING;
      if(m_common_files)
         m_create_flags |= ONNX_COMMON_FOLDER;

      m_run_flags = ONNX_LOGLEVEL_WARNING;
      if(m_use_cpu_only)
         m_run_flags |= ONNX_USE_CPU_ONLY;
      if(m_no_conversion)
         m_run_flags |= ONNX_NO_CONVERSION;
     }

   bool SetOutputShapes(string &reason)
     {
      reason = "";
      if(!m_set_output_shape)
         return true;

      ResetLastError();
      if(m_output_count == 1)
        {
         if(!OnnxSetOutputShape(m_handle, 0, m_probability_shape))
           {
            reason = StringFormat("onnx_set_probability_output_shape_failed:%d", GetLastError());
            return false;
           }
         return true;
        }

      if(m_output_count == 2)
        {
         if(!OnnxSetOutputShape(m_handle, 0, m_label_shape))
           {
            reason = StringFormat("onnx_set_label_output_shape_failed:%d", GetLastError());
            return false;
           }

         ResetLastError();
         if(!OnnxSetOutputShape(m_handle, 1, m_probability_shape))
           {
            reason = StringFormat("onnx_set_probability_output_shape_failed:%d", GetLastError());
            return false;
           }
         return true;
        }

      reason = StringFormat("onnx_output_count_unsupported:%d", (int)m_output_count);
      return false;
     }

public:
   COpModelRuntime()
     {
      m_handle = INVALID_HANDLE;
      m_ready = false;
      m_model_path = "";
      m_model_id = "";
      m_common_files = true;
      m_use_cpu_only = true;
      m_no_conversion = false;
      m_set_output_shape = true;
      m_feature_count = OP_DEFAULT_FEATURE_COUNT;
      m_output_count = 0;
      m_create_flags = 0;
      m_run_flags = 0;
      ArrayResize(m_input_shape, 0);
      ArrayResize(m_label_shape, 0);
      ArrayResize(m_probability_shape, 0);
      ArrayResize(m_input, 0);
      ArrayResize(m_label, 0);
      ArrayResize(m_probability, 0);
     }

   void Configure(const string model_path,
                  const string model_id,
                  const bool common_files,
                  const bool use_cpu_only,
                  const bool no_conversion,
                  const bool set_output_shape,
                  const int feature_count)
     {
      m_model_path = model_path;
      m_model_id = model_id;
      m_common_files = common_files;
      m_use_cpu_only = use_cpu_only;
      m_no_conversion = no_conversion;
      m_set_output_shape = set_output_shape;
      m_feature_count = feature_count > 0 ? feature_count : OP_DEFAULT_FEATURE_COUNT;
     }

   string ModelId() const
     {
      return m_model_id;
     }

   bool IsReady() const
     {
      return (m_ready && m_handle != INVALID_HANDLE);
     }

   bool Init(string &reason)
     {
      reason = "";
      m_ready = false;

      if(m_model_path == "")
        {
         reason = "onnx_model_path_empty";
         return false;
        }

      BuildShapes();
      BuildFlags();

      ResetLastError();
      m_handle = OnnxCreate(m_model_path, m_create_flags);
      if(m_handle == INVALID_HANDLE)
        {
         reason = StringFormat("onnx_create_failed:%d", GetLastError());
         return false;
        }

      const long input_count = OnnxGetInputCount(m_handle);
      m_output_count = OnnxGetOutputCount(m_handle);
      if(input_count != 1 || (m_output_count != 1 && m_output_count != 2))
        {
         reason = StringFormat("onnx_io_count_mismatch:inputs=%d:outputs=%d", (int)input_count, (int)m_output_count);
         Deinit();
         return false;
        }

      ResetLastError();
      if(!OnnxSetInputShape(m_handle, 0, m_input_shape))
        {
         reason = StringFormat("onnx_set_input_shape_failed:%d", GetLastError());
         Deinit();
         return false;
        }

      if(!SetOutputShapes(reason))
        {
         Deinit();
         return false;
        }

      m_ready = true;
      return true;
     }

   void Deinit()
     {
      if(m_handle != INVALID_HANDLE)
        {
         OnnxRelease(m_handle);
         m_handle = INVALID_HANDLE;
        }
      m_output_count = 0;
      m_ready = false;
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

      if(!IsReady())
        {
         reason = "onnx_not_ready";
         return false;
        }

      const int feature_count = EffectiveFeatureCount();
      if(ArraySize(features) != feature_count)
        {
         reason = StringFormat("feature_count_mismatch:expected=%d:actual=%d", feature_count, ArraySize(features));
         return false;
        }

      for(int i = 0; i < feature_count; i++)
        {
         const double value = features[i];
         if(!MathIsValidNumber(value) || MathAbs(value) >= (EMPTY_VALUE / 2.0))
           {
            reason = StringFormat("feature_nonfinite_at:%d", i);
            return false;
           }
         m_input[i] = (float)value;
        }

      ArrayInitialize(m_label, 0);
      ArrayInitialize(m_probability, 0.0f);

      ResetLastError();
      bool ok = false;
      if(m_output_count == 1)
         ok = OnnxRun(m_handle, m_run_flags, m_input, m_probability);
      else if(m_output_count == 2)
         ok = OnnxRun(m_handle, m_run_flags, m_input, m_label, m_probability);
      else
        {
         reason = StringFormat("onnx_output_count_unsupported:%d", (int)m_output_count);
         return false;
        }

      if(!ok)
        {
         reason = StringFormat("onnx_run_failed:%d", GetLastError());
         return false;
        }

      p_short = (double)m_probability[0];
      p_flat = (double)m_probability[1];
      p_long = (double)m_probability[2];

      if(!IsFiniteOutputValue(p_short) || !IsFiniteOutputValue(p_flat) || !IsFiniteOutputValue(p_long))
        {
         reason = "onnx_output_nonfinite";
         return false;
        }

      return true;
     }
  };

#endif
