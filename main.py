#!/usr/bin/env python3
"""Entry point for make.fun news-image-20261120.

Copies the pre-drawn front-page image (entry.png, built by gen_image.py)
to the grader's output directory. No network, no randomness: the output
bytes are identical on every run.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    # The image is a fixed, pre-drawn asset: copying it (never regenerating
    # or deleting anything) is what makes both grader runs byte-identical.
    shutil.copyfile(os.path.join(HERE, "entry.png"),
                    os.path.join(output_dir, "entry.png"))


if __name__ == "__main__":
    main()
