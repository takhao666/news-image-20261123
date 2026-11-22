#!/usr/bin/env python3
"""Entry point for make.fun news-image-20261123.

Copies the pre-rendered front page (entry.png, built by render.py)
to the grader's output directory as /output/entry.png.
Standard library only; no network; deterministic: both runs write
the same bytes.
"""
import hashlib
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def check_png(path):
    """Minimal PNG validation: signature, IHDR size, IEND present."""
    with open(path, "rb") as f:
        data = f.read()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG file")
    if len(data) < 8 + 25:
        raise ValueError("file too short for an IHDR chunk")
    if data[12:16] != b"IHDR":
        raise ValueError("first chunk is not IHDR")
    width, height = struct.unpack(">II", data[16:24])
    if width > 1024 or height > 1024:
        raise ValueError("image larger than 1024x1024: %dx%d" % (width, height))
    if len(data) > 1048576:
        raise ValueError("image larger than 1 MiB: %d bytes" % len(data))
    # A PNG ends with the 12-byte IEND chunk: length 0, "IEND", CRC.
    if len(data) < 12 or data[-8:-4] != b"IEND":
        raise ValueError("missing IEND chunk")
    return width, height, len(data)


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    width, height, size = check_png(SRC)
    shutil.copyfile(SRC, dest)
    # Verify the copy byte for byte so both grading runs are identical.
    with open(SRC, "rb") as f:
        src_hash = hashlib.sha256(f.read()).hexdigest()
    with open(dest, "rb") as f:
        dst_hash = hashlib.sha256(f.read()).hexdigest()
    if src_hash != dst_hash:
        raise ValueError("copy mismatch: %s != %s" % (src_hash, dst_hash))
    print("wrote %s (%dx%d, %d bytes, sha256 %s)"
          % (dest, width, height, size, src_hash))
    return 0


if __name__ == "__main__":
    sys.exit(main())
