#!/usr/bin/env python3
"""Entry point for news-image-20261120.

Copies the pre-made entry.png held beside this file to
$MAKEFUN_OUTPUT_DIR/entry.png (default /output). Standard library only,
no network, deterministic: both runs write identical bytes.
"""

import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.isfile(src):
        print("entry.png not found next to main.py", file=sys.stderr)
        return 1
    out_dir = (os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output").strip()
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    if os.path.getsize(dst) != os.path.getsize(src):
        print("copy incomplete: size mismatch", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
