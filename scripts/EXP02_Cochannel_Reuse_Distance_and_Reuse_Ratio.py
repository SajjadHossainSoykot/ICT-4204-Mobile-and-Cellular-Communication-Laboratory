"""
Experiment 02: Calculation of Co-channel Reuse Distance and Reuse Ratio
Course: Mobile and Cellular Communication Laboratory
Course Code: ICT-4204
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Patch
from matplotlib.lines import Line2D

# Configurable parameters
R_KM = 1.0   # cell radius (km)
I_SHIFT = 2  # hexagonal shift parameter i
J_SHIFT = 1  # hexagonal shift parameter j
MAX_SHIFT = 4  # largest i and j used to list valid cluster sizes


def cluster_size(i, j):
    """Valid hexagonal cluster size N = i^2 + i*j + j^2."""
    return i**2 + i * j + j**2


def reuse_ratio(n_cluster):
    """Co-channel reuse ratio q = D/R = sqrt(3N)."""
    return np.sqrt(3 * n_cluster)


def valid_cluster_sizes(max_shift):
    """All valid cluster sizes for 0 <= i, j <= max_shift (excluding i = j = 0)."""
    sizes = set()
    for ii in range(0, max_shift + 1):
        for jj in range(0, max_shift + 1):
            if ii == 0 and jj == 0:
                continue
            sizes.add(cluster_size(ii, jj))
    return np.array(sorted(sizes))


def plot_frequency_reuse_pattern(r_km=1.0, i=2, j=1):
    """
    Plot a textbook-quality hexagonal cellular frequency reuse pattern for cluster size N = i^2 + ij + j^2.
    Highlights two nearest co-channel cells (F1) separated by reuse distance D = R * sqrt(3*N).
    Uses manually computed pointy-top hexagon vertices with Polygon to guarantee gap-free tiling.
    """
    n_cluster = cluster_size(i, j)
    q = reuse_ratio(n_cluster)
    d_km = r_km * q
    r_draw_km = r_km * 1.002  # drawing overlap to eliminate raster hairlines

    # Pointy-top hexagon vertex angles (points at top and bottom: 30°, 90°, 150°, 210°, 270°, 330°)
    angles = np.array([30, 90, 150, 210, 270, 330]) * np.pi / 180.0

    def get_hexagon_vertices(center, radius):
        """Return 6x2 array of vertices for a pointy-top hexagon centered at center."""
        x = center[0] + radius * np.cos(angles)
        y = center[1] + radius * np.sin(angles)
        return np.column_stack([x, y])

    # Basis displacement vectors for pointy-top hexagon centers (adjacent center distance = sqrt(3)*R)
    d_step = np.sqrt(3) * r_km
    u1 = np.array([d_step, 0.0])
    u2 = np.array([d_step * 0.5, d_step * np.sqrt(3) / 2.0])

    # Coordinates of reference cell (0, 0) and nearest co-channel cell (i, j)
    ref_idx = (0, 0)
    target_idx = (i, j)
    c_ref = ref_idx[0] * u1 + ref_idx[1] * u2
    c_target = target_idx[0] * u1 + target_idx[1] * u2

    # Numerical verification of distance between cell centers
    center_distance_km = np.linalg.norm(c_target - c_ref)
    distance_verified = np.isclose(center_distance_km, d_km)

    print(f"Cluster size N                  = {n_cluster}")
    print(f"Cell radius R                   = {r_km:.2f} km")
    print(f"Reuse ratio q                   = {q:.4f}")
    print(f"Co-channel reuse distance D     = {d_km:.4f} km")
    print(f"Distance between cell centers   = {center_distance_km:.4f} km")
    print(f"Numerical verification (dist==D): {distance_verified}")
    print()

    # Construct hexagonal grid cells with frequency group assignment F1..F7
    cells_to_draw = []
    for u in range(-3, 5):
        for v in range(-2, 4):
            pos = u * u1 + v * u2
            if -5.5 <= pos[0] <= 8.5 and -4.0 <= pos[1] <= 5.0:
                freq = ((2 * u + 3 * v) % 7) + 1
                cells_to_draw.append((u, v, pos, freq))

    fig, ax = plt.subplots(figsize=(11, 8.5))

    # Draw each cell using Polygon with manually computed vertices
    for u, v, pos, freq in cells_to_draw:
        is_ref = (u == ref_idx[0] and v == ref_idx[1])
        is_target = (u == target_idx[0] and v == target_idx[1])
        is_highlighted = is_ref or is_target

        verts = get_hexagon_vertices(pos, r_draw_km)
        facecolor = '#FFCC00' if is_highlighted else '#F5F5F7'
        edgecolor = 'black'
        linewidth = 2.4 if is_highlighted else 1.0

        poly = Polygon(
            verts, closed=True,
            facecolor=facecolor, edgecolor=edgecolor, linewidth=linewidth,
            zorder=2 if is_highlighted else 1
        )
        ax.add_patch(poly)

        # Label cells
        if is_ref:
            ax.text(pos[0], pos[1] + 0.32, "F1", ha='center', va='center',
                    fontsize=11, fontweight='bold', color='#8A3B00', zorder=4)
            ax.text(pos[0], pos[1] - 0.32, "(Ref)", ha='center', va='center',
                    fontsize=8.5, fontweight='bold', color='#8A3B00', zorder=4)
        elif is_target:
            ax.text(pos[0], pos[1] + 0.32, "F1", ha='center', va='center',
                    fontsize=11, fontweight='bold', color='#8A3B00', zorder=4)
            ax.text(pos[0], pos[1] - 0.32, "(Reused)", ha='center', va='center',
                    fontsize=8.5, fontweight='bold', color='#8A3B00', zorder=4)
        elif (u, v) == (1, 0):
            ax.text(pos[0], pos[1] + 0.32, f"F{freq}", ha='center', va='center',
                    fontsize=9.5, color='#333333', zorder=3)
        elif (u, v) == (2, 0):
            ax.text(pos[0], pos[1] - 0.32, f"F{freq}", ha='center', va='center',
                    fontsize=9.5, color='#333333', zorder=3)
        else:
            ax.text(pos[0], pos[1], f"F{freq}", ha='center', va='center',
                    fontsize=9.5, color='#333333', zorder=3)

    # Highlight cell centers
    ax.plot(c_ref[0], c_ref[1], 'o', color='#8A3B00', markersize=6, zorder=6)
    ax.plot(c_target[0], c_target[1], 'o', color='#8A3B00', markersize=6, zorder=6)

    # 1. Co-channel reuse distance D line
    ax.plot([c_ref[0], c_target[0]], [c_ref[1], c_target[1]],
            color='#D32F2F', linestyle='--', linewidth=2.2, zorder=5)

    mid_d = (c_ref + c_target) / 2.0
    ax.text(
        mid_d[0] - 0.25, mid_d[1] + 0.35,
        f"Reuse Distance D = R√21 ≈ {d_km:.2f} km",
        fontsize=9.5, fontweight='bold', color='#B71C1C',
        ha='center', va='bottom',
        bbox=dict(boxstyle='round,pad=0.28', facecolor='#FFFFFF', edgecolor='#D32F2F', linewidth=1.2, alpha=0.96),
        zorder=7
    )

    # 2. Cell radius R line in reference cell (center to bottom-left vertex)
    v_bl = c_ref + np.array([-np.sqrt(3) / 2.0 * r_km, -0.5 * r_km])
    ax.plot([c_ref[0], v_bl[0]], [c_ref[1], v_bl[1]],
            color='#1976D2', linestyle='-', linewidth=2.4, zorder=5)
    ax.plot(v_bl[0], v_bl[1], 's', color='#1976D2', markersize=4, zorder=6)
    mid_r = (c_ref + v_bl) / 2.0
    ax.text(
        mid_r[0] - 0.25, mid_r[1] - 0.25,
        f"Radius R = {r_km:.1f} km",
        fontsize=9, fontweight='bold', color='#0D47A1',
        ha='center', va='top',
        bbox=dict(boxstyle='round,pad=0.2', facecolor='#FFFFFF', edgecolor='#1976D2', linewidth=1.0, alpha=0.96),
        zorder=7
    )

    # 3. Shift trajectory (i = 2, j = 1)
    step_i_end = c_ref + i * u1
    ax.annotate("", xy=step_i_end, xytext=c_ref,
                arrowprops=dict(arrowstyle="-|>", color='#2E7D32', linestyle=':', lw=2.2, mutation_scale=14),
                zorder=4)
    ax.annotate("", xy=c_target, xytext=step_i_end,
                arrowprops=dict(arrowstyle="-|>", color='#2E7D32', linestyle=':', lw=2.2, mutation_scale=14),
                zorder=4)

    ax.text(step_i_end[0] / 2.0, step_i_end[1] - 0.45, f"Step 1: Move i = {i} cells",
            ha='center', va='top', fontsize=8.5, color='#1B5E20', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#E8F5E9', edgecolor='#2E7D32', alpha=0.92),
            zorder=6)

    mid_j = (step_i_end + c_target) / 2.0
    ax.text(mid_j[0] + 0.35, mid_j[1] - 0.2, f"Step 2: Turn 60°\nmove j = {j} cell",
            ha='left', va='center', fontsize=8.5, color='#1B5E20', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#E8F5E9', edgecolor='#2E7D32', alpha=0.92),
            zorder=6)

    # Labels, title, grid, equal aspect ratio
    ax.set_xlabel("Distance (km)", fontsize=11, fontweight='semibold')
    ax.set_ylabel("Distance (km)", fontsize=11, fontweight='semibold')
    ax.set_title(
        f"Cellular Frequency Reuse Pattern (N = {n_cluster}, i = {i}, j = {j}, R = {r_km:.1f} km, D ≈ {d_km:.2f} km)",
        fontsize=12, fontweight='bold', pad=14
    )
    ax.set_aspect('equal')
    ax.grid(True, linestyle=':', alpha=0.45)

    # Clear legend
    legend_elements = [
        Patch(facecolor='#FFCC00', edgecolor='black', linewidth=1.8, label='Reused co-channel cells (F1)'),
        Patch(facecolor='#F5F5F7', edgecolor='black', linewidth=1.0, label='Co-existing cluster cells (F2–F7)'),
        Line2D([0], [0], color='#D32F2F', linestyle='--', linewidth=2.2, label=f'Reuse distance D = {d_km:.2f} km'),
        Line2D([0], [0], color='#1976D2', linestyle='-', linewidth=2.4, label=f'Cell radius R = {r_km:.1f} km'),
        Line2D([0], [0], color='#2E7D32', linestyle=':', linewidth=2.2, label=f'Shift path (i = {i}, j = {j})'),
    ]
    ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(-0.02, 1.02),
              framealpha=0.95, edgecolor='#BDBDBD', fontsize=9.2)

    all_x = [p[0] for _, _, p, _ in cells_to_draw]
    all_y = [p[1] for _, _, p, _ in cells_to_draw]
    ax.set_xlim(min(all_x) - 1.2, max(all_x) + 1.2)
    ax.set_ylim(min(all_y) - 1.2, max(all_y) + 1.6)

    plt.tight_layout()


def main():
    # 1. Single example calculations
    N = cluster_size(I_SHIFT, J_SHIFT)
    q = reuse_ratio(N)
    D_km = R_KM * q

    print(f"Shift parameters (i, j) = ({I_SHIFT}, {J_SHIFT})")
    print(f"Cluster size N          = {N}")
    print(f"Cell radius R           = {R_KM:.2f} km")
    print(f"Reuse ratio q           = {q:.4f}")
    print(f"Reuse distance D        = {D_km:.4f} km")
    print()

    # 2. Cellular frequency reuse pattern visualization
    plot_frequency_reuse_pattern(R_KM, I_SHIFT, J_SHIFT)

    # 3. Several valid cluster sizes
    sizes = valid_cluster_sizes(MAX_SHIFT)
    reuse_ratios = reuse_ratio(sizes)
    reuse_distances = R_KM * reuse_ratios

    print("Some valid cluster sizes:", sizes.tolist())

    # 4. Reuse distance versus cluster size
    plt.figure(figsize=(9, 5))
    plt.plot(sizes, reuse_distances, marker="o")
    plt.xlabel("Cluster size, N")
    plt.ylabel("Reuse distance, D (km)")
    plt.title(f"Reuse Distance vs Cluster Size for R = {R_KM:.1f} km")
    plt.grid(True)

    # 5. Reuse ratio versus cluster size
    plt.figure(figsize=(9, 5))
    plt.plot(sizes, reuse_ratios, marker="o")
    plt.xlabel("Cluster size, N")
    plt.ylabel("Reuse ratio, q = D/R")
    plt.title("Reuse Ratio vs Cluster Size")
    plt.grid(True)

    plt.show()


if __name__ == "__main__":
    main()
