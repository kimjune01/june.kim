"""Generate diagram 09: Keywords Are Tiny Circles.

Left panel: keyword points as tiny dots with vast empty space (unmonetized).
Right panel: same points with radii expanded, filling the gaps.

Matches the visual style of existing AdSpace diagrams (matplotlib, colored regions,
white dots, labeled advertisers).
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from matplotlib.colors import to_rgba
from scipy.spatial import Voronoi

# ── Style constants (matching existing diagrams) ──
COLORS = {
    "Nike":        "#F4A460",   # sandy orange
    "Peloton":     "#6A9FD6",   # medium blue
    "GNC":         "#9B72CF",   # purple
    "Whole Foods": "#5CBB5C",   # green
    "Fitbit":      "#3CB4B4",   # teal
}

BG_COLOR = "#F7F7F7"
EMPTY_COLOR = "#E8E8E8"
FONT = "sans-serif"

# ── Advertiser positions (same as diagram 02) ──
advertisers = {
    "Nike":        {"pos": (0.75, 0.45), "bid": 5.0},
    "Peloton":     {"pos": (0.45, 0.62), "bid": 4.0},
    "GNC":         {"pos": (0.82, 0.78), "bid": 2.5},
    "Whole Foods": {"pos": (0.28, 0.76), "bid": 3.0},
    "Fitbit":      {"pos": (0.35, 0.42), "bid": 3.5},
}

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), facecolor="white")
fig.suptitle("Keywords Are Tiny Circles", fontsize=18, fontweight="bold",
             fontfamily=FONT, y=0.97)

# ── Helper: draw power diagram territory ──
def draw_territories(ax, advertisers, sigmas, title, show_empty_label=False):
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.set_title(title, fontsize=13, fontweight="bold", fontfamily=FONT, pad=12)
    ax.set_xlabel("Topic Dimension  (fitness ← → nutrition)", fontsize=9, fontfamily=FONT)
    ax.set_ylabel("Intent Dimension  (browsing ← → purchase-ready)", fontsize=9, fontfamily=FONT)
    ax.tick_params(labelsize=8)

    # Compute power diagram on a grid
    resolution = 500
    x = np.linspace(0, 1, resolution)
    y = np.linspace(0, 1, resolution)
    X, Y = np.meshgrid(x, y)

    names = list(advertisers.keys())
    scores = np.full((len(names), resolution, resolution), -np.inf)

    for i, name in enumerate(names):
        cx, cy = advertisers[name]["pos"]
        bid = advertisers[name]["bid"]
        sigma = sigmas[name]
        dist_sq = (X - cx)**2 + (Y - cy)**2
        scores[i] = np.log(bid) - dist_sq / (sigma**2)

    winner = np.argmax(scores, axis=0)
    max_score = np.max(scores, axis=0)

    # Threshold: if best score is very low, region is "unmonetized"
    # For tiny sigmas, most of the space has score → -inf
    threshold = -50  # anything below this is effectively uncovered

    # Draw colored regions
    rgba_map = np.zeros((resolution, resolution, 4))
    for i, name in enumerate(names):
        color_rgba = to_rgba(COLORS[name], alpha=0.55)
        mask = (winner == i) & (max_score > threshold)
        rgba_map[mask] = color_rgba

    # Unmonetized regions
    empty_mask = max_score <= threshold
    rgba_map[empty_mask] = to_rgba(EMPTY_COLOR, alpha=1.0)

    ax.imshow(rgba_map, origin="lower", extent=[0, 1, 0, 1], aspect="equal")

    # Draw advertiser dots and labels
    for name, info in advertisers.items():
        cx, cy = info["pos"]
        bid = info["bid"]
        sigma = sigmas[name]

        # White dot with dark border
        ax.plot(cx, cy, "o", color="white", markersize=8,
                markeredgecolor="#333333", markeredgewidth=1.5, zorder=5)

        # Label
        label = f"{name}\n(${bid:.1f})"
        ax.annotate(label, (cx, cy), textcoords="offset points",
                    xytext=(0, 12), ha="center", fontsize=7.5,
                    fontfamily=FONT, fontweight="bold",
                    bbox=dict(boxstyle="round,pad=0.2", facecolor="white",
                              edgecolor="#999999", alpha=0.85))

        # Draw circle showing radius (only if visible)
        if sigma > 0.02:
            circle = plt.Circle((cx, cy), sigma, fill=False,
                                edgecolor=COLORS[name], linewidth=1.5,
                                linestyle="--", alpha=0.7)
            ax.add_patch(circle)

    return empty_mask

# ── Left panel: keywords (tiny radii) ──
tiny_sigmas = {name: 0.018 for name in advertisers}
empty1 = draw_territories(ax1, advertisers, tiny_sigmas,
                          "Keywords: σ ≈ 0\n(tiny dots, mostly empty)")

# Add "unmonetized" label
empty_pct1 = np.sum(empty1) / empty1.size * 100
ax1.text(0.5, 0.15, f"{empty_pct1:.0f}% unmonetized",
         ha="center", fontsize=11, fontfamily=FONT, fontweight="bold",
         color="#888888", style="italic",
         transform=ax1.transAxes)

# ── Right panel: expanded radii ──
expanded_sigmas = {
    "Nike":        0.30,
    "Peloton":     0.20,
    "GNC":         0.35,
    "Whole Foods": 0.25,
    "Fitbit":      0.25,
}
empty2 = draw_territories(ax2, advertisers, expanded_sigmas,
                          "Vectors: σ > 0\n(same points, expanded reach)")

empty_pct2 = np.sum(empty2) / empty2.size * 100
if empty_pct2 > 1:
    ax2.text(0.5, 0.15, f"{empty_pct2:.0f}% unmonetized",
             ha="center", fontsize=11, fontfamily=FONT, fontweight="bold",
             color="#888888", style="italic",
             transform=ax2.transAxes)

# ── Arrow between panels ──
fig.text(0.50, 0.50, "expand σ  →", ha="center", va="center",
         fontsize=13, fontfamily=FONT, fontweight="bold", color="#555555")

# ── Legend ──
legend_handles = []
for name in advertisers:
    patch = mpatches.Patch(color=COLORS[name], alpha=0.55, label=name)
    legend_handles.append(patch)
legend_handles.append(mpatches.Patch(color=EMPTY_COLOR, label="Unmonetized"))

fig.legend(handles=legend_handles, loc="lower center", ncol=6,
           fontsize=8, frameon=True, fancybox=True,
           edgecolor="#CCCCCC", facecolor="white")

plt.tight_layout(rect=[0, 0.06, 1, 0.93])
plt.savefig("/Users/junekim/Documents/kimjune01.github.io/assets/09_keywords_are_tiny_circles.png",
            dpi=200, bbox_inches="tight", facecolor="white")
plt.close()
print("Saved 09_keywords_are_tiny_circles.png")
