from __future__ import annotations

from pathlib import Path
from typing import Sequence

from foundation.control_plane.mechanism_role_map import main as role_map_main


def main(argv: Sequence[str] | None = None) -> int:
    args = list(argv or [])
    if "--root" not in args:
        args.extend(["--root", str(Path(".").resolve())])
    return role_map_main(args)
