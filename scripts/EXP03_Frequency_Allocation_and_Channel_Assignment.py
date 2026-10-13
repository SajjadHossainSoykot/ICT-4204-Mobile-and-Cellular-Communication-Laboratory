"""Experiment 03: Frequency allocation and channel assignment.

Python translation and simplification of the supplied classmate MATLAB E3 plot.
This is an ADDITIONAL 125-channel illustrative planning example; it does not
replace the existing EXP03 notebook's 70-channel traffic-demand example.

Uses only NumPy and Matplotlib. Run with:
    python EXP03_MATLAB_Style_Visualizations.py
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

# Change these values to try another scenario.
BANDWIDTH_MHZ = 25.0       # illustrative spectrum in EACH direction
CHANNEL_SPACING_KHZ = 200.0
UPLINK_START_MHZ = 890.0
DUPLEX_SPACING_MHZ = 45.0
I, J = 2, 1                # reuse shift: N = I^2 + I*J + J^2 = 7
CELL_RADIUS_KM = 1.0
ASSIGNMENT = "sequential"  # or "interleaved"
GRID_RADIUS = 4            # rings of hexagonal cells shown in the plot


def allocate_channels(total_channels, group_count, method):
    """Assign channel numbers to group IDs 1..N using FCA."""
    if method == "interleaved":
        return np.arange(total_channels) % group_count + 1
    if method == "sequential":
        equal_count, remainder = divmod(total_channels, group_count)
        counts = [equal_count + (group < remainder)
                  for group in range(group_count)]
        return np.repeat(np.arange(1, group_count + 1), counts)
    raise ValueError("ASSIGNMENT must be 'sequential' or 'interleaved'")


def axial_to_xy(q, r, radius):
    """Hex-grid coordinates to kilometers for pointy-top hexagons."""
    return (np.sqrt(3) * radius * (q + r / 2), 1.5 * radius * r)


def hex_vertices(cx, cy, radius):
    """Vertices in consistent order so neighboring hexagons touch."""
    angles = np.deg2rad(np.arange(30, 390, 60))
    return np.column_stack((cx + radius * np.cos(angles),
                            cy + radius * np.sin(angles)))


def make_reuse_grid(i, j, ring_count):
    """Return (q, r, group) for a valid N=i^2+ij+j^2 reuse pattern.

    Two modular coordinates are used so the pattern also works for
    valid cases such as (i,j)=(2,0), where a one-residue trick fails.
    """
    n = i * i + i * j + j * j
    coords = [(q, r)
              for q in range(-ring_count, ring_count + 1)
              for r in range(-ring_count, ring_count + 1)
              if max(abs(q), abs(r), abs(q + r)) <= ring_count]

    def residue(q, r):
        return (((i + j) * q + j * r) % n,
                (-j * q + i * r) % n)

    residue_keys = sorted({residue(q, r) for q, r in coords})
    if len(residue_keys) != n:
        raise ValueError("Use more grid rings to display all frequency groups")
    group_by_key = {key: k + 1 for k, key in enumerate(residue_keys)}
    return [(q, r, group_by_key[residue(q, r)]) for q, r in coords]


def plot_frequency_planning(ul, dl, cell_group, counts, colors, reuse_grid, radius, n):
    """Recreate the four informative views from the MATLAB experiment."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10), constrained_layout=True)
    ax1, ax2, ax3, ax4 = axes.flat

    # 1. Each point is one assigned uplink channel.
    ax1.scatter(ul, cell_group, s=20, c=colors[cell_group - 1])
    ax1.set(xlabel="Uplink frequency (MHz)", ylabel="Cell group",
            title="Uplink Channel Assignment")
    ax1.set_yticks(range(1, n + 1))
    ax1.grid(alpha=0.25)

    # 2. Channel capacity by group (not traffic demand).
    ax2.bar(range(1, n + 1), counts, color=colors, edgecolor="black")
    ax2.set(xlabel="Cell group", ylabel="Number of channels",
            title="Channels Assigned per Cell Group")
    ax2.set_xticks(range(1, n + 1))
    ax2.grid(axis="y", alpha=0.25)

    # 3. Hexagonal pattern: 7 frequencies are reused in distant cells.
    for q, r, group in reuse_grid:
        x, y = axial_to_xy(q, r, radius)
        ax3.add_patch(Polygon(hex_vertices(x, y, radius), closed=True,
                              facecolor=colors[group - 1],
                              edgecolor="black", linewidth=0.7))
        ax3.text(x, y, f"F{group}", ha="center", va="center", fontsize=7)
    ax3.set_aspect("equal", adjustable="box")
    ax3.relim()
    ax3.autoscale_view()
    ax3.axis("off")
    ax3.set_title(f"Hexagonal Frequency Reuse (N = {n})")

    # 4. Each uplink carrier has a downlink partner offset by DUPLEX_SPACING.
    ax4.scatter(ul, np.ones_like(ul), c=colors[cell_group - 1], s=19, marker="s")
    ax4.scatter(dl, np.ones_like(dl) * 2, c=colors[cell_group - 1], s=19, marker="s")
    ax4.set(xlabel="Frequency (MHz)", title="Paired Uplink / Downlink Channels")
    ax4.set_yticks([1, 2], ["Uplink", "Downlink"])
    ax4.set_ylim(0.5, 2.5)
    ax4.grid(alpha=0.25)
    return fig


def main(save_dir=None):
    n = I**2 + I*J + J**2
    if n < 1 or CHANNEL_SPACING_KHZ <= 0 or BANDWIDTH_MHZ <= 0:
        raise ValueError("Enter positive spectrum, channel spacing, and valid reuse indices")
    if CELL_RADIUS_KM <= 0:
        raise ValueError("Cell radius must be positive")

    total = int(np.floor(BANDWIDTH_MHZ * 1000 / CHANNEL_SPACING_KHZ))
    channel_ids = np.arange(1, total + 1)
    cell_group = allocate_channels(total, n, ASSIGNMENT)
    counts = np.bincount(cell_group, minlength=n + 1)[1:]
    uplink_mhz = UPLINK_START_MHZ + (channel_ids - 1) * CHANNEL_SPACING_KHZ / 1000
    downlink_mhz = uplink_mhz + DUPLEX_SPACING_MHZ
    reuse_grid = make_reuse_grid(I, J, GRID_RADIUS)

    # Exact physical check of the reuse distance for shift (I,J).
    x, y = axial_to_xy(I, J, CELL_RADIUS_KM)
    expected_d = CELL_RADIUS_KM * np.sqrt(3 * n)
    assert np.isclose(np.hypot(x, y), expected_d)
    assert len(reuse_grid) > 0 and len(np.unique([v[2] for v in reuse_grid])) == n
    assert counts.sum() == total

    print("EXPERIMENT 03 - ILLUSTRATIVE FREQUENCY PLAN")
    print(f"Cluster size N: {n} (i={I}, j={J})")
    print(f"Paired duplex channels: {total}  (guard bands ignored)")
    print(f"Uplink range: {uplink_mhz[0]:.1f} to {uplink_mhz[-1]:.1f} MHz")
    print(f"Downlink range: {downlink_mhz[0]:.1f} to {downlink_mhz[-1]:.1f} MHz")
    print(f"Co-channel center distance: {expected_d:.3f} km")
    for group, count in enumerate(counts, 1):
        print(f"Group {group}: {int(count)} channels")

    palette = np.array(plt.get_cmap("tab10").colors[:n])
    fig = plot_frequency_planning(uplink_mhz, downlink_mhz,
                                  cell_group, counts, palette,
                                  reuse_grid, CELL_RADIUS_KM, n)
    if save_dir is not None:
        from pathlib import Path
        out = Path(save_dir)
        out.mkdir(parents=True, exist_ok=True)
        fig.savefig(out / "EXP03_Frequency_Planning.png", dpi=170, bbox_inches="tight")
    else:
        plt.show()
    return n, total, counts



main()