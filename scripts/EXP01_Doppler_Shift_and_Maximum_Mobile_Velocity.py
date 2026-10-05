"""
Experiment 01: Calculation of Doppler Shift and Maximum Mobile Velocity
Course: Mobile and Cellular Communication Laboratory
Course Code: ICT-4204
"""

import numpy as np
import matplotlib.pyplot as plt

# Physical constant
C = 3e8  # speed of light (m/s)

# Configurable parameters
CARRIER_FREQUENCY_HZ = 900e6     # carrier frequency (Hz)
MOBILE_SPEED_KMH = 72.0          # mobile speed (km/h)
MEASURED_MAX_DOPPLER_HZ = 100.0  # measured maximum Doppler used for the inverse problem (Hz)


def max_doppler_shift(speed_ms, carrier_hz):
    """Maximum Doppler shift f_m = v * f_c / c (Hz)."""
    return speed_ms * carrier_hz / C


def max_velocity_from_doppler(max_doppler_hz, carrier_hz):
    """Maximum mobile velocity v_max = f_m * c / f_c (m/s)."""
    return max_doppler_hz * C / carrier_hz


def main():
    # 1. Maximum Doppler shift for the chosen speed
    mobile_speed_ms = MOBILE_SPEED_KMH / 3.6
    wavelength_m = C / CARRIER_FREQUENCY_HZ
    max_doppler_hz = mobile_speed_ms / wavelength_m

    print(f"Carrier frequency : {CARRIER_FREQUENCY_HZ/1e6:.1f} MHz")
    print(f"Mobile speed      : {MOBILE_SPEED_KMH:.1f} km/h = {mobile_speed_ms:.2f} m/s")
    print(f"Wavelength        : {wavelength_m:.4f} m")
    print(f"Maximum Doppler   : {max_doppler_hz:.2f} Hz")
    print()

    # 2. Inverse problem: velocity from a measured maximum Doppler shift
    estimated_speed_ms = max_velocity_from_doppler(MEASURED_MAX_DOPPLER_HZ, CARRIER_FREQUENCY_HZ)
    estimated_speed_kmh = estimated_speed_ms * 3.6

    print(f"For a measured maximum Doppler of {MEASURED_MAX_DOPPLER_HZ:.1f} Hz:")
    print(f"Estimated speed = {estimated_speed_ms:.2f} m/s")
    print(f"Estimated speed = {estimated_speed_kmh:.2f} km/h")

    # 3. Doppler shift versus arrival angle: f_d = f_m * cos(theta)
    angles_deg = np.linspace(0, 360, 361)
    doppler_hz = max_doppler_hz * np.cos(np.deg2rad(angles_deg))

    plt.figure(figsize=(9, 5))
    plt.plot(angles_deg, doppler_hz)
    plt.xlabel("Arrival angle, θ (degrees)")
    plt.ylabel("Doppler shift, fd (Hz)")
    plt.title("Doppler Shift vs Arrival Angle")
    plt.grid(True)

    # 4. Maximum Doppler shift versus mobile speed
    speeds_kmh = np.linspace(0, 140, 141)
    max_doppler_vs_speed = max_doppler_shift(speeds_kmh / 3.6, CARRIER_FREQUENCY_HZ)

    plt.figure(figsize=(9, 5))
    plt.plot(speeds_kmh, max_doppler_vs_speed)
    plt.xlabel("Mobile speed (km/h)")
    plt.ylabel("Maximum Doppler shift, fm (Hz)")
    plt.title("Maximum Doppler Shift vs Mobile Speed")
    plt.grid(True)

    plt.show()


if __name__ == "__main__":
    main()
