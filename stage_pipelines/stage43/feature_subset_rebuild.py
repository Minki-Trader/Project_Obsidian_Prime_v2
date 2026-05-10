from __future__ import annotations

from typing import Sequence

from stage_pipelines.auto_campaign_02.independent_runtime_probe import main as campaign_main


def main(argv: Sequence[str] | None = None) -> int:
    return campaign_main(["--stages", "43", *(argv or [])])


if __name__ == "__main__":
    raise SystemExit(main())

