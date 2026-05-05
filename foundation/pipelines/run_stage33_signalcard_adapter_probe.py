from __future__ import annotations

from pathlib import Path
from typing import Sequence

from foundation.control_plane.signalcard_adapter_probe import main as signalcard_main


def main(argv: Sequence[str] | None = None) -> int:
    args = list(argv or [])
    if "--root" not in args:
        args.extend(["--root", str(Path(".").resolve())])
    return signalcard_main(args)


if __name__ == "__main__":
    raise SystemExit(main())
