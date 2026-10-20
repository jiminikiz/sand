#!/usr/bin/env python3
"""Draws the app icons: a sand pile under a falling stream, with a flower.

Pixel art on a 16 x 16 plan, scaled with square cells. Standard library only.
Run from anywhere: python3 scripts/make-icons.py
"""
import struct
import zlib
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent

ART = [
    "................",
    "................",
    ".......t........",
    "................",
    ".......s........",
    "........S.......",
    ".......s........",
    ".......t....p...",
    "......sSs..pyp..",
    ".....sStsS..g...",
    "....SstSsts.g...",
    "...sStsStsSsg...",
    "..tsSsStsSstsSs.",
    ".sStsSstsSsStsSs",
    "sStsSstSsStsSstS",
    "StsSstSsStsSstsS",
]

# Colours from MAT in index.html.
PALETTE = {
    ".": (11, 13, 18),     # page background
    "s": (226, 194, 125),  # sand
    "S": (216, 181, 107),
    "t": (207, 169, 94),
    "g": (72, 168, 67),    # plant
    "p": (246, 165, 192),  # petal
    "y": (255, 211, 77),   # flower heart
}


def render(size, cell):
    """The art at `cell` px per cell, centred on a `size` px square. Its two
    bottom rows of sand carry on out to the edges."""
    span = cell * len(ART)
    pad = (size - span) // 2
    rows = []
    for y in range(size):
        row = []
        for x in range(size):
            ax, ay = (x - pad) // cell, (y - pad) // cell
            is_inside = 0 <= ax < 16 and 0 <= ay < 16
            if is_inside:
                key = ART[ay][ax]
            elif ay >= 14:
                key = ART[14 + (ay - 14) % 2][ax % 16]
            else:
                key = "."
            row.append(PALETTE[key])
        rows.append(row)
    return rows


def write_png(path, rows):
    h, w = len(rows), len(rows[0])
    raw = b"".join(b"\x00" + bytes(c for px in row for c in px) for row in rows)

    def chunk(kind, data):
        crc = zlib.crc32(kind + data) & 0xFFFFFFFF
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", crc)

    path.write_bytes(
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(raw, 9))
        + chunk(b"IEND", b"")
    )
    print(f"wrote {path.relative_to(OUT)} ({w}x{h})")


def main():
    assert all(len(r) == 16 for r in ART) and len(ART) == 16
    write_png(OUT / "icon-192.png", render(192, 12))
    write_png(OUT / "icon-512.png", render(512, 32))
    # Maskable icons get cropped to a circle 80% wide; 288 px of art fits inside it.
    write_png(OUT / "icon-maskable-512.png", render(512, 18))
    write_png(OUT / "apple-touch-icon.png", render(180, 11))


if __name__ == "__main__":
    main()
