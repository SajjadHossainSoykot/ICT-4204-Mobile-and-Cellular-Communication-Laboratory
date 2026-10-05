"""
Experiment 06: Received Signal Strength-Based Base Station Selection
Course: Mobile and Cellular Communication Laboratory
Course Code: ICT-4204
"""

import numpy as np
import matplotlib.pyplot as plt

# Base stations placed along a straight road (m)
BS_POSITIONS_M = np.array([0.0, 500.0, 1000.0])
MOBILE_POSITIONS_M = np.linspace(1, 999, 500)

RSS_REFERENCE_DBM = -30.0  # reference received level at d0 = 1 m (dBm)
PATH_LOSS_EXPONENT = 3.0

SAMPLE_POSITIONS_M = [100, 300, 500, 700, 900]


def calculate_rss_dbm(mobile_x_m, bs_x_m, rss_ref_dbm, n):
    """Log-distance model: RSS_i(d) = RSS(d0) - 10 n log10(d_i / d0), d0 = 1 m."""
    distance_m = np.abs(mobile_x_m - bs_x_m)
    distance_m = np.maximum(distance_m, 1.0)  # avoid log10(0)
    return rss_ref_dbm - 10 * n * np.log10(distance_m)


def main():
    # RSS from every base station at every mobile position (rows = base stations)
    rss_matrix = np.array([
        calculate_rss_dbm(MOBILE_POSITIONS_M, bs_x, RSS_REFERENCE_DBM, PATH_LOSS_EXPONENT)
        for bs_x in BS_POSITIONS_M
    ])

    # Selection rule: choose the base station with the maximum RSS
    selected_bs = np.argmax(rss_matrix, axis=0) + 1

    # Sample decisions
    for position in SAMPLE_POSITIONS_M:
        idx = np.argmin(np.abs(MOBILE_POSITIONS_M - position))
        values = rss_matrix[:, idx]
        print(
            f"At x={MOBILE_POSITIONS_M[idx]:.0f} m: "
            f"RSS={np.round(values, 2)} dBm -> select BS{selected_bs[idx]}"
        )

    # RSS curves
    plt.figure(figsize=(10, 5))
    for i in range(len(BS_POSITIONS_M)):
        plt.plot(MOBILE_POSITIONS_M, rss_matrix[i],
                 label=f"BS{i+1} at {BS_POSITIONS_M[i]:.0f} m")
    plt.xlabel("Mobile position (m)")
    plt.ylabel("Received signal strength (dBm)")
    plt.title("RSS from Three Base Stations")
    plt.legend()
    plt.grid(True)

    # Selected base station along the path
    plt.figure(figsize=(10, 4))
    plt.step(MOBILE_POSITIONS_M, selected_bs, where="mid")
    plt.xlabel("Mobile position (m)")
    plt.ylabel("Selected base station")
    plt.yticks([1, 2, 3], ["BS1", "BS2", "BS3"])
    plt.title("RSS-Based Base Station Selection")
    plt.grid(True)

    plt.show()


if __name__ == "__main__":
    main()
