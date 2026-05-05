from __future__ import annotations

from pathlib import Path
from typing import Sequence

from foundation.control_plane.adapter_probe_shortlist import main as shortlist_main


def main(argv: Sequence[str] | None = None) -> int:
    args = list(argv or [])
    if "--root" not in args:
        args.extend(["--root", str(Path(".").resolve())])
    return shortlist_main(args)


if __name__ == "__main__":
    raise SystemExit(main())
