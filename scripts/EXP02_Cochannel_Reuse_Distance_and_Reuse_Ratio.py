"""
Experiment 02: Calculation of Co-channel Reuse Distance and Reuse Ratio
Course: Mobile and Cellular Communication Laboratory
Course Code: ICT-4204
"""

import numpy as np
import matplotlib.pyplot as plt

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


def main():
    # 1. Single example
    N = cluster_size(I_SHIFT, J_SHIFT)
    q = reuse_ratio(N)
    D_km = R_KM * q

    print(f"Shift parameters (i, j) = ({I_SHIFT}, {J_SHIFT})")
    print(f"Cluster size N          = {N}")
    print(f"Cell radius R           = {R_KM:.2f} km")
    print(f"Reuse ratio q           = {q:.4f}")
    print(f"Reuse distance D        = {D_km:.4f} km")
    print()

    # 2. Several valid cluster sizes
    sizes = valid_cluster_sizes(MAX_SHIFT)
    reuse_ratios = reuse_ratio(sizes)
    reuse_distances = R_KM * reuse_ratios

    print("Some valid cluster sizes:", sizes.tolist())

    # 3. Reuse distance versus cluster size
    plt.figure(figsize=(9, 5))
    plt.plot(sizes, reuse_distances, marker="o")
    plt.xlabel("Cluster size, N")
    plt.ylabel("Reuse distance, D (km)")
    plt.title(f"Reuse Distance vs Cluster Size for R = {R_KM:.1f} km")
    plt.grid(True)

    # 4. Reuse ratio versus cluster size
    plt.figure(figsize=(9, 5))
    plt.plot(sizes, reuse_ratios, marker="o")
    plt.xlabel("Cluster size, N")
    plt.ylabel("Reuse ratio, q = D/R")
    plt.title("Reuse Ratio vs Cluster Size")
    plt.grid(True)

    plt.show()


if __name__ == "__main__":
    main()
