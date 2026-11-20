#!/usr/bin/env python3
"""Entry point for news-image-20261120.

Copies the front-page image this repository holds (entry.png, drawn by
draw.py) to the grader's output directory as entry.png. Standard library
only, no network, no randomness: every run writes the same bytes.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("wrote", dst, os.path.getsize(dst), "bytes")


if __name__ == "__main__":
    main()
