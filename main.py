#!/usr/bin/env python3
"""Entry point for the news-image-20261120 bounty.

Copies the pre-rendered poster (entry.png, drawn by draw.py with PIL)
to the grader's output directory. Standard library only.
"""
import os
import shutil


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    here = os.path.dirname(os.path.abspath(__file__))
    shutil.copyfile(os.path.join(here, "entry.png"),
                    os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
