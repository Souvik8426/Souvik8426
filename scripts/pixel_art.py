#!/usr/bin/env python3
"""Generate the pixel-art assets used by the profile README.

Outputs (all written to Assets/pixel/):
  banner.svg          animated header: pixel-font name, starfield, city skyline
  title-<slug>.svg    pixel-font section titles
  divider.svg         animated pixel divider
  footer.svg          "thanks for playing" footer with blinking PRESS START

Run from the repository root:  python3 scripts/pixel_art.py
No dependencies beyond the Python standard library.
"""

from __future__ import annotations

import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "Assets" / "pixel"

# Palette (neon-on-night, works on both GitHub light and dark backgrounds
# because every asset carries its own dark background).
BG = "#0b0f1a"
BG2 = "#141a33"
CYAN = "#00e5ff"
MAGENTA = "#ff2bd6"
YELLOW = "#ffd400"
GREEN = "#39ff14"
WHITE = "#e6edf3"
DIM = "#3a4466"

# --------------------------------------------------------------------------
# 5x7 bitmap font
# --------------------------------------------------------------------------
FONT: dict[str, list[str]] = {
    "A": [" ### ", "#   #", "#   #", "#####", "#   #", "#   #", "#   #"],
    "B": ["#### ", "#   #", "#   #", "#### ", "#   #", "#   #", "#### "],
    "C": [" ####", "#    ", "#    ", "#    ", "#    ", "#    ", " ####"],
    "D": ["#### ", "#   #", "#   #", "#   #", "#   #", "#   #", "#### "],
    "E": ["#####", "#    ", "#    ", "#### ", "#    ", "#    ", "#####"],
    "F": ["#####", "#    ", "#    ", "#### ", "#    ", "#    ", "#    "],
    "G": [" ####", "#    ", "#    ", "#  ##", "#   #", "#   #", " ####"],
    "H": ["#   #", "#   #", "#   #", "#####", "#   #", "#   #", "#   #"],
    "I": ["#####", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "#####"],
    "J": ["  ###", "   # ", "   # ", "   # ", "#  # ", "#  # ", " ##  "],
    "K": ["#   #", "#  # ", "# #  ", "##   ", "# #  ", "#  # ", "#   #"],
    "L": ["#    ", "#    ", "#    ", "#    ", "#    ", "#    ", "#####"],
    "M": ["#   #", "## ##", "# # #", "# # #", "#   #", "#   #", "#   #"],
    "N": ["#   #", "##  #", "# # #", "#  ##", "#   #", "#   #", "#   #"],
    "O": [" ### ", "#   #", "#   #", "#   #", "#   #", "#   #", " ### "],
    "P": ["#### ", "#   #", "#   #", "#### ", "#    ", "#    ", "#    "],
    "Q": [" ### ", "#   #", "#   #", "#   #", "# # #", "#  # ", " ## #"],
    "R": ["#### ", "#   #", "#   #", "#### ", "# #  ", "#  # ", "#   #"],
    "S": [" ####", "#    ", "#    ", " ### ", "    #", "    #", "#### "],
    "T": ["#####", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "  #  "],
    "U": ["#   #", "#   #", "#   #", "#   #", "#   #", "#   #", " ### "],
    "V": ["#   #", "#   #", "#   #", "#   #", "#   #", " # # ", "  #  "],
    "W": ["#   #", "#   #", "#   #", "# # #", "# # #", "## ##", "#   #"],
    "X": ["#   #", "#   #", " # # ", "  #  ", " # # ", "#   #", "#   #"],
    "Y": ["#   #", "#   #", " # # ", "  #  ", "  #  ", "  #  ", "  #  "],
    "Z": ["#####", "    #", "   # ", "  #  ", " #   ", "#    ", "#####"],
    "0": [" ### ", "#   #", "#  ##", "# # #", "##  #", "#   #", " ### "],
    "1": ["  #  ", " ##  ", "  #  ", "  #  ", "  #  ", "  #  ", " ### "],
    "2": [" ### ", "#   #", "    #", "   # ", "  #  ", " #   ", "#####"],
    "3": ["#### ", "    #", "    #", " ### ", "    #", "    #", "#### "],
    "4": ["   # ", "  ## ", " # # ", "#  # ", "#####", "   # ", "   # "],
    "5": ["#####", "#    ", "#### ", "    #", "    #", "#   #", " ### "],
    "6": [" ### ", "#    ", "#    ", "#### ", "#   #", "#   #", " ### "],
    "7": ["#####", "    #", "   # ", "  #  ", " #   ", " #   ", " #   "],
    "8": [" ### ", "#   #", "#   #", " ### ", "#   #", "#   #", " ### "],
    "9": [" ### ", "#   #", "#   #", " ####", "    #", "    #", " ### "],
    " ": ["     "] * 7,
    ">": ["#    ", " #   ", "  #  ", "   # ", "  #  ", " #   ", "#    "],
    "_": ["     "] * 6 + ["#####"],
    "-": ["     ", "     ", "     ", "#####", "     ", "     ", "     "],
    ".": ["     "] * 5 + ["  ## ", "  ## "],
    "/": ["    #", "    #", "   # ", "  #  ", " #   ", "#    ", "#    "],
    "@": [" ### ", "#   #", "# ###", "# # #", "# ###", "#    ", " ####"],
    "&": [" ##  ", "#  # ", "#  # ", " ##  ", "# # #", "#  # ", " ## #"],
    "!": ["  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "     ", "  #  "],
    "$": ["  #  ", " ####", "# #  ", " ### ", "  # #", "#### ", "  #  "],
    ":": ["     ", "  ## ", "  ## ", "     ", "  ## ", "  ## ", "     "],
}
GLYPH_W, GLYPH_H, GAP = 5, 7, 1


def text_width(text: str, scale: int) -> int:
    return (len(text) * (GLYPH_W + GAP) - GAP) * scale


def pixel_text(text: str, x: int, y: int, scale: int, fill: str) -> str:
    """Render text as one <path> of filled squares (no fonts needed)."""
    parts = []
    cx = x
    for ch in text.upper():
        glyph = FONT.get(ch, FONT[" "])
        for row, line in enumerate(glyph):
            col = 0
            while col < GLYPH_W:
                if line[col] == "#":
                    run = col
                    while run < GLYPH_W and line[run] == "#":
                        run += 1
                    px, py = cx + col * scale, y + row * scale
                    parts.append(f"M{px} {py}h{(run - col) * scale}v{scale}h-{(run - col) * scale}z")
                    col = run
                else:
                    col += 1
        cx += (GLYPH_W + GAP) * scale
    return f'<path fill="{fill}" d="{"".join(parts)}"/>'


def svg(width: int, height: int, body: str, label: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" shape-rendering="crispEdges" role="img" aria-label="{label}">'
        f"<title>{label}</title>{body}</svg>\n"
    )


# --------------------------------------------------------------------------
# Banner
# --------------------------------------------------------------------------
def banner() -> str:
    rnd = random.Random(8426)
    W, H = 1200, 320
    body = []

    # Banded "dithered" sky
    bands = [BG, "#0d1222", "#0f152b", "#111833", BG2]
    band_h = H // len(bands)
    for i, c in enumerate(bands):
        body.append(f'<rect x="0" y="{i * band_h}" width="{W}" height="{band_h + 1}" fill="{c}"/>')
    # checker dither between bands
    for i in range(1, len(bands)):
        y = i * band_h - 4
        d = "".join(f"M{x} {y + (x // 4 % 2) * 4}h4v4h-4z" for x in range(0, W, 8))
        body.append(f'<path fill="{bands[i]}" d="{d}"/>')

    # Twinkling stars
    for _ in range(70):
        x, y = rnd.randrange(0, W, 4), rnd.randrange(0, 200, 4)
        if 200 < x < 1010 and 60 < y < 200:  # keep the title area clean
            continue
        size = rnd.choice([4, 4, 4, 8])
        color = rnd.choice([WHITE, WHITE, CYAN, MAGENTA, YELLOW])
        dur = rnd.uniform(1.5, 4.5)
        begin = rnd.uniform(0, 3)
        body.append(
            f'<rect x="{x}" y="{y}" width="{size}" height="{size}" fill="{color}" opacity="0.8">'
            f'<animate attributeName="opacity" values="0.15;1;0.15" dur="{dur:.2f}s" '
            f'begin="{begin:.2f}s" repeatCount="indefinite"/></rect>'
        )

    # Pixel moon
    moon = ["  ####  ", " ###### ", "####### ", "######  ", "######  ", "####### ", " ###### ", "  ####  "]
    for r, line in enumerate(moon):
        for c, ch in enumerate(line):
            if ch == "#":
                body.append(f'<rect x="{1060 + c * 8}" y="{30 + r * 8}" width="8" height="8" fill="{YELLOW}"/>')

    # Skyline with blinking windows
    x = 0
    while x < W:
        bw = rnd.choice([40, 48, 56, 64, 72])
        bh = rnd.choice([48, 64, 80, 96, 112])
        top = H - bh
        body.append(f'<rect x="{x}" y="{top}" width="{bw}" height="{bh}" fill="#070a12"/>')
        body.append(f'<rect x="{x}" y="{top}" width="{bw}" height="4" fill="{DIM}"/>')
        for wy in range(top + 12, H - 8, 16):
            for wx in range(x + 8, x + bw - 8, 12):
                if rnd.random() < 0.35:
                    color = rnd.choice([YELLOW, CYAN, MAGENTA])
                    if rnd.random() < 0.3:
                        dur = rnd.uniform(2, 6)
                        body.append(
                            f'<rect x="{wx}" y="{wy}" width="4" height="8" fill="{color}">'
                            f'<animate attributeName="opacity" values="1;1;0;1" dur="{dur:.2f}s" '
                            f'repeatCount="indefinite"/></rect>'
                        )
                    else:
                        body.append(f'<rect x="{wx}" y="{wy}" width="4" height="8" fill="{color}" opacity="0.85"/>')
        x += bw + rnd.choice([0, 4, 8])

    # Title with offset shadow
    title = "SOUVIK RUHIDAS"
    scale = 9
    tw = text_width(title, scale)
    tx, ty = (W - tw) // 2 // scale * scale, 72
    body.append(pixel_text(title, tx + scale, ty + scale, scale, MAGENTA))
    body.append(pixel_text(title, tx, ty, scale, CYAN))

    # Subtitle + blinking cursor
    sub = "> FRONTEND DEVELOPER"
    s = 4
    sw = text_width(sub, s)
    sx, sy = (W - sw - 6 * s) // 2, ty + GLYPH_H * scale + 28
    body.append(pixel_text(sub, sx, sy, s, GREEN))
    body.append(
        f'<rect x="{sx + sw + 2 * s}" y="{sy}" width="{5 * s}" height="{7 * s}" fill="{GREEN}">'
        f'<animate attributeName="opacity" values="1;1;0;0" dur="1s" repeatCount="indefinite"/></rect>'
    )

    # CRT scanlines
    scan = "".join(f"M0 {y}h{W}v2h-{W}z" for y in range(0, H, 4))
    body.append(f'<path fill="#000" opacity="0.18" d="{scan}"/>')
    return svg(W, H, "".join(body), "Souvik Ruhidas — Frontend Developer")


# --------------------------------------------------------------------------
# Section titles
# --------------------------------------------------------------------------
def title(text: str, accent: str) -> str:
    s = 4
    pad_x, pad_y = 20, 14
    icon_w = 4 * s + 16
    tw = text_width(text, s)
    W = tw + icon_w + pad_x * 2
    H = GLYPH_H * s + pad_y * 2
    b = 4  # pixel border thickness
    body = [
        # notched-corner frame
        f'<path fill="{accent}" d="M{b} 0h{W - 2 * b}v{b}h{b}v{H - 2 * b}h-{b}v{b}h-{W - 2 * b}v-{b}h-{b}v-{H - 2 * b}h{b}z"/>',
        f'<rect x="{b}" y="{b}" width="{W - 2 * b}" height="{H - 2 * b}" fill="{BG}"/>',
    ]
    # blinking arrow icon
    ix, iy = pad_x, pad_y
    arrow = ["#   ", "##  ", "### ", "####", "### ", "##  ", "#   "]
    d = "".join(
        f"M{ix + c * s} {iy + r * s}h{s}v{s}h-{s}z"
        for r, line in enumerate(arrow)
        for c, ch in enumerate(line)
        if ch == "#"
    )
    body.append(
        f'<path fill="{accent}" d="{d}"><animate attributeName="opacity" values="1;0.2;1" '
        f'dur="1.2s" repeatCount="indefinite"/></path>'
    )
    body.append(pixel_text(text, pad_x + icon_w, pad_y, s, WHITE))
    return svg(W, H, "".join(body), text.title())


# --------------------------------------------------------------------------
# Divider
# --------------------------------------------------------------------------
def divider() -> str:
    W, H, s = 1200, 12, 12
    colors = [CYAN, CYAN, MAGENTA, MAGENTA, YELLOW, YELLOW, GREEN, GREEN]
    tile = len(colors) * s
    cells = "".join(
        f'<rect x="{i * s}" y="0" width="{s - 4}" height="{H}" fill="{colors[i % len(colors)]}"/>'
        for i in range(W // s + len(colors))
    )
    body = (
        f'<g>{cells}<animateTransform attributeName="transform" type="translate" '
        f'from="0 0" to="-{tile} 0" dur="2s" repeatCount="indefinite"/></g>'
    )
    return svg(W, H, body, "divider")


# --------------------------------------------------------------------------
# Footer
# --------------------------------------------------------------------------
def footer() -> str:
    W, H = 1200, 150
    body = [f'<rect width="{W}" height="{H}" fill="{BG}"/>']
    line1, s1 = "THANKS FOR PLAYING!", 6
    x1 = (W - text_width(line1, s1)) // 2
    body.append(pixel_text(line1, x1 + s1, 30 + s1, s1, MAGENTA))
    body.append(pixel_text(line1, x1, 30, s1, YELLOW))
    line2, s2 = "PRESS START TO COLLABORATE", 3
    x2 = (W - text_width(line2, s2)) // 2
    body.append(
        f'<g>{pixel_text(line2, x2, 30 + 7 * s1 + 26, s2, WHITE)}'
        f'<animate attributeName="opacity" values="1;1;0;0" dur="1.2s" repeatCount="indefinite"/></g>'
    )
    scan = "".join(f"M0 {y}h{W}v2h-{W}z" for y in range(0, H, 4))
    body.append(f'<path fill="#000" opacity="0.18" d="{scan}"/>')
    return svg(W, H, "".join(body), "Thanks for playing! Press start to collaborate")


SECTIONS = {
    "whoami": ("WHOAMI", CYAN),
    "stack": ("TECH STACK", MAGENTA),
    "projects": ("FEATURED PROJECTS", YELLOW),
    "stats": ("PLAYER STATS", GREEN),
    "arcade": ("ARCADE", CYAN),
}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "banner.svg").write_text(banner())
    (OUT / "divider.svg").write_text(divider())
    (OUT / "footer.svg").write_text(footer())
    for slug, (text, accent) in SECTIONS.items():
        (OUT / f"title-{slug}.svg").write_text(title(text, accent))
    print("wrote", ", ".join(sorted(p.name for p in OUT.iterdir())))


if __name__ == "__main__":
    main()
