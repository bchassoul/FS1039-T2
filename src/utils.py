# src/utils.py
from __future__ import annotations
from pathlib import Path
import numpy as np
from config import DATA_DIR

REQUIRED_FILES = [
    "v_r.npy", "rho.npy", "Pgrad_r.npy", "PBgrad_r.npy", "x.npy", "z.npy", "table.txt"
]

class DataNotFound(Exception):
    pass

def assert_data_present(data_dir: Path) -> None:
    missing = [f for f in REQUIRED_FILES if not (data_dir / f).exists()]
    if missing:
        raise DataNotFound(
            "❌ Missing files in data directory:\n"
            + "\n".join(f" - {m}" for m in missing)
            + f"\nLook in: {data_dir}"
        )

def load_simulation(data_dir: Path | None = None) -> dict:
    """
    Load ALL simulation arrays from `data_dir` (default: ../data).
    Returns a dict with keys: x, z, vr, rho, Pgrad_r, PBgrad_r, table
    """
    data_dir = Path(data_dir or DATA_DIR)
    assert_data_present(data_dir)

    vr       = np.load(data_dir / "v_r.npy")         # cm/s
    rho      = np.load(data_dir / "rho.npy")         # g/cm^3
    Pgrad_r  = np.load(data_dir / "Pgrad_r.npy")     # dyn/cm^3
    PBgrad_r = np.load(data_dir / "PBgrad_r.npy")    # dyn/cm^3
    x        = np.load(data_dir / "x.npy")           # au (2D)
    z        = np.load(data_dir / "z.npy")           # au (2D)
    table    = np.loadtxt(data_dir / "table.txt")    # various columns

    # Validation
    shapes = {k: v.shape for k, v in dict(vr=vr, rho=rho, Pgrad_r=Pgrad_r, PBgrad_r=PBgrad_r, x=x, z=z).items()}
    s = {shapes["vr"], shapes["rho"], shapes["Pgrad_r"], shapes["PBgrad_r"], shapes["x"], shapes["z"]}
    if len(s) != 1:
        raise ValueError(f"Inconsistent shapes: {shapes}")

    print(f"✨ Data loaded successfully!")
    return dict(x=x, z=z, vr=vr, rho=rho, Pgrad_r=Pgrad_r, PBgrad_r=PBgrad_r, table=table)

def percentile_limits(arr: np.ndarray, lo: float = 2, hi: float = 98, symmetric: bool = True):
    """
    Return robust color limits for pcolormesh.
    If symmetric=True, makes symmetric limits around 0.
    """
    p_lo, p_hi = np.nanpercentile(arr, [lo, hi])
    if symmetric:
        bound = max(abs(p_lo), abs(p_hi))
        return -bound, bound
    return p_lo, p_hi

def calculate_region_stats(mask: np.ndarray, values: np.ndarray, 
                          total_points: int | None = None,
                          percentiles: list[float] = [25, 50, 75],
                          return_log_stats: bool = False) -> dict:
    """
    Calculate statistics for a region defined by a boolean mask.
    
    Parameters:
    -----------
    mask : np.ndarray
        Boolean mask defining the region
    values : np.ndarray
        Array of values to calculate statistics on
    total_points : int, optional
        Total number of valid points (for percentage calculation).
        If None, uses mask.sum() as total.
    percentiles : list[float]
        Percentiles to calculate (default: [25, 50, 75])
    return_log_stats : bool
        If True, also returns statistics in log10 space and converts back
        to linear space (useful for density calculations)
    
    Returns:
    --------
    dict with keys: n, area_pct (if total_points provided), percentiles,
    and optionally log10_* keys if return_log_stats=True
    """
    vals = values[mask]
    
    if vals.size == 0 or not np.isfinite(vals).any():
        result = {"n": 0}
        if total_points is not None:
            result["area_pct"] = 0.0
        for p in percentiles:
            result[f"p{int(p)}"] = np.nan
        if return_log_stats:
            result["log10_med"] = np.nan
            result["log10_p25"] = np.nan
            result["log10_p75"] = np.nan
            result["med"] = np.nan
            result["p25"] = np.nan
            result["p75"] = np.nan
        return result
    
    # Calculate percentiles
    perc_values = np.nanpercentile(vals, percentiles)
    
    result = {"n": int(vals.size)}
    
    # Area percentage if total_points provided
    if total_points is not None:
        result["area_pct"] = 100.0 * mask.sum() / total_points if total_points > 0 else 0.0
    
    # Add percentile values
    for p, val in zip(percentiles, perc_values):
        result[f"p{int(p)}"] = float(val)
    
    # Special handling for median (p50)
    if 50 in percentiles:
        result["median"] = float(perc_values[percentiles.index(50)])
    
    # If log stats requested, calculate them
    if return_log_stats:
        log10_vals = np.log10(vals)
        log10_med = float(np.nanmedian(log10_vals))
        log10_p25, log10_p75 = np.nanpercentile(log10_vals, [25, 75])
        
        result["log10_med"] = log10_med
        result["log10_p25"] = float(log10_p25)
        result["log10_p75"] = float(log10_p75)
        
        # Convert back to linear space
        result["med"] = float(10**log10_med)
        result["p25"] = float(10**log10_p25)
        result["p75"] = float(10**log10_p75)
    
    return result

def find_min_step(arr: np.ndarray) -> float:
    """
    Find the minimum non-zero step in a 1D array.
    Useful for estimating grid cell size.
    """
    vals = np.unique(arr[np.isfinite(arr)])
    vals.sort()
    dif = np.diff(vals)
    return float(np.min(dif[dif > 0]))

def order_of_magnitude(x: float) -> float:
    """
    Calculate order of magnitude (nearest power of 10 below).
    """
    return 10**np.floor(np.log10(x))
