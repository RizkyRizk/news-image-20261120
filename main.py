#!/usr/bin/env python3
"""Publish the finished front page.

The image itself is drawn by gen_image.py and committed as entry.png.
This entrypoint only places a copy of it where the grader looks:
the directory named by MAKEFUN_OUTPUT_DIR (or "out" when unset).
"""

from __future__ import annotations

import os
import shutil
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "entry.png"
DEFAULT_OUTPUT = "out"


def publish() -> Path:
    target_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or DEFAULT_OUTPUT)
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / SOURCE.name
    shutil.copyfile(SOURCE, target)
    return target


if __name__ == "__main__":
    publish()
