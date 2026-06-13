#!/usr/bin/env python3
# Renders the "object" torus (3/4 view, occlusion-aware line art) used in the
# triangulation figure of the Verifiable Knowledge paper. Emits an SVG <g>
# fragment spliced into public/assets/triangulation-light.svg.
import math


OUT = "/tmp/torus-prog.svg"

R = 2.4
r = 1.0
tilt = math.radians(58.0)

cx, cy = 360.0, 116.0
target = (252.0, 62.0, 468.0, 170.0)

stroke = "#adadad"
hidden_stroke = "#c2c2c2"
width = 1.3


def torus(u, v):
    q = R + r * math.cos(v)
    x = q * math.cos(u)
    y = q * math.sin(u)
    z = r * math.sin(v)
    return rotate_x(x, y, z)


def rotate_x(x, y, z):
    ct = math.cos(tilt)
    st = math.sin(tilt)
    return x, y * ct - z * st, y * st + z * ct


def apparent_contour(branch, n=720):
    # n_view . n_surface == 0 after the x-axis tilt:
    # sin(tilt) * sin(u) * cos(v) + cos(tilt) * sin(v) == 0.
    pts = []
    st = math.sin(tilt)
    ct = math.cos(tilt)
    for i in range(n + 1):
        u = 2.0 * math.pi * i / n
        v = math.atan2(-st * math.sin(u), ct) + branch * math.pi
        pts.append(torus(u, v))
    return pts


def param_curve(kind, value, n=720):
    pts = []
    for i in range(n + 1):
        t = 2.0 * math.pi * i / n
        if kind == "u":
            pts.append(torus(value, t))
        else:
            pts.append(torus(t, value))
    return pts


def full_surface_samples(nu=260, nv=130):
    pts = []
    for i in range(nu):
        u = 2.0 * math.pi * i / nu
        for j in range(nv):
            v = 2.0 * math.pi * j / nv
            pts.append(torus(u, v))
    return pts


def bounds(points):
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    return min(xs), min(ys), max(xs), max(ys)


surface = full_surface_samples()
raw_min_x, raw_min_y, raw_max_x, raw_max_y = bounds(surface)
raw_w = raw_max_x - raw_min_x
raw_h = raw_max_y - raw_min_y
tx0, ty0, tx1, ty1 = target
scale = min((tx1 - tx0) / raw_w, (ty1 - ty0) / raw_h)
mid_x = 0.5 * (raw_min_x + raw_max_x)
mid_y = 0.5 * (raw_min_y + raw_max_y)


def map_point(p):
    x, y, _ = p
    return cx + (x - mid_x) * scale, cy + (y - mid_y) * scale


# Coarse depth map in projection space. It is deliberately denser than the
# final path sampling so visibility changes occur at stable arc splits.
Z_W = 420
Z_H = 260
zbuf = [[-1.0e9 for _ in range(Z_W)] for __ in range(Z_H)]


def zcell(x, y):
    ix = int((x - raw_min_x) / raw_w * (Z_W - 1))
    iy = int((y - raw_min_y) / raw_h * (Z_H - 1))
    return max(0, min(Z_W - 1, ix)), max(0, min(Z_H - 1, iy))


for x, y, z in surface:
    ix, iy = zcell(x, y)
    if z > zbuf[iy][ix]:
        zbuf[iy][ix] = z


def visible(p):
    x, y, z = p
    ix, iy = zcell(x, y)
    front = -1.0e9
    for yy in range(max(0, iy - 2), min(Z_H, iy + 3)):
        row = zbuf[yy]
        for xx in range(max(0, ix - 2), min(Z_W, ix + 3)):
            if row[xx] > front:
                front = row[xx]
    return z >= front - 0.055


def smooth_visibility(flags, min_len=18):
    flags = flags[:]
    n = len(flags)
    if n == 0:
        return flags
    changed = True
    while changed:
        changed = False
        start = 0
        while start < n:
            end = start + 1
            while end < n and flags[end] == flags[start]:
                end += 1
            if end - start < min_len:
                left = flags[start - 1] if start > 0 else flags[-2]
                right = flags[end] if end < n else flags[1]
                if left == right and left != flags[start]:
                    for k in range(start, end):
                        flags[k] = left
                    changed = True
            start = end
    flags[-1] = flags[0]
    return flags


def split_by_visibility(points):
    flags = smooth_visibility([visible(p) for p in points])
    return split_by_flags(points, flags)


def split_by_flags(points, flags):
    runs = []
    cur = []
    cur_vis = None
    for p, v in zip(points, flags):
        if cur and v != cur_vis:
            runs.append((cur_vis, cur))
            cur = [cur[-1], p]
        else:
            cur.append(p)
        cur_vis = v
    if len(cur) > 1:
        runs.append((cur_vis, cur))
    return runs


def path_data(points):
    mapped = [map_point(p) for p in points]
    return "M " + " L ".join(f"{x:.2f} {y:.2f}" for x, y in mapped)


def emit_path(points, dashed=False, sw=width, color=None):
    if len(points) < 3:
        return ""
    color = color or (hidden_stroke if dashed else stroke)
    dash = ' stroke-dasharray="4 4"' if dashed else ""
    return (
        f'<path d="{path_data(points)}" fill="none" stroke="{color}" '
        f'stroke-width="{sw:.1f}" stroke-linecap="round" '
        f'stroke-linejoin="round"{dash}/>'
    )


curves = []

# True apparent contour: two branches are enough to form the outside tube
# silhouette and the projected top opening of the torus hole.
curves.append(("outer-contour", apparent_contour(0), 1.3, "solid"))
curves.append(("inner-contour", apparent_contour(1), 1.3, "rim"))

# A few canonical surface rulings make the line art read as a solid torus.
# They are visibility split, so far and underside arcs fall back to dashed.
curves.append(("inner-rim", param_curve("v", math.pi), 1.15, "split"))
curves.append(("front-crown", param_curve("v", math.pi * 0.5), 1.05, "split"))
curves.append(("back-crown", param_curve("v", math.pi * 1.5), 1.05, "split"))

parts = [
    '<g fill="none" stroke-linecap="round" stroke-linejoin="round">'
]

# Hidden lines first, then visible strokes on top.
runs = []
for _, pts, sw, mode in curves:
    if mode == "solid":
        runs.append((True, pts, sw))
    elif mode == "rim":
        flags = [map_point(p)[1] <= cy for p in pts]
        flags[-1] = flags[0]
        for vis, run in split_by_flags(pts, flags):
            runs.append((vis, run, sw))
    else:
        for vis, run in split_by_visibility(pts):
            runs.append((vis, run, sw))

for vis, run, sw in runs:
    if not vis:
        s = emit_path(run, dashed=True, sw=sw)
        if s:
            parts.append("  " + s)

for vis, run, sw in runs:
    if vis:
        s = emit_path(run, dashed=False, sw=sw)
        if s:
            parts.append("  " + s)

parts.append("</g>")

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(parts) + "\n")
