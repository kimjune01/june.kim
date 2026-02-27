"""Generate diagram 10: Relocation Fees — Hotelling drift vs. stable positions.

Left panel: No relocation fees — all advertisers drift toward density peak,
            arrows showing movement, chaotic overlapping territories.
Right panel: With relocation fees — advertisers at natural positions, clean territories.

Matches visual style of existing AdSpace diagrams.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from matplotlib.colors import to_rgba

COLORS = {
    "Nike":        "#F4A460",
    "Peloton":     "#6A9FD6",
    "GNC":         "#9B72CF",
    "Whole Foods": "#5CBB5C",
    "Fitbit":      "#3CB4B4",
}

FONT = "sans-serif"
EMPTY_COLOR = "#E8E8E8"

# Natural positions (where advertisers actually belong)
natural_positions = {
    "Nike":        {"pos": (0.75, 0.45), "bid": 5.0, "sigma": 0.30},
    "Peloton":     {"pos": (0.45, 0.62), "bid": 4.0, "sigma": 0.20},
    "GNC":         {"pos": (0.82, 0.78), "bid": 2.5, "sigma": 0.35},
    "Whole Foods": {"pos": (0.28, 0.76), "bid": 3.0, "sigma": 0.25},
    "Fitbit":      {"pos": (0.35, 0.42), "bid": 3.5, "sigma": 0.25},
}

# Density peak
DENSITY_PEAK = (0.50, 0.55)

# Drifted positions (everyone gravitates toward density peak)
drifted_positions = {}
drift_strength = 0.55
for name, info in natural_positions.items():
    nx, ny = info["pos"]
    dx = DENSITY_PEAK[0] - nx
    dy = DENSITY_PEAK[1] - ny
    drifted_positions[name] = {
        "pos": (nx + drift_strength * dx, ny + drift_strength * dy),
        "bid": info["bid"],
        "sigma": info["sigma"] * 0.7,  # also narrow toward center
    }


def compute_territories(ax, advertisers, resolution=500):
    x = np.linspace(0, 1, resolution)
    y = np.linspace(0, 1, resolution)
    X, Y = np.meshgrid(x, y)

    names = list(advertisers.keys())
    scores = np.full((len(names), resolution, resolution), -np.inf)

    for i, name in enumerate(names):
        cx, cy = advertisers[name]["pos"]
        bid = advertisers[name]["bid"]
        sigma = advertisers[name]["sigma"]
        dist_sq = (X - cx)**2 + (Y - cy)**2
        scores[i] = np.log(bid) - dist_sq / (sigma**2)

    winner = np.argmax(scores, axis=0)

    rgba_map = np.zeros((resolution, resolution, 4))
    for i, name in enumerate(names):
        color_rgba = to_rgba(COLORS[name], alpha=0.50)
        mask = winner == i
        rgba_map[mask] = color_rgba

    ax.imshow(rgba_map, origin="lower", extent=[0, 1, 0, 1], aspect="equal")
    return names


def draw_density_contours(ax):
    """Draw impression density as subtle contour rings around the peak."""
    x = np.linspace(0, 1, 300)
    y = np.linspace(0, 1, 300)
    X, Y = np.meshgrid(x, y)
    Z = np.exp(-((X - DENSITY_PEAK[0])**2 + (Y - DENSITY_PEAK[1])**2) / (2 * 0.18**2))
    ax.contour(X, Y, Z, levels=[0.3, 0.5, 0.7, 0.9],
               colors="#888888", linewidths=0.6, linestyles=":", alpha=0.5)
    ax.text(DENSITY_PEAK[0], DENSITY_PEAK[1] + 0.08, "density\npeak",
            ha="center", va="bottom", fontsize=7, color="#777777",
            fontfamily=FONT, style="italic")


def draw_panel(ax, advertisers, title, draw_arrows_from=None):
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.set_title(title, fontsize=12, fontweight="bold", fontfamily=FONT, pad=12)
    ax.set_xlabel("Topic Dimension", fontsize=9, fontfamily=FONT)
    ax.set_ylabel("Intent Dimension", fontsize=9, fontfamily=FONT)
    ax.tick_params(labelsize=8)

    draw_density_contours(ax)
    compute_territories(ax, advertisers)

    for name, info in advertisers.items():
        cx, cy = info["pos"]
        bid = info["bid"]

        # White dot
        ax.plot(cx, cy, "o", color="white", markersize=8,
                markeredgecolor="#333333", markeredgewidth=1.5, zorder=5)

        # Label
        label = f"{name}\n(${bid:.1f})"
        ax.annotate(label, (cx, cy), textcoords="offset points",
                    xytext=(0, 12), ha="center", fontsize=7,
                    fontfamily=FONT, fontweight="bold",
                    bbox=dict(boxstyle="round,pad=0.2", facecolor="white",
                              edgecolor="#999999", alpha=0.85),
                    zorder=6)

        # Draw drift arrows (natural → drifted)
        if draw_arrows_from is not None:
            nx, ny = draw_arrows_from[name]["pos"]
            dx = cx - nx
            dy = cy - ny
            ax.annotate("", xy=(cx, cy), xytext=(nx, ny),
                        arrowprops=dict(arrowstyle="-|>", color="#CC3333",
                                        lw=1.8, connectionstyle="arc3,rad=0.1"),
                        zorder=4)
            # Ghost dot at natural position
            ax.plot(nx, ny, "o", color="#CCCCCC", markersize=6,
                    markeredgecolor="#999999", markeredgewidth=1, alpha=0.6, zorder=3)


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), facecolor="white")
fig.suptitle("Hotelling Drift vs. Relocation Fees",
             fontsize=17, fontweight="bold", fontfamily=FONT, y=0.97)

# Left: no relocation fees (drifted positions, with arrows from natural)
draw_panel(ax1, drifted_positions,
           "Without Relocation Fees\n(everyone drifts to the center)",
           draw_arrows_from=natural_positions)

# Right: with relocation fees (natural positions, stable)
draw_panel(ax2, natural_positions,
           "With Relocation Fees\n(advertisers stay where they belong)")

# Arrow between panels
fig.text(0.50, 0.50, "add λ · d²  →", ha="center", va="center",
         fontsize=13, fontfamily=FONT, fontweight="bold", color="#555555")

# Legend
legend_handles = []
for name in natural_positions:
    patch = mpatches.Patch(color=COLORS[name], alpha=0.50, label=name)
    legend_handles.append(patch)

fig.legend(handles=legend_handles, loc="lower center", ncol=5,
           fontsize=8, frameon=True, fancybox=True,
           edgecolor="#CCCCCC", facecolor="white")

plt.tight_layout(rect=[0, 0.06, 1, 0.93])
plt.savefig("/Users/junekim/Documents/kimjune01.github.io/assets/10_relocation_fees.png",
            dpi=200, bbox_inches="tight", facecolor="white")
plt.close()
print("Saved 10_relocation_fees.png")
