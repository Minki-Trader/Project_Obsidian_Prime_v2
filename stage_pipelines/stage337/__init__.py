from __future__ import annotations

import sys
from pathlib import Path


_PACKAGE_PATH = Path(__file__).resolve().parent

if sys.platform == "win32":
    _path_text = str(_PACKAGE_PATH)
    if not _path_text.startswith("\\\\?\\"):
        __path__ = ["\\\\?\\" + _path_text]
