import runpy

from stage_pipelines.stage12 import extratrees_standalone_batch20 as _impl

globals().update({name: getattr(_impl, name) for name in dir(_impl) if not name.startswith("__")})


if __name__ == "__main__":
    runpy.run_module(_impl.__name__, run_name="__main__")
