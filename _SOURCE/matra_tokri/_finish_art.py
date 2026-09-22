"""Turn raw model output in assets/_raw/ into game-ready art in assets/UI/.

    py -3 _finish_art.py basket            key + trim, report geometry
    py -3 _finish_art.py --all

Two jobs, both of which the model cannot do for us:

1. KEYING. Asked for a transparent background, the image models paint a
   checkerboard — a picture OF transparency. It is cleanly separable: the fake
   background is light and unsaturated, the art is dark-outlined and saturated.
   We flood from the border so only background CONNECTED to the edge is cut;
   a light patch enclosed by the art survives.

   This matters more than it looks. The basket's answer outline is five chained
   drop-shadow passes over its alpha (index.html recipe 21, engine A), and that
   is a dilation — every ragged alpha pixel gets amplified into a visible lump
   on the outline. The alpha has to be clean at the edge, not just roughly right.

2. GEOMETRY. index.html hard-codes numbers taken off the old inline SVG:
   BASKET_W 186, BASKET_CATCH_HALF 84 (the rim half-width), CATCH_Y 512. The
   rim of a generated basket is never at the same proportion, so we measure
   where the rim actually is and print the constants that follow from it.
"""
import os, sys
from collections import deque
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
RAW  = os.path.join(HERE, "_raw")
OUT  = os.path.join(HERE, "UI")

# Full-bleed scenery — keying it would be meaningless.
NOKEY = {"bg_plate"}

# Hand-supplied art that already ships a real alpha channel. Flooding these
# would be, at best, a no-op; at worst it eats a pale highlight that happens to
# touch the edge. Trim and export only.
PREKEYED = {"word_cloud", "hand_nudge", "play_btn", "title", "matra_box", "progress_bar"}

# Full-bleed art that fills the stage but has NO horizon to register against —
# the title screen has no basket standing on the grass, so it is simply scaled
# to the stage rather than run through fit_plate().
COVER = {"cover_bg"}

# Final display width in index.html, in CSS px. We ship at 2x that, as webp.
# The raw stays at generation resolution in _raw/; shipping it would be a 977 KB
# basket drawn into a 186px box, which is the single biggest weight win here.
EXPORT = {
    "basket":     186,
    "cloud_a":    210,
    "cloud_b":    150,
    "cloud_c":    180,
    "nudge_hand":  81,     # object-fit:contain inside the kit's 86x108 box
    "hand_nudge":  86,     # the supplied hand — wider aspect, fits the box by width
    "word_cloud": 204,     # the falling word chip, at its .drop-tile width
    "basket_deep": 186,    # ships as basket.webp + basket_front.webp
    "play_btn":    170,    # the title screen's only control
    "title":       620,    # the cover wordmark
    "matra_box":   100,    # the HUD chip the current matra is written on
    "progress_bar":300,    # the five-slot catch track
}

# Assets that ship as a PAIR of aligned layers. See bowl_front().
SPLIT = {"basket_deep": ("basket", "basket_front")}

# The kit centres the tap ripple on the hand's FINGERTIP, not on the box, so
# swapping the hand art means re-deriving .nh-tapfx's offsets. These are the
# box and ripple-square sizes index.html declares.
NH_BOX = (86.0, 108.0)
NH_FX  = 94.6

# A pixel is fake background if it is UNSATURATED — the model's checkerboard is
# always neutral grey, but it draws a LIGHT one on some assets and a DARK one on
# others (the basket came back light, the pointing hand dark), so lightness is
# not a safe test and only chroma is. White glove and white cloud are neutral
# too, but both are walled off by the navy linework, which is blue enough to
# fail this test — and the flood only ever cuts what the border can reach.
# It also takes the white "sticker rim" the model likes to add, which we want
# gone: the answer outline should hug the object, not a halo around it.
BG_MAX_SAT = 40        # max(r,g,b) - min(r,g,b)


def is_bg(px):
    return (max(px[0], px[1], px[2]) - min(px[0], px[1], px[2])) <= BG_MAX_SAT


def key(im):
    """Cut background connected to the border. Returns RGBA."""
    im = im.convert("RGB")
    w, h = im.size
    px = im.load()
    bg = bytearray(w * h)          # 1 = cut

    q = deque()
    for x in range(w):
        for y in (0, h - 1):
            if is_bg(px[x, y]) and not bg[y * w + x]:
                bg[y * w + x] = 1; q.append((x, y))
    for y in range(h):
        for x in (0, w - 1):
            if is_bg(px[x, y]) and not bg[y * w + x]:
                bg[y * w + x] = 1; q.append((x, y))

    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and not bg[ny * w + nx] and is_bg(px[nx, ny]):
                bg[ny * w + nx] = 1; q.append((nx, ny))

    out = im.convert("RGBA")
    alpha = Image.new("L", (w, h), 255)
    alpha.putdata([0 if v else 255 for v in bg])
    out.putalpha(alpha)
    return out


def trim(im, pad=2):
    bb = im.getchannel("A").getbbox()
    if not bb:
        return im
    l, t, r, b = bb
    l = max(0, l - pad); t = max(0, t - pad)
    r = min(im.width, r + pad); b = min(im.height, b + pad)
    return im.crop((l, t, r, b))


def rim_geometry(im):
    """Widest opaque row near the top = the rim. Feeds BASKET_CATCH_HALF."""
    w, h = im.size
    a = im.getchannel("A").load()
    widest, widest_y = 0, 0
    for y in range(h):
        row = [x for x in range(w) if a[x, y] > 128]
        if row:
            span = row[-1] - row[0] + 1
            if span > widest:
                widest, widest_y = span, y
    return widest, widest_y


# ------------------------------------------------------------ background plate
STAGE_W, STAGE_H = 1333, 750
HORIZON_Y = 465        # 62% of 750 — where index.html's grass break and the
                       # .ground top (369 + 96 header) both already sit.


def find_horizon(im):
    """Row with the biggest vertical jump in mean brightness = sky/grass edge."""
    g = im.convert("L").resize((64, im.height), Image.BILINEAR)
    px = g.load()
    rows = [sum(px[x, y] for x in range(64)) / 64.0 for y in range(im.height)]
    best, best_y = 0.0, im.height // 2
    for y in range(4, im.height - 4):
        d = abs(sum(rows[y:y + 4]) / 4 - sum(rows[y - 4:y]) / 4)
        if d > best:
            best, best_y = d, y
    return best_y


def fit_plate(im):
    """Resize to the stage and slide the horizon onto HORIZON_Y.

    The shift is only ever a few px, so the strip it exposes is filled by
    replicating the edge row — sky at the top, grass at the bottom, both of
    which are flat gradients there. Invisible, and cheaper than regenerating
    until the model happens to land the horizon on the right pixel.
    """
    im = im.convert("RGB").resize((STAGE_W, STAGE_H), Image.LANCZOS)
    y = find_horizon(im)
    dy = HORIZON_Y - y
    print(f"   horizon at y={y} ({100.0*y/STAGE_H:.1f}%), target {HORIZON_Y} -> shift {dy:+d}px")
    if dy == 0:
        return im
    out = Image.new("RGB", (STAGE_W, STAGE_H))
    out.paste(im, (0, dy))
    if dy > 0:                                    # exposed at the top
        out.paste(im.crop((0, 0, STAGE_W, 1)).resize((STAGE_W, dy)), (0, 0))
    else:                                         # exposed at the bottom
        n = -dy
        out.paste(im.crop((0, STAGE_H - 1, STAGE_W, STAGE_H)).resize((STAGE_W, n)),
                  (0, STAGE_H - n))
    return out


# ------------------------------------------------------- two-layer basket split
def bowl_front(im):
    """Cut the FRONT piece out of a front-on basket: the near rim and the body.

    index.html sandwiches a caught word between the whole basket (z4) and this
    piece (z6), so the word is drawn over the bowl's dark interior — it is IN
    the basket — until the near rim covers it. The back layer stays the COMPLETE
    basket on purpose: recipe 21's outline is derived from its alpha, and half a
    basket would outline half a silhouette.

    The cut follows the bowl's inner edge per column rather than a straight line,
    which is the whole reason for doing this in the art instead of with
    clip-path: inset(). The interior is found as the largest connected blob of
    dark WARM pixels — warm excludes the navy linework, largest excludes the
    wicker's own shading, which is many small runs rather than one region.
    """
    im = im.convert("RGBA")
    w, h = im.size
    px = im.load()

    def dark_warm(p):
        r, g, b, a = p
        return a > 128 and (r + g + b) / 3 < 135 and r >= b

    seen = bytearray(w * h)
    best = []
    for sy in range(0, h, 3):                 # seeds on a coarse grid
        for sx in range(0, w, 3):
            if seen[sy * w + sx] or not dark_warm(px[sx, sy]):
                continue
            comp, q = [], deque([(sx, sy)])
            seen[sy * w + sx] = 1
            while q:
                x, y = q.popleft()
                comp.append((x, y))
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < w and 0 <= ny < h and not seen[ny * w + nx] \
                       and dark_warm(px[nx, ny]):
                        seen[ny * w + nx] = 1
                        q.append((nx, ny))
            if len(comp) > len(best):
                best = comp
    if not best:
        raise SystemExit("   ! could not find the bowl interior")

    ys = [p[1] for p in best]
    cols = {}
    for x, y in best:
        if y > cols.get(x, -1):
            cols[x] = y
    widest_y = max(set(ys), key=ys.count)

    # Per-column cut, falling back to the mouth's own mid-line outside it, then
    # smoothed so a stray pixel cannot notch the rim.
    cut = [cols.get(x, widest_y) for x in range(w)]
    R = 6
    cut = [max(cut[max(0, x - R):min(w, x + R + 1)]) for x in range(w)]

    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    op, ip = out.load(), px
    for x in range(w):
        for y in range(cut[x] + 1, h):
            op[x, y] = ip[x, y]
    print(f"   bowl interior: {len(best)}px, widest row y={widest_y} "
          f"({100.0*widest_y/h:.1f}%); cut y {min(cut)}..{max(cut)}")
    return out


def report(name, im):
    w, h = im.size
    a = im.getchannel("A")
    clear = sum(1 for p in a.getdata() if p < 8)
    print(f"   {w}x{h} RGBA — {100.0*clear/(w*h):.0f}% transparent")
    if name == "basket":
        span, y = rim_geometry(im)
        print(f"   widest opaque span: {span}px at y={y} ({100.0*span/w:.1f}% of width, "
              f"{100.0*y/h:.1f}% down)")
        print(f"   -> at BASKET_W 186: BASKET_CATCH_HALF = {round(186 * span / w / 2)}")
    if name in ("nudge_hand", "hand_nudge"):
        # Topmost opaque row is the fingertip; take the middle of that run.
        a = im.getchannel("A").load()
        tip = None
        for y in range(h):
            run = [x for x in range(w) if a[x, y] > 128]
            if run:
                tip = ((run[0] + run[-1]) / 2.0, float(y)); break
        bw, bh = NH_BOX
        s = min(bw / w, bh / h)                       # object-fit: contain
        fx = (bw - w * s) / 2 + tip[0] * s
        fy = (bh - h * s) / 2 + tip[1] * s
        print(f"   fingertip at ({tip[0]:.0f},{tip[1]:.0f}) of the art "
              f"-> ({fx:.1f},{fy:.1f}) in the {bw:.0f}x{bh:.0f} box")
        print(f"   -> .nh-tapfx  left:{fx - NH_FX/2:.2f}px;  top:{fy - NH_FX/2:.2f}px;")


def main():
    args  = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = {a for a in sys.argv[1:] if a.startswith("--")}
    os.makedirs(OUT, exist_ok=True)

    todo = args
    if "--all" in flags:
        todo = [f[:-4] for f in os.listdir(RAW) if f.endswith(".png")]
    if not todo:
        sys.exit("Pass asset names, or --all.")

    for name in todo:
        src = os.path.join(RAW, name + ".png")
        if not os.path.exists(src):
            print(f"!  no raw for {name}"); continue
        print(f">  {name}")
        if name in COVER:
            im = Image.open(src).convert("RGB").resize((STAGE_W, STAGE_H), Image.LANCZOS)
            dst = os.path.join(OUT, name + ".webp")
            im.save(dst, quality=92, method=6)
            print(f"   {im.width}x{im.height} RGB")
            print(f"   -> {os.path.relpath(dst, HERE)}  "
                  f"({os.path.getsize(dst)/1024:.0f} KB)")
            print()
            continue
        if name in NOKEY:
            # Full-bleed scenery: nothing to cut out, but the horizon has to
            # land on the pixel the game's layout constants already assume.
            im = fit_plate(Image.open(src))
            dst = os.path.join(OUT, name + ".webp")
            im.save(dst, quality=92, method=6)
            print(f"   {im.width}x{im.height} RGB\n   -> {os.path.relpath(dst, HERE)}\n")
            continue
        im = Image.open(src).convert("RGBA") if name in PREKEYED else key(Image.open(src))
        im = trim(im)
        report(name, im)

        if name in SPLIT:
            # Split BEFORE resizing, then scale both the same way, so the two
            # layers stay registered to the pixel.
            back_name, front_name = SPLIT[name]
            front = bowl_front(im)
            w2 = EXPORT[name] * 2
            hh = max(1, round(im.height * w2 / im.width))
            for nm, img in ((back_name, im), (front_name, front)):
                o = img.resize((w2, hh), Image.LANCZOS)
                d = os.path.join(OUT, nm + ".webp")
                # LOSSLESS, and only for this pair. The front layer is laid over
                # the back one and its overlap region is meant to be the SAME
                # pixels; compressed separately at q92 they pick up different
                # artefacts, and the difference reads as a seam along the cut.
                o.save(d, lossless=True, method=6, exact=True)
                print(f"   -> {os.path.relpath(d, HERE)}  {o.width}x{o.height}  "
                      f"({os.path.getsize(d)/1024:.0f} KB)")
            span, ry = rim_geometry(im)
            print(f"   BASKET_CATCH_HALF = {round(186 * span / im.width / 2)}   "
                  f"rim {100.0*ry/im.height:.1f}% down -> CATCH_Y = "
                  f"{round(472 + 156 * ry / im.height)}")
            print()
            continue
        if name in EXPORT:
            w2 = EXPORT[name] * 2
            im = im.resize((w2, max(1, round(im.height * w2 / im.width))), Image.LANCZOS)
            print(f"   export @2x of {EXPORT[name]}px -> {im.width}x{im.height}")
        dst = os.path.join(OUT, name + ".webp")
        im.save(dst, quality=92, method=6, exact=True)
        print(f"   -> {os.path.relpath(dst, HERE)}  "
              f"({os.path.getsize(dst)/1024:.0f} KB)\n")


if __name__ == "__main__":
    main()
