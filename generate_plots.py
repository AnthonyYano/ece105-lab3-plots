"""Utilities for generating and plotting synthetic sensor data.

This module provides a helper function ``generate_data`` used by the
notebook and CLI to produce reproducible synthetic temperature readings
for two sensors. It intentionally keeps I/O and plotting separate from
pure data generation so the function is easy to test.
"""
from typing import Tuple

import numpy as np


def generate_data(seed: int) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Generate reproducible synthetic sensor data.

    The function produces 200 time stamps uniformly drawn from 0 to 10
    seconds and two independent Gaussian-distributed temperature sensor
    readings (Sensor A and Sensor B). Returned arrays are sorted by
    increasing timestamp so they are ready for time-ordered plotting.

    Parameters
    ----------
    seed : int
        Integer seed used to initialise ``np.random.default_rng`` for
        reproducible results (for example, the last 4 digits of an ID).

    Returns
    -------
    timestamps : numpy.ndarray
        1-D float64 array of shape (200,) with timestamps in seconds,
        in ascending order.
    sensor_a : numpy.ndarray
        1-D float64 array of shape (200,) containing Sensor A readings
        (mean = 25.0 °C, std = 3.0 °C), ordered to match ``timestamps``.
    sensor_b : numpy.ndarray
        1-D float64 array of shape (200,) containing Sensor B readings
        (mean = 27.0 °C, std = 4.5 °C), ordered to match ``timestamps``.

    Notes
    -----
    Uses the modern NumPy Generator API ``np.random.default_rng`` for
    reproducibility and better statistical properties than the legacy
    global RNG.
    """
    rng = np.random.default_rng(int(seed))
    n = 200

    timestamps = rng.uniform(0.0, 10.0, size=n).astype(np.float64)
    sensor_a = rng.normal(loc=25.0, scale=3.0, size=n).astype(np.float64)
    sensor_b = rng.normal(loc=27.0, scale=4.5, size=n).astype(np.float64)

    order = np.argsort(timestamps)
    timestamps = timestamps[order]
    sensor_a = sensor_a[order]
    sensor_b = sensor_b[order]

    return timestamps, sensor_a, sensor_b


if __name__ == "__main__":
    # smoke test
    t, a, b = generate_data(2143)
    print(f"Generated: timestamps={t.shape}, sensor_a={a.shape}, sensor_b={b.shape}")
