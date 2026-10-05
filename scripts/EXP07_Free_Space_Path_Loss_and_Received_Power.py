"""
Experiment 07: Free-Space Path Loss and Received Power Analysis
(official sheet title: "... Using MATLAB"; implemented here in Python)
Course: Mobile and Cellular Communication Laboratory
Course Code: ICT-4204
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Configurable parameters
FREQUENCY_MHZ = 900.0
TRANSMIT_POWER_DBM = 43.0
TX_GAIN_DBI = 15.0
RX_GAIN_DBI = 0.0
ADDITIONAL_LOSSES_DB = 2.0

DISTANCE_KM = np.linspace(0.1, 20.0, 400)
CHECK_DISTANCES_KM = np.array([0.1, 1, 5, 10, 20], dtype=float)
COMPARISON_FREQUENCIES_MHZ = [700, 900, 1800, 2400]


def fspl_db(distance_km, frequency_mhz):
    """FSPL(dB) = 32.44 + 20 log10(d_km) + 20 log10(f_MHz)."""
    distance_km = np.maximum(distance_km, 1e-9)  # avoid log10(0)
    return 32.44 + 20 * np.log10(distance_km) + 20 * np.log10(frequency_mhz)


def received_power_dbm(distance_km, frequency_mhz):
    """Link budget: Pr = Pt + Gt + Gr - FSPL - L (dBm)."""
    return (
        TRANSMIT_POWER_DBM
        + TX_GAIN_DBI
        + RX_GAIN_DBI
        - fspl_db(distance_km, frequency_mhz)
        - ADDITIONAL_LOSSES_DB
    )


def main():
    # 1. Check table
    table = pd.DataFrame({
        "Distance (km)": CHECK_DISTANCES_KM,
        "FSPL (dB)": np.round(fspl_db(CHECK_DISTANCES_KM, FREQUENCY_MHZ), 2),
        "Received Power (dBm)": np.round(received_power_dbm(CHECK_DISTANCES_KM, FREQUENCY_MHZ), 2),
    })
    print(f"Frequency = {FREQUENCY_MHZ:.0f} MHz, Pt = {TRANSMIT_POWER_DBM:.0f} dBm, "
          f"Gt = {TX_GAIN_DBI:.0f} dBi, Gr = {RX_GAIN_DBI:.0f} dBi, L = {ADDITIONAL_LOSSES_DB:.0f} dB")
    print(table.to_string(index=False))

    path_loss_db = fspl_db(DISTANCE_KM, FREQUENCY_MHZ)
    pr_dbm = received_power_dbm(DISTANCE_KM, FREQUENCY_MHZ)

    # 2. FSPL versus distance
    plt.figure(figsize=(9, 5))
    plt.plot(DISTANCE_KM, path_loss_db)
    plt.xlabel("Distance (km)")
    plt.ylabel("Free-space path loss (dB)")
    plt.title(f"FSPL vs Distance at {FREQUENCY_MHZ:.0f} MHz")
    plt.grid(True)

    # 3. Received power versus distance
    plt.figure(figsize=(9, 5))
    plt.plot(DISTANCE_KM, pr_dbm)
    plt.xlabel("Distance (km)")
    plt.ylabel("Received power (dBm)")
    plt.title(f"Received Power vs Distance at {FREQUENCY_MHZ:.0f} MHz")
    plt.grid(True)

    # 4. Effect of carrier frequency
    plt.figure(figsize=(9, 5))
    for f_mhz in COMPARISON_FREQUENCIES_MHZ:
        plt.plot(DISTANCE_KM, fspl_db(DISTANCE_KM, f_mhz), label=f"{f_mhz} MHz")
    plt.xlabel("Distance (km)")
    plt.ylabel("Free-space path loss (dB)")
    plt.title("Effect of Carrier Frequency on FSPL")
    plt.legend()
    plt.grid(True)

    plt.show()


if __name__ == "__main__":
    main()
