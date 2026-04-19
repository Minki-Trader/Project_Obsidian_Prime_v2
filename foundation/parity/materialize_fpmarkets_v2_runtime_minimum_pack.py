from __future__ import annotations

import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from foundation.parity.materialize_fpmarkets_v2_runtime_pack import main as materialize_runtime_pack_main


def main() -> int:
    return materialize_runtime_pack_main(["--profile", "minimum_0001", *sys.argv[1:]])


if __name__ == "__main__":
    raise SystemExit(main())
