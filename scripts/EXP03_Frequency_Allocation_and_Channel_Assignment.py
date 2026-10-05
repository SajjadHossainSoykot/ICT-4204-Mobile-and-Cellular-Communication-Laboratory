"""
Experiment 03: Study of Frequency Allocation and Channel Assignment in Cellular Networks
Course: Mobile and Cellular Communication Laboratory
Course Code: ICT-4204
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Configurable parameters
NUMBER_OF_CELLS = 7
TOTAL_CHANNELS = 70

# Example busy-hour demand: number of simultaneous call requests per cell
CALL_REQUESTS = {
    "Cell 1": 8,
    "Cell 2": 13,
    "Cell 3": 6,
    "Cell 4": 10,
    "Cell 5": 15,
    "Cell 6": 7,
    "Cell 7": 11,
}


def fixed_channel_assignment(total_channels, number_of_cells):
    """Distribute channels cyclically: cell index = ((channel - 1) mod Nc) + 1."""
    assignment = {f"Cell {i+1}": [] for i in range(number_of_cells)}
    for channel in range(1, total_channels + 1):
        cell_index = (channel - 1) % number_of_cells
        assignment[f"Cell {cell_index + 1}"].append(channel)
    return assignment


def evaluate_demand(assignment, call_requests):
    """Compare demand with fixed capacity in every cell."""
    rows = []
    for cell, channels in assignment.items():
        capacity = len(channels)
        demand = call_requests[cell]
        rows.append({
            "Cell": cell,
            "Assigned Channels": capacity,
            "Call Requests": demand,
            "Served Calls": min(capacity, demand),
            "Blocked Calls": max(0, demand - capacity),
            "Idle Channels": max(0, capacity - demand),
        })
    return pd.DataFrame(rows)


def main():
    # 1. Fixed channel assignment
    assignment = fixed_channel_assignment(TOTAL_CHANNELS, NUMBER_OF_CELLS)
    for cell, channels in assignment.items():
        print(f"{cell}: {channels}")
    print()

    # 2. Served, blocked, and idle resources per cell
    df = evaluate_demand(assignment, CALL_REQUESTS)
    print(df.to_string(index=False))
    print()

    # 3. System totals
    print(f"Total requested calls : {df['Call Requests'].sum()}")
    print(f"Total served calls    : {df['Served Calls'].sum()}")
    print(f"Total blocked calls   : {df['Blocked Calls'].sum()}")
    print(f"Total idle channels   : {df['Idle Channels'].sum()}")

    # 4. Demand versus fixed capacity
    x = np.arange(len(df))

    plt.figure(figsize=(10, 5))
    plt.bar(x, df["Call Requests"], label="Call Requests")
    plt.plot(x, df["Assigned Channels"], marker="o", label="Assigned Channels")
    plt.xticks(x, df["Cell"])
    plt.xlabel("Cell")
    plt.ylabel("Number of simultaneous calls / channels")
    plt.title("Fixed Channel Assignment: Demand vs Capacity")
    plt.legend()
    plt.grid(axis="y")

    plt.show()


if __name__ == "__main__":
    main()
