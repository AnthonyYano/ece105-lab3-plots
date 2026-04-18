"""Utilities for generating and plotting synthetic sensor data.

This module provides a helper function ``generate_data`` used by the
notebook and CLI to produce reproducible synthetic temperature readings
for two sensors. It intentionally keeps I/O and plotting separate from
pure data generation so the function is easy to test.
"""
from typing import Tuple

import numpy as np
import matplotlib.pyplot as plt


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

def plot_scatter(ax, timestamps: np.ndarray, sensor_a: np.ndarray, sensor_b: np.ndarray,
                 *, sensor_a_kwargs: dict = None, sensor_b_kwargs: dict = None,
                 title: str = "Sensor readings vs Time (scatter)") -> None:
    """Draw scatter markers for two sensors onto an existing Axes.

    Modifies the provided Matplotlib ``ax`` in-place. This helper mirrors
    the notebook's scatter plot: Sensor A points in blue, Sensor B in
    orange (square marker). The function accepts optional keyword-arg
    dictionaries to override marker styles for each sensor.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The axes on which to draw the scatter plot. The axes is modified in
        place (labels, title, legend, grid are set).
    timestamps : numpy.ndarray
        1-D array of timestamps in seconds with shape (N,).
    sensor_a : numpy.ndarray
        1-D array of Sensor A temperature readings (°C) with shape (N,).
    sensor_b : numpy.ndarray
        1-D array of Sensor B temperature readings (°C) with shape (N,).
    sensor_a_kwargs : dict, optional
        Additional keyword arguments forwarded to ``ax.scatter`` for
        Sensor A. Keys here override the defaults used by the function.
    sensor_b_kwargs : dict, optional
        Additional keyword arguments forwarded to ``ax.scatter`` for
        Sensor B. Keys here override the defaults used by the function.
    title : str, optional
        Title for the axes. Default is ``'Sensor readings vs Time (scatter)'``.

    Returns
    -------
    None
    """
    # lazy import of Axes type for typing-friendly environments
    try:
        from matplotlib.axes import Axes  # noqa: F401
    except Exception:
        pass

    if sensor_a_kwargs is None:
        sensor_a_kwargs = {}
    if sensor_b_kwargs is None:
        sensor_b_kwargs = {}

    a_defaults = dict(c='blue', s=36, alpha=0.8, label='Sensor A (°C)')
    b_defaults = dict(c='orange', s=36, alpha=0.8, marker='s', label='Sensor B (°C)')

    a_kwargs = {**a_defaults, **sensor_a_kwargs}
    b_kwargs = {**b_defaults, **sensor_b_kwargs}

    ax.scatter(timestamps, sensor_a, **a_kwargs)
    ax.scatter(timestamps, sensor_b, **b_kwargs)

    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Temperature (°C)')
    ax.set_title(title)
    ax.legend()
    ax.grid(True)

def main(seed: int = 2143, out_path: str = 'sensor_analysis.png', dpi: int = 150) -> None:
    """Generate data, create plots, and save a combined figure.

    The function generates reproducible sensor data using :func:`generate_data`,
    creates a 1x3 subplot layout, draws a scatter plot, an overlaid histogram,
    and a box plot for the two sensors, then saves the figure to disk.

    Parameters
    ----------
    seed : int, optional
        Seed passed to :func:`generate_data` to ensure reproducible outputs
        (default is 2143).
    out_path : str, optional
        File path where the combined figure will be saved (default
        ``'sensor_analysis.png'``).
    dpi : int, optional
        Dots-per-inch to use when saving the figure (default 150).

    Returns
    -------
    None
    """
    # Generate data
    timestamps, sensor_a, sensor_b = generate_data(seed)

    # Create 1x3 subplot figure
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))

    # Scatter plot on axes[0]
    plot_scatter(axes[0], timestamps, sensor_a, sensor_b)

    # Histogram on axes[1]
    bins = 20
    axes[1].hist(sensor_a, bins=bins, alpha=0.7, color='blue', label='Sensor A (n=200)', edgecolor='black')
    axes[1].hist(sensor_b, bins=bins, alpha=0.5, color='orange', label='Sensor B (n=200)', edgecolor='black')
    axes[1].set_xlabel('Temperature (°C)')
    axes[1].set_ylabel('Count')
    axes[1].set_title('Overlaid histogram')
    axes[1].legend()
    axes[1].grid(axis='y', alpha=0.3)

    # Box plot on axes[2]
    axes[2].boxplot([sensor_a, sensor_b], labels=['Sensor A', 'Sensor B'], notch=True, showmeans=True,
                    meanprops=dict(marker='D', markeredgecolor='black', markerfacecolor='firebrick'))
    axes[2].set_ylabel('Temperature (°C)')
    axes[2].set_title('Box plot')
    axes[2].grid(axis='y', alpha=0.3)

    # Layout and save
    plt.tight_layout()
    fig.savefig(out_path, dpi=dpi, bbox_inches='tight')
    plt.close(fig)


if __name__ == '__main__':
    main()

