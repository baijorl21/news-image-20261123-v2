#!/usr/bin/env python3
"""Entry program for make.fun bounty news-image-20261123.

The bounty asks for one image summing up the world news of Monday
23 November 2026, written to /output/entry.png. The picture lives in this
repository as entry.png (drawn from scratch by make_image.py with PIL);
this program simply copies those exact bytes to the output path, so every
run produces an identical file. Standard library only, no network.

For a local test outside the grader's container, point MAKEFUN_OUTPUT_DIR
at a scratch directory:

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
import sys
from pathlib import Path


def main() -> None:
    source = Path(__file__).resolve().parent / "entry.png"
    if not source.is_file():
        print(f"entry image missing: {source}", file=sys.stderr)
        raise SystemExit(1)
    destination_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    destination_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination_dir / "entry.png")


if __name__ == "__main__":
    main()
