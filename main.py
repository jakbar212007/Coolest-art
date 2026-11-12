"""Make the coolest art - entry program.

Writes one piece of art to /output/entry.png by copying the image
bundled with this repository. Deterministic: no network, no randomness,
both runs write identical bytes.

After copying, the program verifies the output is a whole PNG within
the competition caps (at most 1 MiB, at most 1024 by 1024 pixels) by
reading its header and its IEND trailer, and exits non-zero if it is not.
"""
import os
import shutil
import struct

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "art.png")
DST = "/output/entry.png"
MAX_BYTES = 1048576
MAX_SIDE = 1024


def png_size(path):
    with open(path, "rb") as f:
        head = f.read(33)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG file")
    width, height = struct.unpack(">II", head[16:24])
    return width, height


def png_is_whole(path):
    with open(path, "rb") as f:
        f.seek(-12, os.SEEK_END)
        tail = f.read(12)
    return tail == b"\x00\x00\x00\x00IEND\xaeB`\x82"


def main():
    os.makedirs("/output", exist_ok=True)
    shutil.copyfile(SRC, DST)
    size = os.path.getsize(DST)
    if size > MAX_BYTES:
        raise SystemExit("entry.png is %d bytes, over the 1 MiB cap" % size)
    width, height = png_size(DST)
    if width > MAX_SIDE or height > MAX_SIDE:
        raise SystemExit(
            "entry.png is %dx%d, over the 1024x1024 cap" % (width, height)
        )
    if not png_is_whole(DST):
        raise SystemExit("entry.png is truncated: missing IEND chunk")


if __name__ == "__main__":
    main()
