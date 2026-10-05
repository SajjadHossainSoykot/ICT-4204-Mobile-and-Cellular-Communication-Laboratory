"""
Experiment 09: Cellular Traffic, Channel Capacity, and Erlang-B Blocking Probability Analysis
Course: Mobile and Cellular Communication Laboratory
Course Code: ICT-4204
"""

import numpy as np
import matplotlib.pyplot as plt

# Configurable parameters (course-style example)
OFFERED_TRAFFIC_ERLANGS = 78.3
CHANNELS = 90
MEAN_HOLDING_TIME_S = 100.0
TARGET_GOS = 0.02  # 2% blocking target

TRAFFIC_RANGE = np.linspace(1, 120, 300)
CHANNEL_SETS = [60, 75, 90, 105]
CHANNEL_RANGE = np.arange(70, 111)


def erlang_b(offered_traffic, channels):
    """Erlang-B by the stable recursion B_n = A B_{n-1} / (n + A B_{n-1}), B_0 = 1."""
    B = 1.0
    for n in range(1, channels + 1):
        B = (offered_traffic * B) / (n + offered_traffic * B)
    return B


def minimum_channels_for_gos(offered_traffic, target_blocking, max_channels=500):
    """Smallest number of channels whose Erlang-B blocking meets the target."""
    for n_channels in range(1, max_channels + 1):
        if erlang_b(offered_traffic, n_channels) <= target_blocking:
            return n_channels
    return None


def main():
    # 1. Blocking for the example
    blocking_probability = erlang_b(OFFERED_TRAFFIC_ERLANGS, CHANNELS)
    carried_traffic = OFFERED_TRAFFIC_ERLANGS * (1 - blocking_probability)
    blocked_traffic = OFFERED_TRAFFIC_ERLANGS * blocking_probability

    print(f"Offered traffic       : {OFFERED_TRAFFIC_ERLANGS:.2f} Erlangs")
    print(f"Number of channels    : {CHANNELS}")
    print(f"Blocking probability  : {blocking_probability:.6f}")
    print(f"Blocking percentage   : {100*blocking_probability:.3f}%")
    print(f"Carried traffic       : {carried_traffic:.3f} Erlangs")
    print(f"Blocked traffic       : {blocked_traffic:.3f} Erlangs")
    print()

    # 2. Calls per hour: Q = 3600 A / T_s
    calls_per_hour = 3600 * OFFERED_TRAFFIC_ERLANGS / MEAN_HOLDING_TIME_S
    print(f"With A = {OFFERED_TRAFFIC_ERLANGS:.1f} Erlangs")
    print(f"and mean holding time = {MEAN_HOLDING_TIME_S:.0f} s,")
    print(f"calls per hour = {calls_per_hour:.1f} ≈ {round(calls_per_hour)} calls/hour")
    print()

    # 3. Minimum channels for the target GoS
    min_channels = minimum_channels_for_gos(OFFERED_TRAFFIC_ERLANGS, TARGET_GOS)
    print(f"Minimum channels for A={OFFERED_TRAFFIC_ERLANGS:.1f} Erlangs")
    print(f"at GoS B <= {TARGET_GOS:.2%}: {min_channels}")

    # 4. Blocking versus offered traffic
    plt.figure(figsize=(9, 5))
    for n_channels in CHANNEL_SETS:
        blocking = [erlang_b(A, n_channels) for A in TRAFFIC_RANGE]
        plt.plot(TRAFFIC_RANGE, blocking, label=f"{n_channels} channels")
    plt.xlabel("Offered traffic, A (Erlangs)")
    plt.ylabel("Blocking probability")
    plt.title("Erlang-B Blocking Probability vs Offered Traffic")
    plt.legend()
    plt.grid(True)

    # 5. Blocking versus number of channels
    blocking_by_channels = np.array([erlang_b(OFFERED_TRAFFIC_ERLANGS, n) for n in CHANNEL_RANGE])
    plt.figure(figsize=(9, 5))
    plt.plot(CHANNEL_RANGE, blocking_by_channels, marker="o")
    plt.axhline(TARGET_GOS, linestyle="--", label=f"{TARGET_GOS:.0%} GoS target")
    plt.xlabel("Number of traffic channels")
    plt.ylabel("Blocking probability")
    plt.title(f"Blocking vs Channel Capacity at A = {OFFERED_TRAFFIC_ERLANGS:.1f} Erlangs")
    plt.legend()
    plt.grid(True)

    plt.show()


if __name__ == "__main__":
    main()
