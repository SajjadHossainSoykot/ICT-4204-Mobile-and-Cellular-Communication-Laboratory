"""
Experiment 05: Simulation of Handover Between Two Cellular Cells
Course: Mobile and Cellular Communication Laboratory
Course Code: ICT-4204
"""

import numpy as np
import matplotlib.pyplot as plt

# Base station positions on a straight road (m)
BS1_POSITION_M = 0.0
BS2_POSITION_M = 1000.0

# Propagation / handover settings
RSS_AT_1M_DBM = -30.0          # reference received level at d0 = 1 m (dBm)
PATH_LOSS_EXPONENT = 3.0
HYSTERESIS_DB = 3.0            # hysteresis margin H (dB)
HANDOVER_THRESHOLD_DBM = -105.0  # handover threshold T_H (dBm)

# Mobile path (starts/ends 1 m from the sites so log10(0) is never evaluated)
MOBILE_POSITIONS_M = np.linspace(1, 999, 500)


def received_signal_dbm(distance_m, rss_ref_dbm=-30.0, n=3.0):
    """Log-distance model: RSS(d) = RSS(d0) - 10 n log10(d / d0), d0 = 1 m."""
    distance_m = np.maximum(distance_m, 1.0)  # avoid log10(0)
    return rss_ref_dbm - 10 * n * np.log10(distance_m)


def simulate_handover(positions, rss1, rss2, hysteresis_db, threshold_dbm):
    """Return the serving cell at each position and the first handover point."""
    serving_cell = []
    current = 1
    handover_position_m = None

    for x, r1, r2 in zip(positions, rss1, rss2):
        if current == 1:
            if (r2 > r1 + hysteresis_db) and (r1 < threshold_dbm):
                current = 2
                if handover_position_m is None:
                    handover_position_m = x
        else:
            if (r1 > r2 + hysteresis_db) and (r2 < threshold_dbm):
                current = 1
        serving_cell.append(current)

    return np.array(serving_cell), handover_position_m


def main():
    rss1 = received_signal_dbm(np.abs(MOBILE_POSITIONS_M - BS1_POSITION_M),
                               RSS_AT_1M_DBM, PATH_LOSS_EXPONENT)
    rss2 = received_signal_dbm(np.abs(MOBILE_POSITIONS_M - BS2_POSITION_M),
                               RSS_AT_1M_DBM, PATH_LOSS_EXPONENT)

    serving_cell, handover_position_m = simulate_handover(
        MOBILE_POSITIONS_M, rss1, rss2, HYSTERESIS_DB, HANDOVER_THRESHOLD_DBM
    )

    print(f"Hysteresis margin   : {HYSTERESIS_DB:.1f} dB")
    print(f"Handover threshold  : {HANDOVER_THRESHOLD_DBM:.1f} dBm")
    if handover_position_m is not None:
        print(f"First handover point: {handover_position_m:.1f} m")
    else:
        print("First handover point: no handover occurred")

    # RSS from both base stations
    plt.figure(figsize=(10, 5))
    plt.plot(MOBILE_POSITIONS_M, rss1, label="RSS from BS1")
    plt.plot(MOBILE_POSITIONS_M, rss2, label="RSS from BS2")
    plt.axhline(HANDOVER_THRESHOLD_DBM, linestyle="--", label="Handover threshold")
    if handover_position_m is not None:
        plt.axvline(handover_position_m, linestyle="--", label="Handover point")
    plt.xlabel("Mobile position (m)")
    plt.ylabel("Received signal strength (dBm)")
    plt.title("RSS-Based Handover Between Two Cells")
    plt.legend()
    plt.grid(True)

    # Serving cell along the path
    plt.figure(figsize=(10, 4))
    plt.step(MOBILE_POSITIONS_M, serving_cell, where="mid")
    plt.xlabel("Mobile position (m)")
    plt.ylabel("Serving cell")
    plt.yticks([1, 2], ["Cell 1", "Cell 2"])
    plt.title("Serving Cell Along the Mobile Path")
    plt.grid(True)

    plt.show()


if __name__ == "__main__":
    main()
